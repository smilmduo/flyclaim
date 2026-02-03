"""
FlyClaim AI - Flask API for n8n Integration
Simple REST API that exposes AI agents as HTTP endpoints
"""

import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.agents.intake_agent import IntakeAgent
from backend.agents.eligibility_agent import EligibilityAgent
from backend.routes.whatsapp_webhook import whatsapp_bp

# Load environment
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for n8n

# Register blueprints
app.register_blueprint(whatsapp_bp)

# Initialize agents
intake_agent = IntakeAgent()
eligibility_agent = EligibilityAgent()

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        'service': 'FlyClaim AI API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'extract': '/api/extract',
            'eligibility': '/api/eligibility',
            'health': '/health'
        }
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for n8n"""
    return jsonify({'status': 'healthy', 'service': 'FlyClaim AI'})


# ============================================================================
# AGENT ENDPOINTS (for n8n)
# ============================================================================

@app.route('/api/extract', methods=['POST'])
def extract_flight_details():
    """
    Intake Agent: Extract flight details from natural language
    
    Request body:
    {
        "message": "My IndiGo flight 6E-234 was delayed 5 hours",
        "context": {}  // optional
    }
    
    Response:
    {
        "flight_number": "6E-234",
        "airline_name": "IndiGo",
        "delay_hours": 5,
        ...
    }
    """
    try:
        data = request.json
        message = data.get('message', '')
        context = data.get('context')
        
        if not message:
            return jsonify({'error': 'Missing message field'}), 400
        
        # Call intake agent
        result = intake_agent.extract_flight_details(message, context)
        
        # Add validation
        validation = intake_agent.validate_extracted_data(result)
        result['validation'] = validation
        
        # Add confirmation message
        result['confirmation_message'] = intake_agent.create_confirmation_message(result)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e), 'agent': 'intake_agent'}), 500


@app.route('/api/eligibility', methods=['POST'])
def check_eligibility():
    """
    Eligibility Agent: Check DGCA compensation eligibility
    
    Request body:
    {
        "flight_number": "6E-234",
        "flight_duration_hours": 2.5,
        "delay_hours": 5,
        "disruption_type": "delay",
        "is_international": false
    }
    
    Response:
    {
        "eligible": true,
        "compensation_amount": 10000,
        "reason": "...",
        ...
    }
    """
    try:
        flight_data = request.json
        
        if not flight_data:
            return jsonify({'error': 'Missing flight data'}), 400
        
        # Call eligibility agent
        result = eligibility_agent.check_eligibility(flight_data)
        
        # Add user-friendly message
        result['user_message'] = eligibility_agent.get_user_friendly_message(result)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e), 'agent': 'eligibility_agent'}), 500


@app.route('/api/claim/generate', methods=['POST'])
def generate_claim_letter():
    """
    Document Agent: Generate DGCA-compliant claim letter
    
    Request body:
    {
        "passenger_name": "Rahul Kumar",
        "passenger_email": "rahul@example.com",
        "flight_number": "6E-234",
        "flight_date": "2024-10-28",
        "route_from": "Delhi",
        "route_to": "Mumbai",
        "delay_hours": 5,
        "compensation_amount": 10000
    }
    
    Response:
    {
        "claim_letter": "...",
        "claim_reference": "FC-20241028-6E234-0001"
    }
    """
    try:
        data = request.json
        
        # Generate claim letter text
        claim_letter = f"""
FLIGHT COMPENSATION CLAIM UNDER DGCA CAR SECTION 3

Date: {data.get('date', 'N/A')}
Claim Reference: {data.get('claim_reference', 'PENDING')}

TO: Customer Relations Department
{data.get('airline_name', 'Airline')}

Dear Sir/Madam,

SUBJECT: Claim for Compensation under DGCA CAR Section 3, Series M, Part IV

I am writing to file a formal claim for compensation for the disruption to my flight as detailed below:

PASSENGER DETAILS:
Name: {data.get('passenger_name', 'N/A')}
Email: {data.get('passenger_email', 'N/A')}
Phone: {data.get('passenger_phone', 'N/A')}

FLIGHT DETAILS:
Flight Number: {data.get('flight_number', 'N/A')}
Date of Travel: {data.get('flight_date', 'N/A')}
Route: {data.get('route_from', 'N/A')} to {data.get('route_to', 'N/A')}
Booking Reference/PNR: {data.get('pnr', 'N/A')}

DISRUPTION DETAILS:
Type: {data.get('disruption_type', 'Delay').upper()}
Delay Duration: {data.get('delay_hours', 'N/A')} hours
Scheduled Departure: {data.get('scheduled_departure', 'N/A')}
Actual Departure: {data.get('actual_departure', 'N/A')}

COMPENSATION CLAIMED:
Amount: ₹{data.get('compensation_amount', 0):,}
Legal Basis: DGCA Civil Aviation Requirements (CAR) Section 3, Series M, Part IV

LEGAL GROUNDS:
As per DGCA CAR Section 3, airlines are mandated to compensate passengers for flight delays exceeding 2 hours (for domestic flights) with compensation ranging from ₹5,000 to ₹20,000 depending on the flight duration and delay magnitude.

My flight was delayed by {data.get('delay_hours', 'N/A')} hours, which clearly exceeds the threshold set by DGCA regulations. Therefore, I am entitled to compensation of ₹{data.get('compensation_amount', 0):,}.

REQUESTED ACTION:
I request you to:
1. Acknowledge receipt of this claim within 7 days
2. Process the compensation as per DGCA guidelines
3. Credit the compensation amount to my account within 30 days

