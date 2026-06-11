"""
Views for accounts app - Authentication APIs
"""
import traceback
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    ForgotPasswordSerializer,
    VerifyOTPSerializer,
    ResetPasswordSerializer,
    GoogleLoginSerializer,
)
from .services import (
    OTPService,
    EmailService,
    GoogleOAuthService,
    TokenService,
)
from .handlers import StandardResponse
from .logging_config import get_logger

logger = get_logger(__name__)

User = get_user_model()


class UserRegistrationView(views.APIView):
    """User registration endpoint."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Register a new user."""
        try:
            serializer = UserRegistrationSerializer(data=request.data)

            if serializer.is_valid():
                user = serializer.save()
                logger.info('New user registered: %s', user.email)

                # Send welcome email (non-fatal if it fails)
                EmailService.send_welcome_email(user.email, user.username)

                # Generate tokens
                refresh = RefreshToken.for_user(user)

                return StandardResponse.success(
                    message='User registered successfully. Please check your email.',
                    data={
                        'user': UserProfileSerializer(user).data,
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    },
                    status_code=status.HTTP_201_CREATED
                )

            logger.warning('Registration validation failed: %s', serializer.errors)
            return StandardResponse.error(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(
                'Unexpected error in UserRegistrationView: %s\n%s',
                str(e), traceback.format_exc(),
            )
            return StandardResponse.error(
                message='Registration failed due to an internal error.',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserLoginView(views.APIView):
    """User login endpoint."""
    permission_classes = [AllowAny]

    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST'))
    def post(self, request):
        """Login user with email and password."""
        try:
            serializer = UserLoginSerializer(data=request.data)

            if serializer.is_valid():
                user = serializer.validated_data
                refresh = RefreshToken.for_user(user)
                logger.info('User logged in: %s', user.email)

                return StandardResponse.success(
                    message='Login successful.',
                    data={
                        'user': UserProfileSerializer(user).data,
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    },
                    status_code=status.HTTP_200_OK
                )

            logger.warning('Login validation failed: %s', serializer.errors)
            return StandardResponse.error(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(
                'Unexpected error in UserLoginView: %s\n%s',
                str(e), traceback.format_exc(),
            )
            return StandardResponse.error(
                message='Login failed due to an internal error.',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserLogoutView(views.APIView):
    """User logout endpoint."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Logout user by blacklisting refresh token."""
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info('User logged out: %s', request.user.email)

            return StandardResponse.success(
                message='Logout successful.',
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(
                'Logout failed for user %s: %s\n%s',
                getattr(request.user, 'email', 'unknown'), str(e), traceback.format_exc(),
            )
            return StandardResponse.error(
                message=f'Logout failed: {str(e)}',
                status_code=status.HTTP_400_BAD_REQUEST
            )


class ForgotPasswordView(views.APIView):
    """Forgot password endpoint - Send OTP to email."""
    permission_classes = [AllowAny]

    @method_decorator(ratelimit(key='ip', rate='3/h', method='POST'))
    def post(self, request):
        """Send OTP to user email."""
        try:
            serializer = ForgotPasswordSerializer(data=request.data)

            if serializer.is_valid():
                email = serializer.validated_data['email']

                # Create OTP
                otp = OTPService.create_otp(email)

                # Send OTP email
                is_sent, message = EmailService.send_otp_email(email, otp.otp_code)

                if is_sent:
                    return StandardResponse.success(
                        message='OTP sent to your email. Please check your inbox.',
                        status_code=status.HTTP_200_OK
                    )
                else:
                    logger.error('OTP email delivery failed for %s: %s', email, message)
                    return StandardResponse.error(
                        message=message,
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            logger.warning('ForgotPassword validation failed: %s', serializer.errors)
            return StandardResponse.error(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(
                'Unexpected error in ForgotPasswordView: %s\n%s',
                str(e), traceback.format_exc(),
            )
            return StandardResponse.error(
                message='Failed to process password reset request due to an internal error.',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyOTPView(views.APIView):
    """Verify OTP endpoint."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Verify OTP and return password reset token."""
        try:
            serializer = VerifyOTPSerializer(data=request.data)

            if serializer.is_valid():
                email = serializer.validated_data['email']
                otp_code = serializer.validated_data['otp_code']

                # Verify OTP
                is_valid, message = OTPService.verify_otp(email, otp_code)

                if is_valid:
                    # Generate password reset token
                    reset_token = TokenService.generate_password_reset_token(email)

                    return StandardResponse.success(
                        message='OTP verified successfully.',
                        data={'reset_token': reset_token},
                        status_code=status.HTTP_200_OK
                    )
                else:
                    return StandardResponse.error(
                        message=message,
                        status_code=status.HTTP_400_BAD_REQUEST
                    )

            logger.warning('VerifyOTP validation failed: %s', serializer.errors)
            return StandardResponse.error(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(
                'Unexpected error in VerifyOTPView: %s\n%s',
                str(e), traceback.format_exc(),
            )
            return StandardResponse.error(
                message='OTP verification failed due to an internal error.',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ResetPasswordView(views.APIView):
    """Reset password endpoint."""
    permission_classes = [AllowAny]

    @method_decorator(ratelimit(key='ip', rate='3/h', method='POST'))
    def post(self, request):
        """Reset password using reset token."""
        try:
            serializer = ResetPasswordSerializer(data=request.data)

            if serializer.is_valid():
                reset_token = serializer.validated_data['reset_token']
                new_password = serializer.validated_data['password']

                # Verify reset token
                is_valid, email = TokenService.verify_password_reset_token(reset_token)

                if not is_valid:
                    logger.warning('Invalid or expired reset token used')
                    return StandardResponse.error(
                        message='Invalid or expired reset token.',
                        status_code=status.HTTP_400_BAD_REQUEST
                    )

                # Update user password
                try:
                    user = User.objects.get(email=email)
                    user.set_password(new_password)
                    user.save()
                    logger.info('Password reset successfully for email: %s', email)

                    return StandardResponse.success(
                        message='Password reset successfully.',
                        status_code=status.HTTP_200_OK
                    )
                except User.DoesNotExist:
                    logger.warning('Password reset attempted for non-existent user: %s', email)
                    return StandardResponse.error(
                        message='User not found.',
                        status_code=status.HTTP_404_NOT_FOUND
                    )

            logger.warning('ResetPassword validation failed: %s', serializer.errors)
            return StandardResponse.error(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(
                'Unexpected error in ResetPasswordView: %s\n%s',
                str(e), traceback.format_exc(),
            )
            return StandardResponse.error(
                message='Password reset failed due to an internal error.',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GoogleLoginView(views.APIView):
    """Google OAuth2 login endpoint."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Login or create user with Google ID token."""
        try:
            serializer = GoogleLoginSerializer(data=request.data)

            if serializer.is_valid():
                id_token_str = serializer.validated_data['id_token']

                # Verify Google token
                is_valid, result = GoogleOAuthService.verify_google_token(id_token_str)

                if not is_valid:
                    logger.warning('Google token verification failed: %s', result)
                    return StandardResponse.error(
                        message=result,
                        status_code=status.HTTP_400_BAD_REQUEST
                    )

                user_data = result
                email = user_data['email']

                # Check if user exists
                try:
                    user = User.objects.get(email=email)
                    logger.info('Existing user logged in via Google: %s', email)
                except User.DoesNotExist:
                    # Create new user
                    user = User.objects.create_user(
                        email=email,
                        username=user_data['username'],
                        first_name=user_data.get('first_name', ''),
                        last_name=user_data.get('last_name', ''),
                    )
                    logger.info('New user created via Google OAuth: %s', email)

                # Generate tokens
                refresh = RefreshToken.for_user(user)

                return StandardResponse.success(
                    message='Google login successful.',
                    data={
                        'user': UserProfileSerializer(user).data,
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    },
                    status_code=status.HTTP_200_OK
                )

            logger.warning('GoogleLogin validation failed: %s', serializer.errors)
            return StandardResponse.error(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(
                'Unexpected error in GoogleLoginView: %s\n%s',
                str(e), traceback.format_exc(),
            )
            return StandardResponse.error(
                message='Google login failed due to an internal error.',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserProfileView(views.APIView):
    """Get user profile endpoint."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get authenticated user profile."""
        try:
            user = request.user
            serializer = UserProfileSerializer(user)

            return StandardResponse.success(
                message='Profile retrieved successfully.',
                data=serializer.data,
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(
                'Unexpected error in UserProfileView for user %s: %s\n%s',
                getattr(request.user, 'email', 'unknown'), str(e), traceback.format_exc(),
            )
            return StandardResponse.error(
                message='Failed to retrieve profile due to an internal error.',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserProfileUpdateView(views.APIView):
    """Update user profile endpoint."""
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """Update authenticated user profile."""
        try:
            user = request.user
            serializer = UserUpdateSerializer(
                user,
                data=request.data,
                partial=True,
                context={'request': request}
            )

            if serializer.is_valid():
                serializer.save()
                logger.info('Profile updated for user: %s', user.email)

                return StandardResponse.success(
                    message='Profile updated successfully.',
                    data=UserProfileSerializer(user).data,
                    status_code=status.HTTP_200_OK
                )

            logger.warning('Profile update validation failed for %s: %s', user.email, serializer.errors)
            return StandardResponse.error(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(
                'Unexpected error in UserProfileUpdateView for user %s: %s\n%s',
                getattr(request.user, 'email', 'unknown'), str(e), traceback.format_exc(),
            )
            return StandardResponse.error(
                message='Failed to update profile due to an internal error.',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CustomTokenRefreshView(TokenRefreshView):
    """Custom token refresh view with standardized response."""

    def post(self, request, *args, **kwargs):
        """Refresh access token."""
        try:
            response = super().post(request, *args, **kwargs)

            if response.status_code == 200:
                return StandardResponse.success(
                    message='Token refreshed successfully.',
                    data=response.data,
                    status_code=status.HTTP_200_OK
                )

            logger.warning('Token refresh failed with status %s', response.status_code)
            return StandardResponse.error(
                message='Token refresh failed.',
                status_code=response.status_code
            )
        except Exception as e:
            logger.error(
                'Unexpected error in CustomTokenRefreshView: %s\n%s',
                str(e), traceback.format_exc(),
            )
            return StandardResponse.error(
                message='Token refresh failed due to an internal error.',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
