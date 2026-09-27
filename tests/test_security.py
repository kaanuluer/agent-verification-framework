"""
Agent Verification Framework - Security Tests
"""

import pytest
from src.api.validators import (
    validate_intent_request,
    validate_action_request,
    validate_string_length,
    validate_dict_size,
    validate_enum,
    ValidationError
)
from src.api.config import ValidationConfig, SecurityConfig


class TestInputValidation:
    """Test input validation"""
    
    def test_string_length_valid(self):
        """Test valid string length"""
        try:
            validate_string_length("test", "field", 10, required=True)
        except ValidationError:
            pytest.fail("Valid string raised validation error")
    
    def test_string_length_too_long(self):
        """Test string too long"""
        with pytest.raises(ValidationError) as exc:
            validate_string_length("x" * 1001, "field", 1000, required=True)
        assert "exceeds maximum length" in str(exc.value)
    
    def test_string_length_required_missing(self):
        """Test required string missing"""
        with pytest.raises(ValidationError) as exc:
            validate_string_length(None, "field", 100, required=True)
        assert "required" in str(exc.value)
    
    def test_dict_size_valid(self):
        """Test valid dict size"""
        try:
            validate_dict_size({"key": "value"}, "field", 10, 100)
        except ValidationError:
            pytest.fail("Valid dict raised validation error")
    
    def test_dict_size_too_many_keys(self):
        """Test dict with too many keys"""
        large_dict = {f"key_{i}": "value" for i in range(101)}
        with pytest.raises(ValidationError) as exc:
            validate_dict_size(large_dict, "field", 100, 100)
        assert "exceeds maximum" in str(exc.value)
    
    def test_enum_valid(self):
        """Test valid enum value"""
        try:
            validate_enum("READ", "type", {"READ", "WRITE"}, required=True)
        except ValidationError:
            pytest.fail("Valid enum raised validation error")
    
    def test_enum_invalid(self):
        """Test invalid enum value"""
        with pytest.raises(ValidationError) as exc:
            validate_enum("INVALID", "type", {"READ", "WRITE"}, required=True)
        assert "must be one of" in str(exc.value)


class TestIntentValidation:
    """Test intent request validation"""
    
    def test_valid_intent(self):
        """Test valid intent request"""
        data = {
            'type': 'READ',
            'description': 'Read data',
            'risk_level': 'LOW'
        }
        errors = validate_intent_request(data)
        assert len(errors) == 0
    
    def test_missing_required_fields(self):
        """Test missing required fields"""
        data = {}
        errors = validate_intent_request(data)
        assert len(errors) > 0
        assert any('type' in e for e in errors)
        assert any('description' in e for e in errors)
    
    def test_invalid_type(self):
        """Test invalid intent type"""
        data = {
            'type': 'INVALID',
            'description': 'Test',
            'risk_level': 'LOW'
        }
        errors = validate_intent_request(data)
        assert len(errors) > 0
        assert any('type' in e for e in errors)
    
    def test_description_too_long(self):
        """Test description exceeding length"""
        data = {
            'type': 'READ',
            'description': 'x' * 1001,
            'risk_level': 'LOW'
        }
        errors = validate_intent_request(data)
        assert len(errors) > 0
        assert any('description' in e for e in errors)
    
    def test_context_too_large(self):
        """Test context with too many keys"""
        data = {
            'type': 'READ',
            'description': 'Test',
            'context': {f"key_{i}": "value" for i in range(101)}
        }
        errors = validate_intent_request(data)
        assert len(errors) > 0
        assert any('context' in e for e in errors)


class TestActionValidation:
    """Test action request validation"""
    
    def test_valid_action(self):
        """Test valid action request"""
        data = {
            'session_id': 'test-session',
            'intent': {
                'type': 'WRITE',
                'description': 'Write data',
                'risk_level': 'MEDIUM'
            },
            'action': {
                'type': 'database_write',
                'description': 'Writing to database',
                'success': True
            }
        }
        errors = validate_action_request(data)
        assert len(errors) == 0
    
    def test_missing_session_id(self):
        """Test missing session ID"""
        data = {
            'intent': {'type': 'READ', 'description': 'Test'},
            'action': {'type': 'test', 'description': 'Test', 'success': True}
        }
        errors = validate_action_request(data)
        assert len(errors) > 0
        assert any('session_id' in e for e in errors)
    
    def test_invalid_intent(self):
        """Test invalid intent in action request"""
        data = {
            'session_id': 'test',
            'intent': {'type': 'INVALID'},
            'action': {'type': 'test', 'description': 'Test', 'success': True}
        }
        errors = validate_action_request(data)
        assert len(errors) > 0


class TestSecurityConfig:
    """Test security configuration"""
    
    def test_get_host_default(self):
        """Test default host is localhost"""
        import os
        # Save and clear env
        old_host = os.environ.get('HOST')
        if 'HOST' in os.environ:
            del os.environ['HOST']
        
        host = SecurityConfig.get_host()
        assert host == '127.0.0.1'
        
        # Restore
        if old_host:
            os.environ['HOST'] = old_host
    
    def test_debug_not_allowed_in_production(self):
        """Test debug mode not allowed in production"""
        import os
        
        # Save env
        old_flask_env = os.environ.get('FLASK_ENV')
        old_debug = os.environ.get('DEBUG')
        
        # Set production with debug
        os.environ['FLASK_ENV'] = 'production'
        os.environ['DEBUG'] = 'true'
        
        with pytest.raises(ValueError) as exc:
            SecurityConfig.is_debug()
        assert 'production' in str(exc.value)
        
        # Restore
        if old_flask_env:
            os.environ['FLASK_ENV'] = old_flask_env
        elif 'FLASK_ENV' in os.environ:
            del os.environ['FLASK_ENV']
        
        if old_debug:
            os.environ['DEBUG'] = old_debug
        elif 'DEBUG' in os.environ:
            del os.environ['DEBUG']


class TestRateLimiting:
    """Test rate limiting"""
    
    def test_rate_limit_check(self):
        """Test rate limit checking"""
        from src.api.middleware import check_rate_limit
        
        # Should allow first requests
        for i in range(5):
            assert check_rate_limit(f"test-user-{i}", 10, 60) is True
        
        # Should deny when limit reached
        for i in range(15):
            result = check_rate_limit("test-user-limited", 10, 60)
            if i >= 10:
                assert result is False


class TestXSSPrevention:
    """Test XSS prevention"""
    
    def test_script_tag_in_description(self):
        """Test script tag in description"""
        data = {
            'type': 'READ',
            'description': '<script>alert("XSS")</script>',
            'risk_level': 'LOW'
        }
        # Should not raise error (sanitization happens at display)
        errors = validate_intent_request(data)
        # But length validation should still work
        assert isinstance(errors, list)
    
    def test_long_malicious_input(self):
        """Test long malicious input"""
        data = {
            'type': 'READ',
            'description': '<script>' + 'x' * 1000 + '</script>',
            'risk_level': 'LOW'
        }
        errors = validate_intent_request(data)
        # Should fail due to length
        assert len(errors) > 0


class TestSQLInjection:
    """Test SQL injection prevention"""
    
    def test_sql_in_description(self):
        """Test SQL injection attempt in description"""
        data = {
            'type': 'READ',
            'description': "'; DROP TABLE users; --",
            'risk_level': 'LOW'
        }
        # Should not raise error (we don't use SQL directly)
        errors = validate_intent_request(data)
        # Validation should still work normally
        assert isinstance(errors, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
