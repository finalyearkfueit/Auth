# AI Studio Backend - Django API

A production-ready Django REST Framework backend for **AI Studio** – an AI-powered image processing application with background removal, image enhancement, and cloth swap features.

## Features

- ✅ **Custom User Authentication** - Email-based login with JWT tokens
- ✅ **User Registration & Auto-Login** - Secure password hashing with automatic token generation
- ✅ **JWT Token System** - Access tokens (15 min) and refresh tokens (7 days)
- ✅ **Forgot Password with OTP** - 6-digit OTP sent via Gmail SMTP with 10-minute expiry
- ✅ **Google OAuth2 Login** - Single sign-on with Google accounts
- ✅ **User Profile Management** - Update username, email, and profile image
- ✅ **Rate Limiting** - Protected endpoints with rate limiting (5 login attempts/min, 3 OTP attempts/hour)
- ✅ **CORS Enabled** - Ready for mobile and web frontends
- ✅ **Production-Ready Security** - HTTPS, HSTS, secure headers configuration
- ✅ **Standardized API Responses** - Consistent JSON format (status/message/data)

## Tech Stack

- **Django** 4.2.11
- **Django REST Framework** 3.14.0
- **SimpleJWT** 5.5.1 - JWT authentication
- **PostgreSQL** - Database
- **Google OAuth2** - Social authentication
- **SMTP Gmail** - Email service for OTP
- **django-ratelimit** 4.1.0 - Rate limiting
- **django-cors-headers** 4.3.1 - CORS support
- **Pillow** 11.0.0+ - Image handling

## Project Structure

```
backend/
├── ai_studio/              # Project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI application
│   └── asgi.py            # ASGI application
├── accounts/              # Authentication app
│   ├── models.py          # CustomUser & OTP models
│   ├── serializers.py     # API serializers
│   ├── views.py           # API views
│   ├── urls.py            # App URL routing
│   ├── services.py        # OTP, Email, OAuth services
│   ├── handlers.py        # Exception handlers & responses
│   └── admin.py           # Django admin configuration
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Installation & Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 12+
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone Repository
```bash
cd backend
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

**Required Environment Variables:**
- `SECRET_KEY` - Django secret key (generate a new one)
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` - PostgreSQL connection
- `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` - Gmail SMTP credentials (App Password)
- `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET` - Google OAuth credentials
- `CORS_ALLOWED_ORIGINS` - Frontend URL(s)

### Step 5: Run Database Migrations
```bash
python manage.py migrate
```

### Step 6: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### Step 7: Start Development Server
```bash
python manage.py runserver
```

Server runs at: `http://localhost:8000`
Admin panel: `http://localhost:8000/admin`

---

## API Endpoints

### Authentication

#### Register
- **POST** `/api/auth/register/`
- Create new user account
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!"
}
```

#### Login
- **POST** `/api/auth/login/` (Rate limited: 5/min)
- Login with email and password
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

#### Logout
- **POST** `/api/auth/logout/` (Requires auth)
- Blacklist refresh token
```json
{
  "refresh": "refresh_token_here"
}
```

#### Token Refresh
- **POST** `/api/auth/token/refresh/`
- Get new access token using refresh token
```json
{
  "refresh": "refresh_token_here"
}
```

### Password Recovery

#### Forgot Password (Send OTP)
- **POST** `/api/auth/forgot-password/` (Rate limited: 3/hour)
- Send OTP to registered email
```json
{
  "email": "john@example.com"
}
```

#### Verify OTP
- **POST** `/api/auth/verify-otp/`
- Verify OTP and get password reset token
```json
{
  "email": "john@example.com",
  "otp_code": "123456"
}
```

#### Reset Password
- **POST** `/api/auth/reset-password/` (Rate limited: 3/hour)
- Reset password with reset token
```json
{
  "reset_token": "reset_token_from_verify_otp",
  "password": "NewPassword123!",
  "password_confirm": "NewPassword123!"
}
```

### Google OAuth

#### Google Login
- **POST** `/api/auth/google-login/`
- Login with Google ID token
```json
{
  "id_token": "google_id_token_from_google_login"
}
```

### User Profile

#### Get Profile
- **GET** `/api/auth/profile/` (Requires auth)
- Retrieve authenticated user profile

#### Update Profile
- **PUT** `/api/auth/profile/update/` (Requires auth)
- Update username and/or profile image
```json
{
  "username": "new_username",
  "profile_image": "image_file_here"
}
```

---

## API Response Format

### Success Response
```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "profile_image": null,
      "created_at": "2024-05-22T10:30:00Z",
      "updated_at": "2024-05-22T10:30:00Z"
    },
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Invalid email or password",
  "data": null
}
```

---

## Authentication

All protected endpoints require JWT token in Authorization header:

```
Authorization: Bearer <access_token>
```

Example:
```bash
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." http://localhost:8000/api/auth/profile/
```

---

## Configuration Guide

### Gmail SMTP Setup

1. Enable 2-Factor Authentication on your Gmail account
2. Generate App Password:
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Click "App Passwords"
   - Select Mail and Device (Windows Computer or Mac)
   - Copy the generated password
3. Add to `.env`:
   ```
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=generated-app-password
   ```

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials (Web application)
5. Add authorized JavaScript origins:
   - `http://localhost:3000` (React/React Native dev)
   - `http://localhost:8000` (Django dev)
