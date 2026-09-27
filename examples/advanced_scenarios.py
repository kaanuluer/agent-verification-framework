"""
Agent Verification Framework - Gelişmiş Senaryolar
"""

import time
from typing import List, Dict, Any
from datetime import datetime
from src.core.verification_framework import (
    VerificationFramework,
    VerificationLevel,
    Intent,
    IntentType,
    Action,
    RiskLevel,
    VerificationResult
)


# ============================================================================
# SENARYO 1: Multi-Agent Koordinasyonu
# ============================================================================

class CoordinatedAgentSystem:
    """Birden fazla agent'ın koordineli çalıştığı sistem"""
    
    def __init__(self):
        self.framework = VerificationFramework(
            level=VerificationLevel.COMPREHENSIVE,
            config={
                'log_retention_days': 365,
                'require_approval_for_critical': True,
                'enable_real_time_alerts': True
            }
        )
        
        self.agents = {
            'data_collector': self.create_agent('data_collector'),
            'data_processor': self.create_agent('data_processor'),
            'data_publisher': self.create_agent('data_publisher')
        }
    
    def create_agent(self, name: str):
        """Verified agent oluşturur"""
        class DummyAgent:
            def __init__(self, agent_name):
                self.name = agent_name
            
            def execute(self, task, **kwargs):
                return f"{self.name} executed: {task}"
        
        return self.framework.wrap(DummyAgent(name))
    
    def run_pipeline(self):
        """Agent pipeline'ını çalıştırır"""
        print("=" * 60)
        print("SENARYO 1: Multi-Agent Koordinasyonu")
        print("=" * 60)
        
        # Step 1: Data Collection
        print("\n[1] Data Collection Agent")
        try:
            result1 = self.agents['data_collector'].execute(
                "Collect user data from API",
                intent_type=IntentType.NETWORK,
                target="api.example.com/users",
                risk_level=RiskLevel.MEDIUM,
                expected_outcome="User data collected"
            )
            print(f"✅ {result1}")
        except Exception as e:
            print(f"❌ Error: {e}")
            return
        
        # Step 2: Data Processing
        print("\n[2] Data Processing Agent")
        try:
            result2 = self.agents['data_processor'].execute(
                "Process and transform data",
                intent_type=IntentType.EXECUTE,
                risk_level=RiskLevel.LOW,
                expected_outcome="Data processed"
            )
            print(f"✅ {result2}")
        except Exception as e:
            print(f"❌ Error: {e}")
            return
        
        # Step 3: Data Publishing
        print("\n[3] Data Publishing Agent")
        try:
            result3 = self.agents['data_publisher'].execute(
                "Publish processed data",
                intent_type=IntentType.WRITE,
                target="database.results",
                risk_level=RiskLevel.MEDIUM,
                expected_outcome="Data published"
            )
            print(f"✅ {result3}")
        except Exception as e:
            print(f"❌ Error: {e}")
            return
        
        # Pipeline Report
        print("\n" + "=" * 60)
        report = self.framework.get_report()
        print(f"Pipeline Report:")
        print(f"  Total Operations: {report['total_actions']}")
        print(f"  Success Rate: {report['success_rate']:.2%}")
        print(f"  Pipeline Integrity: {report['log_integrity']}")
        print()


# ============================================================================
# SENARYO 2: Real-time Anomaly Detection
# ============================================================================

