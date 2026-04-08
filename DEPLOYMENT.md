# Deployment Guide

This guide covers deploying both the frontend and backend of the Profile Management System to production.

## Architecture Overview

```
Frontend (Vercel/Netlify)
        ↓ (HTTPS)
Backend API (Render/Railway/Heroku)
        ↓
MongoDB (Atlas)
```

## Backend Deployment

### Option 1: Render.com (Recommended)

#### Prerequisites
- GitHub account with code pushed
- Render account (free tier available)
- MongoDB Atlas account (free tier available)

#### Steps

1. **Prepare MongoDB Atlas**
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create free cluster
   - Create database user with strong password
   - Whitelist your IPs (or allow all: 0.0.0.0/0)
   - Copy connection string

2. **Prepare Code**
   ```bash
   # In server directory
   # Ensure .env is in .gitignore (not committed)
   # Ensure run.py exists
   ```

3. **Deploy to Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - New → Web Service
   - Connect GitHub repository
   - Configure:
     - Name: `profile-api`
     - Environment: `Python 3.9`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:create_app()`
     - Add Environment Variables:
       ```
       FLASK_ENV=production
       FLASK_DEBUG=False
       MONGODB_URI=<your-mongodb-atlas-uri>
       JWT_SECRET_KEY=<strong-random-key>
       CLIENT_URL=<your-frontend-domain>
       ```
   - Deploy

4. **Wait for deployment** (2-3 minutes)
   - Once deployed, note your API URL: `https://profile-api.onrender.com`

#### Install Gunicorn
Update `requirements.txt`:
```
Flask==2.3.2
Flask-CORS==4.0.0
Flask-JWT-Extended==4.5.2
Flask-Bcrypt==1.0.1
Flask-PyMongo==2.3.0
pymongo==4.5.0
python-dotenv==1.0.0
Werkzeug==2.3.7
gunicorn==20.1.0
```

### Option 2: Railway

