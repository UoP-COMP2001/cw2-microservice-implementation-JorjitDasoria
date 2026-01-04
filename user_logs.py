
from flask import request, abort
from config import db
from models import UserLog, user_logs_schema, user_log_schema, User


def check_admin():
    from flask import session
    role = session.get('role', 'guest')
    if role != 'administrator':
        abort(403, "Permission Denied: Only administrators can view logs.")


def read_all():
    check_admin()
    logs = UserLog.query.order_by(UserLog.timestamp_added.desc()).all()
    return user_logs_schema.dump(logs)

def read_one(log_id):
    check_admin()
    log = UserLog.query.get(log_id)
    if log is not None:
        return user_log_schema.dump(log)
    else:
        abort(404, f"Log with ID {log_id} not found")