6. Copy Client ID and Client Secret to `.env`:
   ```
   GOOGLE_OAUTH_CLIENT_ID=your-client-id
   GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
   ```

### PostgreSQL Setup

1. Install PostgreSQL
2. Create database and user:
   ```sql
   CREATE DATABASE ai_studio;
   CREATE USER ai_user WITH PASSWORD 'your_password';
   ALTER ROLE ai_user SET client_encoding TO 'utf8';
   ALTER ROLE ai_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE ai_user SET default_transaction_deferrable TO ON;
   GRANT ALL PRIVILEGES ON DATABASE ai_studio TO ai_user;
   ```
3. Update `.env` with database credentials

---

## Security Features

- ✅ **Password Hashing** - PBKDF2 with Django default
- ✅ **JWT Tokens** - Short-lived access (15 min), long-lived refresh (7 days)
- ✅ **Rate Limiting** - Prevent brute force attacks
- ✅ **OTP Expiry** - 10-minute expiration for password reset
- ✅ **CORS Whitelist** - Only allowed origins can access API
- ✅ **HTTPS** - Enforced in production
- ✅ **HSTS** - HTTP Strict Transport Security enabled
- ✅ **Secure Headers** - X-Frame-Options, X-Content-Type-Options

---

## Management Commands

### Create Superuser
```bash
python manage.py createsuperuser
```

### Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Clear Expired OTPs
```bash
python manage.py shell
>>> from accounts.services import OTPService
>>> OTPService.cleanup_expired_otps()
```

---

## Deployment

### Production Checklist

1. **Environment Variables**
   ```bash
   DEBUG=False
   SECRET_KEY=generate-random-secure-key
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   SECURE_SSL_REDIRECT=True
   ```

2. **Database** - Use production PostgreSQL instance

3. **Email** - Configure production email service

4. **Static & Media Files** - Use AWS S3 or similar CDN

5. **Web Server** - Use Gunicorn + Nginx

6. **WSGI** - Configure for production deployment

### Production Deployment Example (Gunicorn + Nginx)

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn ai_studio.wsgi:application --bind 0.0.0.0:8000

# Configure Nginx as reverse proxy (see Nginx documentation)
```

---

## Testing

Test endpoints using Postman or ThunderClient:

1. **Register** → Get tokens
2. **Login** → Get new tokens
3. **Profile** → Verify auth works
4. **Forgot Password** → Test OTP flow
5. **Google Login** → Test OAuth

---

## Troubleshooting

### PostgreSQL Connection Error
- Verify PostgreSQL is running
- Check DB credentials in `.env`
- Ensure database exists

### Email Not Sending
- Verify Gmail App Password (not regular password)
- Check SMTP settings in `settings.py`
- Enable "Less secure app access" if needed

### Migration Errors
- Delete `db.sqlite3` if exists
- Run `python manage.py migrate --run-syncdb`
- Check for conflicting migrations

### CORS Errors
- Add frontend URL to `CORS_ALLOWED_ORIGINS` in `.env`
- Ensure `DEBUG=True` or proper domain configuration

---

## Contributing

Future integrations:
- Image processing APIs (background removal, enhancement, cloth swap)
- Payment gateway integration
- Advanced analytics
- User-generated content management

---

## License

This project is part of the Final Year Project (FYP) for AI Studio.

---

## Support

For issues or questions, refer to the documentation or contact the development team.

---

**Last Updated:** May 2024
**Version:** 1.0.0
**Status:** Production Ready ✅
#   A u t h  
 