"""
DGCA CAR Section 3 - Flight Compensation Rules Engine
Based on DGCA Civil Aviation Requirements Section 3, Series M, Part IV

Reference: https://www.dgca.gov.in/digigov-portal/jsp/dgca/homePage/homePage.jsp
"""

from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from enum import Enum


class DisruptionType(Enum):
    """Types of flight disruptions"""
    DELAY = "delay"
    CANCELLATION = "cancellation"
    DENIED_BOARDING = "denied_boarding"
    DOWNGRADE = "downgrade"


class ExemptionReason(Enum):
    """Reasons for compensation exemption"""
    WEATHER = "extraordinary_weather"
    SECURITY = "security_threat"
    ATC_STRIKE = "atc_strike"
    POLITICAL_INSTABILITY = "political_instability"
    EARLY_NOTIFICATION = "notified_2_weeks_prior"
    ALTERNATIVE_OFFERED = "alternative_flight_within_1_hour"
    PASSENGER_FAULT = "passenger_late_or_docs_issue"


class DGCARulesEngine:
    """
    Engine to calculate flight compensation based on DGCA rules
    """
    
    # Compensation matrix (in INR)
    COMPENSATION_MATRIX = {
        # Flight duration in hours: (delay_threshold_hours, compensation_amount)
        "domestic_short": {  # < 1 hour flight
            "delay_threshold": 2,
            "compensation": 5000,
            "applies_to_cancellation": True
        },
        "domestic_medium": {  # 1-2 hours flight
            "delay_threshold": 2,
            "compensation": 7500,
            "applies_to_cancellation": True
        },
        "domestic_long": {  # > 2 hours flight
            "delay_threshold": 2,
            "compensation": 10000,
            "applies_to_cancellation": True
        },
        "international": {  # International flights
            "delay_threshold": 4,
            "compensation": 20000,
            "applies_to_cancellation": True
        }
    }
    
    # Denied boarding compensation
    DENIED_BOARDING_COMPENSATION = {
        "domestic_short": 10000,
        "domestic_medium": 10000,
        "domestic_long": 10000,
        "international": 20000
    }
    
    # Downgrade compensation (refund of fare difference)
    DOWNGRADE_REFUND_PERCENTAGE = {
        "domestic": 75,  # 75% of fare difference
        "international": 50  # 50% of fare difference
    }
    
    @staticmethod
    def calculate_flight_duration_category(
        flight_duration_hours: float,
        is_international: bool = False
    ) -> str:
        """
        Categorize flight based on duration
        
        Args:
            flight_duration_hours: Duration of flight in hours
            is_international: Whether it's an international flight
            
        Returns:
            Category string
        """
        if is_international:
            return "international"
        
        if flight_duration_hours < 1:
            return "domestic_short"
        elif flight_duration_hours <= 2:
            return "domestic_medium"
        else:
            return "domestic_long"
    
    @staticmethod
    def check_exemption(
        disruption_type: DisruptionType,
        reason: Optional[str] = None,
        notification_days: Optional[int] = None,
        alternative_offered_within_hours: Optional[float] = None
    ) -> Tuple[bool, Optional[ExemptionReason]]:
        """
        Check if the disruption qualifies for exemption from compensation
        
        Args:
            disruption_type: Type of disruption
            reason: Reason for disruption (weather, security, etc.)
            notification_days: Days before flight passenger was notified
            alternative_offered_within_hours: Hours within which alternative was offered
            
        Returns:
            Tuple of (is_exempt, exemption_reason)
        """
        # Check extraordinary circumstances
        exempt_reasons = [
            "weather", "extraordinary weather", "cyclone", "storm",
            "security", "security threat", "terrorism",
            "atc strike", "air traffic control strike",
            "political instability", "riots", "civil unrest"
        ]
        
        if reason and any(exempt in reason.lower() for exempt in exempt_reasons):
            if "weather" in reason.lower():
                return True, ExemptionReason.WEATHER
            elif "security" in reason.lower():
                return True, ExemptionReason.SECURITY
            elif "atc" in reason.lower() or "strike" in reason.lower():
                return True, ExemptionReason.ATC_STRIKE
            elif "political" in reason.lower() or "riot" in reason.lower():
                return True, ExemptionReason.POLITICAL_INSTABILITY
        
        # Check cancellation-specific exemptions
        if disruption_type == DisruptionType.CANCELLATION:
            # Passenger notified >= 2 weeks before
            if notification_days and notification_days >= 14:
                return True, ExemptionReason.EARLY_NOTIFICATION
            
            # Alternative flight offered within 1 hour
            if alternative_offered_within_hours and alternative_offered_within_hours <= 1:
                return True, ExemptionReason.ALTERNATIVE_OFFERED
        
        return False, None
    
    @staticmethod
    def calculate_compensation(
        disruption_type: DisruptionType,
        flight_duration_hours: float,
        delay_hours: Optional[float] = None,
        is_international: bool = False,
        exemption_reason: Optional[str] = None,
        notification_days: Optional[int] = None,
        alternative_offered_within_hours: Optional[float] = None,
        fare_paid: Optional[float] = None,
        downgrade_class_from: Optional[str] = None,
        downgrade_class_to: Optional[str] = None
    ) -> Dict:
        """
        Calculate compensation amount based on DGCA rules
        
        Args:
            disruption_type: Type of disruption
            flight_duration_hours: Duration of scheduled flight in hours
            delay_hours: Hours of delay (if applicable)
            is_international: Whether it's an international flight
            exemption_reason: Reason for exemption (if any)
            notification_days: Days before flight passenger was notified (for cancellation)
            alternative_offered_within_hours: Hours within which alternative offered
            fare_paid: Fare paid by passenger (for downgrade)
            downgrade_class_from: Original class (for downgrade)
            downgrade_class_to: Downgraded class
            
        Returns:
            Dictionary with compensation details
        """
        result = {
            "eligible": False,
            "compensation_amount": 0,
            "currency": "INR",
            "disruption_type": disruption_type.value,
            "reason": "",
            "exemption_applied": False,
            "exemption_reason": None
        }
        
        # Check for exemptions first
        is_exempt, exemption = DGCARulesEngine.check_exemption(
            disruption_type,
            exemption_reason,
            notification_days,
            alternative_offered_within_hours
        )
        
        if is_exempt:
            result["exemption_applied"] = True
            result["exemption_reason"] = exemption.value if exemption else None
            result["reason"] = f"No compensation due to: {exemption.value if exemption else 'exemption'}"
            return result
        
        # Determine flight category
        category = DGCARulesEngine.calculate_flight_duration_category(
            flight_duration_hours,
            is_international
        )
        
        # Calculate based on disruption type
        if disruption_type == DisruptionType.DELAY:
            if not delay_hours:
                result["reason"] = "Delay duration not provided"
                return result
            
            rules = DGCARulesEngine.COMPENSATION_MATRIX[category]
            
            if delay_hours >= rules["delay_threshold"]:
                result["eligible"] = True
                result["compensation_amount"] = rules["compensation"]
                result["reason"] = (
                    f"Delay of {delay_hours} hours exceeds threshold of "
                    f"{rules['delay_threshold']} hours for {category} flight"
                )
            else:
                result["reason"] = (
                    f"Delay of {delay_hours} hours does not meet minimum threshold of "
                    f"{rules['delay_threshold']} hours"
                )
        
        elif disruption_type == DisruptionType.CANCELLATION:
            rules = DGCARulesEngine.COMPENSATION_MATRIX[category]
            
            if rules["applies_to_cancellation"]:
                result["eligible"] = True
                result["compensation_amount"] = rules["compensation"]
                result["reason"] = f"Flight cancellation without adequate notice or alternative"
            else:
                result["reason"] = "Cancellation does not qualify for compensation"
        
        elif disruption_type == DisruptionType.DENIED_BOARDING:
            result["eligible"] = True
            result["compensation_amount"] = DGCARulesEngine.DENIED_BOARDING_COMPENSATION[category]
            result["reason"] = "Denied boarding despite valid confirmed ticket"
        
        elif disruption_type == DisruptionType.DOWNGRADE:
            if not fare_paid:
                result["reason"] = "Fare information required for downgrade compensation"
                return result
            
            refund_percentage = (
                DGCARulesEngine.DOWNGRADE_REFUND_PERCENTAGE["international"]
                if is_international
                else DGCARulesEngine.DOWNGRADE_REFUND_PERCENTAGE["domestic"]
            )
            
            # Simplified calculation - in real scenario, need fare difference
            result["eligible"] = True
            result["compensation_amount"] = int((fare_paid * refund_percentage) / 100)
            result["reason"] = (
                f"Downgrade from {downgrade_class_from} to {downgrade_class_to}: "
                f"{refund_percentage}% refund"
            )
        
        return result
    
    @staticmethod
    def get_airline_obligations(delay_hours: float, flight_duration_hours: float) -> Dict:
        """
        Get airline obligations based on delay duration (facilities to be provided)
        
        Args:
            delay_hours: Hours of delay
            flight_duration_hours: Scheduled flight duration
            
        Returns:
            Dictionary of obligations
        """
        obligations = {
            "meals_and_refreshments": False,
            "hotel_accommodation": False,
            "communication": False,  # 2 phone calls/emails
            "refund_option": False
        }
        
        category = DGCARulesEngine.calculate_flight_duration_category(flight_duration_hours)
        
        # For delays >= 2 hours
        if delay_hours >= 2:
            obligations["meals_and_refreshments"] = True
            obligations["communication"] = True
        
        # For significant delays (>= 6 hours for domestic, >= 12 for international)
        delay_threshold = 6 if "domestic" in category else 12
        
        if delay_hours >= delay_threshold:
            obligations["hotel_accommodation"] = True
            obligations["refund_option"] = True
        
        return obligations
    
    @staticmethod
    def format_claim_details(
        passenger_name: str,
        flight_number: str,
        flight_date: str,
        route: str,
        disruption_type: DisruptionType,
        compensation_result: Dict
    ) -> str:
        """
        Format claim details for legal documents
        
        Args:
            passenger_name: Name of passenger
            flight_number: Flight number
            flight_date: Date of flight
            route: Route (e.g., "Delhi to Mumbai")
            disruption_type: Type of disruption
            compensation_result: Result from calculate_compensation
            
        Returns:
            Formatted claim text
        """
        claim_text = f"""
FLIGHT COMPENSATION CLAIM UNDER DGCA CAR SECTION 3

Passenger Name: {passenger_name}
Flight Number: {flight_number}
Flight Date: {flight_date}
Route: {route}
Disruption Type: {disruption_type.value.upper()}

ELIGIBILITY STATUS: {'ELIGIBLE' if compensation_result['eligible'] else 'NOT ELIGIBLE'}
Compensation Amount: ₹{compensation_result['compensation_amount']:,}

Reason: {compensation_result['reason']}
"""
        
        if compensation_result.get('exemption_applied'):
            claim_text += f"\nExemption Applied: {compensation_result['exemption_reason']}"
        
        claim_text += """

LEGAL BASIS:
This claim is filed under DGCA Civil Aviation Requirements (CAR) Section 3, 
Series M, Part IV, which mandates airlines to compensate passengers for 
flight delays, cancellations, and denied boarding, except in cases of 
extraordinary circumstances beyond the airline's control.
"""
        
        return claim_text


