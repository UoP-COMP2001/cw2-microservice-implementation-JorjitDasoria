# auth.py
from flask import request, abort, jsonify, session
from werkzeug.security import check_password_hash
from models import User

def login():
    
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

   
    user = User.query.filter_by(email=email).one_or_none()

    
    if user and user.password and check_password_hash(user.password, password):
        
        session['user_id'] = user.user_id
        session['role'] = user.role.role_name.lower()
        return jsonify({"message": "Logged in successfully"}), 200
    
    abort(401, "Invalid Credentials")

def logout():

    session.clear()
    return jsonify({"message": "Logged out"}), 200