1. Go to [Railway](https://railway.app/)
2. New Project
3. Deploy from GitHub
4. Select repository
5. Add Environment Variables (same as Render)
6. Deploy

### Option 3: Heroku

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create profile-api

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set JWT_SECRET_KEY=<your-key>
heroku config:set MONGODB_URI=<your-uri>
heroku config:set CLIENT_URL=<your-frontend>

# Deploy
git push heroku main
```

## Frontend Deployment

### Option 1: Vercel (Recommended for Next.js/React)

#### Steps

1. **Prepare Code**
   ```bash
   # Ensure .env.production is in .gitignore
   # Build locally to verify: npm run build
   ```

2. **Deploy to Vercel**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - New Project
   - Import your GitHub repository
   - Configure:
     - Framework: React
     - Build Command: `npm run build`
     - Output Directory: `build`
     - Environment Variables:
       ```
       REACT_APP_API_URL=https://your-backend-url/api
       ```
   - Deploy

3. **Wait for deployment**
   - Once deployed, note your URL: `https://profile-manager.vercel.app`

### Option 2: Netlify

1. Go to [Netlify](https://app.netlify.com/)
2. New site from Git
3. Select repository
4. Configure:
   - Build Command: `npm run build`
   - Publish Directory: `build`
5. Add environment variables:
   ```
   REACT_APP_API_URL=https://your-backend-url/api
   ```
6. Deploy

### Option 3: Manual Hosting (AWS S3 + CloudFront)

1. **Build the application**
   ```bash
   npm run build
   ```

2. **Upload to S3**
   - Create S3 bucket
   - Enable static website hosting
   - Upload contents of `build/` folder

3. **Setup CloudFront**
   - Create distribution pointing to S3 bucket
   - Get CloudFront domain

## Environment Configuration

### Production Environment Variables

**Backend (.env)**
```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<generate-strong-key>
JWT_SECRET_KEY=<generate-strong-key>
MONGODB_URI=<production-mongodb-uri>
MONGODB_DB=profile_db
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif
SERVER_PORT=5000
CLIENT_URL=https://your-frontend-domain.com
```

**Frontend (.env.production)**
```
REACT_APP_API_URL=https://your-api-domain.com/api
```

### Generating Strong Keys

```python
# Python
import secrets
print(secrets.token_hex(32))
```

```bash
# Terminal
openssl rand -hex 32
```

## Deployment Checklist

### Backend
- [ ] MongoDB Atlas cluster created and configured
- [ ] Database user created with strong password
- [ ] Connection string obtained
- [ ] requirements.txt includes gunicorn
- [ ] run.py is correct entry point
- [ ] All environment variables set correctly
- [ ] CORS configured for frontend domain
- [ ] Server deployed and accessible
- [ ] Test API endpoints with Postman

### Frontend
- [ ] .env.production set with correct backend URL
- [ ] npm run build succeeds locally
- [ ] No console errors in production build
- [ ] API_URL points to correct backend
- [ ] Frontend deployed and accessible
- [ ] Test login/signup flow end-to-end

### Integration
- [ ] Backend and frontend communicate correctly
- [ ] CORS issues resolved
- [ ] JWT tokens work in production
- [ ] File uploads work
- [ ] Database operations succeed

## Testing Production

### API Testing
```bash
# Test registration
curl -X POST https://your-api.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!",
    "name": "Test User"
  }'

# Test login
curl -X POST https://your-api.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!"
  }'
```

### Frontend Testing
1. Visit frontend domain in browser
2. Sign up with test account
3. Test profile editing
4. Test image upload
5. Test password change
6. Test logout and login

## Domain Setup (Optional)

### Custom Domain on Vercel
1. Go to Project Settings
2. Domains section
3. Add custom domain
4. Follow DNS setup instructions
5. Points to Vercel default domain

### Custom Domain on Render
1. Go to Service Settings
2. Custom Domains
3. Add domain
4. Update DNS records as instructed

## Monitoring & Maintenance

### Vercel Monitoring
- Dashboard shows deployment status
- Analytics tab shows usage
- Logs tab for error tracking

### Render Monitoring
- Service dashboard shows health
- Logs for debugging
- Metrics tab for performance

### Database Monitoring
- MongoDB Atlas dashboard
- Connection monitoring
- Performance metrics

## Troubleshooting Deployment

### Backend Won't Deploy
**Error**: `ModuleNotFoundError`
- Add missing module to requirements.txt
- Run pip install locally to verify

**Error**: `Port already in use`
- Render/Railway handle port automatically
- Check process isn't already running

### Frontend Won't Build
**Error**: `REACT_APP_API_URL is not set`
- Add environment variable in deployment platform
- Rebuild after adding variable

### API Connection Issues
**Error**: `CORS blocked`
- Check CLIENT_URL in backend .env
- Verify frontend domain matches exactly

**Error**: `Cannot connect to MongoDB`
- Verify MongoDB URI is correct
- Check IP whitelist in MongoDB Atlas
- Test connection string locally

## Performance Optimization

### Backend
- Enable caching for read operations
- Use CDN for static files
- Compress API responses

### Frontend
- Enable gzip compression
- Lazy load routes and components
- Optimize images before upload
- Use CSS minification

## Security Checklist

- [ ] HTTPS enabled on both frontend and backend
- [ ] Strong JWT secret key (minimum 32 characters)
- [ ] Database credentials kept secure
- [ ] API keys not committed to git
- [ ] CORS restricted to frontend domain
- [ ] Environment variables not exposed
- [ ] Password validation enforced
- [ ] Input sanitization implemented
- [ ] Rate limiting considered
- [ ] File upload validation enabled

## Rollback Procedure

### Vercel
1. Dashboard → Deployments
2. Select previous deployment
3. Click "Redeploy"

### Render
1. Service → Deployments
2. Select previous deployment
3. Click "Deploy"

## Cost Considerations

### Free Tier Options
- **Vercel**: 100GB/month bandwidth free
- **Render**: 500 free dyno hours/month
- **MongoDB Atlas**: 512 MB free storage
- **Railway**: $5 free tier

### Estimated Costs (Paid Tier)
- **Backend**: $7-15/month
- **Frontend**: Usually free or <$5/month
- **Database**: $9-15/month (varies)
- **Total**: ~$20-30/month for small app

## Support Links

- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [MongoDB Atlas Help](https://docs.atlas.mongodb.com/)
- [GitHub Actions](https://docs.github.com/en/actions)

---

**Deployment complete!** Your Profile Management System is now live.

### Deployed URLs Example
- Backend: https://profile-api.onrender.com
- Frontend: https://profile-manager.vercel.app
- MongoDB: MongoDB Atlas (cloud database)

Keep monitoring logs and user feedback for any issues.