If I do not receive a satisfactory response within 30 days, I will be compelled to escalate this matter to:
- AirSewa (DGCA's grievance portal)
- Directorate General of Civil Aviation (DGCA)
- Consumer Court

I have attached/will provide upon request:
- Copy of boarding pass
- Copy of ticket/booking confirmation
- Any other relevant documents

I look forward to your prompt response and resolution of this matter.

Yours sincerely,
{data.get('passenger_name', 'N/A')}
{data.get('passenger_email', 'N/A')}
{data.get('passenger_phone', 'N/A')}

Date: {data.get('date', 'N/A')}

---
This claim is generated by FlyClaim AI - Automated Flight Compensation System
"""
        
        response = {
            'claim_letter': claim_letter,
            'claim_reference': data.get('claim_reference', 'PENDING'),
            'generated_at': data.get('date'),
            'agent': 'document_agent'
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e), 'agent': 'document_agent'}), 500


@app.route('/api/claim/submit', methods=['POST'])
def submit_claim():
    """
    Submission Agent: Prepare claim for email submission
    (n8n will handle actual email sending)
    
    Request body:
    {
        "claim_letter": "...",
        "airline_code": "6E",
        "passenger_email": "user@example.com"
    }
    
    Response:
    {
        "airline_email": "customer.relations@goindigo.in",
        "subject": "Flight Compensation Claim - FC-...",
        "ready_to_send": true
    }
    """
    try:
        data = request.json
        airline_code = data.get('airline_code', '')
        
        # Airline email mapping
        airline_emails = {
            '6E': 'customer.relations@goindigo.in',
            'AI': 'feedback@airindia.in',
            'SG': 'complaints@spicejet.com',
            'UK': 'customer.feedback@airvistara.com',
            'I5': 'support@airasia.com',
            'G8': 'care@flygofirst.com',
            'QP': 'support@akasaair.com'
        }
        
        airline_email = airline_emails.get(airline_code.upper(), 'unknown@airline.com')
        
        response = {
            'airline_email': airline_email,
            'cc_email': data.get('passenger_email'),
            'subject': f"Flight Compensation Claim - {data.get('claim_reference', 'DGCA CAR Section 3')}",
            'body': data.get('claim_letter', ''),
            'ready_to_send': True,
            'agent': 'submission_agent'
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e), 'agent': 'submission_agent'}), 500


# ============================================================================
# SIMPLE WEB INTERFACE (Optional - for testing without n8n)
# ============================================================================

@app.route('/demo', methods=['GET'])
def demo():
    """Simple demo page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FlyClaim AI - Demo</title>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #2563eb; }
            .input-group { margin: 20px 0; }
            textarea { width: 100%; padding: 10px; font-size: 14px; }
            button { background: #2563eb; color: white; padding: 10px 20px; border: none; cursor: pointer; font-size: 16px; }
            button:hover { background: #1d4ed8; }
            .result { background: #f3f4f6; padding: 20px; margin-top: 20px; border-radius: 8px; }
            pre { white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <h1>🛫 FlyClaim AI - API Demo</h1>
        <p>Test the Intake Agent by entering a flight delay message:</p>
        
        <div class="input-group">
            <textarea id="message" rows="3" placeholder="Example: My IndiGo flight 6E-234 from Delhi to Mumbai on 28 Oct was delayed by 5 hours">My IndiGo flight 6E-234 from Delhi to Mumbai on 28 October was delayed by 5 hours</textarea>
        </div>
        
        <button onclick="testExtract()">Extract Flight Details</button>
        <button onclick="testEligibility()" style="background: #059669;">Check Eligibility</button>
        
        <div id="result" class="result" style="display: none;">
            <h3>Result:</h3>
            <pre id="output"></pre>
        </div>
        
        <script>
        async function testExtract() {
            const message = document.getElementById('message').value;
            const response = await fetch('/api/extract', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ message })
            });
            const data = await response.json();
            document.getElementById('result').style.display = 'block';
            document.getElementById('output').textContent = JSON.stringify(data, null, 2);
        }

        async function testEligibility() {
            const message = document.getElementById('message').value;

            // 1️⃣ Step 1: Extract flight details
            const extractRes = await fetch('/api/extract', {
                 method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ message })
            });
            const extractData = await extractRes.json();

            // 2️⃣ Step 2: Prepare data for eligibility
            const eligibilityPayload = {
                flight_number: extractData.flight_number,
                flight_duration_hours: 2.5, // default / later calculate
                delay_hours: extractData.delay_hours,
                disruption_type: extractData.disruption_type,
                is_international: false
            };

            // 3️⃣ Step 3: Call eligibility agent
            const eligibilityRes = await fetch('/api/eligibility', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(eligibilityPayload)
            });

            const eligibilityData = await eligibilityRes.json();

            document.getElementById('result').style.display = 'block';
            document.getElementById('output').textContent =
                eligibilityData.user_message || JSON.stringify(eligibilityData, null, 2);
        }
        </script>
    </body>
    </html>
    """


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    print("\n" + "="*60)
    print("🛫 FlyClaim AI - API Server Starting")
    print("="*60)
    print(f"Server running on: http://localhost:{port}")
    print(f"Health check: http://localhost:{port}/health")
    print(f"Demo page: http://localhost:{port}/demo")
    print("\nAPI Endpoints:")
    print("  POST /api/extract - Extract flight details")
    print("  POST /api/eligibility - Check compensation eligibility")
    print("  POST /api/claim/generate - Generate claim letter")
    print("  POST /api/claim/submit - Prepare claim for submission")
    print("\nReady for n8n integration!")
    print("="*60 + "\n")
    
    app.run(host="0.0.0.0", port=5000, debug=True)
