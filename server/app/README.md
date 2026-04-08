# Profile Management System - Backend (Flask)

## Overview
This is the backend API for the Profile Management System built with Flask, MongoDB, and JWT authentication.

## Features
- User registration and login with JWT authentication
- User profile management
- Profile picture upload
- Password change with secure validation
- Privacy settings management
- Input validation and error handling
- RESTful API endpoints

## Tech Stack
- **Framework**: Flask 2.3.2
- **Database**: MongoDB with PyMongo
- **Authentication**: JWT (Flask-JWT-Extended)
- **Security**: Bcrypt for password hashing
- **Validation**: Custom validators
- **File Upload**: Werkzeug

## Installation

### Prerequisites
- Python 3.8+
- MongoDB (local or cloud instance)
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
```bash
cd server
```

2. **Create a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your settings:
- MONGODB_URI: MongoDB connection string
- JWT_SECRET_KEY: Secret key for JWT tokens
- FLASK_DEBUG: Set to True for development
- And other configurations as needed
```

5. **Run the server**
```bash
python run.py
```

The server should now be running at `http://localhost:5000`

## API Endpoints

### Authentication Routes (`/api/auth`)

#### Register User
- **POST** `/auth/register`
- **Body**: `{ "email": "user@example.com", "password": "Password123!", "name": "John Doe" }`
- **Response**: `{ "message": "User registered successfully", "user_id": "..." }`

#### Login User
- **POST** `/auth/login`
- **Body**: `{ "email": "user@example.com", "password": "Password123!" }`
- **Response**: `{ "message": "Login successful", "access_token": "...", "user": {...} }`

### Profile Routes (`/api/users`) - All require JWT token

#### Get User Profile
- **GET** `/users/<user_id>`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{ "user": {...} }`

#### Update Profile
- **PUT** `/users/<user_id>`
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `{ "name": "...", "email": "...", "location": "...", "bio": "..." }`
- **Response**: `{ "message": "Profile updated successfully", "user": {...} }`

#### Upload Profile Picture
- **POST** `/users/<user_id>/upload-avatar`
- **Headers**: `Authorization: Bearer <token>`, `Content-Type: multipart/form-data`
- **Body**: FormData with `avatar` file
- **Response**: `{ "message": "Avatar uploaded successfully", "avatar": "..." }`

#### Change Password
- **PUT** `/users/<user_id>/change-password`
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `{ "current_password": "...", "new_password": "..." }`
- **Response**: `{ "message": "Password changed successfully" }`

#### Update Privacy Settings
- **PUT** `/users/<user_id>/privacy`
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `{ "privacy": { "email_visible": false, "location_visible": true, "bio_visible": true } }`
- **Response**: `{ "message": "Privacy settings updated successfully", "user": {...} }`

## Project Structure
```
server/
├── app/
│   ├── __init__.py           # Flask app initialization
│   ├── routes/
│   │   ├── auth.py          # Authentication routes
│   │   └── profile.py       # Profile routes
│   ├── models/
│   │   └── user.py          # User model and database operations
│   ├── middleware/
│   │   └── jwt_handler.py   # JWT authentication middleware
│   └── utils/
│       ├── validators.py    # Input validation functions
│       └── file_handler.py  # File upload handling
├── uploads/                 # Profile picture storage
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment variables
└── .gitignore              # Git ignore rules
```

## Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one digit
- At least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)

## Security Best Practices
1. Always use HTTPS in production
2. Keep JWT_SECRET_KEY secure and change it regularly
3. Use strong MongoDB credentials
4. Implement rate limiting on authentication endpoints
5. Enable CORS only for trusted domains
6. Validate and sanitize all inputs
7. Hash passwords using bcrypt
8. Store sensitive data in environment variables

## Deployment

### Render/Railway Setup
1. Push code to GitHub
2. Connect GitHub repository to Render/Railway
3. Add environment variables in the dashboard
4. Set start command to `python run.py`
5. Deploy

### Environment Variables for Production
```
FLASK_ENV=production
FLASK_DEBUG=False
MONGODB_URI=<production-mongodb-uri>
JWT_SECRET_KEY=<strong-random-key>
CLIENT_URL=<frontend-url>
```

## Error Handling
All endpoints return appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `409`: Conflict (e.g., email already exists)
- `500`: Internal Server Error

## Testing
To test the API, use tools like:
- [Postman](https://www.postman.com/)
- [Insomnia](https://insomnia.rest/)
- [curl](https://curl.se/)

## Troubleshooting

### MongoDB Connection Issues
- Verify MongoDB URI in .env
- Check MongoDB service is running
- Ensure network access is enabled for your IP

### JWT Token Issues
- Token may be expired (tokens expire in 30 days)
- Ensure token is included in Authorization header
- Check JWT_SECRET_KEY is consistent

### File Upload Issues
- Check UPLOAD_FOLDER has write permissions
- Verify file size is under MAX_CONTENT_LENGTH
- Ensure file extension is in ALLOWED_EXTENSIONS

## License
MIT License

## Support
For issues and questions, please refer to the main project README.
