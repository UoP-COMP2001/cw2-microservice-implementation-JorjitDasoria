# activities.py
from flask import abort, make_response
from config import db
from models import Activity, ActivitySchema

# Create schema instances
activity_schema = ActivitySchema()
activities_schema = ActivitySchema(many=True)

def read_all():
    activities = Activity.query.all()
    return activities_schema.dump(activities)

def read_one(activity_id):
    activity = Activity.query.get(activity_id)
    if activity is not None:
        return activity_schema.dump(activity)
    else:
        abort(404, f"Activity with ID {activity_id} not found")

def create(activity_data):
    name = activity_data.get("activity_name")
    existing_activity = Activity.query.filter(Activity.activity_name == name).one_or_none()

    if existing_activity is None:
        new_activity = activity_schema.load(activity_data, session=db.session)
        db.session.add(new_activity)
        db.session.commit()
        return activity_schema.dump(new_activity), 201
    else:
        abort(406, f"Activity {name} already exists")

def update(activity_id, activity_data):
    existing_activity = Activity.query.get(activity_id)

    if existing_activity:
        update_activity = activity_schema.load(activity_data, session=db.session)
        existing_activity.activity_name = update_activity.activity_name
        db.session.merge(existing_activity)
        db.session.commit()
        return activity_schema.dump(existing_activity), 200
    else:
        abort(404, f"Activity with ID {activity_id} not found")

def delete(activity_id):
    existing_activity = Activity.query.get(activity_id)

    if existing_activity:
        db.session.delete(existing_activity)
        db.session.commit()
        return make_response(f"Activity {activity_id} successfully deleted", 204)
    else:
        abort(404, f"Activity with ID {activity_id} not found")