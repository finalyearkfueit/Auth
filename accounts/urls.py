"""
URL routing for accounts app
"""
from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    ForgotPasswordView,
    VerifyOTPView,
    ResetPasswordView,
    GoogleLoginView,
    UserProfileView,
    UserProfileUpdateView,
    CustomTokenRefreshView,
)

app_name = 'accounts'

urlpatterns = [
    # Authentication endpoints
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),

    # Password recovery endpoints
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),

    # Google OAuth endpoint
    path('google-login/', GoogleLoginView.as_view(), name='google-login'),

    # User profile endpoints
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
]
