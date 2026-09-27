"""
Agent Verification Framework - Unit Tests
"""

import pytest
from datetime import datetime
from src.core.verification_framework import (
    VerificationFramework,
    VerificationLevel,
    Intent,
    IntentType,
    Action,
    RiskLevel,
    IntentValidator,
    ActionTracker,
    BehaviorAnalyzer,
    SecurityGuard,
    AuditLogger
)


class TestIntent:
    """Intent class testleri"""
    
    def test_intent_creation(self):
        intent = Intent(
            type=IntentType.READ,
            description="Test intent",
            target="test_file.txt",
            risk_level=RiskLevel.LOW
        )
        
        assert intent.type == IntentType.READ
        assert intent.description == "Test intent"
        assert intent.target == "test_file.txt"
        assert intent.risk_level == RiskLevel.LOW
        assert intent.id is not None
    
    def test_intent_to_dict(self):
        intent = Intent(
            type=IntentType.WRITE,
            description="Write test",
            risk_level=RiskLevel.MEDIUM
        )
        
        data = intent.to_dict()
        
        assert data['type'] == 'write'
        assert data['description'] == 'Write test'
        assert data['risk_level'] == 'medium'
        assert 'id' in data
        assert 'timestamp' in data


class TestAction:
    """Action class testleri"""
    
    def test_action_creation(self):
        action = Action(
            type="file_read",
            description="Read file",
            success=True
        )
        
        assert action.type == "file_read"
        assert action.description == "Read file"
        assert action.success is True
        assert action.id is not None
    
    def test_action_with_error(self):
        action = Action(
            type="file_write",
            description="Write file",
            success=False,
            error="Permission denied"
        )
        
        assert action.success is False
        assert action.error == "Permission denied"
    
    def test_action_to_dict(self):
        action = Action(
            type="test_action",
            description="Test",
            parameters={'key': 'value'},
            success=True
        )
        
        data = action.to_dict()
        
        assert data['type'] == "test_action"
        assert data['parameters'] == {'key': 'value'}
        assert data['success'] is True


class TestIntentValidator:
    """IntentValidator testleri"""
    
    def test_validate_safe_intent(self):
        validator = IntentValidator({})
        intent = Intent(
            type=IntentType.READ,
            description="Read safe file",
            risk_level=RiskLevel.SAFE
        )
        
        is_valid, warnings = validator.validate(intent)
        
        assert is_valid is True
        assert len(warnings) == 0
    
    def test_validate_critical_intent(self):
        validator = IntentValidator({'require_approval_for_critical': True})
        intent = Intent(
            type=IntentType.SYSTEM,
            description="System operation",
            risk_level=RiskLevel.CRITICAL
        )
        
        is_valid, warnings = validator.validate(intent)
        
        assert intent.requires_approval is True
        assert any('approval' in w.lower() for w in warnings)
    
    def test_validate_empty_description(self):
        validator = IntentValidator({})
        intent = Intent(
            type=IntentType.READ,
            description="",
            risk_level=RiskLevel.LOW
        )
        
        is_valid, warnings = validator.validate(intent)
        
        assert any('description' in w.lower() for w in warnings)


class TestActionTracker:
    """ActionTracker testleri"""
    
    def test_track_action(self):
        tracker = ActionTracker({})
        action = Action(
            type="test",
            description="Test action",
            success=True
        )
        
        tracker.track(action)
        
        assert len(tracker.actions) == 1
        assert tracker.actions[0] == action
    
    def test_track_multiple_actions(self):
        tracker = ActionTracker({})
        
        for i in range(5):
            action = Action(
                type=f"action_{i}",
                description=f"Action {i}",
                success=True
            )
            tracker.track(action)
        
        assert len(tracker.actions) == 5
    
    def test_get_actions_for_intent(self):
        tracker = ActionTracker({})
        intent_id = "test_intent_123"
        
        # Add actions for specific intent
        for i in range(3):
            action = Action(
                intent_id=intent_id,
                type=f"action_{i}",
                description=f"Action {i}",
                success=True
            )
            tracker.track(action)
        
        # Add action for different intent
        other_action = Action(
            intent_id="other_intent",
            type="other",
            description="Other action",
            success=True
        )
        tracker.track(other_action)
        
        intent_actions = tracker.get_actions_for_intent(intent_id)
        
        assert len(intent_actions) == 3
        assert all(a.intent_id == intent_id for a in intent_actions)
    
    def test_get_recent_actions(self):
        tracker = ActionTracker({})
        
        for i in range(20):
            action = Action(
                type=f"action_{i}",
                description=f"Action {i}",
                success=True
            )
            tracker.track(action)
        
        recent = tracker.get_recent_actions(5)
        
        assert len(recent) == 5
        assert recent[-1].type == "action_19"


