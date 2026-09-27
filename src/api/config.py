"""
Agent Verification Framework - Secure Configuration Module
"""

import os
from typing import Optional


class SecurityConfig:
    """Security configuration with environment variable support"""
    
    @staticmethod
    def get_secret_key() -> str:
        """Get Flask secret key from environment"""
        secret_key = os.environ.get('SECRET_KEY')
        if not secret_key:
            if os.environ.get('FLASK_ENV') == 'production':
                raise ValueError(
                    "SECRET_KEY environment variable must be set in production. "
                    "Generate one with: python -c 'import secrets; print(secrets.token_hex(32))'"
                )
            # Development only
            return 'dev-secret-key-CHANGE-THIS-IN-PRODUCTION'
        return secret_key
    
    @staticmethod
    def get_api_key() -> str:
        """Get default API key from environment"""
        api_key = os.environ.get('API_KEY')
        if not api_key:
            if os.environ.get('FLASK_ENV') == 'production':
                raise ValueError(
                    "API_KEY environment variable must be set in production. "
                    "Generate one with: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
                )
            # Development only
            return 'dev-api-key-CHANGE-THIS-IN-PRODUCTION'
        return api_key
    
    @staticmethod
    def get_host() -> str:
        """Get host from environment (default to localhost for security)"""
        return os.environ.get('HOST', '127.0.0.1')
    
    @staticmethod
    def get_port() -> int:
        """Get port from environment"""
        return int(os.environ.get('PORT', 5000))
    
    @staticmethod
    def is_debug() -> bool:
        """Check if debug mode is enabled"""
        debug = os.environ.get('DEBUG', 'false').lower()
        if debug in ('true', '1', 'yes'):
            if os.environ.get('FLASK_ENV') == 'production':
                raise ValueError("DEBUG mode must not be enabled in production")
            return True
        return False
    
    @staticmethod
    def get_max_content_length() -> int:
        """Get maximum request body size in bytes"""
        # Default: 10MB
        return int(os.environ.get('MAX_CONTENT_LENGTH', 10 * 1024 * 1024))
    
    @staticmethod
    def get_cors_origins() -> list:
        """Get CORS allowed origins"""
        origins = os.environ.get('CORS_ORIGINS', '')
        if not origins:
            return ['*'] if os.environ.get('FLASK_ENV') != 'production' else []
        return [origin.strip() for origin in origins.split(',')]
    
    @staticmethod
    def get_rate_limit_enabled() -> bool:
        """Check if rate limiting is enabled"""
        return os.environ.get('RATE_LIMIT_ENABLED', 'true').lower() in ('true', '1', 'yes')
    
    @staticmethod
    def get_rate_limit_per_minute() -> int:
        """Get rate limit per minute"""
        return int(os.environ.get('RATE_LIMIT_PER_MINUTE', 100))
    
    @staticmethod
    def require_https() -> bool:
        """Check if HTTPS is required"""
        return os.environ.get('REQUIRE_HTTPS', 'false').lower() in ('true', '1', 'yes')


class ValidationConfig:
    """Input validation configuration"""
    
    MAX_DESCRIPTION_LENGTH = 1000
    MAX_TARGET_LENGTH = 500
    MAX_CONTEXT_SIZE = 100  # Max number of context keys
    MAX_CONTEXT_VALUE_LENGTH = 1000
    MAX_PARAMETERS_SIZE = 100
    MAX_SIDE_EFFECTS = 50
    
    ALLOWED_INTENT_TYPES = {
        'READ', 'WRITE', 'DELETE', 'EXECUTE', 'NETWORK', 'SYSTEM', 'USER_INTERACTION'
    }
    
    ALLOWED_RISK_LEVELS = {
        'SAFE', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    }
    
    ALLOWED_VERIFICATION_LEVELS = {
        'NONE', 'BASIC', 'STANDARD', 'COMPREHENSIVE', 'PARANOID'
    }
