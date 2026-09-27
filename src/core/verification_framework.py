"""
Agent Verification Framework - Core Implementation
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json
import hashlib
import uuid


class VerificationLevel(Enum):
    """Verification seviyelerini tanımlar"""
    NONE = 0
    BASIC = 1
    STANDARD = 2
    COMPREHENSIVE = 3
    PARANOID = 4


class IntentType(Enum):
    """Agent intent türleri"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"
    NETWORK = "network"
    SYSTEM = "system"
    USER_INTERACTION = "user_interaction"


class RiskLevel(Enum):
    """Risk seviyeleri"""
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Intent:
    """Agent'ın intent'ini temsil eder"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: IntentType = IntentType.READ
    description: str = ""
    target: Optional[str] = None
    expected_outcome: Optional[str] = None
    risk_level: RiskLevel = RiskLevel.SAFE
    requires_approval: bool = False
    timestamp: datetime = field(default_factory=datetime.utcnow)
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Intent'i dictionary'ye çevirir"""
        return {
            'id': self.id,
            'type': self.type.value,
            'description': self.description,
            'target': self.target,
            'expected_outcome': self.expected_outcome,
            'risk_level': self.risk_level.value,
            'requires_approval': self.requires_approval,
            'timestamp': self.timestamp.isoformat(),
            'context': self.context
        }


@dataclass
class Action:
    """Agent'ın gerçekleştirdiği bir aksiyonu temsil eder"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    intent_id: Optional[str] = None
    type: str = ""
    description: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    result: Optional[Any] = None
    success: bool = True
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    duration_ms: Optional[float] = None
    side_effects: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Action'ı dictionary'ye çevirir"""
        return {
            'id': self.id,
            'intent_id': self.intent_id,
            'type': self.type,
            'description': self.description,
            'parameters': self.parameters,
            'result': str(self.result) if self.result else None,
            'success': self.success,
            'error': self.error,
            'timestamp': self.timestamp.isoformat(),
            'duration_ms': self.duration_ms,
            'side_effects': self.side_effects
        }


@dataclass
class VerificationResult:
    """Verification sonucunu temsil eder"""
    intent_id: str
    action_id: str
    verified: bool
    alignment_score: float  # 0.0 - 1.0
    risk_assessment: RiskLevel
    security_violations: List[str] = field(default_factory=list)
    behavior_anomalies: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Verification result'ı dictionary'ye çevirir"""
        return {
            'intent_id': self.intent_id,
            'action_id': self.action_id,
            'verified': self.verified,
            'alignment_score': self.alignment_score,
            'risk_assessment': self.risk_assessment.value,
            'security_violations': self.security_violations,
            'behavior_anomalies': self.behavior_anomalies,
            'recommendations': self.recommendations,
            'timestamp': self.timestamp.isoformat()
        }


class IntentValidator:
    """Intent'leri validate eder"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.risk_rules = self._load_risk_rules()
    
    def _load_risk_rules(self) -> Dict[IntentType, RiskLevel]:
        """Default risk rules'ları yükler"""
        return {
            IntentType.READ: RiskLevel.SAFE,
            IntentType.WRITE: RiskLevel.MEDIUM,
            IntentType.DELETE: RiskLevel.HIGH,
            IntentType.EXECUTE: RiskLevel.HIGH,
            IntentType.NETWORK: RiskLevel.MEDIUM,
            IntentType.SYSTEM: RiskLevel.CRITICAL,
            IntentType.USER_INTERACTION: RiskLevel.LOW
        }
    
    def validate(self, intent: Intent) -> tuple[bool, List[str]]:
        """
        Intent'i validate eder
        Returns: (is_valid, warnings)
        """
        warnings = []
        
        # Basic validation
        if not intent.description:
            warnings.append("Intent description is empty")
        
        # Risk assessment
        base_risk = self.risk_rules.get(intent.type, RiskLevel.MEDIUM)
        if intent.risk_level.value < base_risk.value:
            warnings.append(f"Intent risk level ({intent.risk_level.value}) is lower than expected ({base_risk.value})")
        
        # Critical operation check
        if intent.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            if not intent.requires_approval and self.config.get('require_approval_for_critical', True):
                warnings.append("Critical intent requires approval")
                intent.requires_approval = True
        
        # Context validation
        if intent.type == IntentType.WRITE and 'backup_available' not in intent.context:
            warnings.append("Write operation without backup information")
        
        is_valid = len(warnings) == 0 or not self.config.get('strict_validation', False)
        
        return is_valid, warnings


