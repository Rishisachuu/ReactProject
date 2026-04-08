# API Testing Guide

This guide shows how to test all API endpoints using various tools and methods.

## Testing Tools

You can use any of these tools to test the API:
- **Postman** (GUI, recommended) - https://www.postman.com/downloads/
- **Insomnia** (GUI) - https://insomnia.rest/
- **cURL** (Command line)
- **Thunder Client** (VS Code extension)
- **REST Client** (VS Code extension)

## Base URL

**Development**: `http://localhost:5000/api`
**Production**: `https://your-api-domain.com/api`

## Test Data

Use these credentials for testing:
```
Email: test@example.com
Password: TestPassword123!
Name: Test User
```

**Note**: Password must have:
- At least 8 characters
- 1 uppercase letter
- 1 digit
- 1 special character (!@#$%^&*)

## Endpoints & Examples

### 1. User Registration

**Endpoint**: `POST /auth/register`

**Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "email": "test@example.com",
  "password": "TestPassword123!",
  "name": "Test User"
}
```

**Success Response (201)**:
```json
{
  "message": "User registered successfully",
  "user_id": "507f1f77bcf86cd799439011"
}
```

**Error Response (409)**:
```json
{
  "error": "Email already exists"
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!",
    "name": "Test User"
  }'
```

---

### 2. User Login

**Endpoint**: `POST /auth/login`

**Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "email": "test@example.com",
  "password": "TestPassword123!"
}
```

