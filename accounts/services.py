"""
Services for OTP, Email, and Google OAuth
"""
import random
import string
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from .models import OTP
from .email_templates import EmailTemplates
import jwt
from google.auth.transport import requests
from google.oauth2 import id_token


class OTPService:
    """Service for generating and managing OTPs."""

    @staticmethod
    def generate_otp():
        """Generate a 6-digit OTP."""
        return ''.join(random.choices(string.digits, k=6))

    @staticmethod
    def create_otp(email):
        """Create an OTP for the given email."""
        otp_code = OTPService.generate_otp()
        expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)

        otp = OTP.objects.create(
            email=email,
            otp_code=otp_code,
            expires_at=expires_at
        )

        return otp

    @staticmethod
    def verify_otp(email, otp_code):
        """Verify OTP for the given email."""
        try:
            otp = OTP.objects.get(email=email, otp_code=otp_code, is_verified=False)

            if timezone.now() > otp.expires_at:
                otp.delete()
                return False, 'OTP has expired.'

            otp.is_verified = True
            otp.save()
            return True, 'OTP verified successfully.'

        except OTP.DoesNotExist:
            return False, 'Invalid OTP.'

    @staticmethod
    def cleanup_expired_otps():
        """Delete expired OTPs."""
        OTP.objects.filter(expires_at__lt=timezone.now()).delete()


class EmailService:
    """Service for sending emails via Gmail SMTP with HTML templates."""

    @staticmethod
    def send_otp_email(email, otp_code):
        """Send OTP to user email with beautiful HTML template."""
        subject = '🔐 Password Reset - AI Studio'
        html_content = EmailTemplates.get_otp_email_html(
            otp_code, 
            settings.OTP_EXPIRY_MINUTES
        )
        plain_text = f'''
Your One-Time Password (OTP) for resetting your AI Studio password is:

{otp_code}

This OTP will expire in {settings.OTP_EXPIRY_MINUTES} minutes.

If you did not request this, please ignore this email.

Best regards,
AI Studio Team
        '''
        try:
            msg = EmailMultiAlternatives(
                subject,
                plain_text,
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=False)
            return True, 'OTP sent successfully.'
        except Exception as e:
            return False, f'Failed to send email: {str(e)}'

    @staticmethod
    def send_welcome_email(email, username):
        """Send welcome email to new user with HTML template."""
        subject = '🎨 Welcome to AI Studio!'
        html_content = EmailTemplates.get_welcome_email_html(username)
        plain_text = f'''
Hello {username},

Welcome to AI Studio! Your account has been successfully created.

You can now log in using your email and password.

Start transforming your images with our AI-powered tools:
- Background Removal
- Image Enhancement
- Cloth Swap

Best regards,
AI Studio Team
        '''
        try:
            msg = EmailMultiAlternatives(
                subject,
                plain_text,
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=False)
            return True, 'Welcome email sent.'
        except Exception as e:
            return False, f'Failed to send email: {str(e)}'


class GoogleOAuthService:
    """Service for Google OAuth2 authentication."""

    @staticmethod
    def verify_google_token(id_token_str):
        """
        Verify Google ID token and return user information.
        Returns: (is_valid, user_data or error_message)
        """
        try:
            # Verify token with Google
            idinfo = id_token.verify_oauth2_token(
                id_token_str,
                requests.Request(),
                settings.GOOGLE_OAUTH_CLIENT_ID
            )

            # Token is valid, extract user info
            user_data = {
                'email': idinfo.get('email'),
                'username': idinfo.get('email', '').split('@')[0],  # Use email prefix as username
                'first_name': idinfo.get('given_name', ''),
                'last_name': idinfo.get('family_name', ''),
                'picture': idinfo.get('picture'),
            }

            return True, user_data

        except ValueError as e:
            return False, f'Invalid token: {str(e)}'
        except Exception as e:
            return False, f'Token verification failed: {str(e)}'


class TokenService:
    """Service for JWT token generation and management."""

    @staticmethod
    def generate_password_reset_token(email):
        """Generate a short-lived JWT token for password reset."""
        payload = {
            'email': email,
            'type': 'password_reset',
            'exp': timezone.now() + timedelta(minutes=15),  # 15 minutes expiry
            'iat': timezone.now()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token

    @staticmethod
    def verify_password_reset_token(token):
        """Verify and decode password reset token."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            if payload.get('type') != 'password_reset':
                return False, None

            return True, payload.get('email')

        except jwt.ExpiredSignatureError:
            return False, None
        except jwt.InvalidTokenError:
            return False, None
