import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, 'Password must be at least 8 characters long'
    
    if not any(char.isupper() for char in password):
        return False, 'Password must contain at least one uppercase letter'
    
    if not any(char.isdigit() for char in password):
        return False, 'Password must contain at least one digit'
    
    if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?' for char in password):
        return False, 'Password must contain at least one special character'
    
    return True, 'Password is valid'

def validate_name(name):
    """Validate name format"""
    if len(name.strip()) < 2:
        return False
    return True

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
