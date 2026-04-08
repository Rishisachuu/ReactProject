from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from flask import jsonify

def token_required(fn):
    """Decorator to require valid JWT token"""
    @wraps(fn)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            return fn(current_user_id, *args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Unauthorized access'}), 401
    return decorated
