"""
Database Models for FlyClaim AI
SQLAlchemy ORM models for claims, users, and tracking
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class ClaimStatus(enum.Enum):
    """Status of a claim"""
    INITIATED = "initiated"
    ELIGIBILITY_CHECKED = "eligibility_checked"
    DOCUMENT_GENERATED = "document_generated"
    SUBMITTED_TO_AIRLINE = "submitted_to_airline"
    AWAITING_RESPONSE = "awaiting_response"
    AIRLINE_RESPONDED = "airline_responded"
    ESCALATED_AIRSEWA = "escalated_airsewa"
    ESCALATED_DGCA = "escalated_dgca"
    RESOLVED = "resolved"
    REJECTED = "rejected"
    PAID = "paid"
    CANCELLED = "cancelled"


class DisruptionType(enum.Enum):
    """Type of flight disruption"""
    DELAY = "delay"
    CANCELLATION = "cancellation"
    DENIED_BOARDING = "denied_boarding"
    DOWNGRADE = "downgrade"


class User(Base):
    """User/Passenger model"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100))
    email = Column(String(100))
    password_hash = Column(String(128))
    
    # WhatsApp conversation state
    whatsapp_state = Column(String(50), default='idle')  # idle, collecting_info, awaiting_confirmation
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    claims = relationship("Claim", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, phone={self.phone_number}, name={self.name})>"


class Claim(Base):
    """Flight compensation claim model"""
    __tablename__ = 'claims'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    claim_reference = Column(String(50), unique=True, nullable=False, index=True)
    
    # Foreign key
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Flight details
    flight_number = Column(String(20), nullable=False)
    airline_code = Column(String(10))
    airline_name = Column(String(100))
    flight_date = Column(DateTime, nullable=False)
    route_from = Column(String(100))
    route_to = Column(String(100))
    flight_duration_hours = Column(Float)
    is_international = Column(Boolean, default=False)
    
    # Disruption details
    disruption_type = Column(SQLEnum(DisruptionType), nullable=False)
    delay_hours = Column(Float)
    cancellation_notice_days = Column(Integer)
    exemption_reason = Column(Text)
    
    # Compensation calculation
    is_eligible = Column(Boolean, default=False)
    compensation_amount = Column(Integer, default=0)
    compensation_currency = Column(String(10), default='INR')
    calculation_reason = Column(Text)
    exemption_applied = Column(Boolean, default=False)
    
    # Document paths
    claim_letter_path = Column(String(500))
    supporting_documents = Column(Text)  # JSON array of document paths
    
    # Submission details
    submitted_to_email = Column(String(100))
    submitted_at = Column(DateTime)
    airline_response_deadline = Column(DateTime)
    
    # Status tracking
    status = Column(SQLEnum(ClaimStatus), default=ClaimStatus.INITIATED, nullable=False)
    
    # Escalation
    escalated_to_airsewa = Column(Boolean, default=False)
    airsewa_reference = Column(String(100))
    airsewa_escalation_date = Column(DateTime)
    
    escalated_to_dgca = Column(Boolean, default=False)
    dgca_reference = Column(String(100))
    dgca_escalation_date = Column(DateTime)
    
    # Resolution
    resolution_date = Column(DateTime)
    resolution_notes = Column(Text)
    amount_received = Column(Integer)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="claims")
    activities = relationship("ClaimActivity", back_populates="claim", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Claim(id={self.id}, ref={self.claim_reference}, flight={self.flight_number}, status={self.status.value})>"
    
    def to_dict(self):
        """Convert claim to dictionary"""
        return {
            'id': self.id,
            'claim_reference': self.claim_reference,
            'flight_number': self.flight_number,
            'airline_name': self.airline_name,
            'flight_date': self.flight_date.isoformat() if self.flight_date else None,
            'route': f"{self.route_from} to {self.route_to}" if self.route_from and self.route_to else None,
            'disruption_type': self.disruption_type.value if self.disruption_type else None,
            'delay_hours': self.delay_hours,
            'is_eligible': self.is_eligible,
            'compensation_amount': self.compensation_amount,
            'status': self.status.value if self.status else None,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ClaimActivity(Base):
    """Activity log for claims (audit trail)"""
    __tablename__ = 'claim_activities'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    claim_id = Column(Integer, ForeignKey('claims.id'), nullable=False)
    
    # Activity details
    activity_type = Column(String(50), nullable=False)  # e.g., 'status_change', 'email_sent', 'escalation'
    description = Column(Text)
    performed_by = Column(String(50), default='system')  # 'system', 'user', 'admin'
    
    # Additional data (JSON serialized)
    activity_metadata = Column(Text)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    claim = relationship("Claim", back_populates="activities")
    
    def __repr__(self):
        return f"<ClaimActivity(id={self.id}, claim_id={self.claim_id}, type={self.activity_type})>"


class AirlineNodalOfficer(Base):
    """Airline nodal officer contact information"""
    __tablename__ = 'airline_nodal_officers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    airline_code = Column(String(10), unique=True, nullable=False, index=True)
    airline_name = Column(String(100), nullable=False)
    
    # Contact details
    nodal_officer_name = Column(String(100))
    email = Column(String(100), nullable=False)
    alternate_email = Column(String(100))
    phone = Column(String(20))
    
    # Address
    office_address = Column(Text)
    
    # Metadata
    verified = Column(Boolean, default=False)
    last_verified_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<AirlineNodalOfficer(airline={self.airline_name}, email={self.email})>"


class FlightVerification(Base):
    """Cache for flight verification API responses"""
    __tablename__ = 'flight_verifications'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_number = Column(String(20), nullable=False, index=True)
    flight_date = Column(DateTime, nullable=False, index=True)
    
    # API response data
    actual_departure = Column(DateTime)
    scheduled_departure = Column(DateTime)
    actual_arrival = Column(DateTime)
    scheduled_arrival = Column(DateTime)
    
    delay_minutes = Column(Integer)
    status = Column(String(50))  # scheduled, delayed, cancelled, active, landed
    
    # Route
    departure_airport = Column(String(10))
    arrival_airport = Column(String(10))
    
    # Raw API response (JSON)
    raw_response = Column(Text)
    
    # Cache metadata
    verified_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    
    def __repr__(self):
        return f"<FlightVerification(flight={self.flight_number}, date={self.flight_date}, status={self.status})>"


# Utility functions
def generate_claim_reference(claim_id: int, flight_number: str) -> str:
    """Generate unique claim reference number"""
    from datetime import datetime
    timestamp = datetime.utcnow().strftime('%Y%m%d')
    return f"FC-{timestamp}-{flight_number}-{claim_id:04d}"


def get_airline_name(airline_code: str) -> str:
    """Map airline code to full name"""
    airline_map = {
        '6E': 'IndiGo',
        'AI': 'Air India',
        'SG': 'SpiceJet',
        'UK': 'Vistara',
        'I5': 'AirAsia India',
        'G8': 'Go First',
        'QP': 'Akasa Air',
        '9I': 'Alliance Air',
        # International
        'EK': 'Emirates',
        'QR': 'Qatar Airways',
        'SQ': 'Singapore Airlines',
        'TG': 'Thai Airways',
        'BA': 'British Airways',
        'LH': 'Lufthansa',
    }
    return airline_map.get(airline_code.upper(), airline_code)


def parse_flight_number(flight_number: str) -> tuple:
    """
    Parse flight number to extract airline code
    Example: '6E-234' -> ('6E', '234')
    """
    import re
    match = re.match(r'([A-Z0-9]{2})[- ]?(\d+)', flight_number.upper())
    if match:
        return match.group(1), match.group(2)
    return None, None
