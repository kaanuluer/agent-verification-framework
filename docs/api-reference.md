# Agent Verification Framework - API Reference

## 📚 Core API

### VerificationFramework

Ana framework sınıfı. Agent'ların verification işlemlerini yönetir.

#### Constructor

```python
VerificationFramework(
    level: VerificationLevel = VerificationLevel.STANDARD,
    config: Optional[Dict[str, Any]] = None
)
```

**Parameters:**
- `level`: Verification seviyesi (NONE, BASIC, STANDARD, COMPREHENSIVE, PARANOID)
- `config`: Framework konfigürasyon dictionary'si

**Example:**
```python
framework = VerificationFramework(
    level=VerificationLevel.STANDARD,
    config={
        'log_retention_days': 90,
        'require_approval_for_critical': True
    }
)
```

#### Methods

##### verify_intent()

```python
def verify_intent(self, intent: Intent) -> tuple[bool, List[str]]
```

Intent'i validate eder ve warning'leri döner.

**Parameters:**
- `intent`: Validate edilecek Intent objesi

**Returns:**
- `tuple[bool, List[str]]`: (is_valid, warnings)

**Example:**
```python
intent = Intent(
    type=IntentType.READ,
    description="Read user data",
    risk_level=RiskLevel.LOW
)
is_valid, warnings = framework.verify_intent(intent)
```

##### verify_action()

```python
def verify_action(self, intent: Intent, action: Action) -> VerificationResult
```

Action'ı verify eder ve detaylı sonuç döner.

**Parameters:**
- `intent`: İlişkili Intent objesi
- `action`: Verify edilecek Action objesi

**Returns:**
- `VerificationResult`: Verification sonuçları

**Example:**
```python
action = Action(
    intent_id=intent.id,
    type="database_read",
    description="SELECT * FROM users",
    success=True
)
result = framework.verify_action(intent, action)
```

##### wrap()

```python
def wrap(self, agent: Any) -> VerifiedAgent
```

Agent'ı verification layer ile wrap eder.

**Parameters:**
- `agent`: Wrap edilecek agent objesi

**Returns:**
- `VerifiedAgent`: Verified agent wrapper

**Example:**
```python
agent = MyAgent()
verified_agent = framework.wrap(agent)
```

##### get_report()

```python
def get_report(self) -> Dict[str, Any]
```

Framework'ün genel raporunu döner.

**Returns:**
- `Dict[str, Any]`: Metrikler ve istatistikler

**Example:**
```python
report = framework.get_report()
print(f"Success Rate: {report['success_rate']:.2%}")
```

#### Properties

```python
framework.intent_validator: IntentValidator
framework.action_tracker: ActionTracker
framework.behavior_analyzer: BehaviorAnalyzer
framework.security_guard: SecurityGuard
framework.audit_logger: AuditLogger
```

#### Callbacks

```python
framework.on_verification_complete: Optional[Callable]
framework.on_security_violation: Optional[Callable]
```

**Example:**
```python
def handle_violation(result: VerificationResult):
    print(f"ALERT: {result.security_violations}")

framework.on_security_violation = handle_violation
```

---

### Intent

Agent'ın ne yapmak istediğini temsil eder.

#### Constructor

```python
Intent(
    type: IntentType,
    description: str,
    target: Optional[str] = None,
    expected_outcome: Optional[str] = None,
    risk_level: RiskLevel = RiskLevel.SAFE,
    requires_approval: bool = False,
    context: Dict[str, Any] = {}
)
```

**Example:**
```python
intent = Intent(
    type=IntentType.WRITE,
    description="Update user profile",
    target="users/profile/123",
    expected_outcome="Profile updated successfully",
    risk_level=RiskLevel.MEDIUM,
    context={'user_id': 123, 'backup_available': True}
)
```

#### Properties

