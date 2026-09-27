"""
Agent Verification Framework - Authentication Module
"""

from flask import request, jsonify
from functools import wraps
from typing import Optional, Dict, Any
import os
import hashlib
import secrets
import time


class AuthManager:
    """Manages API authentication"""
    
    def __init__(self, app=None):
        self.api_keys: Dict[str, Dict[str, Any]] = {}
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app"""
        self.app = app
        
        # Load API keys from environment or config
        default_key = os.environ.get('API_KEY', 'dev-api-key-change-in-production')
        self.add_api_key(default_key, 'default', 'admin')
    
    def generate_api_key(self) -> str:
        """Generate a new API key"""
        return secrets.token_urlsafe(32)
    
    def hash_api_key(self, api_key: str) -> str:
        """Hash an API key"""
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    def add_api_key(
        self, 
        api_key: str, 
        name: str, 
        role: str = 'user',
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add an API key"""
        key_hash = self.hash_api_key(api_key)
        self.api_keys[key_hash] = {
            'name': name,
            'role': role,
            'created_at': time.time(),
            'metadata': metadata or {}
        }
    
    def verify_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Verify an API key"""
        key_hash = self.hash_api_key(api_key)
        return self.api_keys.get(key_hash)
    
    def revoke_api_key(self, api_key: str) -> bool:
        """Revoke an API key"""
        key_hash = self.hash_api_key(api_key)
        if key_hash in self.api_keys:
            del self.api_keys[key_hash]
            return True
        return False


# Global auth manager instance
auth_manager = AuthManager()


def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get API key from header
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            # Try Authorization header
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                api_key = auth_header[7:]
        
        if not api_key:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'API key is required. Provide via X-API-Key header or Authorization: Bearer <key>'
            }), 401
        
        # Verify API key
        key_info = auth_manager.verify_api_key(api_key)
        
        if not key_info:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid API key'
            }), 401
        
        # Add key info to request context
        request.auth_info = key_info
        
        return f(*args, **kwargs)
    
    return decorated_function


def require_role(role: str):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(request, 'auth_info'):
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'Authentication required'
                }), 401
            
            user_role = request.auth_info.get('role')
            
            if user_role != role and user_role != 'admin':
                return jsonify({
                    'error': 'Forbidden',
                    'message': f'Role "{role}" required'
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