class ActionTracker:
    """Action'ları track eder"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.actions: List[Action] = []
        self.action_chains: Dict[str, List[str]] = {}
    
    def track(self, action: Action) -> None:
        """Bir action'ı kaydeder"""
        self.actions.append(action)
        
        # Chain tracking
        if action.intent_id:
            if action.intent_id not in self.action_chains:
                self.action_chains[action.intent_id] = []
            self.action_chains[action.intent_id].append(action.id)
    
    def get_actions_for_intent(self, intent_id: str) -> List[Action]:
        """Bir intent için tüm action'ları döner"""
        return [a for a in self.actions if a.intent_id == intent_id]
    
    def get_recent_actions(self, count: int = 10) -> List[Action]:
        """En son action'ları döner"""
        return self.actions[-count:]


class BehaviorAnalyzer:
    """Agent davranışlarını analiz eder"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.patterns: Dict[str, int] = {}
    
    def analyze_alignment(self, intent: Intent, action: Action) -> float:
        """
        Intent-action alignment'ı analiz eder
        Returns: 0.0 - 1.0 arası alignment score
        """
        score = 1.0
        
        # Type matching
        if intent.type == IntentType.WRITE and 'write' not in action.type.lower():
            score -= 0.3
        
        # Target matching
        if intent.target and action.parameters.get('target') != intent.target:
            score -= 0.2
        
        # Success check
        if not action.success:
            score -= 0.4
        
        # Expected outcome check
        if intent.expected_outcome:
            # Bu kısımda outcome'ı AI ile karşılaştırabilirsiniz
            pass
        
        return max(0.0, score)
    
    def detect_anomalies(self, action: Action, history: List[Action]) -> List[str]:
        """Davranış anomalilerini tespit eder"""
        anomalies = []
        
        # Rate limiting check
        recent_similar = [
            a for a in history[-10:]
            if a.type == action.type and a.timestamp > datetime.utcnow()
        ]
        if len(recent_similar) > 5:
            anomalies.append(f"High frequency of {action.type} actions detected")
        
        # Unusual error rate
        recent_errors = [a for a in history[-20:] if not a.success]
        if len(recent_errors) > 5:
            anomalies.append("High error rate detected")
        
        # Side effect explosion
        if len(action.side_effects) > 10:
            anomalies.append(f"Excessive side effects detected: {len(action.side_effects)}")
        
        return anomalies


class SecurityGuard:
    """Güvenlik kontrolleri yapar"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.blacklist = config.get('blacklist', [])
        self.whitelist = config.get('whitelist', [])
    
    def check(self, intent: Intent, action: Action) -> List[str]:
        """Güvenlik kontrollerini yapar, violation'ları döner"""
        violations = []
        
        # Blacklist check
        if intent.target in self.blacklist:
            violations.append(f"Target is blacklisted: {intent.target}")
        
        # Whitelist check (if enabled)
        if self.whitelist and intent.target and intent.target not in self.whitelist:
            violations.append(f"Target is not whitelisted: {intent.target}")
        
        # Permission check
        if intent.type == IntentType.DELETE and not self.config.get('allow_delete', False):
            violations.append("Delete operations are not allowed")
        
        # Network security
        if intent.type == IntentType.NETWORK:
            domain = action.parameters.get('domain')
            if domain and not self._is_safe_domain(domain):
                violations.append(f"Unsafe network domain: {domain}")
        
        return violations
    
    def _is_safe_domain(self, domain: str) -> bool:
        """Domain'in güvenli olup olmadığını kontrol eder"""
        unsafe_domains = self.config.get('unsafe_domains', [])
        return domain not in unsafe_domains


class AuditLogger:
    """Immutable audit log'ları tutar"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logs: List[Dict[str, Any]] = []
    
    def log_intent(self, intent: Intent) -> None:
        """Intent'i loglar"""
        log_entry = {
            'type': 'intent',
            'data': intent.to_dict(),
            'hash': self._compute_hash(intent.to_dict())
        }
        self.logs.append(log_entry)
    
    def log_action(self, action: Action) -> None:
        """Action'ı loglar"""
        log_entry = {
            'type': 'action',
            'data': action.to_dict(),
            'hash': self._compute_hash(action.to_dict())
        }
        self.logs.append(log_entry)
    
    def log_verification(self, result: VerificationResult) -> None:
        """Verification result'ı loglar"""
        log_entry = {
            'type': 'verification',
            'data': result.to_dict(),
            'hash': self._compute_hash(result.to_dict())
        }
        self.logs.append(log_entry)
    
    def _compute_hash(self, data: Dict[str, Any]) -> str:
        """Data'nın hash'ini hesaplar"""
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()
    
    def export_logs(self, filepath: str) -> None:
        """Log'ları dosyaya export eder"""
        with open(filepath, 'w') as f:
            json.dump(self.logs, f, indent=2)
    
    def verify_integrity(self) -> bool:
        """Log integrity'sini doğrular"""
        for log in self.logs:
            expected_hash = self._compute_hash(log['data'])
            if log['hash'] != expected_hash:
                return False
        return True