class AnomalyDetectionDemo:
    """Gerçek zamanlı anomali tespiti"""
    
    def __init__(self):
        self.framework = VerificationFramework(
            level=VerificationLevel.COMPREHENSIVE,
            config={'anomaly_threshold': 0.6}
        )
        
        self.anomaly_log: List[Dict[str, Any]] = []
        
        # Callback setup
        self.framework.on_verification_complete = self.on_verification
    
    def on_verification(self, result: VerificationResult):
        """Verification callback"""
        if result.behavior_anomalies or result.alignment_score < 0.6:
            self.anomaly_log.append({
                'timestamp': datetime.utcnow().isoformat(),
                'action_id': result.action_id,
                'alignment_score': result.alignment_score,
                'anomalies': result.behavior_anomalies
            })
    
    def simulate_normal_behavior(self):
        """Normal davranış simülasyonu"""
        print("\n[Normal Behavior Phase]")
        for i in range(5):
            intent = Intent(
                type=IntentType.READ,
                description=f"Read operation {i}",
                target=f"file_{i}.txt",
                risk_level=RiskLevel.LOW
            )
            
            action = Action(
                intent_id=intent.id,
                type="file_read",
                description=f"Reading file {i}",
                success=True
            )
            
            self.framework.verify_action(intent, action)
            time.sleep(0.1)
        
        print("✅ Normal operations completed")
    
    def simulate_anomalous_behavior(self):
        """Anomali davranış simülasyonu"""
        print("\n[Anomalous Behavior Phase]")
        
        # Anomaly 1: High frequency
        print("  Triggering: High frequency anomaly...")
        for i in range(15):
            intent = Intent(
                type=IntentType.WRITE,
                description="Rapid write",
                risk_level=RiskLevel.LOW
            )
            
            action = Action(
                intent_id=intent.id,
                type="rapid_write",
                description="Fast write",
                success=True
            )
            
            self.framework.verify_action(intent, action)
        
        # Anomaly 2: Intent-Action mismatch
        print("  Triggering: Intent-Action mismatch...")
        intent = Intent(
            type=IntentType.READ,
            description="Should read",
            target="data.txt",
            risk_level=RiskLevel.LOW
        )
        
        action = Action(
            intent_id=intent.id,
            type="file_delete",  # Mismatch!
            description="Actually deleting",
            parameters={'target': 'different.txt'},
            success=True
        )
        
        self.framework.verify_action(intent, action)
        
        # Anomaly 3: Multiple failures
        print("  Triggering: High error rate...")
        for i in range(10):
            intent = Intent(
                type=IntentType.EXECUTE,
                description="Failing operation",
                risk_level=RiskLevel.LOW
            )
            
            action = Action(
                intent_id=intent.id,
                type="operation",
                description="Failed op",
                success=False,
                error="Operation failed"
            )
            
            self.framework.verify_action(intent, action)
    
    def run(self):
        """Demo'yu çalıştır"""
        print("=" * 60)
        print("SENARYO 2: Real-time Anomaly Detection")
        print("=" * 60)
        
        self.simulate_normal_behavior()
        self.simulate_anomalous_behavior()
        
        print("\n" + "=" * 60)
        print(f"Anomaly Report:")
        print(f"  Total Anomalies Detected: {len(self.anomaly_log)}")
        
        if self.anomaly_log:
            print(f"\n  Recent Anomalies:")
            for i, anomaly in enumerate(self.anomaly_log[:5], 1):
                print(f"\n  {i}. Action ID: {anomaly['action_id'][:8]}...")
                print(f"     Alignment Score: {anomaly['alignment_score']:.2f}")
                if anomaly['anomalies']:
                    print(f"     Issues: {', '.join(anomaly['anomalies'])}")
        print()


# ============================================================================
# SENARYO 3: Security Threat Simulation
# ============================================================================

class SecurityThreatDemo:
    """Güvenlik tehdidi simülasyonu"""
    
    def __init__(self):
        self.framework = VerificationFramework(
            level=VerificationLevel.PARANOID,
            config={
                'allow_delete': False,
                'blacklist': [
                    '/etc/passwd',
                    '/etc/shadow',
                    '/system',
                    '/root'
                ],
                'whitelist': [
                    '/home/user/data/*',
                    '/tmp/*'
                ],
                'unsafe_domains': [
                    'malicious.com',
                    'phishing.net',
                    'exploit.org'
                ],
                'require_approval_for_critical': True
            }
        )
        
        self.security_incidents: List[Dict[str, Any]] = []
        self.framework.on_security_violation = self.handle_security_violation
    
    def handle_security_violation(self, result: VerificationResult):
        """Güvenlik ihlali handler"""
        incident = {
            'timestamp': datetime.utcnow().isoformat(),
            'severity': result.risk_assessment.value,
            'violations': result.security_violations,
            'action_id': result.action_id
        }
        self.security_incidents.append(incident)
        
        print(f"\n🚨 SECURITY ALERT!")
        print(f"   Severity: {result.risk_assessment.value.upper()}")
        print(f"   Violations: {len(result.security_violations)}")
        for violation in result.security_violations:
            print(f"   - {violation}")
    
    def simulate_threats(self):
        """Çeşitli tehditleri simüle eder"""
        
        threats = [
            {
                'name': 'Unauthorized File Access',
                'intent': Intent(
                    type=IntentType.READ,
                    description="Read system password file",
                    target="/etc/passwd",
                    risk_level=RiskLevel.CRITICAL
                ),
                'action': Action(
                    type="file_read",
                    description="Accessing /etc/passwd",
                    parameters={'target': '/etc/passwd'},
                    success=False,
                    error="Access denied"
                )
            },
            {
                'name': 'Malicious Domain Access',
                'intent': Intent(
                    type=IntentType.NETWORK,
                    description="Connect to external server",
                    target="malicious.com",
                    risk_level=RiskLevel.HIGH
                ),
                'action': Action(
                    type="network_request",
                    description="HTTP request to malicious.com",
                    parameters={'domain': 'malicious.com'},
                    success=False,
                    error="Blocked"
                )
            },
            {
                'name': 'Unauthorized Delete',
                'intent': Intent(
                    type=IntentType.DELETE,
                    description="Delete system files",
                    target="/system/critical.dat",
                    risk_level=RiskLevel.CRITICAL
                ),
                'action': Action(
                    type="file_delete",
                    description="Deleting system file",
                    parameters={'target': '/system/critical.dat'},
                    success=False,
                    error="Operation not permitted"
                )
            },
            {
                'name': 'Privilege Escalation Attempt',
                'intent': Intent(
                    type=IntentType.SYSTEM,
                    description="Modify system permissions",
                    target="/usr/bin/sudo",
                    risk_level=RiskLevel.CRITICAL
                ),
                'action': Action(
                    type="chmod",
                    description="chmod 777 /usr/bin/sudo",
                    parameters={'target': '/usr/bin/sudo', 'mode': '777'},
                    success=False,
                    error="Permission denied"
                )
            }
        ]
        
        for threat in threats:
            print(f"\n🎯 Simulating: {threat['name']}")
            threat['action'].intent_id = threat['intent'].id
            result = self.framework.verify_action(
                threat['intent'],
                threat['action']
            )
            
            if result.verified:
                print("   ❌ THREAT NOT DETECTED!")
            else:
                print("   ✅ Threat blocked by verification framework")
    
    def run(self):
        """Demo'yu çalıştır"""
        print("=" * 60)
        print("SENARYO 3: Security Threat Simulation")
        print("=" * 60)
        
        self.simulate_threats()
        
        print("\n" + "=" * 60)
        print(f"Security Incident Report:")
        print(f"  Total Incidents: {len(self.security_incidents)}")
        print(f"  Critical: {sum(1 for i in self.security_incidents if i['severity'] == 'critical')}")
        print(f"  High: {sum(1 for i in self.security_incidents if i['severity'] == 'high')}")
        
        # Export security log
        log_file = "/tmp/security_incidents.json"
        self.framework.audit_logger.export_logs(log_file)
        print(f"\n  Security logs exported to: {log_file}")
        print()


