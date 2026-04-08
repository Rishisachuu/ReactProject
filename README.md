# Profile Management System

A full-stack web application for managing user profiles with secure authentication, profile editing, image uploads, and privacy settings. Built with React (frontend) and Flask (backend), using MongoDB for data storage.

## 🎯 Features

### User Authentication
- Secure user registration with password strength validation
- JWT-based login system
- Protected routes for authenticated users
- Session management with automatic token storage

### Profile Management
- View personal profile information
- Edit multiple profile fields (name, email, location, bio)
- Upload and update profile picture
- Change password securely
- Privacy settings control

### Security
- Bcrypt password hashing
- JWT token authentication
- Input validation and sanitization
- CORS protection
- Secure file upload handling
- Strong password requirements

### User Experience
- Clean, modern responsive interface
- Real-time form validation
- Loading states and error messages
- Image preview before upload
- Mobile-friendly design

## 📋 Tech Stack

### Frontend
- **React 18** - UI library
- **React Router 6** - Client-side routing
- **Axios** - HTTP client
- **Context API** - State management
- **CSS3** - Styling with responsive design

### Backend
- **Flask 2.3** - Web framework
- **MongoDB** - NoSQL database
- **PyMongo** - MongoDB driver
- **Flask-JWT-Extended** - JWT authentication
- **Flask-Bcrypt** - Password hashing
- **Flask-CORS** - Cross-origin requests

## 📁 Project Structure

```
profile-management-system/
├── client/                      # React frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.js
│   │   │   └── ProtectedRoute.js
│   │   ├── pages/
│   │   │   ├── Home.js
│   │   │   ├── Login.js
│   │   │   ├── Signup.js
│   │   │   ├── Dashboard.js
│   │   │   └── EditProfile.js
│   │   ├── context/
│   │   │   └── AuthContext.js
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── styles/
│   │   │   ├── App.css
│   │   │   ├── Auth.css
│   │   │   ├── Dashboard.css
│   │   │   ├── EditProfile.css
│   │   │   ├── Home.css
│   │   │   ├── Navbar.css
│   │   │   └── index.css
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   ├── .env.example
│   ├── .gitignore
│   └── README.md
│
└── server/                      # Flask backend
    ├── app/
    │   ├── __init__.py         # Flask app factory
    │   ├── routes/
    │   │   ├── auth.py         # Authentication endpoints
    │   │   └── profile.py      # Profile endpoints
    │   ├── models/
    │   │   └── user.py         # User model
    │   ├── middleware/
    │   │   └── jwt_handler.py  # JWT protection
    │   └── utils/
    │       ├── validators.py   # Input validation
    │       └── file_handler.py # File operations
    ├── uploads/                 # Profile picture storage
    ├── run.py                   # Application entry point
    ├── requirements.txt         # Python dependencies
    ├── .env.example            # Example environment variables
    ├── .gitignore              # Git ignore rules
    └── README.md               # Backend documentation
```

## 🚀 Quick Start

### Backend Setup

1. **Navigate to server directory**
   ```bash
   cd server
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB URI and other settings
   ```

5. **Run the server**
   ```bash
   python run.py
   ```
   Server runs on `http://localhost:5000`

### Frontend Setup

1. **Navigate to client directory**
   ```bash
   cd client
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Ensure REACT_APP_API_URL points to your backend
   ```

4. **Start development server**
   ```bash
   npm start
   ```
   Application opens at `http://localhost:3000`

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | User login |

### Profile (JWT Required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/<id>` | Get user profile |
| PUT | `/api/users/<id>` | Update profile info |
| POST | `/api/users/<id>/upload-avatar` | Upload profile picture |
| PUT | `/api/users/<id>/change-password` | Change password |
| PUT | `/api/users/<id>/privacy` | Update privacy settings |

## 🔐 Password Requirements
- Minimum 8 characters
- At least one uppercase letter (A-Z)
- At least one digit (0-9)
- At least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)

## 📊 Database Schema

### User Collection
```javascript
{
  _id: ObjectId,
  email: String (unique),
  password: String (hashed),
  name: String,
  location: String,
  bio: String,
  avatar: String (filename),
  privacy: {
    email_visible: Boolean,
    location_visible: Boolean,
    bio_visible: Boolean
  },
  created_at: Date,
  updated_at: Date
}
```

## 🌐 Deployment

### Backend Deployment (Render/Railway)
1. Push code to GitHub
2. Connect repository to Render/Railway
3. Set environment variables:
   - FLASK_ENV=production
   - MONGODB_URI=<your-mongodb-url>
   - JWT_SECRET_KEY=<strong-secret>
   - CLIENT_URL=<frontend-url>
4. Deploy with start command: `python run.py`

### Frontend Deployment (Vercel/Netlify)
1. Push code to GitHub
2. Connect to Vercel or Netlify
3. Set build command: `npm run build`
4. Set environment variable: `REACT_APP_API_URL=<backend-url>`
5. Deploy

### Example Deployed URLs
- Backend: `https://profile-api.onrender.com`
- Frontend: `https://profile-manager.vercel.app`

## 🧪 Testing

### Backend Testing with Postman/Insomnia
1. Register a new user
2. Login to get JWT token
3. Use token in Authorization header for protected endpoints
4. Test all CRUD operations

### Frontend Testing
```bash
cd client
npm test
```

## 📝 Configuration

### Environment Variables

**Backend (.env)**
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/profile_db
MONGODB_DB=profile_db
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif
SERVER_PORT=5000
CLIENT_URL=http://localhost:3000
```

**Frontend (.env)**
```
REACT_APP_API_URL=http://localhost:5000/api
```

## 🔒 Security Considerations

1. **Backend**
   - Change JWT_SECRET_KEY in production
   - Use strong MongoDB credentials
   - Enable HTTPS only in production
   - Implement rate limiting
   - Validate all inputs server-side

2. **Frontend**
   - Store JWT tokens securely
   - Don't hardcode API URLs
   - Validate inputs before submission
   - Use HTTPS in production
   - Implement token refresh mechanism

## 🛠️ Troubleshooting

### Connection Issues
- Verify backend server is running on correct port
- Check MongoDB connection string in .env
- Ensure CORS is configured correctly

### Authentication Issues
- Token may be expired - login again
- Clear browser localStorage and retry
- Check JWT_SECRET_KEY consistency

### File Upload Issues
- Verify upload directory exists and is writable
- Check file size and format restrictions
- Ensure proper multipart/form-data headers

### Port Conflicts
- Backend running on different port: Update REACT_APP_API_URL
- Kill process on port 3000 or 5000: Use `lsof -i :PORT` (macOS/Linux) or `netstat -ano | findstr :PORT` (Windows)

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [JWT Introduction](https://jwt.io/introduction)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)

## 📄 License

MIT License - feel free to use this project for learning and development.

## 👤 Author

Profile Management System - Full-Stack Web Application

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to fork and submit pull requests.

## 📞 Support

For questions or issues:
1. Check the README files in `/client` and `/server`
2. Review API endpoint documentation
3. Check browser console for frontend errors
4. Check server logs for backend errors

---

**Happy coding! 🎉**