class TestBehaviorAnalyzer:
    """BehaviorAnalyzer testleri"""
    
    def test_analyze_alignment_perfect(self):
        analyzer = BehaviorAnalyzer({})
        
        intent = Intent(
            type=IntentType.WRITE,
            description="Write to file",
            target="test.txt",
            risk_level=RiskLevel.LOW
        )
        
        action = Action(
            intent_id=intent.id,
            type="file_write",
            description="Writing to file",
            parameters={'target': 'test.txt'},
            success=True
        )
        
        score = analyzer.analyze_alignment(intent, action)
        
        assert score >= 0.8
    
    def test_analyze_alignment_mismatch(self):
        analyzer = BehaviorAnalyzer({})
        
        intent = Intent(
            type=IntentType.WRITE,
            description="Write to file",
            target="test.txt",
            risk_level=RiskLevel.LOW
        )
        
        action = Action(
            intent_id=intent.id,
            type="database_read",  # Mismatch!
            description="Reading from database",
            parameters={'target': 'different.txt'},  # Different target!
            success=True
        )
        
        score = analyzer.analyze_alignment(intent, action)
        
        assert score < 0.7
    
    def test_detect_anomalies_high_frequency(self):
        analyzer = BehaviorAnalyzer({})
        
        # Create history with many similar actions
        history = []
        for i in range(10):
            action = Action(
                type="repeated_action",
                description=f"Action {i}",
                success=True
            )
            history.append(action)
        
        new_action = Action(
            type="repeated_action",
            description="Another one",
            success=True
        )
        
        anomalies = analyzer.detect_anomalies(new_action, history)
        
        assert len(anomalies) > 0
        assert any('frequency' in a.lower() for a in anomalies)


class TestSecurityGuard:
    """SecurityGuard testleri"""
    
    def test_blacklist_check(self):
        guard = SecurityGuard({
            'blacklist': ['/etc/passwd', '/system']
        })
        
        intent = Intent(
            type=IntentType.READ,
            description="Read system file",
            target="/etc/passwd",
            risk_level=RiskLevel.HIGH
        )
        
        action = Action(
            intent_id=intent.id,
            type="file_read",
            description="Reading file",
            success=False
        )
        
        violations = guard.check(intent, action)
        
        assert len(violations) > 0
        assert any('blacklist' in v.lower() for v in violations)
    
    def test_whitelist_check(self):
        guard = SecurityGuard({
            'whitelist': ['allowed_file.txt']
        })
        
        intent = Intent(
            type=IntentType.READ,
            description="Read file",
            target="not_allowed.txt",
            risk_level=RiskLevel.LOW
        )
        
        action = Action(
            intent_id=intent.id,
            type="file_read",
            description="Reading file",
            success=True
        )
        
        violations = guard.check(intent, action)
        
        assert len(violations) > 0
        assert any('whitelist' in v.lower() for v in violations)
    
    def test_delete_prevention(self):
        guard = SecurityGuard({
            'allow_delete': False
        })
        
        intent = Intent(
            type=IntentType.DELETE,
            description="Delete file",
            target="file.txt",
            risk_level=RiskLevel.HIGH
        )
        
        action = Action(
            intent_id=intent.id,
            type="file_delete",
            description="Deleting file",
            success=False
        )
        
        violations = guard.check(intent, action)
        
        assert len(violations) > 0
        assert any('delete' in v.lower() for v in violations)


