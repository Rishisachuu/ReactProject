# Installation & Setup Guide

This guide will help you set up both the frontend and backend of the Profile Management System locally.

## Prerequisites

### System Requirements
- **Node.js**: 14.0.0 or higher (for React frontend)
- **Python**: 3.8 or higher (for Flask backend)
- **MongoDB**: Local or MongoDB Atlas account
- **Git**: For version control

## Installation Steps

### Part 1: Backend Setup (Flask)

#### Step 1: Navigate to Server Directory
```bash
cd server
```

#### Step 2: Create Python Virtual Environment
On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

Expected output shows all packages installing successfully (Flask, Flask-CORS, Flask-JWT-Extended, Flask-Bcrypt, Flask-PyMongo, etc.)

#### Step 4: Setup Environment Variables
```bash
# Copy example file
cp .env.example .env

# Or on Windows:
copy .env.example .env
```

Edit the `.env` file with your configuration:

**For Local MongoDB:**
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
MONGODB_URI=mongodb://localhost:27017/profile_db
MONGODB_DB=profile_db
SERVER_PORT=5000
CLIENT_URL=http://localhost:3000
```

**For MongoDB Atlas (Cloud):**
```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/profile_db?retryWrites=true&w=majority
```

#### Step 5: Test Backend Server
```bash
python run.py
```

Expected output:
```
 * Running on http://0.0.0.0:5000
```

The server is now running! Keep this terminal open.

### Part 2: Frontend Setup (React)

#### Step 1: Open New Terminal and Navigate to Client Directory
```bash
cd client
```

#### Step 2: Install Node Dependencies
```bash
npm install
```

This installs React, React Router, Axios, and other dependencies.

#### Step 3: Setup Environment Variables
```bash
# Copy example file
cp .env.example .env

# Or on Windows:
copy .env.example .env
```

The `.env` should contain:
```
REACT_APP_API_URL=http://localhost:5000/api
```

#### Step 4: Start Development Server
```bash
npm start
```

Expected output:
```
Compiled successfully!

You can now view profile-management-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

The application automatically opens at `http://localhost:3000`

## Verification

### Backend Verification
1. Open Postman or similar API testing tool
2. Make a test request to: `http://localhost:5000/api/auth/register`
3. Method: POST
4. Body (JSON):
```json
{
  "email": "test@example.com",
  "password": "TestPassword123!",
  "name": "Test User"
}
```
5. Should receive: `{"message": "User registered successfully", "user_id": "..."}`

### Frontend Verification
1. Visit `http://localhost:3000` in your browser
2. You should see the home page with "Login" and "Sign Up" buttons
3. Try signing up with:
   - Email: test@example.com
   - Name: Test User
   - Password: TestPassword123!
   - Confirm: TestPassword123!

## Troubleshooting

### Backend Won't Start
**Issue**: `ModuleNotFoundError: No module named 'flask'`

**Solution**: Ensure virtual environment is activated:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### MongoDB Connection Error
**Issue**: `Connection refused` or `Cannot connect to server`

**Solution**: 
- Ensure MongoDB is running locally, OR
- Verify MongoDB Atlas connection string in `.env`
- Check firewall allowing port 27017

### React App Won't Start
**Issue**: Port 3000 already in use

**Solution**:
```bash
# Kill process on port 3000
# Windows (PowerShell as Admin):
Get-Process | Where-Object {$_.Port -eq 3000} | Stop-Process -Force

# macOS/Linux:
lsof -ti:3000 | xargs kill -9

# Or use different port:
PORT=3001 npm start
```

### CORS Issues
**Issue**: `Access to XMLHttpRequest blocked by CORS policy`

**Solution**: Verify in backend `.env`:
```
CLIENT_URL=http://localhost:3000
```

Ensure both servers are running on correct ports.

### API Requests Failing
**Issue**: 404 errors or cannot connect to backend

**Solution**:
1. Verify backend is running on port 5000
2. Check `.env` in frontend has correct API URL
3. Check browser console for error details
4. Verify CORS configuration

## Next Steps

Once both servers are running:

1. **Create a test account** on the signup page
2. **Login** with your credentials
3. **View your profile** on the dashboard
4. **Edit your profile** - add location, bio, upload avatar
5. **Change password** in edit profile
6. **Manage privacy settings** for your profile

## Project Structure Overview

```
sharone/
├── client/                 # React Frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── context/
│   │   ├── services/
│   │   └── styles/
│   ├── .env                # Frontend environment
│   ├── .gitignore
│   ├── package.json
│   └── README.md
└── server/                 # Flask Backend
    ├── app/
    │   ├── routes/
    │   ├── models/
    │   ├── middleware/
    │   └── utils/
    ├── uploads/
    ├── .env                # Backend environment
    ├── .gitignore
    ├── requirements.txt
    └── README.md
```

## Commands Reference

### Backend Commands
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run server
python run.py

# Deactivate virtual environment
deactivate
```

### Frontend Commands
```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

## Environment Variables Summary

### .env Files Location
- Backend: `server/.env`
- Frontend: `client/.env`

### Required Variables

**Backend**
- MONGODB_URI: MongoDB connection string
- JWT_SECRET_KEY: Secret for JWT tokens
- CLIENT_URL: Frontend URL for CORS

**Frontend**
- REACT_APP_API_URL: Backend API URL

## Common Workflows

### Full Restart
1. Stop both servers (Ctrl+C)
2. Restart backend: `cd server && python run.py`
3. Start frontend: `cd client && npm start`

### Reset Database (MongoDB)
1. Delete MongoDB database or clear collection
2. Create new account to test
3. Verify all operations work

### Testing Workflow
1. Register new account
2. Login with credentials
3. Test each feature:
   - Edit profile
   - Upload avatar
   - Change password
   - Update privacy settings

## Getting Help

1. Check README files in `/client` and `/server`
2. Review console error messages (browser + terminal)
3. Check MongoDB Atlas status if using cloud
4. Verify all environment variables are set correctly

---

**Installation complete!** You're ready to use the Profile Management System.
