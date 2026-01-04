from datetime import date
from sqlalchemy import text
import config
from models import User, Role, Location, Activity

# Data to initialize
TEST_ROLES = [
    {"role_name": "general user"},
    {"role_name": "administrator"}
]

TEST_LOCATIONS = [
    {"location_name": "Bristol, Devon, England", "default_units": "Metric", "default_language": "en"},
    {"location_name": "England", "default_units": "Imperial", "default_language": "en"},
    {"location_name": "Exeter, Devon, England", "default_units": "Imperial", "default_language": "en"},
    {"location_name": "Plymouth, Devon, England", "default_units": "Metric", "default_language": "en"},
    {"location_name": "England", "default_units": "Metric", "default_language": "en"},
    {"location_name": "Westminster, london, GreaterLondon", "default_units": "Imperial", "default_language": "en"}
]

TEST_ACTIVITIES = [
    {"activity_name": "Backpacking"},
    {"activity_name": "Bike Touring"},
    {"activity_name": "Birding"},
    {"activity_name": "Camping"},
    {"activity_name": "Cross-Country skiing"},
    {"activity_name": "Fishing"},
    {"activity_name": "Hiking"},
    {"activity_name": "Horseback riding"},
    {"activity_name": "Mountain biking"},
    {"activity_name": "Off-road driving"},
    {"activity_name": "Paddle sports"},
    {"activity_name": "Road biking"},
    {"activity_name": "Rock climbing"},
    {"activity_name": "Running"},
    {"activity_name": "Scenic driving"},
    {"activity_name": "skiing"},
    {"activity_name": "Snowshoeing"},
    {"activity_name": "Via ferrata"},
    {"activity_name": "Walking"}
]

TEST_USERS = [
    {
        "first_name": "Tim", "last_name": "Berners-Lee", "email": "tim@example.com",
        "phone_number": "0123456789", "about_me": "I invented the web.", "password": "hashed_secret_password",
        "activity_time_preference": "pace", "height": 1.80, "weight": 75.50, "birthday": date(1955, 6, 8),
        "role_name": "general user",
        "location_name": "Plymouth, Devon, England", "location_units": "Metric",
        "activities": ["Running", "Road biking"]
    },
    {
        "first_name": "Ada", "last_name": "Lovelace", "email": "ada@example.com",
        "phone_number": "07700900123", "about_me": "First programmer.", "password": "secure_password_1",
        "activity_time_preference": "speed", "height": 1.65, "weight": 60.00, "birthday": date(1815, 12, 10),
        "role_name": "administrator",
        "location_name": "Westminster, london, GreaterLondon", "location_units": "Imperial",
        "activities": ["Walking", "Hiking", "Birding"]
    },
    {
        "first_name": "Alan", "last_name": "Turing", "email": "alan@example.com",
        "phone_number": "07700900456", "about_me": "Running implies computing.", "password": "enigma_code",
        "activity_time_preference": "pace", "height": 1.78, "weight": 70.20, "birthday": date(1912, 6, 23),
        "role_name": "general user",
        "location_name": "England", "location_units": "Imperial", 
        "activities": ["Running", "Cross-Country skiing"]
    },
    {
        "first_name": "Grace", "last_name": "Hopper", "email": "grace@example.com",
        "phone_number": "07700900789", "about_me": "Debugging the trail.", "password": "cobol_forever",
        "activity_time_preference": "speed", "height": 1.68, "weight": 65.00, "birthday": date(1906, 12, 9),
        "role_name": "general user",
        "location_name": "Exeter, Devon, England", "location_units": "Imperial",
        "activities": ["Paddle sports", "Camping"]
    },
    {
        "first_name": "Katherine", "last_name": "Johnson", "email": "katherine@example.com",
        "phone_number": "07700900999", "about_me": "Calculated the trajectory.", "password": "nasa_orbit",
        "activity_time_preference": "pace", "height": 1.62, "weight": 58.50, "birthday": date(1918, 8, 26),
        "role_name": "general user",
        "location_name": "Bristol, Devon, England", "location_units": "Metric",
        "activities": ["Walking", "Scenic driving"]
    },
    {
        "first_name": "Margaret", "last_name": "Hamilton", "email": "margaret@example.com",
        "phone_number": "07700900000", "about_me": "Software engineering pioneer.", "password": "apollo_11",
        "activity_time_preference": "speed", "height": 1.70, "weight": 62.00, "birthday": date(1936, 8, 17),
        "role_name": "administrator",
        "location_name": "England", "location_units": "Metric",
        "activities": ["Hiking", "Rock climbing", "Mountain biking"]
    }
]