```python
intent.id: str                          # Unique ID (auto-generated)
intent.type: IntentType                 # Intent türü
intent.description: str                 # İnsan-okunabilir açıklama
intent.target: Optional[str]            # Hedef resource
intent.expected_outcome: Optional[str]  # Beklenen sonuç
intent.risk_level: RiskLevel           # Risk seviyesi
intent.requires_approval: bool          # Onay gereksinimi
intent.timestamp: datetime              # Oluşturulma zamanı
intent.context: Dict[str, Any]         # Ek context bilgisi
```

#### Methods

```python
def to_dict(self) -> Dict[str, Any]
```

Intent'i dictionary'ye serialize eder.

---

### Action

Agent'ın gerçekleştirdiği bir aksiyonu temsil eder.

#### Constructor

```python
Action(
    intent_id: Optional[str] = None,
    type: str = "",
    description: str = "",
    parameters: Dict[str, Any] = {},
    result: Optional[Any] = None,
    success: bool = True,
    error: Optional[str] = None,
    duration_ms: Optional[float] = None,
    side_effects: List[str] = []
)
```

**Example:**
```python
action = Action(
    intent_id=intent.id,
    type="database_update",
    description="UPDATE users SET name = 'John'",
    parameters={'table': 'users', 'user_id': 123},
    result={'rows_affected': 1},
    success=True,
    duration_ms=45.3,
    side_effects=['cache_invalidated', 'audit_log_created']
)
```

#### Properties

```python
action.id: str                          # Unique ID (auto-generated)
action.intent_id: Optional[str]         # İlişkili intent ID
action.type: str                        # Action türü
action.description: str                 # Açıklama
action.parameters: Dict[str, Any]       # Action parametreleri
action.result: Optional[Any]            # Action sonucu
action.success: bool                    # Başarı durumu
action.error: Optional[str]             # Hata mesajı (varsa)
action.timestamp: datetime              # Gerçekleşme zamanı
action.duration_ms: Optional[float]     # Süre (ms)
action.side_effects: List[str]         # Side effect'ler
```

#### Methods

```python
def to_dict(self) -> Dict[str, Any]
```

Action'ı dictionary'ye serialize eder.

---

### VerificationResult

Verification işleminin sonucunu temsil eder.

#### Constructor

```python
VerificationResult(
    intent_id: str,
    action_id: str,
    verified: bool,
    alignment_score: float,
    risk_assessment: RiskLevel,
    security_violations: List[str] = [],
    behavior_anomalies: List[str] = [],
    recommendations: List[str] = []
)
```

#### Properties

```python
result.intent_id: str                   # İlişkili intent ID
result.action_id: str                   # İlişkili action ID
result.verified: bool                   # Genel verification durumu
result.alignment_score: float           # 0.0-1.0 arası alignment skoru
result.risk_assessment: RiskLevel       # Risk değerlendirmesi
result.security_violations: List[str]   # Güvenlik ihlalleri
result.behavior_anomalies: List[str]    # Davranış anomalileri
result.recommendations: List[str]       # Öneriler
result.timestamp: datetime              # Verification zamanı
```

#### Methods

```python
def to_dict(self) -> Dict[str, Any]
```

Result'ı dictionary'ye serialize eder.

---

### VerifiedAgent

Verification layer ile wrap edilmiş agent.

#### Methods

##### execute()

```python
def execute(self, task: str, **kwargs) -> Any
```

Task'ı verified şekilde execute eder.

**Parameters:**
- `task`: Execute edilecek task
- `**kwargs`: Ek parametreler
  - `intent_type`: IntentType
  - `target`: str
  - `expected_outcome`: str
  - `risk_level`: RiskLevel
  - diğer custom parametreler

**Returns:**
- `Any`: Task'ın sonucu

**Raises:**
- `ValueError`: Invalid intent
- `RuntimeError`: Execution failure

**Example:**
```python
result = verified_agent.execute(
    "Process user data",
    intent_type=IntentType.READ,
    target="users.db",
    risk_level=RiskLevel.LOW
)
```

---

## 🎯 Enums

### VerificationLevel

