"""
Agent Verification Framework - REST API Server
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any, Optional
import uuid
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.core import (
    VerificationFramework,
    VerificationLevel,
    Intent,
    IntentType,
    Action,
    RiskLevel
)
from .auth import AuthManager, require_auth
from .middleware import setup_middleware
from .config import SecurityConfig, ValidationConfig
from .validators import validate_intent_request, validate_action_request
from .models import (
    IntentRequest,
    ActionRequest,
    VerificationResponse,
    ErrorResponse
)


# Global session storage (in production, use Redis or database)
verification_sessions: Dict[str, VerificationFramework] = {}


def create_app(config: Optional[Dict[str, Any]] = None) -> Flask:
    """Create and configure the Flask application"""
    
    app = Flask(__name__)
    
    # Security Configuration
    app.config['JSON_SORT_KEYS'] = False
    app.config['SECRET_KEY'] = SecurityConfig.get_secret_key()
    app.config['MAX_CONTENT_LENGTH'] = SecurityConfig.get_max_content_length()
    
    # Security headers
    app.config['SESSION_COOKIE_SECURE'] = SecurityConfig.require_https()
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    if config:
        app.config.update(config)
    
    # Enable CORS with proper origins
    cors_origins = SecurityConfig.get_cors_origins()
    CORS(app, resources={
        r"/api/*": {
            "origins": cors_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-API-Key"],
            "max_age": 3600
        }
    })
    
    # Setup middleware
    setup_middleware(app)
    
    # Initialize auth manager
    auth_manager = AuthManager(app)
    
    return app


app = create_app()


# ============================================================================
# Utility Functions
# ============================================================================

def get_or_create_session(
    session_id: Optional[str] = None,
    level: str = "STANDARD",
    config: Optional[Dict[str, Any]] = None
) -> tuple[str, VerificationFramework]:
    """Get existing session or create new one"""
    
    if session_id and session_id in verification_sessions:
        return session_id, verification_sessions[session_id]
    
    # Create new session
    new_session_id = session_id or str(uuid.uuid4())
    
    # Parse verification level
    try:
        verification_level = VerificationLevel[level.upper()]
    except KeyError:
        verification_level = VerificationLevel.STANDARD
    
    # Create framework instance
    framework = VerificationFramework(
        level=verification_level,
        config=config or {}
    )
    
    verification_sessions[new_session_id] = framework
    
    return new_session_id, framework


def parse_intent_type(intent_type: str) -> IntentType:
    """Parse intent type from string"""
    try:
        return IntentType[intent_type.upper()]
    except KeyError:
        return IntentType.EXECUTE


def parse_risk_level(risk_level: str) -> RiskLevel:
    """Parse risk level from string"""
    try:
        return RiskLevel[risk_level.upper()]
    except KeyError:
        return RiskLevel.MEDIUM


# ============================================================================
# Health Check
# ============================================================================

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'agent-verification-framework',
        'version': '0.2.0',
        'timestamp': datetime.utcnow().isoformat(),
        'active_sessions': len(verification_sessions)
    }), 200


# ============================================================================
# Session Management
# ============================================================================

@app.route('/api/v1/sessions', methods=['POST'])
@require_auth
def create_session():
    """Create a new verification session"""
    
    data = request.get_json() or {}
    
    level = data.get('level', 'STANDARD')
    config = data.get('config', {})
    
    session_id, framework = get_or_create_session(level=level, config=config)
    
    return jsonify({
        'session_id': session_id,
        'level': framework.level.name,
        'created_at': datetime.utcnow().isoformat(),
        'config': framework.config
    }), 201


@app.route('/api/v1/sessions/<session_id>', methods=['GET'])
@require_auth
def get_session(session_id: str):
    """Get session information"""
    
    if session_id not in verification_sessions:
        return jsonify({
            'error': 'Session not found',
            'session_id': session_id
        }), 404
    
    framework = verification_sessions[session_id]
    report = framework.get_report()
    
    return jsonify({
        'session_id': session_id,
        'level': framework.level.name,
        'report': report
    }), 200


@app.route('/api/v1/sessions/<session_id>', methods=['DELETE'])
@require_auth
def delete_session(session_id: str):
    """Delete a verification session"""
    
    if session_id not in verification_sessions:
        return jsonify({
            'error': 'Session not found',
            'session_id': session_id
        }), 404
    
    del verification_sessions[session_id]
    
    return jsonify({
        'message': 'Session deleted',
        'session_id': session_id
    }), 200


@app.route('/api/v1/sessions', methods=['GET'])
@require_auth
def list_sessions():
    """List all active sessions"""
    
    sessions = []
    for session_id, framework in verification_sessions.items():
        report = framework.get_report()
        sessions.append({
            'session_id': session_id,
            'level': framework.level.name,
            'total_actions': report['total_actions'],
            'success_rate': report['success_rate']
        })
    
    return jsonify({
        'sessions': sessions,
        'total': len(sessions)
    }), 200


# ============================================================================
# Intent Verification
# ============================================================================

@app.route('/api/v1/verify/intent', methods=['POST'])
@require_auth
def verify_intent():
    """Verify an intent"""
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    # Validate input
    validation_errors = validate_intent_request(data)
    if validation_errors:
        return jsonify({
            'error': 'Validation failed',
            'details': validation_errors
        }), 400
    
    # Get or create session
    session_id = data.get('session_id')
    level = data.get('level', 'STANDARD')
    config = data.get('config', {})
    
    session_id, framework = get_or_create_session(session_id, level, config)
    
    # Parse intent
    try:
        intent = Intent(
            type=parse_intent_type(data.get('type', 'EXECUTE')),
            description=data.get('description', ''),
            target=data.get('target'),
            expected_outcome=data.get('expected_outcome'),
            risk_level=parse_risk_level(data.get('risk_level', 'MEDIUM')),
            context=data.get('context', {})
        )
    except Exception as e:
        return jsonify({
            'error': 'Invalid intent data',
            'details': str(e)
        }), 400
    
    # Verify intent
    is_valid, warnings = framework.verify_intent(intent)
    
    return jsonify({
        'session_id': session_id,
        'intent_id': intent.id,
        'valid': is_valid,
        'warnings': warnings,
        'intent': {
            'type': intent.type.value,
            'description': intent.description,
            'risk_level': intent.risk_level.value,
            'requires_approval': intent.requires_approval
        }
    }), 200


# ============================================================================
# Action Verification
# ============================================================================

@app.route('/api/v1/verify/action', methods=['POST'])
@require_auth
def verify_action():
    """Verify an action"""
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    # Validate input
    validation_errors = validate_action_request(data)
    if validation_errors:
        return jsonify({
            'error': 'Validation failed',
            'details': validation_errors
        }), 400
    
    session_id = data.get('session_id')
    
    if not session_id or session_id not in verification_sessions:
        return jsonify({
            'error': 'Invalid or missing session_id',
            'message': 'Create a session first or provide valid session_id'
        }), 400
    
    framework = verification_sessions[session_id]
    
    # Parse intent
    intent_data = data.get('intent', {})
    try:
        intent = Intent(
            type=parse_intent_type(intent_data.get('type', 'EXECUTE')),
            description=intent_data.get('description', ''),
            target=intent_data.get('target'),
            expected_outcome=intent_data.get('expected_outcome'),
            risk_level=parse_risk_level(intent_data.get('risk_level', 'MEDIUM')),
            context=intent_data.get('context', {})
        )
    except Exception as e:
        return jsonify({
            'error': 'Invalid intent data',
            'details': str(e)
        }), 400
    
    # Parse action
    action_data = data.get('action', {})
    try:
        action = Action(
            intent_id=intent.id,
            type=action_data.get('type', ''),
            description=action_data.get('description', ''),
            parameters=action_data.get('parameters', {}),
            result=action_data.get('result'),
            success=action_data.get('success', True),
            error=action_data.get('error'),
            duration_ms=action_data.get('duration_ms'),
            side_effects=action_data.get('side_effects', [])
        )
    except Exception as e:
        return jsonify({
            'error': 'Invalid action data',
            'details': str(e)
        }), 400
    
    # Verify action
    result = framework.verify_action(intent, action)
    
    return jsonify({
        'session_id': session_id,
        'intent_id': result.intent_id,
        'action_id': result.action_id,
        'verified': result.verified,
        'alignment_score': result.alignment_score,
        'risk_assessment': result.risk_assessment.value,
        'security_violations': result.security_violations,
        'behavior_anomalies': result.behavior_anomalies,
        'recommendations': result.recommendations,
        'timestamp': result.timestamp.isoformat()
    }), 200


# ============================================================================
# Reporting
# ============================================================================

@app.route('/api/v1/reports/<session_id>', methods=['GET'])
@require_auth
def get_report(session_id: str):
    """Get verification report for a session"""
    
    if session_id not in verification_sessions:
        return jsonify({
            'error': 'Session not found',
            'session_id': session_id
        }), 404
    
    framework = verification_sessions[session_id]
    report = framework.get_report()
    
    return jsonify({
        'session_id': session_id,
        'report': report
    }), 200


@app.route('/api/v1/reports/<session_id>/actions', methods=['GET'])
@require_auth
def get_actions(session_id: str):
    """Get all actions for a session"""
    
    if session_id not in verification_sessions:
        return jsonify({
            'error': 'Session not found',
            'session_id': session_id
        }), 404
    
    framework = verification_sessions[session_id]
    
    # Get query parameters
    limit = request.args.get('limit', type=int, default=10)
    offset = request.args.get('offset', type=int, default=0)
    
    actions = framework.action_tracker.actions[offset:offset + limit]
    
    return jsonify({
        'session_id': session_id,
        'actions': [action.to_dict() for action in actions],
        'total': len(framework.action_tracker.actions),
        'limit': limit,
        'offset': offset
    }), 200


@app.route('/api/v1/reports/<session_id>/audit', methods=['GET'])
@require_auth
def get_audit_logs(session_id: str):
    """Get audit logs for a session"""
    
    if session_id not in verification_sessions:
        return jsonify({
            'error': 'Session not found',
            'session_id': session_id
        }), 404
    
    framework = verification_sessions[session_id]
    
    # Get query parameters
    limit = request.args.get('limit', type=int, default=10)
    offset = request.args.get('offset', type=int, default=0)
    
    logs = framework.audit_logger.logs[offset:offset + limit]
    
    return jsonify({
        'session_id': session_id,
        'logs': logs,
        'total': len(framework.audit_logger.logs),
        'limit': limit,
        'offset': offset,
        'integrity_verified': framework.audit_logger.verify_integrity()
    }), 200


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'error': 'Bad Request',
        'message': str(error)
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'error': 'Unauthorized',
        'message': 'Invalid or missing API key'
    }), 401


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': str(error)
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred'
    }), 500


# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Agent Verification Framework API Server')
    parser.add_argument('--host', default=None, help='Host to bind to (default: from env or 127.0.0.1)')
    parser.add_argument('--port', type=int, default=None, help='Port to bind to (default: from env or 5000)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode (development only)')
    
    args = parser.parse_args()
    
    # Get configuration from environment or args
    host = args.host or SecurityConfig.get_host()
    port = args.port or SecurityConfig.get_port()
    debug = args.debug or SecurityConfig.is_debug()
    
    # Security warning for 0.0.0.0 binding
    if host == '0.0.0.0':
        print("⚠️  WARNING: Binding to 0.0.0.0 (all interfaces)")
        print("   This should only be used in development or behind a firewall")
        print("   Set HOST=127.0.0.1 environment variable for localhost only\n")
    
    # Security warning for debug mode
    if debug:
        print("⚠️  WARNING: Debug mode is enabled")
        print("   This should NEVER be used in production\n")
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║  Agent Verification Framework API Server                 ║
    ║  Version: 0.2.0                                          ║
    ║  Host: {host:48s} ║
    ║  Port: {port:48d} ║
    ║  Debug: {str(debug):46s} ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    app.run(host=host, port=port, debug=debug)
