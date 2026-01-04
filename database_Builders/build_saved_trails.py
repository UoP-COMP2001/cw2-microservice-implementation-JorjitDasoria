# build_saved_trails.py
import config
from models import SavedTrail

def build_saved_trails_table():
    app = config.connex_app.app
    with app.app_context():
        config.db.create_all() 
        print("create complete.")

if __name__ == "__main__":
    build_saved_trails_table()