class TestAuditLogger:
    """AuditLogger testleri"""
    
    def test_log_intent(self):
        logger = AuditLogger({})
        intent = Intent(
            type=IntentType.READ,
            description="Test intent",
            risk_level=RiskLevel.LOW
        )
        
        logger.log_intent(intent)
        
        assert len(logger.logs) == 1
        assert logger.logs[0]['type'] == 'intent'
        assert 'hash' in logger.logs[0]
    
    def test_log_action(self):
        logger = AuditLogger({})
        action = Action(
            type="test",
            description="Test action",
            success=True
        )
        
        logger.log_action(action)
        
        assert len(logger.logs) == 1
        assert logger.logs[0]['type'] == 'action'
    
    def test_verify_integrity(self):
        logger = AuditLogger({})
        
        intent = Intent(
            type=IntentType.READ,
            description="Test",
            risk_level=RiskLevel.LOW
        )
        logger.log_intent(intent)
        
        action = Action(
            type="test",
            description="Test",
            success=True
        )
        logger.log_action(action)
        
        # Integrity should be valid
        assert logger.verify_integrity() is True
    
    def test_detect_tampering(self):
        logger = AuditLogger({})
        
        intent = Intent(
            type=IntentType.READ,
            description="Test",
            risk_level=RiskLevel.LOW
        )
        logger.log_intent(intent)
        
        # Tamper with log
        logger.logs[0]['data']['description'] = "Modified!"
        
        # Integrity check should fail
        assert logger.verify_integrity() is False


class TestVerificationFramework:
    """VerificationFramework integration testleri"""
    
    def test_framework_creation(self):
        framework = VerificationFramework(
            level=VerificationLevel.STANDARD
        )
        
        assert framework.level == VerificationLevel.STANDARD
        assert framework.intent_validator is not None
        assert framework.action_tracker is not None
    
    def test_verify_intent(self):
        framework = VerificationFramework(level=VerificationLevel.STANDARD)
        
        intent = Intent(
            type=IntentType.READ,
            description="Read file",
            risk_level=RiskLevel.LOW
        )
        
        is_valid, warnings = framework.verify_intent(intent)
        
        assert is_valid is True
    
    def test_verify_action(self):
        framework = VerificationFramework(level=VerificationLevel.STANDARD)
        
        intent = Intent(
            type=IntentType.READ,
            description="Read file",
            risk_level=RiskLevel.LOW
        )
        
        action = Action(
            intent_id=intent.id,
            type="file_read",
            description="Reading file",
            success=True
        )
        
        result = framework.verify_action(intent, action)
        
        assert result.intent_id == intent.id
        assert result.action_id == action.id
        assert isinstance(result.alignment_score, float)
        assert 0.0 <= result.alignment_score <= 1.0
    
    def test_verification_level_none(self):
        framework = VerificationFramework(level=VerificationLevel.NONE)
        
        intent = Intent(
            type=IntentType.DELETE,
            description="Delete everything",
            risk_level=RiskLevel.CRITICAL
        )
        
        action = Action(
            intent_id=intent.id,
            type="mass_delete",
            description="Deleting",
            success=True
        )
        
        result = framework.verify_action(intent, action)
        
        # Should pass with no verification
        assert result.verified is True
        assert result.alignment_score == 1.0
    
    def test_get_report(self):
        framework = VerificationFramework(level=VerificationLevel.STANDARD)
        
        # Perform some operations
        intent = Intent(
            type=IntentType.READ,
            description="Test",
            risk_level=RiskLevel.LOW
        )
        
        action = Action(
            intent_id=intent.id,
            type="test",
            description="Test",
            success=True
        )
        
        framework.verify_action(intent, action)
        
        report = framework.get_report()
        
        assert 'total_actions' in report
        assert 'successful_actions' in report
        assert 'success_rate' in report
        assert report['total_actions'] == 1
        assert report['successful_actions'] == 1


class TestVerifiedAgent:
    """VerifiedAgent testleri"""
    
    class DummyAgent:
        def execute(self, task: str, **kwargs):
            return f"Executed: {task}"
    
    def test_wrap_agent(self):
        framework = VerificationFramework(level=VerificationLevel.BASIC)
        agent = self.DummyAgent()
        
        verified_agent = framework.wrap(agent)
        
        assert verified_agent.agent == agent
        assert verified_agent.framework == framework
    
    def test_execute_verified(self):
        framework = VerificationFramework(level=VerificationLevel.STANDARD)
        agent = self.DummyAgent()
        
        verified_agent = framework.wrap(agent)
        
        result = verified_agent.execute(
            "Test task",
            intent_type=IntentType.READ,
            risk_level=RiskLevel.LOW
        )
        
        assert "Executed: Test task" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
