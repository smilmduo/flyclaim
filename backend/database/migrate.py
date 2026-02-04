"""
Database Migration Script
Safely updates existing database schema
"""

import sys
import os
import sqlite3

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_PATH = 'flyclaim.db'

def run_migrations():
    """Update database schema with new columns"""
    print(f"Checking database schema for {DB_PATH}...")

    if not os.path.exists(DB_PATH):
        print("Database does not exist. Run init_db.py instead.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check columns in claims table
        cursor.execute("PRAGMA table_info(claims)")
        existing_columns = [info[1] for info in cursor.fetchall()]

        # Define new columns to add
        new_columns = {
            'eligibility_details': 'TEXT',
            'resolution_notes': 'TEXT',
            'amount_received': 'INTEGER',
            'submitted_to_email': 'VARCHAR(100)',
            'airline_response_deadline': 'DATETIME',
            'pnr': 'VARCHAR(10)',
            'passenger_name': 'VARCHAR(100)',
            'route_from': 'VARCHAR(100)',
            'route_to': 'VARCHAR(100)'
        }

        # Add missing columns
        for col_name, col_type in new_columns.items():
            if col_name not in existing_columns:
                print(f"Adding missing column: {col_name} ({col_type})")
                cursor.execute(f"ALTER TABLE claims ADD COLUMN {col_name} {col_type}")

        conn.commit()
        print("✓ Schema migration completed successfully")

    except Exception as e:
        print(f"✗ Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    run_migrations()
