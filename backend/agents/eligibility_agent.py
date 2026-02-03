"""
Eligibility Agent - Checks DGCA compensation eligibility
Uses the DGCA rules engine to determine if passenger qualifies for compensation
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from typing import Dict
from backend.utils.dgca_rules import DGCARulesEngine, DisruptionType


class EligibilityAgent:
    """
    Agent responsible for checking flight compensation eligibility under DGCA rules
    """
    
    def __init__(self):
        self.rules_engine = DGCARulesEngine()
    
    def check_eligibility(self, flight_data: Dict) -> Dict:
        """
        Check if passenger is eligible for compensation
        
        Args:
            flight_data: Dictionary with flight details from Intake Agent
            
        Returns:
            Dictionary with eligibility result and compensation details
        """
        
        # Extract required fields
        disruption_type_str = flight_data.get('disruption_type', 'delay')
        flight_duration_hours = flight_data.get('flight_duration_hours', 2.0)
        delay_hours = flight_data.get('delay_hours')
        is_international = flight_data.get('is_international', False)
        exemption_reason = flight_data.get('exemption_reason')
        
        # Map string to enum
        disruption_type_map = {
            'delay': DisruptionType.DELAY,
            'cancellation': DisruptionType.CANCELLATION,
            'denied_boarding': DisruptionType.DENIED_BOARDING,
            'downgrade': DisruptionType.DOWNGRADE
        }
        
        disruption_type = disruption_type_map.get(disruption_type_str, DisruptionType.DELAY)
        
        # Calculate compensation using DGCA rules
        result = self.rules_engine.calculate_compensation(
            disruption_type=disruption_type,
            flight_duration_hours=flight_duration_hours,
            delay_hours=delay_hours,
            is_international=is_international,
            exemption_reason=exemption_reason,
            notification_days=flight_data.get('cancellation_notice_days'),
            alternative_offered_within_hours=flight_data.get('alternative_offered_hours'),
            fare_paid=flight_data.get('fare_paid')
        )
        
        # Get airline obligations
        obligations = {}
        if delay_hours:
            obligations = self.rules_engine.get_airline_obligations(
                delay_hours=delay_hours,
                flight_duration_hours=flight_duration_hours
            )
        
        # Format response
        response = {
            'eligible': result['eligible'],
            'compensation_amount': result['compensation_amount'],
            'currency': result['currency'],
            'disruption_type': result['disruption_type'],
            'reason': result['reason'],
            'exemption_applied': result['exemption_applied'],
            'exemption_reason': result.get('exemption_reason'),
            'airline_obligations': obligations,
            'agent': 'eligibility_agent',
            'legal_basis': 'DGCA CAR Section 3, Series M, Part IV'
        }
        
        return response
    
    def get_user_friendly_message(self, eligibility_result: Dict) -> str:
        """
        Convert eligibility result to user-friendly message
        
        Args:
            eligibility_result: Result from check_eligibility
            
        Returns:
            Formatted message for user
        """
        if eligibility_result['eligible']:
            amount = eligibility_result['compensation_amount']
            message = f"✅ **Good News!**\n\n"
            message += f"You are **eligible** for compensation of **₹{amount:,}**\n\n"
            message += f"**Reason:** {eligibility_result['reason']}\n\n"
            
            # Add obligations if any
            if eligibility_result.get('airline_obligations'):
                oblig = eligibility_result['airline_obligations']
                message += "**Airline Must Also Provide:**\n"
                if oblig.get('meals_and_refreshments'):
                    message += "• Meals and refreshments\n"
                if oblig.get('hotel_accommodation'):
                    message += "• Hotel accommodation\n"
                if oblig.get('communication'):
                    message += "• 2 phone calls/emails\n"
                if oblig.get('refund_option'):
                    message += "• Full refund option\n"
                message += "\n"
            
            message += "**Legal Basis:** DGCA CAR Section 3\n\n"
            message += "Would you like me to file the claim on your behalf?"
        else:
            message = f"❌ **Eligibility Status**\n\n"
            message += f"Unfortunately, you may not be eligible for compensation.\n\n"
            message += f"**Reason:** {eligibility_result['reason']}\n"
            
            if eligibility_result.get('exemption_applied'):
                message += f"\n**Exemption:** {eligibility_result['exemption_reason']}"
        
        return message


# Example usage
if __name__ == "__main__":
    agent = EligibilityAgent()
    
    # Test case 1: Eligible delay
    print("=== Test Case 1: Eligible Delay ===")
    flight_data1 = {
        'flight_number': '6E-234',
        'flight_duration_hours': 2.5,
        'delay_hours': 5,
        'disruption_type': 'delay',
        'is_international': False
    }
    result1 = agent.check_eligibility(flight_data1)
    print(agent.get_user_friendly_message(result1))
    
    # Test case 2: Weather exemption
    print("\n=== Test Case 2: Weather Exemption ===")
    flight_data2 = {
        'flight_number': 'AI-615',
        'flight_duration_hours': 3.0,
        'delay_hours': 4,
        'disruption_type': 'delay',
        'is_international': False,
        'exemption_reason': 'extraordinary weather conditions'
    }
    result2 = agent.check_eligibility(flight_data2)
    print(agent.get_user_friendly_message(result2))
    
    # Test case 3: Cancellation
    print("\n=== Test Case 3: Cancellation ===")
    flight_data3 = {
        'flight_number': 'SG-456',
        'flight_duration_hours': 1.5,
        'disruption_type': 'cancellation',
        'is_international': False
    }
    result3 = agent.check_eligibility(flight_data3)
    print(agent.get_user_friendly_message(result3))