```python
class VerificationLevel(Enum):
    NONE = 0           # Verification yok
    BASIC = 1          # Temel tracking
    STANDARD = 2       # Standart verification (önerilen)
    COMPREHENSIVE = 3  # Kapsamlı verification
    PARANOID = 4       # Maksimum güvenlik
```

### IntentType

```python
class IntentType(Enum):
    READ = "read"                      # Okuma operasyonu
    WRITE = "write"                    # Yazma operasyonu
    DELETE = "delete"                  # Silme operasyonu
    EXECUTE = "execute"                # Execution
    NETWORK = "network"                # Network erişimi
    SYSTEM = "system"                  # Sistem operasyonu
    USER_INTERACTION = "user_interaction"  # Kullanıcı etkileşimi
```

### RiskLevel

```python
class RiskLevel(Enum):
    SAFE = "safe"         # Güvenli, risk yok
    LOW = "low"           # Düşük risk
    MEDIUM = "medium"     # Orta risk
    HIGH = "high"         # Yüksek risk
    CRITICAL = "critical" # Kritik risk
```

---

## 🧩 Component APIs

### IntentValidator

```python
class IntentValidator:
    def __init__(self, config: Dict[str, Any])
    
    def validate(self, intent: Intent) -> tuple[bool, List[str]]
        """Intent'i validate eder"""
```

### ActionTracker

```python
class ActionTracker:
    def __init__(self, config: Dict[str, Any])
    
    def track(self, action: Action) -> None
        """Action'ı kaydeder"""
    
    def get_actions_for_intent(self, intent_id: str) -> List[Action]
        """Bir intent için tüm action'ları döner"""
    
    def get_recent_actions(self, count: int = 10) -> List[Action]
        """En son action'ları döner"""
    
    @property
    def actions(self) -> List[Action]
        """Tüm action'lar"""
    
    @property
    def action_chains(self) -> Dict[str, List[str]]
        """Intent ID -> Action ID list mapping"""
```

### BehaviorAnalyzer

```python
class BehaviorAnalyzer:
    def __init__(self, config: Dict[str, Any])
    
    def analyze_alignment(self, intent: Intent, action: Action) -> float
        """
        Intent-action alignment'ı analiz eder
        Returns: 0.0 - 1.0 arası alignment score
        """
    
    def detect_anomalies(
        self, 
        action: Action, 
        history: List[Action]
    ) -> List[str]
        """
        Davranış anomalilerini tespit eder
        Returns: Anomali açıklamaları listesi
        """
```

### SecurityGuard

```python
class SecurityGuard:
    def __init__(self, config: Dict[str, Any])
    
    def check(self, intent: Intent, action: Action) -> List[str]
        """
        Güvenlik kontrollerini yapar
        Returns: Violation açıklamaları listesi
        """
```

### AuditLogger

```python
class AuditLogger:
    def __init__(self, config: Dict[str, Any])
    
    def log_intent(self, intent: Intent) -> None
        """Intent'i loglar"""
    
    def log_action(self, action: Action) -> None
        """Action'ı loglar"""
    
    def log_verification(self, result: VerificationResult) -> None
        """Verification result'ı loglar"""
    
    def export_logs(self, filepath: str) -> None
        """Log'ları dosyaya export eder"""
    
    def verify_integrity(self) -> bool
        """Log integrity'sini doğrular"""
    
    @property
    def logs(self) -> List[Dict[str, Any]]
        """Tüm log entry'leri"""
```

---

## 🔧 Configuration Options

### Framework Config

```python
config = {
    # Logging Configuration
    'log_retention_days': 90,           # Log saklama süresi (gün)
    'log_export_path': '/var/log',      # Export path
    
    # Security Configuration
    'require_approval_for_critical': True,  # Kritik işlemler için onay
    'allow_delete': False,                  # Delete operasyonlarına izin
    'blacklist': [],                        # Yasak target'lar
    'whitelist': [],                        # İzinli target'lar (varsa sadece bunlar)
    'unsafe_domains': [],                   # Güvenli olmayan domain'ler
    
    # Validation Configuration
    'strict_validation': False,             # Strict mode
    
    # Behavior Configuration
    'anomaly_threshold': 0.7,               # Anomali threshold
    'rate_limit_window': 60,                # Rate limit penceresi (saniye)
    
    # Alert Configuration
    'enable_real_time_alerts': True,        # Real-time alertler
    'alert_channels': ['slack', 'email'],   # Alert kanalları
    
    # Performance Configuration
    'max_history_size': 1000,               # Analiz için max history
    'enable_caching': True                  # Cache'leme
}
```

