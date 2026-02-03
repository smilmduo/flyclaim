"""
Escalation Agent - Handles escalation to AirSewa/DGCA
Generates grievance text for regulatory bodies
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from typing import Dict

class EscalationAgent:
    """
    Agent responsible for escalating claims
    """

    def __init__(self):
        pass

    def generate_airsewa_complaint(self, claim_data: Dict) -> Dict:
        """
        Generate complaint text for AirSewa portal

        Args:
            claim_data: Claim details

        Returns:
            Dictionary with complaint details
        """

        complaint_text = f"""
I am filing this grievance regarding the lack of response/resolution from {claim_data.get('airline_name')}
regarding my flight compensation claim.

Flight Details:
- Flight Number: {claim_data.get('flight_number')}
- Date: {claim_data.get('flight_date')}
- Sector: {claim_data.get('route_from')} to {claim_data.get('route_to')}
- PNR: {claim_data.get('pnr', 'N/A')}

Issue:
My flight was {claim_data.get('disruption_type')} by {claim_data.get('delay_hours', 'N/A')} hours.
As per DGCA CAR Section 3, Series M, Part IV, I am eligible for compensation of ₹{claim_data.get('compensation_amount')}.

I submitted a formal claim to the airline on {claim_data.get('submitted_at_date', 'unknown date')}.
It has been over 30 days and I have not received a satisfactory response/resolution.

I request the DGCA/Ministry of Civil Aviation to intervene and ensure the airline complies with the regulations.
        """

        return {
            'portal': 'AirSewa (https://airsewa.gov.in)',
            'category': 'Flight Delays/Cancellations',
            'complaint_text': complaint_text.strip(),
            'documents_needed': ['Ticket Copy', 'Boarding Pass', 'Claim Letter Sent to Airline'],
            'agent': 'escalation_agent'
        }

    def generate_consumer_court_draft(self, claim_data: Dict) -> Dict:
        """
        Generate draft for Consumer Court (NCDRC/State Commission)
        """
        # Simplified placeholder for legal draft
        draft = f"""
        BEFORE THE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION

        COMPLAINANT: {claim_data.get('passenger_name')}
        VERSUS
        OPPOSITE PARTY: {claim_data.get('airline_name')}

        SUBJECT: COMPLAINT UNDER CONSUMER PROTECTION ACT, 2019 FOR DEFICIENCY IN SERVICE

        1. The Complainant booked a flight...
        [Full legal draft would go here]
        """

        return {
            'type': 'Consumer Court Complaint',
            'draft_text': draft,
            'agent': 'escalation_agent'
        }

# Example usage
if __name__ == "__main__":
    agent = EscalationAgent()

    test_data = {
        'airline_name': 'IndiGo',
        'flight_number': '6E-234',
        'flight_date': '2025-10-28',
        'route_from': 'Delhi',
        'route_to': 'Mumbai',
        'disruption_type': 'Delayed',
        'delay_hours': 5,
        'compensation_amount': 10000,
        'submitted_at_date': '2025-10-30'
    }

    print(agent.generate_airsewa_complaint(test_data))