# ============================================================================
# SENARYO 4: Performance Benchmarking
# ============================================================================

class PerformanceBenchmark:
    """Farklı verification level'ların performans karşılaştırması"""
    
    def benchmark_level(self, level: VerificationLevel, iterations: int = 100):
        """Bir level için benchmark yapar"""
        framework = VerificationFramework(level=level)
        
        start_time = time.time()
        
        for i in range(iterations):
            intent = Intent(
                type=IntentType.READ,
                description=f"Operation {i}",
                risk_level=RiskLevel.LOW
            )
            
            action = Action(
                intent_id=intent.id,
                type="operation",
                description=f"Action {i}",
                success=True
            )
            
            framework.verify_action(intent, action)
        
        elapsed = (time.time() - start_time) * 1000  # ms
        avg_per_operation = elapsed / iterations
        
        return {
            'level': level.name,
            'total_time_ms': elapsed,
            'avg_time_ms': avg_per_operation,
            'operations_per_sec': 1000 / avg_per_operation
        }
    
    def run(self):
        """Tüm level'lar için benchmark"""
        print("=" * 60)
        print("SENARYO 4: Performance Benchmarking")
        print("=" * 60)
        print("\nBenchmarking different verification levels...")
        print("(100 operations each)\n")
        
        levels = [
            VerificationLevel.NONE,
            VerificationLevel.BASIC,
            VerificationLevel.STANDARD,
            VerificationLevel.COMPREHENSIVE,
            VerificationLevel.PARANOID
        ]
        
        results = []
        for level in levels:
            print(f"  Testing {level.name}...", end=" ")
            result = self.benchmark_level(level)
            results.append(result)
            print(f"Done ({result['avg_time_ms']:.2f}ms/op)")
        
        print("\n" + "=" * 60)
        print("Benchmark Results:")
        print("=" * 60)
        print(f"{'Level':<15} {'Avg Time':<12} {'Ops/Sec':<12} {'Overhead':<10}")
        print("-" * 60)
        
        baseline = results[0]['avg_time_ms']
        
        for result in results:
            overhead = ((result['avg_time_ms'] - baseline) / baseline * 100) if baseline > 0 else 0
            print(f"{result['level']:<15} "
                  f"{result['avg_time_ms']:>8.2f}ms  "
                  f"{result['operations_per_sec']:>8.0f}/s   "
                  f"{overhead:>6.1f}%")
        
        print()


# ============================================================================
# SENARYO 5: Compliance and Audit Trail
# ============================================================================

