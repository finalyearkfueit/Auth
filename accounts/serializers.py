"""
Serializers for accounts app
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import OTP
import re

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')

    def validate(self, data):
        """Validate password confirmation."""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists.'})

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'Username already exists.'})

        return data

    def create(self, validated_data):
        """Create user with hashed password."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        """Validate credentials."""
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError('Email and password are required.')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'email': 'User with this email does not exist.'})

        if not user.check_password(password):
            raise serializers.ValidationError({'password': 'Invalid credentials.'})

        if not user.is_active:
            raise serializers.ValidationError({'email': 'User account is inactive.'})

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile_image', 'created_at', 'updated_at')
        read_only_fields = ('id', 'email', 'created_at', 'updated_at')


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for user profile update."""
    class Meta:
        model = User
        fields = ('username', 'profile_image')

    def validate_username(self, value):
        """Validate username uniqueness."""
        user = self.context.get('request').user
        if User.objects.filter(username=value).exclude(id=user.id).exists():
            raise serializers.ValidationError('Username already exists.')
        return value


class ForgotPasswordSerializer(serializers.Serializer):
    """Serializer for forgot password request."""
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """Validate email exists."""
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email does not exist.')
        return value


class VerifyOTPSerializer(serializers.Serializer):
    """Serializer for OTP verification."""
    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(max_length=6, required=True)

    def validate_otp_code(self, value):
        """Validate OTP format."""
        if not re.match(r'^\d{6}$', value):
            raise serializers.ValidationError('OTP must be 6 digits.')
        return value


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer for password reset."""
    reset_token = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, data):
        """Validate passwords match."""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data


class GoogleLoginSerializer(serializers.Serializer):
    """Serializer for Google OAuth login."""
    id_token = serializers.CharField(required=True)
