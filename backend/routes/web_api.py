
from flask import Blueprint, request, jsonify
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database.db_session import get_db
from backend.database.models import User, Claim, DisruptionType, ClaimStatus, generate_claim_reference
from backend.agents.eligibility_agent import EligibilityAgent
from backend.agents.document_agent import DocumentAgent
from backend.agents.submission_agent import SubmissionAgent

web_api_bp = Blueprint('web_api', __name__)

@web_api_bp.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.json
    db = next(get_db())

    try:
        phone = data.get('phone')
        password = data.get('password')
        if not phone or not password:
            return jsonify({'error': 'Phone number and password are required'}), 400

        existing_user = db.query(User).filter(User.phone_number == phone).first()
        if existing_user:
            return jsonify({'error': 'User already exists'}), 400

        new_user = User(
            phone_number=phone,
            name=data.get('name'),
            email=data.get('email'),
            password_hash=generate_password_hash(password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return jsonify({
            'message': 'User created successfully',
            'user': {
                'id': new_user.id,
                'name': new_user.name,
                'phone': new_user.phone_number,
                'email': new_user.email
            }
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@web_api_bp.route('/api/claims/<claim_reference>/status', methods=['PUT'])
def update_claim_status(claim_reference):
    db = next(get_db())
    try:
        data = request.json
        new_status = data.get('status')
        if not new_status:
             return jsonify({'error': 'Status is required'}), 400

        claim = db.query(Claim).filter(Claim.claim_reference == claim_reference).first()
        if not claim:
            return jsonify({'error': 'Claim not found'}), 404

        # Validate status enum
        try:
            status_enum = ClaimStatus(new_status)
        except ValueError:
             return jsonify({'error': f'Invalid status. Valid values: {[s.value for s in ClaimStatus]}'}), 400

        claim.status = status_enum

        # If rejected/resolved, maybe update resolution notes/amount
        if 'resolution_notes' in data:
            claim.resolution_notes = data['resolution_notes']

        if 'amount_received' in data:
            claim.amount_received = data['amount_received']

        db.commit()
        return jsonify({
            'message': f'Claim status updated to {new_status}',
            'claim': claim.to_dict()
        }), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@web_api_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    db = next(get_db())

    try:
        phone = data.get('phone')
        password = data.get('password')

        if not phone or not password:
            return jsonify({'error': 'Phone number and password are required'}), 400

        user = db.query(User).filter(User.phone_number == phone).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Invalid credentials'}), 401

        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'name': user.name,
                'phone': user.phone_number,
                'email': user.email
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@web_api_bp.route('/api/claims', methods=['POST'])
def create_claim():
    data = request.json
    db = next(get_db())

    try:
        # Validate required fields
        required_fields = ['user_id', 'flight_number', 'flight_date', 'airline_name', 'reason']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing field: {field}'}), 400

        # Parse flight date
        try:
            flight_date = datetime.fromisoformat(data['flight_date'].replace('Z', '+00:00'))
        except ValueError:
            flight_date = datetime.strptime(data['flight_date'], '%Y-%m-%d')

        # Determine disruption type (simplified mapping)
        reason = data.get('reason', '').lower()
        disruption_type = DisruptionType.DELAY
        if 'cancel' in reason:
            disruption_type = DisruptionType.CANCELLATION
        elif 'denied' in reason:
            disruption_type = DisruptionType.DENIED_BOARDING

        new_claim = Claim(
            user_id=data['user_id'],
            flight_number=data['flight_number'],
            airline_name=data['airline_name'],
            flight_date=flight_date,
            pnr=data.get('pnr'),
            passenger_name=data.get('passenger_name'),
            route_from=data.get('route_from'),
            route_to=data.get('route_to'),
            disruption_type=disruption_type,
            claim_reference='TEMP', # Placeholder
            status=ClaimStatus.INITIATED
        )

        db.add(new_claim)
        db.flush() # Get ID

        # Generate real reference
        new_claim.claim_reference = generate_claim_reference(new_claim.id, new_claim.flight_number)

        db.commit()
        db.refresh(new_claim)

        # ----------------------------------------------------------------
        # AUTOMATED PROCESSING: Run Agents Immediately
        # ----------------------------------------------------------------
        try:
            # 1. Eligibility Check
            eligibility_agent = EligibilityAgent()
            agent_input = {
                'flight_number': new_claim.flight_number,
                'disruption_type': new_claim.disruption_type.value if new_claim.disruption_type else 'delay',
                'is_international': new_claim.is_international,
                'delay_hours': float(data.get('delay_hours', 3.0)), # Default to eligible delay for demo
                'cancellation_notice_days': int(data.get('cancellation_notice_days', 0)) if data.get('cancellation_notice_days') else None
            }

            eligibility_result = eligibility_agent.check_eligibility(agent_input)

            new_claim.is_eligible = eligibility_result['eligible']
            new_claim.compensation_amount = eligibility_result['compensation_amount']
            new_claim.calculation_reason = eligibility_result['reason']

            if new_claim.is_eligible:
                # 2. Document Generation (Simulated)
                # In a real background job, we'd generate PDFs here.
                new_claim.status = ClaimStatus.ELIGIBILITY_CHECKED

                # 3. Auto-Submit (Simulated)
                # Move to 'In Review' state immediately for UX
                new_claim.status = ClaimStatus.SUBMITTED_TO_AIRLINE
                new_claim.submitted_at = datetime.utcnow()
                new_claim.airline_response_deadline = datetime.utcnow() # + 30 days usually
            else:
                new_claim.status = ClaimStatus.REJECTED
                new_claim.resolution_notes = "Determined ineligible by AI: " + eligibility_result['reason']

            db.commit()
            db.refresh(new_claim)

        except Exception as e:
            print(f"Auto-processing failed: {str(e)}")
            # Fallback: leave as INITIATED

        return jsonify({
            'message': 'Claim submitted successfully',
            'claim': new_claim.to_dict()
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@web_api_bp.route('/api/claims/<claim_reference>/process', methods=['POST'])
def process_claim(claim_reference):
    """
    Manual endpoint to trigger/advance workflow for a claim.
    Useful for Admin or if auto-processing failed.
    """
    db = next(get_db())
    try:
        claim = db.query(Claim).filter(Claim.claim_reference == claim_reference).first()
        if not claim:
            return jsonify({'error': 'Claim not found'}), 404

        # Run Eligibility Agent
        eligibility_agent = EligibilityAgent()
        agent_input = {
            'flight_number': claim.flight_number,
            'disruption_type': claim.disruption_type.value if claim.disruption_type else 'delay',
            'is_international': claim.is_international,
            'delay_hours': claim.delay_hours or 3.0,
        }

        eligibility_result = eligibility_agent.check_eligibility(agent_input)

        claim.is_eligible = eligibility_result['eligible']
        claim.compensation_amount = eligibility_result['compensation_amount']
        claim.calculation_reason = eligibility_result['reason']

        if claim.is_eligible:
            # Advance status
            if claim.status == ClaimStatus.INITIATED:
                claim.status = ClaimStatus.SUBMITTED_TO_AIRLINE
                claim.submitted_at = datetime.utcnow()
            elif claim.status == ClaimStatus.SUBMITTED_TO_AIRLINE:
                # DEMO MODE: Simulate Airline Response
                # In a real system, this would happen via email webhook or manual admin action
                claim.status = ClaimStatus.RESOLVED
                claim.resolution_notes = "Airline accepted the claim after review. Compensation approved."
                claim.amount_received = claim.compensation_amount
                claim.resolution_date = datetime.utcnow()
        else:
            claim.status = ClaimStatus.REJECTED

        db.commit()

        return jsonify({
            'message': 'Claim processed successfully',
            'claim': claim.to_dict()
        }), 200

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@web_api_bp.route('/api/claims/<claim_reference>', methods=['GET'])
def get_claim(claim_reference):
    db = next(get_db())
    try:
        claim = db.query(Claim).filter(Claim.claim_reference == claim_reference).first()
        if not claim:
            return jsonify({'error': 'Claim not found'}), 404

        return jsonify(claim.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@web_api_bp.route('/api/users/<int:user_id>/claims', methods=['GET'])
def get_user_claims(user_id):
    db = next(get_db())
    try:
        claims = db.query(Claim).filter(Claim.user_id == user_id).all()
        return jsonify([c.to_dict() for c in claims]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()
