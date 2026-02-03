"""
Database Initialization Script
Creates tables and seeds initial data
"""

import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.models import Base, AirlineNodalOfficer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///flyclaim.db')


def create_tables(engine):
    """Create all tables"""
    print("Creating database tables...")
    Base.metadata.create_all(engine)
    print("✓ Tables created successfully")


def seed_airline_data(session):
    """Seed airline nodal officer information"""
    print("\nSeeding airline nodal officer data...")
    
    airlines = [
        {
            'airline_code': '6E',
            'airline_name': 'IndiGo',
            'email': 'customer.relations@goindigo.in',
            'phone': '+91-9910383838',
            'office_address': 'Upper Ground Floor, Thapar House, Gate No. 2, Western Wing, 124 Janpath, New Delhi - 110001'
        },
        {
            'airline_code': 'AI',
            'airline_name': 'Air India',
            'email': 'feedback@airindia.in',
            'phone': '+91-124-2641407',
            'office_address': 'Airlines House, 113, Gurudwara Rakabganj Road, New Delhi - 110001'
        },
        {
            'airline_code': 'SG',
            'airline_name': 'SpiceJet',
            'email': 'complaints@spicejet.com',
            'phone': '+91-987-1803333',
            'office_address': '319, Udyog Vihar, Phase IV, Gurgaon - 122015, Haryana'
        },
        {
            'airline_code': 'UK',
            'airline_name': 'Vistara',
            'email': 'customer.feedback@airvistara.com',
            'phone': '+91-9289228888',
            'office_address': 'One Horizon Center, Golf Course Road, DLF Phase 5, Sector 43, Gurgaon - 122002'
        },
        {
            'airline_code': 'I5',
            'airline_name': 'AirAsia India',
            'email': 'support@airasia.com',
            'phone': '+91-80-46452500',
            'office_address': 'Gopalan Millennium Tower, ITPL Main Road, Whitefield, Bangalore - 560066'
        },
        {
            'airline_code': 'G8',
            'airline_name': 'Go First',
            'email': 'care@flygofirst.com',
            'phone': '+91-22-71229900',
            'office_address': 'Mumbai Airport, Domestic Terminal 1, Santa Cruz East, Mumbai - 400099'
        },
        {
            'airline_code': 'QP',
            'airline_name': 'Akasa Air',
            'email': 'support@akasaair.com',
            'phone': '+91-22-71229900',
            'office_address': 'Akasa Air, Mumbai, Maharashtra'
        },
    ]
    
    for airline_data in airlines:
        # Check if already exists
        existing = session.query(AirlineNodalOfficer).filter_by(
            airline_code=airline_data['airline_code']
        ).first()
        
        if not existing:
            officer = AirlineNodalOfficer(**airline_data)
            session.add(officer)
            print(f"  ✓ Added {airline_data['airline_name']}")
        else:
            print(f"  - {airline_data['airline_name']} already exists")
    
    session.commit()
    print("✓ Airline data seeded successfully")


def init_database():
    """Initialize the complete database"""
    print("=" * 60)
    print("FlyClaim AI - Database Initialization")
    print("=" * 60)
    
    # Create engine
    print(f"\nConnecting to database: {DATABASE_URL}")
    engine = create_engine(DATABASE_URL, echo=False)
    
    # Create tables
    create_tables(engine)
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Seed data
        seed_airline_data(session)
        
        print("\n" + "=" * 60)
        print("✓ Database initialization completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error during initialization: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    init_database()
