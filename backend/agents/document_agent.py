"""
Document Agent - Generates legal claim documents
Uses the PDF Generator to create DGCA-compliant claim letters
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from typing import Dict
from backend.utils.pdf_generator import PDFGenerator
from backend.utils.dgca_rules import DGCARulesEngine, DisruptionType

class DocumentAgent:
    """
    Agent responsible for generating legal claim documents
    """

    def __init__(self):
        self.pdf_generator = PDFGenerator()
        self.rules_engine = DGCARulesEngine()

    def generate_claim_documents(self, claim_data: Dict) -> Dict:
        """
        Generate all necessary documents for a claim

        Args:
            claim_data: Dictionary containing valid claim information

        Returns:
            Dictionary with paths to generated documents
        """

        # 1. Generate Main Claim Letter
        try:
            pdf_path = self.pdf_generator.generate_claim_letter(claim_data)

            # 2. Generate Email Template (Text body)
            email_body = self._generate_email_body(claim_data)

            return {
                'success': True,
                'claim_letter_path': pdf_path,
                'email_body': email_body,
                'agent': 'document_agent'
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'agent': 'document_agent'
            }

    def _generate_email_body(self, data: Dict) -> str:
        """
        Generate the email body text
        """
        return f"""
        <html>
        <body>
        <p>Dear Customer Relations Team,</p>

        <p><b>Reference: Claim for Flight {data.get('flight_number')} on {data.get('flight_date')}</b></p>

        <p>Please find attached my formal claim for flight compensation under DGCA CAR Section 3.</p>

        <p>
        <b>Flight Details:</b><br>
        Flight Number: {data.get('flight_number')}<br>
        Date: {data.get('flight_date')}<br>
        Disruption: {str(data.get('disruption_type', 'Delay')).title()}<br>
        </p>

        <p>I look forward to your prompt response within the stipulated 30-day period.</p>

        <p>Sincerely,</p>
        <p>{data.get('passenger_name')}</p>
        </body>
        </html>
        """

# Example usage
if __name__ == "__main__":
    agent = DocumentAgent()

    test_data = {
        'claim_reference': 'TEST-DOC-001',
        'airline_name': 'IndiGo',
        'passenger_name': 'Priya Sharma',
        'flight_number': '6E-555',
        'flight_date': '2025-11-01',
        'route_from': 'Bangalore',
        'route_to': 'Delhi',
        'disruption_type': 'Delay',
        'delay_hours': 4,
        'compensation_amount': 7500,
        'passenger_email': 'priya@example.com',
        'passenger_phone': '+91 98765 43210'
    }

    result = agent.generate_claim_documents(test_data)
    print(result)
