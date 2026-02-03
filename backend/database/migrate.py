
import sqlite3
import os
from backend.database.db_session import DATABASE_URL

def run_migrations():
    """
    Check for missing columns in the database and add them if necessary.
    This handles the migration from the old schema to the new one with PNR/Passenger fields.
    """
    print("Checking for database migrations...")

    # Parse DB URL (assuming sqlite:///flyclaim.db)
    if DATABASE_URL.startswith('sqlite:///'):
        db_path = DATABASE_URL.replace('sqlite:///', '')
    else:
        print("Skipping migration: Non-SQLite database")
        return

    if not os.path.exists(db_path):
        print("Database not found, skipping migration (will be created by init_db or on first request)")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get existing columns in claims table
        cursor.execute("PRAGMA table_info(claims)")
        columns = [info[1] for info in cursor.fetchall()]

        # Define new columns to check/add
        new_columns = {
            'pnr': 'VARCHAR(10)',
            'passenger_name': 'VARCHAR(100)',
            'route_from': 'VARCHAR(100)',
            'route_to': 'VARCHAR(100)'
        }

        migrated = False
        for col_name, col_type in new_columns.items():
            if col_name not in columns:
                print(f"Migrating: Adding column '{col_name}' to claims table...")
                try:
                    cursor.execute(f"ALTER TABLE claims ADD COLUMN {col_name} {col_type}")
                    migrated = True
                except sqlite3.OperationalError as e:
                    print(f"Error adding column {col_name}: {e}")

        if migrated:
            conn.commit()
            print("Database migration completed successfully.")
        else:
            print("Database schema is up to date.")

        conn.close()

    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    run_migrations()