---

## 💡 Usage Examples

### Basic Setup

```python
from agent_verification import (
    VerificationFramework,
    VerificationLevel,
    Intent,
    IntentType,
    RiskLevel
)

# Framework oluştur
framework = VerificationFramework(
    level=VerificationLevel.STANDARD
)

# Agent'ı wrap et
verified_agent = framework.wrap(my_agent)

# Kullan
result = verified_agent.execute(
    "Process data",
    intent_type=IntentType.READ,
    risk_level=RiskLevel.LOW
)
```

### Advanced Setup with Callbacks

```python
def on_verification(result):
    if result.alignment_score < 0.7:
        send_alert(f"Low alignment: {result.alignment_score}")

def on_violation(result):
    emergency_shutdown()
    send_critical_alert(result.security_violations)

framework = VerificationFramework(
    level=VerificationLevel.COMPREHENSIVE,
    config={
        'blacklist': ['/etc/passwd', '/system'],
        'enable_real_time_alerts': True
    }
)

framework.on_verification_complete = on_verification
framework.on_security_violation = on_violation
```

### Manual Verification

```python
# Intent oluştur
intent = Intent(
    type=IntentType.WRITE,
    description="Update database",
    target="users.db",
    risk_level=RiskLevel.MEDIUM
)

# Validate et
is_valid, warnings = framework.verify_intent(intent)
if not is_valid:
    handle_invalid_intent(warnings)

# Action oluştur ve verify et
action = Action(
    intent_id=intent.id,
    type="database_update",
    description="UPDATE users",
    success=True
)

result = framework.verify_action(intent, action)

if not result.verified:
    handle_violation(result)
```

### Export and Analysis

```python
# Rapor al
report = framework.get_report()
print(f"""
Total Actions: {report['total_actions']}
Success Rate: {report['success_rate']:.2%}
Log Integrity: {report['log_integrity']}
""")

# Log'ları export et
framework.audit_logger.export_logs('/var/log/agent_audit.json')

# Integrity check
if not framework.audit_logger.verify_integrity():
    raise SecurityError("Log integrity compromised!")
```

---

## 🔍 Error Handling

### Common Exceptions

```python
try:
    result = verified_agent.execute(task)
except ValueError as e:
    # Invalid intent
    print(f"Invalid intent: {e}")
except RuntimeError as e:
    # Execution failure
    print(f"Execution failed: {e}")
except SecurityError as e:
    # Security violation
    print(f"Security error: {e}")
```

### Best Practices

1. Always check `is_valid` from `verify_intent()`
2. Handle `VerificationResult.verified == False`
3. Monitor callbacks for real-time issues
4. Regular integrity checks with `verify_integrity()`
5. Export logs periodically for backup

---

## 📊 Return Value Examples

### verify_intent() Return

```python
(True, [])  # Valid, no warnings

(True, ["Warning: High risk operation"])  # Valid but with warnings

(False, ["Error: Empty description", "Error: Invalid target"])  # Invalid
```

### verify_action() Return

```python
VerificationResult(
    intent_id="abc-123",
    action_id="xyz-789",
    verified=True,
    alignment_score=0.95,
    risk_assessment=RiskLevel.LOW,
    security_violations=[],
    behavior_anomalies=[],
    recommendations=[]
)
```

### get_report() Return

```python
{
    'framework_level': 2,
    'total_actions': 1234,
    'successful_actions': 1210,
    'success_rate': 0.98,
    'total_intents': 456,
    'log_integrity': True,
    'timestamp': '2026-09-27T16:06:00.000Z'
}
```
