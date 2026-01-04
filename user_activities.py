# user_activities.py
from flask import request, abort, make_response
from config import db
from models import User, Activity, user_schema

def check_permission(target_user_id):
    requester_id = request.headers.get('X-User-ID')
    
    if not requester_id:
        abort(401, "Authentication Header (X-User-ID) missing")

    if str(requester_id) == str(target_user_id):
        return True

    requester = User.query.get(requester_id)
    if requester and requester.role and requester.role.role_name.lower() == "administrator":
        return True

    abort(403, "Permission Denied: You can only edit your own favorites.")

def add_favorite(user_id, activity_data):
    
    check_permission(user_id) # Security Check

    activity_id = activity_data.get("activity_id")
    
    user = User.query.get(user_id)
    activity = Activity.query.get(activity_id)

    if not user:
        abort(404, f"User {user_id} not found")
    if not activity:
        abort(404, f"Activity {activity_id} not found")


    if activity in user.activities:
        abort(409, f"User already has activity '{activity.activity_name}' listed")


    user.activities.append(activity)
    db.session.commit()

    return user_schema.dump(user), 201

def remove_favorite(user_id, activity_id):

    check_permission(user_id) # Security Check

    user = User.query.get(user_id)
    activity = Activity.query.get(activity_id)

    if not user:
        abort(404, f"User {user_id} not found")
    if not activity:
        abort(404, f"Activity {activity_id} not found")

    if activity not in user.activities:
        abort(404, "This activity is not in the user's list")

    user.activities.remove(activity)
    db.session.commit()

    return make_response(f"Activity removed from User {user_id}", 204)