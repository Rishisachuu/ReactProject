from datetime import datetime

class User:
    def __init__(self, mongo):
        self.mongo = mongo
    
    def get_collection(self):
        return self.mongo.db.users
    
    def create_user(self, email, password, name):
        """Create a new user"""
        from app import bcrypt
        
        collection = self.get_collection()
        
        # Check if user exists
        if collection.find_one({'email': email}):
            return None
        
        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        user_data = {
            'email': email,
            'password': hashed_password,
            'name': name,
            'location': '',
            'bio': '',
            'avatar': None,
            'privacy': {
                'email_visible': False,
                'location_visible': True,
                'bio_visible': True
            },
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = collection.insert_one(user_data)
        return str(result.inserted_id)
    
    def find_by_email(self, email):
        """Find user by email"""
        collection = self.get_collection()
        user = collection.find_one({'email': email})
        return user
    
    def find_by_id(self, user_id):
        """Find user by ID"""
        collection = self.get_collection()
        user = collection.find_one({'_id': user_id})
        return user
    
    def update_profile(self, user_id, data):
        """Update user profile"""
        collection = self.get_collection()
        try:
            update_data = {k: v for k, v in data.items() if k != 'password'}
            update_data['updated_at'] = datetime.utcnow()
            
            result = collection.update_one(
                {'_id': user_id},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except:
            return False
    
    def update_password(self, user_id, new_password):
        """Update user password"""
        from app import bcrypt
        
        collection = self.get_collection()
        try:
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            result = collection.update_one(
                {'_id': user_id},
                {'$set': {'password': hashed_password, 'updated_at': datetime.utcnow()}}
            )
            return result.modified_count > 0
        except:
            return False
    
    def update_avatar(self, user_id, avatar_path):
        """Update user avatar"""
        collection = self.get_collection()
        try:
            result = collection.update_one(
                {'_id': user_id},
                {'$set': {'avatar': avatar_path, 'updated_at': datetime.utcnow()}}
            )
            return result.modified_count > 0
        except:
            return False
    
    def update_privacy(self, user_id, privacy_data):
        """Update privacy settings"""
        collection = self.get_collection()
        try:
            result = collection.update_one(
                {'_id': user_id},
                {'$set': {'privacy': privacy_data, 'updated_at': datetime.utcnow()}}
            )
            return result.modified_count > 0
        except:
            return False
