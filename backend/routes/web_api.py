
from flask import Blueprint, request, jsonify
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database.db_session import get_db
from backend.database.models import User, Claim, DisruptionType, ClaimStatus, generate_claim_reference

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

        return jsonify({
            'message': 'Claim submitted successfully',
            'claim': new_claim.to_dict()
        }), 201

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