class VerificationFramework:
    """Ana verification framework"""
    
    def __init__(
        self,
        level: VerificationLevel = VerificationLevel.STANDARD,
        config: Optional[Dict[str, Any]] = None
    ):
        self.level = level
        self.config = config or {}
        
        # Components
        self.intent_validator = IntentValidator(self.config)
        self.action_tracker = ActionTracker(self.config)
        self.behavior_analyzer = BehaviorAnalyzer(self.config)
        self.security_guard = SecurityGuard(self.config)
        self.audit_logger = AuditLogger(self.config)
        
        # Callbacks
        self.on_verification_complete: Optional[Callable] = None
        self.on_security_violation: Optional[Callable] = None
    
    def verify_intent(self, intent: Intent) -> tuple[bool, List[str]]:
        """Intent'i verify eder"""
        if self.level == VerificationLevel.NONE:
            return True, []
        
        # Log intent
        self.audit_logger.log_intent(intent)
        
        # Validate
        is_valid, warnings = self.intent_validator.validate(intent)
        
        return is_valid, warnings
    
    def verify_action(self, intent: Intent, action: Action) -> VerificationResult:
        """Action'ı verify eder ve result döner"""
        
        # Track action
        self.action_tracker.track(action)
        self.audit_logger.log_action(action)
        
        if self.level == VerificationLevel.NONE:
            result = VerificationResult(
                intent_id=intent.id,
                action_id=action.id,
                verified=True,
                alignment_score=1.0,
                risk_assessment=RiskLevel.SAFE
            )
            return result
        
        # Analyze alignment
        alignment_score = self.behavior_analyzer.analyze_alignment(intent, action)
        
        # Detect anomalies
        history = self.action_tracker.get_recent_actions(50)
        anomalies = self.behavior_analyzer.detect_anomalies(action, history)
        
        # Security check
        violations = self.security_guard.check(intent, action)
        
        # Build result
        result = VerificationResult(
            intent_id=intent.id,
            action_id=action.id,
            verified=len(violations) == 0 and alignment_score > 0.5,
            alignment_score=alignment_score,
            risk_assessment=intent.risk_level,
            security_violations=violations,
            behavior_anomalies=anomalies
        )
        
        # Add recommendations
        if alignment_score < 0.7:
            result.recommendations.append("Low alignment score - review intent-action matching")
        if anomalies:
            result.recommendations.append("Behavioral anomalies detected - investigate pattern")
        if violations:
            result.recommendations.append("Security violations found - immediate action required")
        
        # Log result
        self.audit_logger.log_verification(result)
        
        # Callbacks
        if self.on_verification_complete:
            self.on_verification_complete(result)
        
        if violations and self.on_security_violation:
            self.on_security_violation(result)
        
        return result
    
    def wrap(self, agent: Any) -> 'VerifiedAgent':
        """Agent'ı verification layer ile wrap eder"""
        return VerifiedAgent(agent, self)
    
    def get_report(self) -> Dict[str, Any]:
        """Verification raporu oluşturur"""
        total_actions = len(self.action_tracker.actions)
        successful_actions = len([a for a in self.action_tracker.actions if a.success])
        
        return {
            'framework_level': self.level.value,
            'total_actions': total_actions,
            'successful_actions': successful_actions,
            'success_rate': successful_actions / total_actions if total_actions > 0 else 0,
            'total_intents': len(self.action_tracker.action_chains),
            'log_integrity': self.audit_logger.verify_integrity(),
            'timestamp': datetime.utcnow().isoformat()
        }


class VerifiedAgent:
    """Verification ile wrap edilmiş agent"""
    
    def __init__(self, agent: Any, framework: VerificationFramework):
        self.agent = agent
        self.framework = framework
    
    def execute(self, task: str, **kwargs) -> Any:
        """Task'ı verified şekilde execute eder"""
        
        # Create intent
        intent = Intent(
            type=kwargs.get('intent_type', IntentType.EXECUTE),
            description=f"Execute task: {task}",
            target=kwargs.get('target'),
            expected_outcome=kwargs.get('expected_outcome'),
            risk_level=kwargs.get('risk_level', RiskLevel.MEDIUM),
            context=kwargs
        )
        
        # Verify intent
        is_valid, warnings = self.framework.verify_intent(intent)
        if not is_valid:
            raise ValueError(f"Invalid intent: {warnings}")
        
        # Execute
        start_time = datetime.utcnow()
        try:
            result = self.agent.execute(task, **kwargs)
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)
        
        duration = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        # Create action
        action = Action(
            intent_id=intent.id,
            type='execute',
            description=f"Executed: {task}",
            parameters={'task': task, **kwargs},
            result=result,
            success=success,
            error=error,
            duration_ms=duration
        )
        
        # Verify action
        verification = self.framework.verify_action(intent, action)
        
        if not verification.verified:
            print(f"⚠️  Verification failed: {verification.security_violations}")
        
        if not success:
            raise RuntimeError(f"Agent execution failed: {error}")
        
        return result
