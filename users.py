from flask import request, abort, make_response
from flask import session
from config import db
from models import User, UserLog, user_schema, users_schema

def get_requester_role():
    return session.get('role', 'guest')


def filter_user_data(user_data, requester_role):
    """
    If the user is NOT an admin, remove the password field.
    Everything else (email, phone, etc.) remains visible.
    """
    if requester_role != 'administrator':
        user_data.pop('password', None) 
    return user_data


def read_all():
    requester_role = get_requester_role()

    print(f"DEBUG: The API sees your role as: '{requester_role}'")

    users = User.query.all()
    all_data = users_schema.dump(users)
    
    
    filtered_list = [filter_user_data(u, requester_role) for u in all_data]
    return filtered_list

def read_one(user_id):
    requester_role = get_requester_role()
    user = User.query.get(user_id)
    
    if user is not None:
        full_data = user_schema.dump(user)
        return filter_user_data(full_data, requester_role)
    else:
        abort(404, f"User with ID {user_id} not found")

def create(user_data):
    requester_role = get_requester_role()
    if requester_role != 'administrator':
        abort(403, "Permission Denied: Only administrators can create new users.")

    email = user_data.get("email")
    if User.query.filter(User.email == email).one_or_none():
        abort(406, f"User with email {email} already exists")

    new_user = user_schema.load(user_data, session=db.session)
    if user_data.get('password'):
        new_user.set_password(user_data.get('password'))
    
    db.session.add(new_user)
    db.session.flush()

    new_log = UserLog(
        user_id_added=new_user.user_id,
        first_name_added=new_user.first_name,
        last_name_added=new_user.last_name,
        email_added=new_user.email
    )
    db.session.add(new_log)
    db.session.commit()

    return user_schema.dump(new_user), 201

def update(user_id, user_data):
    requester_role = get_requester_role()
    if requester_role != 'administrator':
        abort(403, "Permission Denied: Only administrators can update users.")

    existing_user = User.query.get(user_id)
    if existing_user:
        update_user = user_schema.load(user_data, session=db.session)
        
        existing_user.first_name = update_user.first_name
        existing_user.last_name = update_user.last_name
        existing_user.email = update_user.email
        existing_user.phone_number = update_user.phone_number
        existing_user.about_me = update_user.about_me
        existing_user.location_id = update_user.location_id
        existing_user.role_id = update_user.role_id
        existing_user.height = update_user.height
        existing_user.weight = update_user.weight
        existing_user.birthday = update_user.birthday
        
        
        if update_user.password:
            existing_user.password = update_user.password
        
        db.session.merge(existing_user)
        db.session.commit()
        return user_schema.dump(existing_user), 200
    else:
        abort(404, f"User with ID {user_id} not found")

def delete(user_id):
    requester_role = get_requester_role()
    if requester_role != 'administrator':
        abort(403, "Permission Denied: Only administrators can delete users.")

    existing_user = User.query.get(user_id)
    if existing_user:
        db.session.delete(existing_user)
        db.session.commit()
        return make_response(f"User {user_id} successfully deleted", 204)
    else:
        abort(404, f"User with ID {user_id} not found")