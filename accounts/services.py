"""
Services for OTP, Email, and Google OAuth
"""
import random
import string
import traceback
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from .models import OTP
from .email_templates import EmailTemplates
from .logging_config import get_logger
import jwt
from google.auth.transport import requests
from google.oauth2 import id_token

logger = get_logger(__name__)


class OTPService:
    """Service for generating and managing OTPs."""

    @staticmethod
    def generate_otp():
        """Generate a 6-digit OTP."""
        return ''.join(random.choices(string.digits, k=6))

    @staticmethod
    def create_otp(email):
        """Create an OTP for the given email."""
        try:
            otp_code = OTPService.generate_otp()
            expires_at = timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)

            otp = OTP.objects.create(
                email=email,
                otp_code=otp_code,
                expires_at=expires_at
            )

            logger.info('OTP created for email: %s', email)
            return otp
        except Exception:
            logger.error('Failed to create OTP for email %s:\n%s', email, traceback.format_exc())
            raise

    @staticmethod
    def verify_otp(email, otp_code):
        """Verify OTP for the given email."""
        try:
            otp = OTP.objects.get(email=email, otp_code=otp_code, is_verified=False)

            if timezone.now() > otp.expires_at:
                otp.delete()
                logger.info('Expired OTP used for email: %s', email)
                return False, 'OTP has expired.'

            otp.is_verified = True
            otp.save()
            logger.info('OTP verified successfully for email: %s', email)
            return True, 'OTP verified successfully.'

        except OTP.DoesNotExist:
            logger.warning('Invalid OTP attempt for email: %s', email)
            return False, 'Invalid OTP.'
        except Exception:
            logger.error('Unexpected error verifying OTP for email %s:\n%s', email, traceback.format_exc())
            return False, 'OTP verification failed due to an internal error.'

    @staticmethod
    def cleanup_expired_otps():
        """Delete expired OTPs."""
        try:
            deleted_count, _ = OTP.objects.filter(expires_at__lt=timezone.now()).delete()
            logger.info('Cleaned up %d expired OTP(s)', deleted_count)
        except Exception:
            logger.error('Failed to clean up expired OTPs:\n%s', traceback.format_exc())


class EmailService:
    """Service for sending emails via Gmail SMTP with HTML templates."""

    @staticmethod
    def _check_email_config():
        """
        Verify that the required SMTP credentials are present.
        Returns (ok: bool, error_message: str | None).
        """
        missing = []
        if not getattr(settings, 'EMAIL_HOST_USER', ''):
            missing.append('EMAIL_HOST_USER')
        if not getattr(settings, 'EMAIL_HOST_PASSWORD', ''):
            missing.append('EMAIL_HOST_PASSWORD')

        if missing:
            msg = (
                'Email service is not configured. '
                f'Missing environment variable(s): {", ".join(missing)}. '
                'Set these in your Railway service variables.'
            )
            logger.error(msg)
            return False, msg

        return True, None

    @staticmethod
    def send_otp_email(email, otp_code):
        """Send OTP to user email with beautiful HTML template."""
        ok, err = EmailService._check_email_config()
        if not ok:
            return False, err

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
            logger.info('OTP email sent successfully to: %s', email)
            return True, 'OTP sent successfully.'
        except Exception as e:
            logger.error(
                'Failed to send OTP email to %s: %s\n%s',
                email, str(e), traceback.format_exc(),
            )
            return False, f'Failed to send email: {str(e)}'

    @staticmethod
    def send_welcome_email(email, username):
        """Send welcome email to new user with HTML template."""
        ok, err = EmailService._check_email_config()
        if not ok:
            # Welcome email failure is non-fatal — log and continue
            logger.warning(
                'Skipping welcome email to %s (%s): %s',
                email, username, err,
            )
            return False, err

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
            logger.info('Welcome email sent successfully to: %s', email)
            return True, 'Welcome email sent.'
        except Exception as e:
            logger.error(
                'Failed to send welcome email to %s: %s\n%s',
                email, str(e), traceback.format_exc(),
            )
            return False, f'Failed to send email: {str(e)}'


class GoogleOAuthService:
    """Service for Google OAuth2 authentication."""

    @staticmethod
    def verify_google_token(id_token_str):
        """
        Verify Google ID token and return user information.
        Returns: (is_valid, user_data or error_message)
        """
        client_id = getattr(settings, 'GOOGLE_OAUTH_CLIENT_ID', '')
        if not client_id:
            msg = (
                'Google OAuth is not configured. '
                'Missing environment variable: GOOGLE_OAUTH_CLIENT_ID. '
                'Set this in your Railway service variables.'
            )
            logger.error(msg)
            return False, msg

        try:
            # Verify token with Google
            idinfo = id_token.verify_oauth2_token(
                id_token_str,
                requests.Request(),
                client_id,
            )

            # Token is valid, extract user info
            user_data = {
                'email': idinfo.get('email'),
                'username': idinfo.get('email', '').split('@')[0],  # Use email prefix as username
                'first_name': idinfo.get('given_name', ''),
                'last_name': idinfo.get('family_name', ''),
                'picture': idinfo.get('picture'),
            }

            logger.info('Google token verified for email: %s', user_data.get('email'))
            return True, user_data

        except ValueError as e:
            logger.warning('Invalid Google token: %s', str(e))
            return False, f'Invalid token: {str(e)}'
        except Exception as e:
            logger.error(
                'Google token verification failed: %s\n%s',
                str(e), traceback.format_exc(),
            )
            return False, f'Token verification failed: {str(e)}'


class TokenService:
    """Service for JWT token generation and management."""

    @staticmethod
    def generate_password_reset_token(email):
        """Generate a short-lived JWT token for password reset."""
        try:
            payload = {
                'email': email,
                'type': 'password_reset',
                'exp': timezone.now() + timedelta(minutes=15),  # 15 minutes expiry
                'iat': timezone.now()
            }

            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            logger.info('Password reset token generated for email: %s', email)
            return token
        except Exception:
            logger.error(
                'Failed to generate password reset token for email %s:\n%s',
                email, traceback.format_exc(),
            )
            raise

    @staticmethod
    def verify_password_reset_token(token):
        """Verify and decode password reset token."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            if payload.get('type') != 'password_reset':
                logger.warning('Password reset token has unexpected type: %s', payload.get('type'))
                return False, None

            return True, payload.get('email')

        except jwt.ExpiredSignatureError:
            logger.warning('Expired password reset token used')
            return False, None
        except jwt.InvalidTokenError as e:
            logger.warning('Invalid password reset token: %s', str(e))
            return False, None
        except Exception:
            logger.error('Unexpected error verifying password reset token:\n%s', traceback.format_exc())
            return False, None
