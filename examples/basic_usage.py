"""
Agent Verification Framework - Temel Kullanım Örnekleri
"""

from src.core.verification_framework import (
    VerificationFramework,
    VerificationLevel,
    Intent,
    IntentType,
    RiskLevel,
    Action
)
from datetime import datetime


class SimpleAgent:
    """Basit bir örnek agent"""
    
    def execute(self, task: str, **kwargs):
        """Task'ı execute eder"""
        print(f"Executing: {task}")
        return f"Completed: {task}"


def example_1_basic_verification():
    """Örnek 1: Temel verification kullanımı"""
    print("=" * 60)
    print("ÖRNEK 1: Temel Verification")
    print("=" * 60)
    
    # Framework'ü oluştur
    framework = VerificationFramework(
        level=VerificationLevel.STANDARD,
        config={
            'log_retention_days': 90,
            'require_approval_for_critical': True
        }
    )
    
    # Intent oluştur
    intent = Intent(
        type=IntentType.READ,
        description="Kullanıcı verilerini oku",
        target="database.users",
        expected_outcome="Kullanıcı listesi döndürülecek",
        risk_level=RiskLevel.LOW
    )
    
    # Intent'i verify et
    is_valid, warnings = framework.verify_intent(intent)
    print(f"\nIntent Valid: {is_valid}")
    if warnings:
        print(f"Warnings: {warnings}")
    
    # Action oluştur
    action = Action(
        intent_id=intent.id,
        type="database_read",
        description="SELECT * FROM users",
        parameters={'table': 'users', 'limit': 100},
        success=True,
        result={'users': ['user1', 'user2', 'user3']}
    )
    
    # Action'ı verify et
    result = framework.verify_action(intent, action)
    
    print(f"\nVerification Result:")
    print(f"  Verified: {result.verified}")
    print(f"  Alignment Score: {result.alignment_score:.2f}")
    print(f"  Risk Assessment: {result.risk_assessment.value}")
    print(f"  Security Violations: {result.security_violations}")
    print(f"  Behavior Anomalies: {result.behavior_anomalies}")
    print()


def example_2_wrapped_agent():
    """Örnek 2: Agent'ı wrap ederek kullanma"""
    print("=" * 60)
    print("ÖRNEK 2: Wrapped Agent Kullanımı")
    print("=" * 60)
    
    # Framework ve agent oluştur
    framework = VerificationFramework(level=VerificationLevel.STANDARD)
    agent = SimpleAgent()
    
    # Agent'ı wrap et
    verified_agent = framework.wrap(agent)
    
    # Verify edilmiş agent'ı kullan
    try:
        result = verified_agent.execute(
            "Create backup of database",
            intent_type=IntentType.WRITE,
            target="database",
            risk_level=RiskLevel.MEDIUM,
            expected_outcome="Database backup created"
        )
        print(f"\nResult: {result}")
    except Exception as e:
        print(f"\nError: {e}")
    
    # Rapor al
    report = framework.get_report()
    print(f"\nFramework Report:")
    print(f"  Total Actions: {report['total_actions']}")
    print(f"  Success Rate: {report['success_rate']:.2%}")
    print(f"  Log Integrity: {report['log_integrity']}")
    print()


def example_3_security_violations():
    """Örnek 3: Güvenlik ihlallerini tespit etme"""
    print("=" * 60)
    print("ÖRNEK 3: Güvenlik İhlalleri")
    print("=" * 60)
    
    # Framework'ü güvenlik ayarlarıyla oluştur
    framework = VerificationFramework(
        level=VerificationLevel.COMPREHENSIVE,
        config={
            'allow_delete': False,
            'blacklist': ['/etc/passwd', '/system'],
            'unsafe_domains': ['malicious.com', 'phishing.net']
        }
    )
    
    # Riskli intent
    intent = Intent(
        type=IntentType.DELETE,
        description="Sistem dosyasını sil",
        target="/etc/passwd",
        risk_level=RiskLevel.CRITICAL
    )
    
    is_valid, warnings = framework.verify_intent(intent)
    print(f"\nIntent Valid: {is_valid}")
    print(f"Warnings: {warnings}")
    
    # Riskli action
    action = Action(
        intent_id=intent.id,
        type="file_delete",
        description="Delete system file",
        parameters={'path': '/etc/passwd'},
        success=False,
        error="Permission denied"
    )
    
    # Verify
    result = framework.verify_action(intent, action)
    
    print(f"\nVerification Result:")
    print(f"  Verified: {result.verified}")
    print(f"  Security Violations: {result.security_violations}")
    print(f"  Recommendations: {result.recommendations}")
    print()


