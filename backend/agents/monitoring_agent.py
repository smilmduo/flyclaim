"""
Monitoring Agent - Tracks claim status and deadlines
Checks if 30-day response window has passed
"""

import sys
import os
from datetime import datetime, timedelta
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from typing import Dict, List

class MonitoringAgent:
    """
    Agent responsible for monitoring claim status
    """

    def __init__(self):
        pass

    def check_claim_status(self, claim_data: Dict) -> Dict:
        """
        Check status of a single claim

        Args:
            claim_data: Dictionary containing claim status and dates

        Returns:
            Dictionary with status update
        """
        current_status = claim_data.get('status', 'initiated')
        submitted_at_str = claim_data.get('submitted_at')

        response = {
            'claim_reference': claim_data.get('claim_reference'),
            'current_status': current_status,
            'action_required': False,
            'agent': 'monitoring_agent'
        }

        if not submitted_at_str or current_status != 'submitted_to_airline':
            return response

        # Parse date
        try:
            submitted_at = datetime.fromisoformat(submitted_at_str)
        except ValueError:
            return response

        # Calculate time passed
        now = datetime.utcnow()
        days_passed = (now - submitted_at).days

        response['days_since_submission'] = days_passed

        # DGCA mandates 30 day response time
        if days_passed >= 30:
            response['action_required'] = True
            response['recommended_action'] = 'escalate_to_airsewa'
            response['reason'] = 'Airline response deadline (30 days) exceeded'
        elif days_passed >= 15:
             response['action_required'] = True
             response['recommended_action'] = 'send_reminder'
             response['reason'] = '15 days passed without response'

        return response

    def batch_monitor_claims(self, claims_list: List[Dict]) -> List[Dict]:
        """
        Monitor a batch of claims
        """
        updates = []
        for claim in claims_list:
            result = self.check_claim_status(claim)
            if result.get('action_required'):
                updates.append(result)
        return updates

# Example usage
if __name__ == "__main__":
    agent = MonitoringAgent()

    # Test case 1: Recent claim
    recent_claim = {
        'claim_reference': 'REF-001',
        'status': 'submitted_to_airline',
        'submitted_at': datetime.utcnow().isoformat()
    }
    print("Recent:", agent.check_claim_status(recent_claim))

    # Test case 2: Overdue claim
    past_date = (datetime.utcnow() - timedelta(days=31)).isoformat()
    overdue_claim = {
        'claim_reference': 'REF-002',
        'status': 'submitted_to_airline',
        'submitted_at': past_date
    }
    print("Overdue:", agent.check_claim_status(overdue_claim))
