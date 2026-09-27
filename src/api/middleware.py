"""
Agent Verification Framework - Middleware
"""

from flask import request, g, jsonify
import time
import logging
from collections import defaultdict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Simple in-memory rate limiting (use Redis in production)
rate_limit_storage = defaultdict(list)


def check_rate_limit(identifier: str, max_requests: int, window_seconds: int) -> bool:
    """Check if request is within rate limit"""
    now = datetime.utcnow()
    cutoff = now - timedelta(seconds=window_seconds)
    
    # Clean old requests
    rate_limit_storage[identifier] = [
        req_time for req_time in rate_limit_storage[identifier]
        if req_time > cutoff
    ]
    
    # Check limit
    if len(rate_limit_storage[identifier]) >= max_requests:
        return False
    
    # Add current request
    rate_limit_storage[identifier].append(now)
    return True


def setup_middleware(app):
    """Setup Flask middleware"""
    
    @app.before_request
    def before_request():
        """Before request handler"""
        g.start_time = time.time()
        g.request_id = request.headers.get('X-Request-ID', f"req-{int(time.time() * 1000)}")
        
        # Rate limiting (skip health check)
        if request.path != '/api/v1/health':
            # Use API key or IP as identifier
            identifier = request.headers.get('X-API-Key', request.remote_addr)
            
            # 100 requests per minute
            if not check_rate_limit(f"minute:{identifier}", 100, 60):
                return jsonify({
                    'error': 'Rate Limit Exceeded',
                    'message': 'Too many requests. Please try again later.',
                    'retry_after': 60
                }), 429
            
            # 1000 requests per hour
            if not check_rate_limit(f"hour:{identifier}", 1000, 3600):
                return jsonify({
                    'error': 'Rate Limit Exceeded',
                    'message': 'Hourly rate limit exceeded.',
                    'retry_after': 3600
                }), 429
    
    @app.after_request
    def after_request(response):
        """After request handler"""
        # Add request ID to response
        response.headers['X-Request-ID'] = g.get('request_id', 'unknown')
        
        # Calculate request duration
        if hasattr(g, 'start_time'):
            duration_ms = (time.time() - g.start_time) * 1000
            response.headers['X-Response-Time'] = f"{duration_ms:.2f}ms"
            
            # Log request
            logger.info(
                f"{request.method} {request.path} "
                f"- {response.status_code} "
                f"- {duration_ms:.2f}ms"
            )
        
        # Add security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        return response
    
    @app.teardown_request
    def teardown_request(exception=None):
        """Teardown request handler"""
        if exception:
            logger.error(f"Request error: {exception}")