def example_4_behavior_analysis():
    """Örnek 4: Davranış analizi ve anomali tespiti"""
    print("=" * 60)
    print("ÖRNEK 4: Davranış Analizi")
    print("=" * 60)
    
    framework = VerificationFramework(level=VerificationLevel.COMPREHENSIVE)
    
    # Birçok benzer action oluştur (rate limiting test)
    print("\nSimulating high-frequency actions...")
    
    for i in range(10):
        intent = Intent(
            type=IntentType.WRITE,
            description=f"Write operation {i}",
            target=f"file_{i}.txt",
            risk_level=RiskLevel.LOW
        )
        
        action = Action(
            intent_id=intent.id,
            type="file_write",
            description=f"Writing to file {i}",
            parameters={'file': f"file_{i}.txt"},
            success=True
        )
        
        result = framework.verify_action(intent, action)
        
        if result.behavior_anomalies:
            print(f"\n⚠️  Anomaly detected at action {i}:")
            for anomaly in result.behavior_anomalies:
                print(f"    - {anomaly}")
    
    print()


def example_5_callbacks():
    """Örnek 5: Callback fonksiyonları kullanma"""
    print("=" * 60)
    print("ÖRNEK 5: Callback Fonksiyonları")
    print("=" * 60)
    
    def on_verification_complete(result):
        print(f"\n✅ Verification completed for action: {result.action_id}")
        print(f"   Alignment Score: {result.alignment_score:.2f}")
    
    def on_security_violation(result):
        print(f"\n🚨 SECURITY ALERT!")
        print(f"   Action ID: {result.action_id}")
        print(f"   Violations: {result.security_violations}")
    
    framework = VerificationFramework(
        level=VerificationLevel.COMPREHENSIVE,
        config={'blacklist': ['sensitive_data']}
    )
    
    # Callback'leri ayarla
    framework.on_verification_complete = on_verification_complete
    framework.on_security_violation = on_security_violation
    
    # Normal action
    intent1 = Intent(
        type=IntentType.READ,
        description="Read normal file",
        target="normal_file.txt",
        risk_level=RiskLevel.SAFE
    )
    action1 = Action(
        intent_id=intent1.id,
        type="file_read",
        description="Reading normal file",
        success=True
    )
    framework.verify_action(intent1, action1)
    
    # Riskli action
    intent2 = Intent(
        type=IntentType.READ,
        description="Read sensitive data",
        target="sensitive_data",
        risk_level=RiskLevel.HIGH
    )
    action2 = Action(
        intent_id=intent2.id,
        type="file_read",
        description="Reading sensitive data",
        success=True
    )
    framework.verify_action(intent2, action2)
    
    print()


def example_6_audit_trail():
    """Örnek 6: Audit trail ve log integrity"""
    print("=" * 60)
    print("ÖRNEK 6: Audit Trail ve Log Integrity")
    print("=" * 60)
    
    framework = VerificationFramework(level=VerificationLevel.STANDARD)
    
    # Birkaç operation yap
    for i in range(5):
        intent = Intent(
            type=IntentType.WRITE,
            description=f"Operation {i}",
            risk_level=RiskLevel.LOW
        )
        
        action = Action(
            intent_id=intent.id,
            type="operation",
            description=f"Performing operation {i}",
            success=True
        )
        
        framework.verify_action(intent, action)
    
    # Log integrity check
    print(f"\nLog Integrity: {framework.audit_logger.verify_integrity()}")
    print(f"Total Log Entries: {len(framework.audit_logger.logs)}")
    
    # Export logs
    log_file = "/tmp/audit_logs.json"
    framework.audit_logger.export_logs(log_file)
    print(f"Logs exported to: {log_file}")
    
    # Log örnekleri göster
    print("\nSample Log Entries:")
    for i, log in enumerate(framework.audit_logger.logs[:3]):
        print(f"\n  Entry {i + 1}:")
        print(f"    Type: {log['type']}")
        print(f"    Hash: {log['hash'][:16]}...")
    
    print()


def main():
    """Tüm örnekleri çalıştır"""
    print("\n🔍 AGENT VERIFICATION FRAMEWORK - EXAMPLES\n")
    
    example_1_basic_verification()
    example_2_wrapped_agent()
    example_3_security_violations()
    example_4_behavior_analysis()
    example_5_callbacks()
    example_6_audit_trail()
    
    print("\n✨ All examples completed!\n")


if __name__ == "__main__":
    main()
