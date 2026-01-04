# roles.py
from flask import abort, make_response
from config import db
from models import Role, RoleSchema

# Create schema instances
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

def read_all():

    roles = Role.query.all()
    return roles_schema.dump(roles)

def read_one(role_id):
   
    role = Role.query.get(role_id)
    if role is not None:
        return role_schema.dump(role)
    else:
        abort(404, f"Role with ID {role_id} not found")

def create(role_data):
    
    role_name = role_data.get("role_name")
    existing_role = Role.query.filter(Role.role_name == role_name).one_or_none()

    if existing_role is None:
        new_role = role_schema.load(role_data, session=db.session)
        db.session.add(new_role)
        db.session.commit()
        return role_schema.dump(new_role), 201
    else:
        abort(406, f"Role {role_name} already exists")

def update(role_id, role_data):
    
    existing_role = Role.query.get(role_id)

    if existing_role:
        update_role = role_schema.load(role_data, session=db.session)
        existing_role.role_name = update_role.role_name
        db.session.merge(existing_role)
        db.session.commit()
        return role_schema.dump(existing_role), 200
    else:
        abort(404, f"Role with ID {role_id} not found")

def delete(role_id):
    
    existing_role = Role.query.get(role_id)

    if existing_role:
        db.session.delete(existing_role)
        db.session.commit()
        return make_response(f"Role {role_id} successfully deleted", 204)
    else:
        abort(404, f"Role with ID {role_id} not found")