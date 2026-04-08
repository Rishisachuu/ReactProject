from flask import Blueprint, request, jsonify
from app import mongo, bcrypt
from app.models.user import User
from app.middleware.jwt_handler import token_required
from app.utils.validators import validate_email, validate_password
from app.utils.file_handler import save_upload_file, delete_file
import os
from dotenv import load_dotenv

load_dotenv()

profile_bp = Blueprint('profile', __name__)
user_model = User(mongo)

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'jpg,jpeg,png,gif').split(','))

@profile_bp.route('/<user_id>', methods=['GET'])
@token_required
def get_profile(current_user_id, user_id):
    """Get user profile"""
    try:
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        user = user_model.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Remove password from response
        user.pop('password', None)
        
        return jsonify({'user': user}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profile_bp.route('/<user_id>', methods=['PUT'])
@token_required
def update_profile(current_user_id, user_id):
    """Update user profile"""
    try:
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        data = request.get_json()
        
        # Validate email if provided
        if 'email' in data:
            if not validate_email(data['email']):
                return jsonify({'error': 'Invalid email format'}), 400
            
            # Check if email already exists
            existing_user = user_model.find_by_email(data['email'])
            if existing_user and existing_user['_id'] != user_id:
                return jsonify({'error': 'Email already exists'}), 409
        
        # Update only allowed fields
        allowed_fields = ['name', 'email', 'location', 'bio']
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        if not update_data:
            return jsonify({'error': 'No valid fields to update'}), 400
        
        success = user_model.update_profile(user_id, update_data)
        
        if not success:
            return jsonify({'error': 'Failed to update profile'}), 500
        
        user = user_model.find_by_id(user_id)
        user.pop('password', None)
        
        return jsonify({'message': 'Profile updated successfully', 'user': user}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profile_bp.route('/<user_id>/upload-avatar', methods=['POST'])
@token_required
def upload_avatar(current_user_id, user_id):
    """Upload user avatar"""
    try:
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        # Check if file is present
        if 'avatar' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['avatar']
        
        # Save file
        filename, error = save_upload_file(file, UPLOAD_FOLDER, ALLOWED_EXTENSIONS)
        
        if error:
            return jsonify({'error': error}), 400
        
        # Get old avatar and delete if exists
        user = user_model.find_by_id(user_id)
        if user and user.get('avatar'):
            delete_file(user['avatar'], UPLOAD_FOLDER)
        
        # Update user avatar in database
        success = user_model.update_avatar(user_id, filename)
        
        if not success:
            delete_file(filename, UPLOAD_FOLDER)
            return jsonify({'error': 'Failed to update avatar'}), 500
        
        return jsonify({
            'message': 'Avatar uploaded successfully',
            'avatar': filename
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profile_bp.route('/<user_id>/change-password', methods=['PUT'])
@token_required
def change_password(current_user_id, user_id):
    """Change user password"""
    try:
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        data = request.get_json()
        
        # Validate input
        if not data or not all(key in data for key in ['current_password', 'new_password']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        
        # Get user
        user = user_model.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Verify current password
        if not bcrypt.check_password_hash(user['password'], current_password):
            return jsonify({'error': 'Current password is incorrect'}), 401
        
        # Validate new password
        is_valid, message = validate_password(new_password)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Check if new password is same as current
        if bcrypt.check_password_hash(user['password'], new_password):
            return jsonify({'error': 'New password must be different from current password'}), 400
        
        # Update password
        success = user_model.update_password(user_id, new_password)
        
        if not success:
            return jsonify({'error': 'Failed to change password'}), 500
        
        return jsonify({'message': 'Password changed successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profile_bp.route('/<user_id>/privacy', methods=['PUT'])
@token_required
def update_privacy(current_user_id, user_id):
    """Update privacy settings"""
    try:
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        data = request.get_json()
        
        if not data or 'privacy' not in data:
            return jsonify({'error': 'Missing privacy settings'}), 400
        
        privacy_data = data.get('privacy')
        
        # Validate privacy settings
        allowed_settings = ['email_visible', 'location_visible', 'bio_visible']
        privacy_data = {k: v for k, v in privacy_data.items() if k in allowed_settings}
        
        if not privacy_data:
            return jsonify({'error': 'No valid privacy settings'}), 400
        
        # Update privacy
        success = user_model.update_privacy(user_id, privacy_data)
        
        if not success:
            return jsonify({'error': 'Failed to update privacy settings'}), 500
        
        user = user_model.find_by_id(user_id)
        user.pop('password', None)
        
        return jsonify({'message': 'Privacy settings updated successfully', 'user': user}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
