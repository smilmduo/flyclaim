"""
Intake Agent - Extracts flight details from natural language input
Uses GPT-4 to parse user messages and extract structured flight information
"""
print("🔥 USING GEMINI INTAKE AGENT 🔥")

import os
import json
from datetime import datetime
from typing import Dict, Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class IntakeAgent:
    """
    Agent responsible for extracting flight information from user input
    """
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            model_name = "gemini-3-flash-preview"
            print("Using Gemini model:", model_name)
            self.model = genai.GenerativeModel(model_name)
        else:
            print("⚠️ Gemini API key not found. Using fallback regex parser.")
            self.model = None

    
    def extract_flight_details(self, user_message: str, context: Optional[Dict] = None) -> Dict:
        """
        Extract flight details from natural language input
        
        Args:
            user_message: User's message describing their flight issue
            context: Optional previous conversation context
            
        Returns:
            Dictionary with extracted flight details
        """
        
        system_prompt = """You are an AI assistant for FlyClaim AI, helping passengers file flight compensation claims.

Your task is to extract flight information from the user's message.

Extract the following information:
1. Flight number (e.g., 6E-234, AI-615)
2. Airline name (if mentioned)
3. Flight date (convert to YYYY-MM-DD format, assume current year if not mentioned)
4. Departure city/airport
5. Arrival city/airport
6. Disruption type (delay, cancellation, denied_boarding)
7. Delay duration in hours (if mentioned)
8. Passenger name (if mentioned)
9. Any additional context

IMPORTANT RULES:
- If the date is mentioned as "yesterday", "today", "last week", calculate the actual date
- Extract flight number in format: AIRLINE_CODE-NUMBER (e.g., 6E-234)
- For delays, extract the number of hours
- Identify if it's a delay, cancellation, or denied boarding
- If information is missing, mark it as null

Respond ONLY with valid JSON in this exact format:
{
  "flight_number": "string or null",
  "airline_name": "string or null",
  "flight_date": "YYYY-MM-DD or null",
  "departure": "string or null",
  "arrival": "string or null",
  "disruption_type": "delay|cancellation|denied_boarding or null",
  "delay_hours": number or null,
  "passenger_name": "string or null",
  "additional_context": "string or null",
  "confidence": "high|medium|low",
  "missing_fields": ["array of missing required fields"]
}

Example:
Input: "My IndiGo flight 6E-234 from Delhi to Mumbai on 28 Oct was delayed by 5 hours"
Output:
{
  "flight_number": "6E-234",
  "airline_name": "IndiGo",
  "flight_date": "2024-10-28",
  "departure": "Delhi",
  "arrival": "Mumbai",
  "disruption_type": "delay",
  "delay_hours": 5,
  "passenger_name": null,
  "additional_context": null,
  "confidence": "high",
  "missing_fields": ["passenger_name"]
}
"""
        
        user_prompt = f"User message: {user_message}"
        
        if context:
            user_prompt += f"\n\nPrevious context: {json.dumps(context)}"
        
        try:
            if self.model:
                prompt = f"""
                {system_prompt}

                User message:
                {user_message}

                Respond ONLY with valid JSON.
               """

                response = self.model.generate_content(prompt)
                result = json.loads(response.text)
            else:
                # Fallback Regex Implementation
                import re

                # Mock result structure
                result = {
                    "flight_number": None,
                    "airline_name": None,
                    "flight_date": None,
                    "departure": None,
                    "arrival": None,
                    "disruption_type": None,
                    "delay_hours": None,
                    "passenger_name": None,
                    "additional_context": None,
                    "confidence": "low",
                    "missing_fields": []
                }

                # Flight Number (e.g. 6E-234, AI-101)
                flight_match = re.search(r'([A-Z0-9]{2,3}-?\d{3,4})', user_message, re.IGNORECASE)
                if flight_match:
                    result['flight_number'] = flight_match.group(1).upper().replace(' ', '-')

                # Airline (Simple check)
                airlines = ['IndiGo', 'Air India', 'SpiceJet', 'Vistara', 'Akasa']
                for airline in airlines:
                    if airline.lower() in user_message.lower():
                        result['airline_name'] = airline
                        break

                # Date (YYYY-MM-DD or simple date) - Very simplified for fallback
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', user_message)
                if date_match:
                    result['flight_date'] = date_match.group(1)
                else:
                    # Look for "28 October 2025" style
                    date_match_text = re.search(r'(\d{1,2})\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{4})', user_message, re.IGNORECASE)
                    if date_match_text:
                        try:
                            dt = datetime.strptime(date_match_text.group(0), "%d %B %Y")
                            result['flight_date'] = dt.strftime("%Y-%m-%d")
                        except:
                            pass

                # Delay
                if "delay" in user_message.lower():
                    result['disruption_type'] = "delay"
                    hours_match = re.search(r'(\d+)\s*hours?', user_message)
                    if hours_match:
                        result['delay_hours'] = int(hours_match.group(1))
                elif "cancel" in user_message.lower():
                    result['disruption_type'] = "cancellation"
                elif "denied" in user_message.lower():
                    result['disruption_type'] = "denied_boarding"

                # From/To (Simple "from X to Y")
                route_match = re.search(r'from\s+([A-Za-z]+)\s+to\s+([A-Za-z]+)', user_message, re.IGNORECASE)
                if route_match:
                    result['departure'] = route_match.group(1).title()
                    result['arrival'] = route_match.group(2).title()
            
            # Add metadata
            result['raw_message'] = user_message
            result['extracted_at'] = datetime.utcnow().isoformat()
            result['agent'] = 'intake_agent'
            
            return result
            
        except Exception as e:
            return {
                'error': str(e),
                'raw_message': user_message,
                'agent': 'intake_agent',
                'confidence': 'low',
                'missing_fields': ['all']
            }
    
    def validate_extracted_data(self, extracted_data: Dict) -> Dict:
        """
        Validate and normalize extracted data
        
        Args:
            extracted_data: Data extracted by extract_flight_details
            
        Returns:
            Dictionary with validation results
        """
        validation = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'required_follow_up': []
        }
        
        # Check required fields
        required_fields = ['flight_number', 'flight_date', 'disruption_type']
        
        for field in required_fields:
            if not extracted_data.get(field):
                validation['is_valid'] = False
                validation['errors'].append(f"Missing required field: {field}")
                validation['required_follow_up'].append(field)
        
        # Validate flight number format
        if extracted_data.get('flight_number'):
            flight_num = extracted_data['flight_number']
            if not any(char.isdigit() for char in flight_num):
                validation['warnings'].append("Flight number format may be incorrect")
        
        # Validate date format
        if extracted_data.get('flight_date'):
            try:
                datetime.strptime(extracted_data['flight_date'], '%Y-%m-%d')
            except ValueError:
                validation['errors'].append("Invalid date format")
                validation['is_valid'] = False
        
        # Check for delay duration if disruption is delay
        if extracted_data.get('disruption_type') == 'delay':
            if not extracted_data.get('delay_hours'):
                validation['warnings'].append("Delay duration not specified")
                validation['required_follow_up'].append('delay_hours')
        
        # Check route information
        if not extracted_data.get('departure') or not extracted_data.get('arrival'):
            validation['warnings'].append("Route information incomplete")
            validation['required_follow_up'].extend(['departure', 'arrival'])
        
        return validation
    
    def generate_follow_up_question(self, missing_field: str) -> str:
        """
        Generate a natural follow-up question for missing information
        
        Args:
            missing_field: Name of the missing field
            
        Returns:
            Follow-up question string
        """
        questions = {
            'flight_number': "Could you please provide your flight number? (e.g., 6E-234, AI-615)",
            'flight_date': "When was your flight? Please provide the date.",
            'disruption_type': "What happened with your flight? Was it delayed, cancelled, or were you denied boarding?",
            'delay_hours': "How many hours was your flight delayed?",
            'departure': "Which city or airport did your flight depart from?",
            'arrival': "Which city or airport was your destination?",
            'passenger_name': "What is your full name as it appears on the ticket?",
            'passenger_email': "What is your email address for communication?",
            'passenger_phone': "What is your phone number?"
        }
        
        return questions.get(missing_field, f"Please provide the {missing_field.replace('_', ' ')}.")
    
    def create_confirmation_message(self, extracted_data: Dict) -> str:
        """
        Create a confirmation message summarizing extracted information
        
        Args:
            extracted_data: Extracted flight details
            
        Returns:
            Formatted confirmation message
        """
        parts = []
        
        if extracted_data.get('flight_number'):
            parts.append(f"Flight: {extracted_data['flight_number']}")
        
        if extracted_data.get('airline_name'):
            parts.append(f"Airline: {extracted_data['airline_name']}")
        
        if extracted_data.get('flight_date'):
            parts.append(f"Date: {extracted_data['flight_date']}")
        
        if extracted_data.get('departure') and extracted_data.get('arrival'):
            parts.append(f"Route: {extracted_data['departure']} → {extracted_data['arrival']}")
        
        if extracted_data.get('disruption_type'):
            disruption = extracted_data['disruption_type'].replace('_', ' ').title()
            parts.append(f"Issue: {disruption}")
        
        if extracted_data.get('delay_hours'):
            parts.append(f"Delay: {extracted_data['delay_hours']} hours")
        
        message = "I've extracted the following information:\n\n" + "\n".join([f"✓ {part}" for part in parts])
        
        if extracted_data.get('missing_fields') and len(extracted_data['missing_fields']) > 0:
            message += "\n\n⚠️ We still need some information to proceed with your claim."
        
        return message


# Example usage and testing
if __name__ == "__main__":
    agent = IntakeAgent()
    
    # Test case 1: Complete information
    print("=== Test Case 1: Complete Information ===")
    message1 = "My IndiGo flight 6E-234 from Delhi to Mumbai on 28 October was delayed by 5 hours"
    result1 = agent.extract_flight_details(message1)
    print(json.dumps(result1, indent=2))
    print(f"\nConfirmation:\n{agent.create_confirmation_message(result1)}")
    
    # Test case 2: Incomplete information
    print("\n\n=== Test Case 2: Incomplete Information ===")
    message2 = "My flight was delayed yesterday"
    result2 = agent.extract_flight_details(message2)
    print(json.dumps(result2, indent=2))
    
    validation = agent.validate_extracted_data(result2)
    print(f"\nValidation: {json.dumps(validation, indent=2)}")
    
    # Test case 3: Cancellation
    print("\n\n=== Test Case 3: Cancellation ===")
    message3 = "Air India flight AI-615 from Bangalore to Delhi on 1st November was cancelled"
    result3 = agent.extract_flight_details(message3)
    print(json.dumps(result3, indent=2))
