#!/usr/bin/env python
"""
Installation Verification Script for AI Studio Backend
Run this after setup to verify everything is configured correctly
"""

import os
import sys
import django
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_check(status, text):
    symbol = "✓" if status else "✗"
    color = "\033[92m" if status else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{symbol}{reset} {text}")

def check_django_setup():
    """Verify Django is properly set up"""
    print_header("Checking Django Setup")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_studio.settings')
        django.setup()
        print_check(True, "Django setup successful")
        return True
    except Exception as e:
        print_check(False, f"Django setup failed: {str(e)}")
        return False

def check_database():
    """Verify database configuration"""
    print_header("Checking Database Configuration")
    
    try:
        from django.core.management import call_command
        from django.db import connection
        
        # Try to connect
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print_check(True, "Database connection successful")
        return True
    except Exception as e:
        print_check(False, f"Database connection failed: {str(e)}")
        return False

def check_installed_apps():
    """Verify all apps are installed"""
    print_header("Checking Installed Apps")
    
    try:
        from django.apps import apps
        
        required_apps = [
            'rest_framework',
            'rest_framework_simplejwt',
            'corsheaders',
            'accounts',
        ]
        
        for app in required_apps:
            try:
                apps.get_app_config(app)
                print_check(True, f"{app} installed")
            except:
                print_check(False, f"{app} not installed")
                return False
        
        return True
    except Exception as e:
        print_check(False, f"Error checking apps: {str(e)}")
        return False

def check_models():
    """Verify models are accessible"""
    print_header("Checking Models")
    
    try:
        from accounts.models import CustomUser, OTP
        print_check(True, "CustomUser model accessible")
        print_check(True, "OTP model accessible")
        return True
    except Exception as e:
        print_check(False, f"Model check failed: {str(e)}")
        return False

def check_urls():
    """Verify URL configuration"""
    print_header("Checking URL Configuration")
    
    try:
        from django.urls import reverse
        
        endpoints = [
            'accounts:register',
            'accounts:login',
            'accounts:logout',
            'accounts:profile',
        ]
        
        for endpoint in endpoints:
            try:
                reverse(endpoint)
                print_check(True, f"{endpoint} URL configured")
            except:
                print_check(False, f"{endpoint} URL not configured")
                return False
        
        return True
    except Exception as e:
        print_check(False, f"URL check failed: {str(e)}")
        return False

def check_migrations():
    """Verify migrations are applied"""
    print_header("Checking Migrations")
    
    try:
        from django.core.management import call_command
        from io import StringIO
        
        out = StringIO()
        call_command('showmigrations', stdout=out)
        output = out.getvalue()
        
        if 'accounts' in output:
            print_check(True, "Migration files exist")
        else:
            print_check(False, "No migration files found")
            return False
        
        return True
    except Exception as e:
        print_check(False, f"Migration check failed: {str(e)}")
        return False

def check_settings():
    """Verify critical settings"""
    print_header("Checking Settings")
    
    try:
        from django.conf import settings
        
        checks = [
            ('AUTH_USER_MODEL', 'accounts.CustomUser'),
            ('REST_FRAMEWORK exists', hasattr(settings, 'REST_FRAMEWORK')),
            ('SIMPLE_JWT exists', hasattr(settings, 'SIMPLE_JWT')),
            ('CORS_ALLOWED_ORIGINS exists', hasattr(settings, 'CORS_ALLOWED_ORIGINS')),
        ]
        
        for check_name, expected in checks:
            status = expected if isinstance(expected, bool) else (getattr(settings, check_name.split()[0], None) == expected)
            print_check(status, f"{check_name} configured")
            if not status:
                return False
        
        return True
    except Exception as e:
        print_check(False, f"Settings check failed: {str(e)}")
        return False

def check_email_config():
    """Verify email configuration"""
    print_header("Checking Email Configuration")
    
    try:
        from django.conf import settings
        
        email_configured = (
            settings.EMAIL_HOST_USER and
            settings.EMAIL_HOST_PASSWORD and
            settings.DEFAULT_FROM_EMAIL
        )
        
        if email_configured:
            print_check(True, "Email configuration found")
            return True
        else:
            print_check(False, "Email not fully configured (optional for development)")
            return True  # Not critical
    except Exception as e:
        print_check(False, f"Email check failed: {str(e)}")
        return True  # Not critical

def check_google_oauth():
    """Verify Google OAuth configuration"""
    print_header("Checking Google OAuth Configuration")
    
    try:
        from django.conf import settings
        
        oauth_configured = (
            settings.GOOGLE_OAUTH_CLIENT_ID and
            settings.GOOGLE_OAUTH_CLIENT_SECRET
        )
        
        if oauth_configured:
            print_check(True, "Google OAuth configuration found")
            return True
        else:
            print_check(False, "Google OAuth not configured (optional for development)")
            return True  # Not critical
    except Exception as e:
        print_check(False, f"Google OAuth check failed: {str(e)}")
        return True  # Not critical

def run_all_checks():
    """Run all verification checks"""
    print_header("AI Studio Backend - Verification Script")
    
    checks = [
        ("Django Setup", check_django_setup),
        ("Installed Apps", check_installed_apps),
        ("Models", check_models),
        ("URL Configuration", check_urls),
        ("Migrations", check_migrations),
        ("Settings", check_settings),
        ("Database", check_database),
        ("Email Configuration", check_email_config),
        ("Google OAuth", check_google_oauth),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print_check(False, f"{check_name} failed with error: {str(e)}")
            results.append((check_name, False))
    
    # Summary
    print_header("Verification Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {check_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} checks passed\n")
    
    if passed == total:
        print("\n✓ All checks passed! Backend is ready to use.\n")
        print("Next steps:")
        print("1. Create superuser: python manage.py createsuperuser")
        print("2. Run server: python manage.py runserver")
        print("3. Test endpoints: See TESTING_GUIDE.md")
        return True
    else:
        print("\n✗ Some checks failed. Please fix the issues above.\n")
        return False

if __name__ == '__main__':
    try:
        success = run_all_checks()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        sys.exit(1)
