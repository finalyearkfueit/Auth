from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTP


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin configuration for CustomUser model."""
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'first_name', 'last_name', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at', 'last_login')


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    """Admin configuration for OTP model."""
    list_display = ('email', 'otp_code', 'is_verified', 'created_at', 'expires_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('email', 'otp_code')
    readonly_fields = ('created_at', 'otp_code')
    fieldsets = (
        (None, {'fields': ('email', 'otp_code')}),
        ('Status', {'fields': ('is_verified',)}),
        ('Dates', {'fields': ('created_at', 'expires_at')}),
    )
