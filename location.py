# location.py
from flask import request, abort, make_response
from config import db
from models import Location, LocationSchema, User


location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)


def check_admin():
    
    requester_id = request.headers.get('X-User-ID')
    
    if not requester_id:
        abort(401, "Authentication Header (X-User-ID) missing")

    user = User.query.get(requester_id)
    

    if not user or not user.role or user.role.role_name.lower() != "administrator":
        abort(403, "Permission Denied: Only administrators can manage locations.")



def read_all():
    
    locations = Location.query.all()
    return locations_schema.dump(locations)

def read_one(location_id):
    
    location = Location.query.get(location_id)
    if location is not None:
        return location_schema.dump(location)
    else:
        abort(404, f"Location with ID {location_id} not found")

def create(location_data):
    
    check_admin() 
    name = location_data.get("location_name")
    units = location_data.get("default_units")
    
    existing = Location.query.filter_by(location_name=name, default_units=units).one_or_none()

    if existing is None:
        new_loc = location_schema.load(location_data, session=db.session)
        db.session.add(new_loc)
        db.session.commit()
        return location_schema.dump(new_loc), 201
    else:
        abort(406, f"Location '{name}' with units '{units}' already exists")

def update(location_id, location_data):
    
    check_admin()

    existing_loc = Location.query.get(location_id)

    if existing_loc:
        update_loc = location_schema.load(location_data, session=db.session)
        
        existing_loc.location_name = update_loc.location_name
        existing_loc.default_units = update_loc.default_units
        existing_loc.default_language = update_loc.default_language
        
        db.session.merge(existing_loc)
        db.session.commit()
        return location_schema.dump(existing_loc), 200
    else:
        abort(404, f"Location with ID {location_id} not found")

def delete(location_id):
    
    check_admin() # Security Check

    existing_loc = Location.query.get(location_id)

    if existing_loc:
        # Note: This might fail if users are currently assigned to this location
        try:
            db.session.delete(existing_loc)
            db.session.commit()
            return make_response(f"Location {location_id} successfully deleted", 204)
        except Exception:
            db.session.rollback()
            abort(409, "Cannot delete location because users are assigned to it.")
    else:
        abort(404, f"Location with ID {location_id} not found")