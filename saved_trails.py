from flask import session, abort, make_response
from config import db
from models import User, SavedTrail, saved_trail_schema, saved_trails_schema

def check_permission(target_user_id):
    requester_id = session.get('user_id')
    requester_role = session.get('role', 'guest')

    if not requester_id:
        abort(401, "Please log in")
    if requester_role == 'administrator':
        return True
    if str(requester_id) == str(target_user_id):
        return True
        
    abort(403, "Permission Denied: You can only modify your own saved trails.")

# Endpoint functions

def read_all(user_id):

    check_permission(user_id)

    user = User.query.get(user_id)
    if not user:
        abort(404, f"User {user_id} not found")

    return saved_trails_schema.dump(user.saved_trails)

def add_trail(user_id, trail_data):

    check_permission(user_id)

    trail_ref_id = trail_data.get("trail_id")
    if not trail_ref_id:
        abort(400, "trail_id is required")

    existing = SavedTrail.query.filter_by(user_id=user_id, trail_id=trail_ref_id).first()
    if existing:
        abort(409, f"Trail {trail_ref_id} is already saved by this user")

    new_save = SavedTrail(
        user_id=user_id,
        trail_id=trail_ref_id
    )
    
    db.session.add(new_save)
    db.session.commit()
    
    return saved_trail_schema.dump(new_save), 201

def remove_trail(user_id, trail_id):
    check_permission(user_id)
    saved_entry = SavedTrail.query.filter_by(user_id=user_id, trail_id=trail_id).first()

    if saved_entry:
        db.session.delete(saved_entry)
        db.session.commit()
        return make_response(f"Trail {trail_id} removed from saved list", 204)
    else:
        abort(404, f"Trail {trail_id} not found in user's list")