# Helper functions for easy use
def check_delay_compensation(
    flight_duration_hours: float,
    delay_hours: float,
    is_international: bool = False,
    exemption_reason: Optional[str] = None
) -> Dict:
    """Quick helper to check delay compensation"""
    return DGCARulesEngine.calculate_compensation(
        DisruptionType.DELAY,
        flight_duration_hours,
        delay_hours=delay_hours,
        is_international=is_international,
        exemption_reason=exemption_reason
    )


def check_cancellation_compensation(
    flight_duration_hours: float,
    is_international: bool = False,
    notification_days: Optional[int] = None,
    alternative_offered_within_hours: Optional[float] = None,
    exemption_reason: Optional[str] = None
) -> Dict:
    """Quick helper to check cancellation compensation"""
    return DGCARulesEngine.calculate_compensation(
        DisruptionType.CANCELLATION,
        flight_duration_hours,
        is_international=is_international,
        notification_days=notification_days,
        alternative_offered_within_hours=alternative_offered_within_hours,
        exemption_reason=exemption_reason
    )


def check_denied_boarding_compensation(
    flight_duration_hours: float,
    is_international: bool = False
) -> Dict:
    """Quick helper to check denied boarding compensation"""
    return DGCARulesEngine.calculate_compensation(
        DisruptionType.DENIED_BOARDING,
        flight_duration_hours,
        is_international=is_international
    )


