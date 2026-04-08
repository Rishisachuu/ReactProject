import os
import secrets
from werkzeug.utils import secure_filename

def save_upload_file(file, upload_folder, allowed_extensions):
    """Save uploaded file and return filename"""
    if not file or file.filename == '':
        return None, 'No file selected'
    
    from app.utils.validators import allowed_file
    
    if not allowed_file(file.filename, allowed_extensions):
        return None, f'Only {", ".join(allowed_extensions)} files are allowed'
    
    try:
        # Create upload folder if it doesn't exist
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # Generate secure filename
        filename = secure_filename(file.filename)
        filename = secrets.token_hex(8) + '_' + filename
        
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        return filename, None
    except Exception as e:
        return None, str(e)

def delete_file(filename, upload_folder):
    """Delete uploaded file"""
    try:
        filepath = os.path.join(upload_folder, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
    except:
        pass
    return False
