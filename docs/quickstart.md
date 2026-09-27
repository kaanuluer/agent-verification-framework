# Quick Start Guide

Agent Verification Framework'ü hızlıca kullanmaya başlamak için bu kılavuzu takip edin.

## 📦 Kurulum

### 1. Repository'yi klonlayın

```bash
git clone https://github.com/example/agent-verification-framework.git
cd agent-verification-framework
```

### 2. Virtual environment oluşturun

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### 3. Bağımlılıkları yükleyin

```bash
pip install -r requirements.txt

# veya development için
pip install -e ".[dev]"
```

### 4. Testleri çalıştırın (opsiyonel)

```bash
pytest tests/ -v
```

## 🚀 İlk Kullanım

### Basit Örnek

```python
from src.core import (
    VerificationFramework,
    VerificationLevel,
    Intent,
    IntentType,
    RiskLevel
)

# 1. Framework'ü oluştur
framework = VerificationFramework(
    level=VerificationLevel.STANDARD
)

# 2. Intent oluştur
intent = Intent(
    type=IntentType.READ,
    description="Kullanıcı verilerini oku",
    target="database.users",
    risk_level=RiskLevel.LOW
)

# 3. Intent'i validate et
is_valid, warnings = framework.verify_intent(intent)
print(f"Valid: {is_valid}")
if warnings:
    print(f"Warnings: {warnings}")
```

### Agent'ı Wrap Etme

```python
# Kendi agent'ınız
class MyAgent:
    def execute(self, task, **kwargs):
        # Agent logic
        return f"Executed: {task}"

# Agent'ı wrap edin
agent = MyAgent()
verified_agent = framework.wrap(agent)

# Artık verified şekilde kullanabilirsiniz
result = verified_agent.execute(
    "Process data",
    intent_type=IntentType.READ,
    risk_level=RiskLevel.LOW
)
```

## 📊 Temel Örnekler

### 1. Okuma Operasyonu

```python
from src.core import Intent, IntentType, RiskLevel

intent = Intent(
    type=IntentType.READ,
    description="Read configuration file",
    target="config.json",
    risk_level=RiskLevel.SAFE
)

is_valid, warnings = framework.verify_intent(intent)
```

### 2. Yazma Operasyonu

```python
intent = Intent(
    type=IntentType.WRITE,
    description="Update user profile",
    target="users/123/profile",
    risk_level=RiskLevel.MEDIUM,
    context={'backup_available': True}
)

is_valid, warnings = framework.verify_intent(intent)
```

### 3. Kritik Operasyon

```python
intent = Intent(
    type=IntentType.DELETE,
    description="Delete old backups",
    target="/backups/old/",
    risk_level=RiskLevel.HIGH,
    requires_approval=True
)

is_valid, warnings = framework.verify_intent(intent)
```

## 🔧 Konfigürasyon

### Temel Konfigürasyon

```python
framework = VerificationFramework(
    level=VerificationLevel.STANDARD,
    config={
        # Logging
        'log_retention_days': 90,
        
        # Security
        'require_approval_for_critical': True,
        'allow_delete': False,
        
        # Alerts
        'enable_real_time_alerts': True
    }
)
```

### Konfigürasyon Dosyasından Yükleme

```python
import json

with open('config/default_config.json', 'r') as f:
    config = json.load(f)

framework = VerificationFramework(
    level=VerificationLevel.STANDARD,
    config=config
)
```

## 📈 Raporlama

### Basit Rapor

```python
report = framework.get_report()

print(f"Total Actions: {report['total_actions']}")
print(f"Success Rate: {report['success_rate']:.2%}")
print(f"Log Integrity: {report['log_integrity']}")
```

### Audit Log Export

```python
framework.audit_logger.export_logs('/path/to/audit_log.json')
```

## 🔐 Güvenlik Kontrolleri

### Blacklist Kullanımı

```python
framework = VerificationFramework(
    level=VerificationLevel.STANDARD,
    config={
        'blacklist': ['/etc/passwd', '/system', '/root']
    }
)
```

### Whitelist Kullanımı

```python
framework = VerificationFramework(
    level=VerificationLevel.COMPREHENSIVE,
    config={
        'whitelist': ['/home/user/data/*', '/tmp/*'],
        'enable_whitelist': True
    }
)
```

## 🎯 Callback'ler

### Verification Complete Callback

```python
def on_verification(result):
    print(f"Verification completed: {result.verified}")
    if result.alignment_score < 0.7:
        print(f"Low alignment: {result.alignment_score}")

framework.on_verification_complete = on_verification
```

### Security Violation Callback

```python
def on_violation(result):
    print(f"🚨 SECURITY ALERT!")
    print(f"Violations: {result.security_violations}")
    # Send alert, log, etc.

framework.on_security_violation = on_violation
```

## 📝 Örnek Uygulamalar