# Example usage
if __name__ == "__main__":
    # Example 1: Domestic flight delay
    print("=== Example 1: Domestic Flight Delay ===")
    result1 = check_delay_compensation(
        flight_duration_hours=2.5,  # Delhi to Mumbai (long)
        delay_hours=5,
        is_international=False
    )
    print(f"Eligible: {result1['eligible']}")
    print(f"Amount: ₹{result1['compensation_amount']:,}")
    print(f"Reason: {result1['reason']}\n")
    
    # Example 2: Cancellation with early notice (exempt)
    print("=== Example 2: Cancellation with Early Notice ===")
    result2 = check_cancellation_compensation(
        flight_duration_hours=1.5,
        is_international=False,
        notification_days=20  # Notified 20 days before
    )
    print(f"Eligible: {result2['eligible']}")
    print(f"Exemption: {result2['exemption_applied']}")
    print(f"Reason: {result2['reason']}\n")
    
    # Example 3: Denied boarding
    print("=== Example 3: Denied Boarding ===")
    result3 = check_denied_boarding_compensation(
        flight_duration_hours=2,
        is_international=False
    )
    print(f"Eligible: {result3['eligible']}")
    print(f"Amount: ₹{result3['compensation_amount']:,}")
    print(f"Reason: {result3['reason']}")
