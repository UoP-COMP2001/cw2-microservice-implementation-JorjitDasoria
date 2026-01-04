from datetime import datetime, timezone
from sqlalchemy import text
import config
from models import UserLog, User

def build_log_table():
    app = config.connex_app.app
    
    with app.app_context():
        print("Checking database for UserLog table...")

        try:
            with config.db.engine.connect() as connection:
                connection.execute(text("IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'CW2') BEGIN EXEC('CREATE SCHEMA [CW2]') END"))
                connection.commit()
        except Exception as e:
            print(f"Schema check skipped (might already exist): {e}")

        
        config.db.create_all()
        print("UserLog table created (if it didn't exist).")

       
        if not UserLog.query.first():
            print("UserLog table is empty. Attempting to seed a test entry...")
            
            
            existing_user = User.query.first()
            
            if existing_user:
                test_log = UserLog(
                    user_id_added=existing_user.user_id,
                    first_name_added=existing_user.first_name,
                    last_name_added=existing_user.last_name,
                    email_added=existing_user.email,
                    
                    ##timestamp_added=datetime.now(datetime.timezone.utc)()
                    timestamp_added=datetime.now(timezone.utc)
                )
                config.db.session.add(test_log)
                config.db.session.commit()
                print(f"Success! Seeded one audit log for user: {existing_user.first_name}")
            else:
                print("Warning: No users found in database, so could not create a dummy log.")
        else:
            print("UserLog table already has data. Skipping seed.")

if __name__ == "__main__":
    build_log_table()