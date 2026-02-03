"""
Submission Agent - Handles claim submission to airlines
Uses Email Sender to send claim documents
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from typing import Dict
from backend.utils.email_sender import EmailSender, MockEmailSender
from backend.database.models import get_airline_name

class SubmissionAgent:
    """
    Agent responsible for submitting claims to airlines
    """

    def __init__(self):
        # Use Mock sender if no credentials in prod (for safety in demo)
        if os.getenv('SMTP_PASSWORD'):
            self.email_sender = EmailSender()
        else:
            self.email_sender = MockEmailSender()

        # Airline contact database (Simplified)
        self.airline_contacts = {
            '6E': 'customer.relations@goindigo.in',
            'AI': 'feedback@airindia.in',
            'SG': 'complaints@spicejet.com',
            'UK': 'customer.feedback@airvistara.com',
            'I5': 'support@airasia.com',
            'G8': 'care@flygofirst.com',
            'QP': 'support@akasaair.com'
        }

    def submit_claim(self, claim_data: Dict, document_paths: list) -> Dict:
        """
        Submit claim to airline via email

        Args:
            claim_data: Claim details
            document_paths: List of file paths to attach (PDFs)

        Returns:
            Submission result
        """

        # 1. Determine Airline Email
        flight_number = claim_data.get('flight_number', '')
        airline_code = flight_number.split('-')[0] if '-' in flight_number else flight_number[:2]

        airline_email = self.airline_contacts.get(airline_code.upper())

        if not airline_email:
            return {
                'success': False,
                'error': f"Airline contact not found for code {airline_code}",
                'agent': 'submission_agent'
            }

        # 2. Prepare Email
        passenger_email = claim_data.get('passenger_email')
        subject = f"Flight Compensation Claim - {claim_data.get('flight_number')} - {claim_data.get('claim_reference')}"

        body = claim_data.get('email_body')
        if not body:
            # Fallback body
            body = f"Please find attached claim for flight {flight_number}."

        # 3. Send Email
        result = self.email_sender.send_email(
            to_email=airline_email,
            subject=subject,
            body=body,
            attachments=document_paths,
            cc_email=passenger_email # CC the passenger
        )

        response = {
            'success': result['success'],
            'submitted_to': airline_email,
            'submitted_at': 'now', # In real app, use datetime
            'agent': 'submission_agent'
        }

        if not result['success']:
            response['error'] = result.get('error')

        return response

# Example usage
if __name__ == "__main__":
    agent = SubmissionAgent()

    test_data = {
        'flight_number': '6E-234',
        'claim_reference': 'TEST-SUB-001',
        'passenger_email': 'user@example.com',
        'email_body': '<p>Please process my claim.</p>'
    }

    # We need a dummy file to test attachment
    with open("test_dummy.pdf", "w") as f:
        f.write("dummy pdf content")

    result = agent.submit_claim(test_data, ["test_dummy.pdf"])
    print(result)

    os.remove("test_dummy.pdf")
