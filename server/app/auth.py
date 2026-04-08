from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from datetime import timedelta
from app import mongo, bcrypt
from app.models.user import User
from app.utils.validators import validate_email, validate_password, validate_name

auth_bp = Blueprint('auth', __name__)
user_model = User(mongo)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not all(key in data for key in ['email', 'password', 'name']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        
        # Validate email
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate name
        if not validate_name(name):
            return jsonify({'error': 'Name must be at least 2 characters'}), 400
        
        # Validate password
        is_valid, message = validate_password(password)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Create user
        user_id = user_model.create_user(email, password, name)
        if not user_id:
            return jsonify({'error': 'Email already exists'}), 409
        
        return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not all(key in data for key in ['email', 'password']):
            return jsonify({'error': 'Missing email or password'}), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Find user
        user = user_model.find_by_email(email)
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Verify password
        if not bcrypt.check_password_hash(user['password'], password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Create JWT token
        access_token = create_access_token(
            identity=user['_id'],
            expires_delta=timedelta(days=30)
        )
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user['_id'],
                'email': user['email'],
                'name': user['name']
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