### Çalışan Örnekler

```bash
# Temel kullanım örnekleri
python examples/basic_usage.py

# Gelişmiş senaryolar
python examples/advanced_scenarios.py
```

### Örnekler İçinde:

1. **basic_usage.py**
   - Temel verification
   - Wrapped agent kullanımı
   - Güvenlik ihlalleri
   - Davranış analizi
   - Callback'ler
   - Audit trail

2. **advanced_scenarios.py**
   - Multi-agent koordinasyonu
   - Real-time anomaly detection
   - Security threat simulation
   - Performance benchmarking
   - Compliance & audit

## 🧪 Test Etme

### Kendi Agent'ınızı Test Etme

```python
import pytest
from src.core import VerificationFramework, VerificationLevel

def test_my_agent():
    framework = VerificationFramework(level=VerificationLevel.STANDARD)
    agent = MyAgent()
    verified_agent = framework.wrap(agent)
    
    result = verified_agent.execute(
        "test task",
        intent_type=IntentType.READ,
        risk_level=RiskLevel.LOW
    )
    
    assert result is not None
    report = framework.get_report()
    assert report['success_rate'] == 1.0
```

### Unit Testler

```bash
# Tüm testleri çalıştır
pytest tests/ -v

# Coverage ile
pytest tests/ --cov=src --cov-report=html

# Specific test
pytest tests/test_verification_framework.py::TestIntent -v
```

## 🔍 Debugging

### Log Seviyesi Ayarlama

```python
import logging

logging.basicConfig(level=logging.DEBUG)

framework = VerificationFramework(level=VerificationLevel.STANDARD)
# Şimdi detaylı loglar göreceksiniz
```

### Verification Result İnceleme

```python
result = framework.verify_action(intent, action)

print(f"Verified: {result.verified}")
print(f"Alignment Score: {result.alignment_score}")
print(f"Risk: {result.risk_assessment.value}")
print(f"Violations: {result.security_violations}")
print(f"Anomalies: {result.behavior_anomalies}")
print(f"Recommendations: {result.recommendations}")
```

## 🎨 Verification Levels Karşılaştırma

```python
levels = [
    VerificationLevel.NONE,        # Test only
    VerificationLevel.BASIC,       # Minimal overhead
    VerificationLevel.STANDARD,    # Recommended
    VerificationLevel.COMPREHENSIVE,  # High security
    VerificationLevel.PARANOID     # Maximum security
]

for level in levels:
    framework = VerificationFramework(level=level)
    # Test your agent with different levels
```

## 💡 Best Practices

1. **Production'da STANDARD veya üstü kullanın**
   ```python
   framework = VerificationFramework(level=VerificationLevel.STANDARD)
   ```

2. **Intent'lere açıklayıcı description'lar verin**
   ```python
   intent = Intent(
       type=IntentType.WRITE,
       description="Update user email address after verification",
       target="users/123/email"
   )
   ```

3. **Risk level'ı doğru belirleyin**
   ```python
   # Kritik operasyonlar için
   risk_level=RiskLevel.HIGH  # veya CRITICAL
   ```

4. **Context bilgisi ekleyin**
   ```python
   intent = Intent(
       # ...
       context={
           'user_id': 123,
           'backup_available': True,
           'approved_by': 'admin@example.com'
       }
   )
   ```

5. **Callback'leri kullanın**
   ```python
   framework.on_security_violation = send_alert
   framework.on_verification_complete = log_to_monitoring
   ```

## 📚 İleri Okuma

- [Mimari Dokümantasyon](architecture.md)
- [API Reference](api-reference.md)
- [Test Suite](../tests/)
- [Örnekler](../examples/)

## ❓ Sorun Giderme

### Import Hatası

```python
# Eğer import hatası alıyorsanız:
import sys
sys.path.insert(0, '/path/to/agent-verification-framework')

from src.core import VerificationFramework
```

### Framework Çok Yavaş

```python
# Daha düşük level kullanın
framework = VerificationFramework(level=VerificationLevel.BASIC)

# veya history size'ı azaltın
framework = VerificationFramework(
    level=VerificationLevel.STANDARD,
    config={'max_history_size': 100}
)
```

### Çok Fazla False Positive

```python
# Threshold'ları ayarlayın
framework = VerificationFramework(
    level=VerificationLevel.STANDARD,
    config={
        'anomaly_threshold': 0.5,  # Daha toleranslı
        'strict_validation': False
    }
)
```

## 🤝 Yardım ve Destek

- GitHub Issues: https://github.com/example/agent-verification-framework/issues
- Documentation: https://docs.example.com
- Email: support@example.com

## 🎉 Başarıyla Kuruldu!

Framework'ü başarıyla kurdunuz! Şimdi agent'larınızı güvenli bir şekilde verify edebilirsiniz.

Happy verifying! 🚀