**Success Response (200)**:
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "email": "test@example.com",
    "name": "Test User"
  }
}
```

**Error Response (401)**:
```json
{
  "error": "Invalid email or password"
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'
```

**Save the token for next requests!**

---

### 3. Get User Profile

**Endpoint**: `GET /users/<user_id>`

**Headers**:
```
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json
```

**URL Example**:
```
http://localhost:5000/api/users/507f1f77bcf86cd799439011
```

**Success Response (200)**:
```json
{
  "user": {
    "_id": "507f1f77bcf86cd799439011",
    "email": "test@example.com",
    "name": "Test User",
    "location": "New York",
    "bio": "Hello World!",
    "avatar": "abc123_profile.jpg",
    "privacy": {
      "email_visible": false,
      "location_visible": true,
      "bio_visible": true
    },
    "created_at": "2024-01-15T10:30:00.000Z",
    "updated_at": "2024-01-15T10:30:00.000Z"
  }
}
```

**Error Response (401)**:
```json
{
  "error": "Unauthorized access"
}
```

**cURL Example**:
```bash
curl -X GET http://localhost:5000/api/users/507f1f77bcf86cd799439011 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

---

### 4. Update User Profile

**Endpoint**: `PUT /users/<user_id>`

**Headers**:
```
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json
```

**Request Body**:
```json
{
  "name": "Updated Name",
  "email": "newemail@example.com",
  "location": "San Francisco",
  "bio": "Updated bio text"
}
```

**Success Response (200)**:
```json
{
  "message": "Profile updated successfully",
  "user": {
    "_id": "507f1f77bcf86cd799439011",
    "email": "newemail@example.com",
    "name": "Updated Name",
    "location": "San Francisco",
    "bio": "Updated bio text",
    "avatar": null,
    "privacy": {...},
    "created_at": "2024-01-15T10:30:00.000Z",
    "updated_at": "2024-01-15T11:45:00.000Z"
  }
}
```

**cURL Example**:
```bash
curl -X PUT http://localhost:5000/api/users/507f1f77bcf86cd799439011 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "location": "San Francisco",
    "bio": "Updated bio"
  }'
```

---

### 5. Upload Profile Avatar

**Endpoint**: `POST /users/<user_id>/upload-avatar`

**Headers**:
```
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: multipart/form-data
```

**Form Data**:
- Key: `avatar`
- Value: [Select image file]

**Allowed File Types**: jpg, jpeg, png, gif
**Max File Size**: 16 MB

**Success Response (200)**:
```json
{
  "message": "Avatar uploaded successfully",
  "avatar": "abc123def456_photo.jpg"
}
```

**Error Response (400)**:
```json
{
  "error": "Only jpg, jpeg, png, gif files are allowed"
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:5000/api/users/507f1f77bcf86cd799439011/upload-avatar \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "avatar=@/path/to/image.jpg"
```

**Postman Steps**:
1. Set method to POST
2. Set URL to endpoint
3. Go to "Headers" tab → Add: `Authorization: Bearer YOUR_TOKEN`
4. Go to "Body" tab → Select "form-data"
5. Add key "avatar" with type "File"
6. Click "Select Files" and choose your image
7. Send

---

### 6. Change Password

**Endpoint**: `PUT /users/<user_id>/change-password`

**Headers**:
```
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json
```

**Request Body**:
```json
{
  "current_password": "TestPassword123!",
  "new_password": "NewPassword456!"
}
```

**Password Requirements for New Password**:
- At least 8 characters
- 1 uppercase letter
- 1 digit
- 1 special character

**Success Response (200)**:
```json
{
  "message": "Password changed successfully"
}
```

**Error Responses**:

401 - Wrong current password:
```json
{
  "error": "Current password is incorrect"
}
```

400 - Weak new password:
```json
{
  "error": "Password must be at least 8 characters long"
}
```

**cURL Example**:
```bash
curl -X PUT http://localhost:5000/api/users/507f1f77bcf86cd799439011/change-password \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "TestPassword123!",
    "new_password": "NewPassword456!"
  }'
```

---

### 7. Update Privacy Settings

**Endpoint**: `PUT /users/<user_id>/privacy`

**Headers**:
```
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json
```

**Request Body**:
```json
{
  "privacy": {
    "email_visible": true,
    "location_visible": false,
    "bio_visible": true
  }
}
```

**Success Response (200)**:
```json
{
  "message": "Privacy settings updated successfully",
  "user": {
    "_id": "507f1f77bcf86cd799439011",
    "email": "test@example.com",
    "name": "Test User",
    "privacy": {
      "email_visible": true,
      "location_visible": false,
      "bio_visible": true
    },
    "created_at": "2024-01-15T10:30:00.000Z",
    "updated_at": "2024-01-15T12:00:00.000Z"
  }
}
```

**cURL Example**:
```bash
curl -X PUT http://localhost:5000/api/users/507f1f77bcf86cd799439011/privacy \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "privacy": {
      "email_visible": true,
      "location_visible": false,
      "bio_visible": true
    }
  }'
```

---

## Testing Workflow

### Step 1: Register User
```bash
POST /auth/register
{
  "email": "test@example.com",
  "password": "TestPassword123!",
  "name": "Test User"
}
```
✓ Get user_id

### Step 2: Login
```bash
POST /auth/login
{
  "email": "test@example.com",
  "password": "TestPassword123!"
}
```
✓ Get access_token

### Step 3: Get Profile
```bash
GET /users/{user_id}
Header: Authorization: Bearer {access_token}
```
✓ Verify user data

### Step 4: Update Profile
```bash
PUT /users/{user_id}
Header: Authorization: Bearer {access_token}
{
  "name": "Updated Name",
  "location": "New York",
  "bio": "My bio"
}
```
✓ Verify updates

### Step 5: Upload Avatar
```bash
POST /users/{user_id}/upload-avatar
Header: Authorization: Bearer {access_token}
Body: Form-data with avatar file
```
✓ Check avatar URL

### Step 6: Change Password
```bash
PUT /users/{user_id}/change-password
Header: Authorization: Bearer {access_token}
{
  "current_password": "TestPassword123!",
  "new_password": "NewPassword456!"
}
```
✓ Try new password on next login

### Step 7: Update Privacy
```bash
PUT /users/{user_id}/privacy
Header: Authorization: Bearer {access_token}
{
  "privacy": {
    "email_visible": true,
    "location_visible": true,
    "bio_visible": true
  }
}
```
✓ Verify privacy settings

---

## Postman Collection (JSON)

Create a new file `postman_collection.json`:

```json
{
  "info": {
    "name": "Profile Management API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Register",
      "request": {
        "method": "POST",
        "url": "{{api_url}}/auth/register",
        "body": {
          "mode": "raw",
          "raw": "{\"email\":\"test@example.com\",\"password\":\"TestPassword123!\",\"name\":\"Test User\"}"
        }
      }
    },
    {
      "name": "Login",
      "request": {
        "method": "POST",
        "url": "{{api_url}}/auth/login",
        "body": {
          "mode": "raw",
          "raw": "{\"email\":\"test@example.com\",\"password\":\"TestPassword123!\"}"
        }
      }
    }
  ]
}
```

---

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Missing/invalid token | Include valid JWT in Authorization header |
| 400 Bad Request | Missing/invalid body | Check request body format and required fields |
| 404 Not Found | Invalid endpoint | Verify URL spelling and method (GET vs POST) |
| 409 Conflict | Email already exists | Use different email for registration |
| 500 Internal Error | Server issue | Check server logs for details |

---

## Environment Variables for Testing

Set in Postman:

```
api_url = http://localhost:5000/api
token = [JWT from login response]
user_id = [ID from register/login response]
```

Use these in requests:
- URL: `{{api_url}}/auth/login`
- Header: `Authorization: Bearer {{token}}`

---

## Response Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 500 | Server Error |

---

**Happy testing! 🚀**

For more help, check the backend README.md
