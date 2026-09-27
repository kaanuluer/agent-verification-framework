"""
Agent Verification Framework - Middleware
"""

from flask import request, g
import time
import logging

logger = logging.getLogger(__name__)


def setup_middleware(app):
    """Setup Flask middleware"""
    
    @app.before_request
    def before_request():
        """Before request handler"""
        g.start_time = time.time()
        g.request_id = request.headers.get('X-Request-ID', f"req-{int(time.time() * 1000)}")
    
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