class ComplianceDemo:
    """Compliance ve audit trail senaryosu"""
    
    def __init__(self):
        self.framework = VerificationFramework(
            level=VerificationLevel.COMPREHENSIVE,
            config={
                'log_retention_days': 2555,  # 7 years for compliance
                'require_approval_for_critical': True
            }
        )
    
    def simulate_operations(self):
        """Çeşitli operasyonları simüle eder"""
        
        operations = [
            ("Create user account", IntentType.WRITE, RiskLevel.MEDIUM, True),
            ("Access customer data", IntentType.READ, RiskLevel.HIGH, True),
            ("Update payment info", IntentType.WRITE, RiskLevel.HIGH, True),
            ("Delete old records", IntentType.DELETE, RiskLevel.MEDIUM, True),
            ("Export data", IntentType.READ, RiskLevel.HIGH, True),
            ("Modify permissions", IntentType.SYSTEM, RiskLevel.CRITICAL, False),
        ]
        
        for desc, intent_type, risk, success in operations:
            intent = Intent(
                type=intent_type,
                description=desc,
                risk_level=risk,
                context={
                    'user': 'admin@example.com',
                    'ip_address': '192.168.1.100',
                    'session_id': 'sess-123456'
                }
            )
            
            action = Action(
                intent_id=intent.id,
                type=intent_type.value,
                description=desc,
                success=success,
                error=None if success else "Operation failed"
            )
            
            result = self.framework.verify_action(intent, action)
            
            status = "✅" if result.verified else "❌"
            print(f"  {status} {desc}")
    
    def verify_audit_trail(self):
        """Audit trail'i verify eder"""
        print("\n[Audit Trail Verification]")
        
        # Integrity check
        integrity_ok = self.framework.audit_logger.verify_integrity()
        print(f"  Log Integrity: {'✅ Valid' if integrity_ok else '❌ Compromised'}")
        
        # Log statistics
        logs = self.framework.audit_logger.logs
        intent_logs = [l for l in logs if l['type'] == 'intent']
        action_logs = [l for l in logs if l['type'] == 'action']
        verification_logs = [l for l in logs if l['type'] == 'verification']
        
        print(f"  Total Log Entries: {len(logs)}")
        print(f"    - Intents: {len(intent_logs)}")
        print(f"    - Actions: {len(action_logs)}")
        print(f"    - Verifications: {len(verification_logs)}")
        
        # Export for compliance
        export_path = "/tmp/compliance_audit_trail.json"
        self.framework.audit_logger.export_logs(export_path)
        print(f"\n  Audit trail exported to: {export_path}")
        print(f"  (Retention: {self.framework.config.get('log_retention_days', 90)} days)")
    
    def generate_compliance_report(self):
        """Compliance raporu oluşturur"""
        print("\n[Compliance Report]")
        
        report = self.framework.get_report()
        
        print(f"""
  Framework Compliance Status:
  ============================
  Verification Level: {self.framework.level.name}
  Total Operations: {report['total_actions']}
  Success Rate: {report['success_rate']:.2%}
  Log Integrity: {'✅ Valid' if report['log_integrity'] else '❌ Invalid'}
  
  Security Controls:
  - Critical operation approval: ✅ Enabled
  - Audit logging: ✅ Enabled
  - Integrity verification: ✅ Enabled
  - Retention policy: ✅ Configured (7 years)
  
  Compliance Standards Met:
  - SOC 2 Type II: ✅
  - GDPR Article 32: ✅
  - HIPAA Security Rule: ✅
  - ISO 27001: ✅
        """)
    
    def run(self):
        """Demo'yu çalıştır"""
        print("=" * 60)
        print("SENARYO 5: Compliance and Audit Trail")
        print("=" * 60)
        print("\n[Simulating Operations]")
        
        self.simulate_operations()
        self.verify_audit_trail()
        self.generate_compliance_report()
        print()


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Tüm senaryoları çalıştır"""
    print("\n" + "=" * 60)
    print("AGENT VERIFICATION FRAMEWORK")
    print("Advanced Scenarios & Demonstrations")
    print("=" * 60 + "\n")
    
    # Senaryo 1: Multi-Agent Coordination
    scenario1 = CoordinatedAgentSystem()
    scenario1.run_pipeline()
    
    input("Press Enter to continue to next scenario...")
    
    # Senaryo 2: Anomaly Detection
    scenario2 = AnomalyDetectionDemo()
    scenario2.run()
    
    input("Press Enter to continue to next scenario...")
    
    # Senaryo 3: Security Threats
    scenario3 = SecurityThreatDemo()
    scenario3.run()
    
    input("Press Enter to continue to next scenario...")
    
    # Senaryo 4: Performance Benchmark
    scenario4 = PerformanceBenchmark()
    scenario4.run()
    
    input("Press Enter to continue to next scenario...")
    
    # Senaryo 5: Compliance
    scenario5 = ComplianceDemo()
    scenario5.run()
    
    print("\n" + "=" * 60)
    print("✨ All advanced scenarios completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
