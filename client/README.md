# Profile Management System - Frontend (React)

## Overview
This is the frontend application for the Profile Management System built with React, featuring user authentication, profile management, image upload, and privacy settings.

## Features
- User authentication (Login/Signup)
- Profile viewing and editing
- Profile picture upload with preview
- Password management
- Privacy settings control
- Responsive design
- Form validation
- Error handling with user feedback

## Tech Stack
- **Framework**: React 18.2.0 with Hooks
- **Bundler**: Vite 4.3.9 (fast dev server & build)
- **Routing**: React Router DOM 6.14.1
- **HTTP Client**: Axios
- **State Management**: Context API
- **Styling**: CSS3

## Installation

### Prerequisites
- Node.js 14+ and npm
- Internet connection

### Setup Steps

1. **Clone the repository**
```bash
cd client
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment variables**
```bash
# Copy the example env file
cp .env.example .env

# Edit .env file:
VITE_API_URL=http://localhost:5000/api
```

4. **Start the development server**
```bash
npm run dev
```

The application should open at `http://localhost:3000`

## Project Structure
```
client/
├── src/
│   ├── components/
│   │   ├── Navbar.js           # Navigation component
│   │   └── ProtectedRoute.js   # Route protection wrapper
│   ├── pages/
│   │   ├── Home.js             # Home page
│   │   ├── Login.js            # Login page
│   │   ├── Signup.js           # Signup page
│   │   ├── Dashboard.js        # Profile view page
│   │   └── EditProfile.js      # Profile editing page
│   ├── context/
│   │   └── AuthContext.js      # Authentication context
│   ├── services/
│   │   └── api.js              # API service with Axios
│   ├── styles/
│   │   ├── App.css             # Global styles
│   │   ├── Auth.css            # Auth pages styles
│   │   ├── Dashboard.css       # Dashboard styles
│   │   ├── EditProfile.css     # Edit profile styles
│   │   ├── Home.css            # Home page styles
│   │   ├── Navbar.css          # Navigation styles
│   │   └── index.css           # Base styles
│   ├── App.js                  # Main app component
│   └── index.js                # React DOM entry point
├── public/
│   └── index.html              # HTML template
├── package.json                # Dependencies and scripts
├── .env.example               # Example environment variables
└── .gitignore                 # Git ignore rules
```

## Available Routes

| Route | Description | Authentication Required |
|-------|-------------|------------------------|
| `/` | Home page | No |
| `/login` | User login | No |
| `/signup` | User registration | No |
| `/dashboard` | User profile view | Yes |
| `/edit-profile` | Profile editing page | Yes |

## Vite Features

- ⚡ **Lightning-fast** HMR (Hot Module Replacement)
- 🚀 **Optimized builds** with automatic code splitting
- 📦 **Small bundle size** compared to webpack/CRA
- 🔧 **Native ES modules** support
- 🎯 **Instant server start** on changes

## How It Works

### Authentication Flow
1. User registers or logs in on Auth pages
2. Upon successful login, JWT token is received and stored in localStorage
3. Token is automatically included in all API requests
4. User context stores authenticated user info
5. Protected routes check authentication status

### Profile Management
1. Users can view their profile on Dashboard
2. Edit Profile page allows updating:
   - Personal information (name, email, location, bio)
   - Profile picture
   - Password
   - Privacy settings
3. All changes are validated before sending to backend
4. Success/error messages provide user feedback

### State Management
- **AuthContext** manages:
  - User authentication state
  - JWT token storage
  - User information
  - Login/logout actions

## Form Validation

### Login/Signup
- Email format validation
- Password strength validation:
  - Minimum 8 characters
  - At least one uppercase letter
  - At least one digit
  - At least one special character
- Confirm password matching

### Profile Update
- Email uniqueness check (backend validation)
- Optional location and bio fields
- Name validation (minimum 2 characters)

### Password Change
- Current password verification
- New password strength validation
- Password confirmation matching

## API Integration
The frontend communicates with the Flask backend using Axios:

```javascript
// Examples of API calls
authService.login(email, password)
authService.register(email, password, name)
profileService.getProfile(userId)
profileService.updateProfile(userId, data)
profileService.uploadAvatar(userId, file)
profileService.changePassword(userId, oldPassword, newPassword)
profileService.updatePrivacy(userId, privacySettings)
```

## Styling
The application uses modern CSS3 with:
- Flexbox layouts
- Gradient backgrounds
- Responsive design (mobile-first)
- Smooth transitions and hover effects
- Custom color scheme

### Color Palette
- Primary: #3498db (Blue)
- Secondary: #667eea (Purple)
- Success: #27ae60 (Green)
- Error: #e74c3c (Red)
- Dark: #2c3e50

## Responsive Design
The application is fully responsive with breakpoints:
- Mobile: < 480px
- Tablet: 480px - 768px
- Desktop: > 768px

## Error Handling
- Network errors are caught and displayed to users
- Validation errors are shown with helpful messages
- API errors are translated to user-friendly messages
- Loading states prevent duplicate submissions

## Local Storage
The run dev
```

### Building for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

## Environment Variables

### Development
```
VITE_API_URL=http://localhost:5000/api
```

### Production
```
VITE
### Development
```
REACT_APP_API_URL=http://localhost:5000/api
```

### Production
```
REACT_APP_API_URL=https://your-backend-url/api
```

## Troubleshooting

### CORS Errors
- Ensure backend CORS is configured for your frontend URL
- Check `CLIENT_URL` in backend .env file

### 401 Unauthorized Errors
- Token may be expired
- Clear localStorage and log in again
- Check backend JWT_SECRET_KEY

### Image Upload Not Working
- Verify backend has /uploads directory with write permissions
- Check file size is under MAX_CONTENT_LENGTH
- Ensure file format is jpg, jpeg, png, or gif

### API Not Responding
- Verify backend server is running
- Check backend port matches REACT_APP_API_URL
- Check network connectivity

## Performance Tips
- Use React DevTools to profile components
- Lazy load routes if needed
- Minimize bundle size with code splitting
- Optimize images before upload

## Security Best Practices
1. Never hardcode sensitive data
2. Use environment variables for API URLs
3. Store JWT tokens securely (consider httpOnly cookies)
4. Validate all user inputs
5. Don't expose error details in production
6. Use HTTPS in production

## License
MIT License

## Support
For issues and questions, please refer to the main project README.