def build_db():
    app = config.connex_app.app
    
    with app.app_context():
        # Creating schema 
        try:
            with config.db.engine.connect() as connection:
                connection.execute(text("IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'CW2') BEGIN EXEC('CREATE SCHEMA [CW2]') END"))
                connection.commit()
                print("Schema 'CW2' checked/created.")
        except Exception as e:
            print(f"Error checking schema: {e}")
            return 

        #c create tables
        config.db.create_all()
        print("Tables created (if they didn't exist).")
        
        
        
        #roles
        roles_map = {}
        for r_data in TEST_ROLES:
            role = Role.query.filter_by(role_name=r_data["role_name"]).one_or_none()
            if not role:
                role = Role(role_name=r_data["role_name"])
                config.db.session.add(role)
                print(f"Adding Role: {r_data['role_name']}")
            roles_map[r_data["role_name"]] = role
            
        #locations
        locs_map = {}
        for l_data in TEST_LOCATIONS:
            
            loc = Location.query.filter_by(
                location_name=l_data["location_name"], 
                default_units=l_data["default_units"]
            ).one_or_none()
            
            if not loc:
                loc = Location(
                    location_name=l_data["location_name"],
                    default_units=l_data["default_units"],
                    default_language=l_data["default_language"]
                )
                config.db.session.add(loc)
                print(f"Adding Location: {l_data['location_name']} ({l_data['default_units']})")
            
            
            key = f"{l_data['location_name']}_{l_data['default_units']}"
            locs_map[key] = loc

        #activities
        acts_map = {}
        for a_data in TEST_ACTIVITIES:
            act = Activity.query.filter_by(activity_name=a_data["activity_name"]).one_or_none()
            if not act:
                act = Activity(activity_name=a_data["activity_name"])
                config.db.session.add(act)
                print(f"Adding Activity: {a_data['activity_name']}")
            acts_map[a_data["activity_name"]] = act

        config.db.session.commit()

        #users loop
        print("\n--- Seeding Users ---")
        for u_data in TEST_USERS:
            
            user = User.query.filter_by(email=u_data["email"]).one_or_none()
            
            if not user:
                
                role_obj = roles_map.get(u_data["role_name"])
                
                
                loc_key = f"{u_data['location_name']}_{u_data['location_units']}"
                loc_obj = locs_map.get(loc_key)

                if role_obj and loc_obj:
                    new_user = User(
                        first_name=u_data["first_name"],
                        last_name=u_data["last_name"],
                        email=u_data["email"],
                        phone_number=u_data["phone_number"],
                        about_me=u_data["about_me"],
                        activity_time_preference=u_data["activity_time_preference"],
                        height=u_data["height"],
                        weight=u_data["weight"],
                        birthday=u_data["birthday"],
                        password=u_data["password"],
                        role=role_obj,
                        location=loc_obj
                    )
                    
                    
                    for act_name in u_data["activities"]:
                        if act_name in acts_map:
                            new_user.activities.append(acts_map[act_name])
                            
                    config.db.session.add(new_user)
                    print(f"Creating user: {u_data['email']}")
                else:
                    print(f"Skipping {u_data['email']}: Role or Location not found in maps.")
            else:
                print(f"User {u_data['email']} already exists.")

        config.db.session.commit()
        print("Database build complete.")

if __name__ == "__main__":
    build_db()