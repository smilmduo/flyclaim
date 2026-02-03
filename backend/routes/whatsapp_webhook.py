"""
WhatsApp Webhook Handler for Twilio Integration
Receives messages from WhatsApp and processes claims
"""

import os
from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from backend.agents.intake_agent import IntakeAgent
from backend.agents.eligibility_agent import EligibilityAgent

# Create blueprint
whatsapp_bp = Blueprint('whatsapp', __name__)

# Initialize agents
intake_agent = IntakeAgent()
eligibility_agent = EligibilityAgent()

# Initialize Twilio client
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_client = Client(account_sid, auth_token) if account_sid and auth_token else None


@whatsapp_bp.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """
    Receive WhatsApp messages from Twilio and process flight claims
    """
    # Get message details from Twilio
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')
    
    # Create Twilio response
    resp = MessagingResponse()
    msg = resp.message()
    
    # Handle empty message
    if not incoming_msg:
        msg.body("👋 Welcome to FlyClaim AI!\n\n"
                "I help you claim flight compensation automatically.\n\n"
                "Just tell me about your delayed or cancelled flight.\n\n"
                "Example: 'My IndiGo flight 6E-234 from Delhi to Mumbai on 28 Oct was delayed by 5 hours'")
        return str(resp)
    
    # Handle commands
    if incoming_msg.lower() in ['help', 'start', 'hi', 'hello']:
        msg.body("👋 Hi! I'm FlyClaim AI.\n\n"
                "I can help you claim ₹5,000-₹20,000 compensation for:\n"
                "• Flight delays (>2 hours)\n"
                "• Flight cancellations\n"
                "• Denied boarding\n\n"
                "Just tell me:\n"
                "1. Flight number\n"
                "2. Date of travel\n"
                "3. What happened (delay/cancellation)\n"
                "4. How many hours delayed\n\n"
                "Example: 'My IndiGo 6E-234 from Delhi to Mumbai on 28 Oct was delayed 5 hours'")
        return str(resp)
    
    try:
        # Step 1: Extract flight details using Intake Agent
        extracted_data = intake_agent.extract_flight_details(incoming_msg)
        
        # Check if extraction was successful
        if extracted_data.get('error'):
            msg.body("❌ Sorry, I couldn't understand that.\n\n"
                    "Please include:\n"
                    "• Flight number (e.g., 6E-234)\n"
                    "• Date\n"
                    "• Delay duration\n\n"
                    "Try again with more details.")
            return str(resp)
        
        # Validate extracted data
        validation = intake_agent.validate_extracted_data(extracted_data)
        
        if not validation['is_valid']:
            # Ask for missing information
            missing = validation['required_follow_up'][:2]  # Max 2 at a time
            follow_up = '\n'.join([intake_agent.generate_follow_up_question(field) for field in missing])
            msg.body(f"⚠️ I need some more information:\n\n{follow_up}")
            return str(resp)
        
        # Step 2: Check eligibility using Eligibility Agent
        eligibility_result = eligibility_agent.check_eligibility({
            'flight_number': extracted_data.get('flight_number'),
            'flight_duration_hours': extracted_data.get('flight_duration_hours', 2.0),
            'delay_hours': extracted_data.get('delay_hours'),
            'disruption_type': extracted_data.get('disruption_type'),
            'is_international': extracted_data.get('is_international', False)
        })
        
        # Step 3: Send result to user
        if eligibility_result.get('eligible'):
            amount = eligibility_result['compensation_amount']
            response_text = (
                f"✅ Great News!\n\n"
                f"You are eligible for ₹{amount:,} compensation!\n\n"
                f"📋 Details:\n"
                f"Flight: {extracted_data.get('flight_number')}\n"
                f"Date: {extracted_data.get('flight_date')}\n"
                f"Route: {extracted_data.get('departure')} → {extracted_data.get('arrival')}\n"
                f"Issue: {extracted_data.get('disruption_type').title()}\n\n"
                f"💼 Legal Basis:\n"
                f"DGCA CAR Section 3\n\n"
                f"🚀 Next Steps:\n"
                f"Reply 'YES' to file the claim automatically, or 'INFO' for more details."
            )
            msg.body(response_text)
        else:
            reason = eligibility_result.get('reason', 'Unknown reason')
            response_text = (
                f"❌ Eligibility Check\n\n"
                f"Unfortunately, you may not be eligible for compensation.\n\n"
                f"Reason: {reason}\n\n"
                f"You can still contact the airline directly for goodwill compensation.\n\n"
                f"Reply 'HELP' for more information."
            )
            msg.body(response_text)
        
    except Exception as e:
        msg.body(f"❌ An error occurred: {str(e)}\n\n"
                "Please try again or contact support.")
    
    return str(resp)


@whatsapp_bp.route('/webhook/whatsapp/status', methods=['POST'])
def whatsapp_status():
    """Handle WhatsApp message status updates"""
    message_sid = request.values.get('MessageSid')
    message_status = request.values.get('MessageStatus')
    
    print(f"Message {message_sid} status: {message_status}")
    
    return '', 200


def send_whatsapp_message(to_number: str, message: str):
    """
    Send a WhatsApp message via Twilio
    
    Args:
        to_number: Recipient's WhatsApp number (format: whatsapp:+919876543210)
        message: Message text to send
    """
    if not twilio_client:
        print("Twilio client not initialized. Check your credentials.")
        return None
    
    try:
        message = twilio_client.messages.create(
            from_=os.getenv('TWILIO_WHATSAPP_NUMBER'),
            body=message,
            to=to_number
        )
        return message.sid
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
        return None
