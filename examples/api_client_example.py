"""
Agent Verification Framework - API Client Example
"""

import requests
import json
from typing import Dict, Any, Optional


class VerificationAPIClient:
    """Client for Agent Verification Framework API"""
    
    def __init__(self, base_url: str = "http://localhost:5000", api_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key or "dev-api-key-change-in-production"
        self.session_id: Optional[str] = None
    
    def _headers(self) -> Dict[str, str]:
        """Get request headers"""
        return {
            'Content-Type': 'application/json',
            'X-API-Key': self.api_key
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        response = requests.get(
            f"{self.base_url}/api/v1/health",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()
    
    def create_session(
        self, 
        level: str = "STANDARD",
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new verification session"""
        response = requests.post(
            f"{self.base_url}/api/v1/sessions",
            headers=self._headers(),
            json={
                'level': level,
                'config': config or {}
            }
        )
        response.raise_for_status()
        data = response.json()
        self.session_id = data['session_id']
        return data
    
    def get_session(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Get session information"""
        sid = session_id or self.session_id
        if not sid:
            raise ValueError("No session ID provided")
        
        response = requests.get(
            f"{self.base_url}/api/v1/sessions/{sid}",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()
    
    def delete_session(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Delete a session"""
        sid = session_id or self.session_id
        if not sid:
            raise ValueError("No session ID provided")
        
        response = requests.delete(
            f"{self.base_url}/api/v1/sessions/{sid}",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()
    
    def list_sessions(self) -> Dict[str, Any]:
        """List all sessions"""
        response = requests.get(
            f"{self.base_url}/api/v1/sessions",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()
    
    def verify_intent(
        self,
        intent_type: str,
        description: str,
        target: Optional[str] = None,
        expected_outcome: Optional[str] = None,
        risk_level: str = "MEDIUM",
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Verify an intent"""
        response = requests.post(
            f"{self.base_url}/api/v1/verify/intent",
            headers=self._headers(),
            json={
                'session_id': self.session_id,
                'type': intent_type,
                'description': description,
                'target': target,
                'expected_outcome': expected_outcome,
                'risk_level': risk_level,
                'context': context or {}
            }
        )
        response.raise_for_status()
        return response.json()
    
    def verify_action(
        self,
        intent: Dict[str, Any],
        action: Dict[str, Any],
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Verify an action"""
        sid = session_id or self.session_id
        if not sid:
            raise ValueError("No session ID provided")
        
        response = requests.post(
            f"{self.base_url}/api/v1/verify/action",
            headers=self._headers(),
            json={
                'session_id': sid,
                'intent': intent,
                'action': action
            }
        )
        response.raise_for_status()
        return response.json()
    
    def get_report(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Get verification report"""
        sid = session_id or self.session_id
        if not sid:
            raise ValueError("No session ID provided")
        
        response = requests.get(
            f"{self.base_url}/api/v1/reports/{sid}",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_actions(
        self,
        session_id: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> Dict[str, Any]:
        """Get actions for a session"""
        sid = session_id or self.session_id
        if not sid:
            raise ValueError("No session ID provided")
        
        response = requests.get(
            f"{self.base_url}/api/v1/reports/{sid}/actions",
            headers=self._headers(),
            params={'limit': limit, 'offset': offset}
        )
        response.raise_for_status()
        return response.json()
    
    def get_audit_logs(
        self,
        session_id: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> Dict[str, Any]:
        """Get audit logs for a session"""
        sid = session_id or self.session_id
        if not sid:
            raise ValueError("No session ID provided")
        
        response = requests.get(
            f"{self.base_url}/api/v1/reports/{sid}/audit",
            headers=self._headers(),
            params={'limit': limit, 'offset': offset}
        )
        response.raise_for_status()
        return response.json()


def example_1_basic_usage():
    """Example 1: Basic API usage"""
    print("=" * 60)
    print("EXAMPLE 1: Basic API Usage")
    print("=" * 60)
    
    # Create client
    client = VerificationAPIClient()
    
    # Health check
    print("\n[1] Health Check")
    health = client.health_check()
    print(f"✅ API Status: {health['status']}")
    print(f"   Version: {health['version']}")
    print(f"   Active Sessions: {health['active_sessions']}")
    
    # Create session
    print("\n[2] Creating Session")
    session = client.create_session(level="STANDARD")
    print(f"✅ Session Created: {session['session_id']}")
    print(f"   Level: {session['level']}")
    
    # Verify intent
    print("\n[3] Verifying Intent")
    intent_result = client.verify_intent(
        intent_type="READ",
        description="Read user data from database",
        target="database.users",
        risk_level="LOW"
    )
    print(f"✅ Intent Valid: {intent_result['valid']}")
    print(f"   Intent ID: {intent_result['intent_id']}")
    
    # Get report
    print("\n[4] Getting Report")
    report = client.get_report()
    print(f"✅ Report Retrieved")
    print(f"   Total Actions: {report['report']['total_actions']}")
    print(f"   Success Rate: {report['report']['success_rate']:.2%}")
    
    print()


def example_2_complete_verification():
    """Example 2: Complete verification workflow"""
    print("=" * 60)
    print("EXAMPLE 2: Complete Verification Workflow")
    print("=" * 60)
    
    client = VerificationAPIClient()
    
    # Create session
    print("\n[1] Creating Session")
    session = client.create_session(
        level="COMPREHENSIVE",
        config={
            'log_retention_days': 90,
            'require_approval_for_critical': True
        }
    )
    print(f"✅ Session: {session['session_id']}")
    
    # Define intent
    intent = {
        'type': 'WRITE',
        'description': 'Update user profile',
        'target': 'users/123/profile',
        'risk_level': 'MEDIUM',
        'context': {'user_id': 123}
    }
    
    # Define action
    action = {
        'type': 'database_update',
        'description': 'UPDATE users SET name="John" WHERE id=123',
        'parameters': {'user_id': 123, 'field': 'name', 'value': 'John'},
        'success': True,
        'duration_ms': 45.3
    }
    
    # Verify action
    print("\n[2] Verifying Action")
    result = client.verify_action(intent, action)
    print(f"✅ Verified: {result['verified']}")
    print(f"   Alignment Score: {result['alignment_score']:.2f}")
    print(f"   Risk: {result['risk_assessment']}")
    
    if result['security_violations']:
        print(f"   ⚠️  Violations: {result['security_violations']}")
    
    if result['behavior_anomalies']:
        print(f"   ⚠️  Anomalies: {result['behavior_anomalies']}")
    
    if result['recommendations']:
        print(f"   💡 Recommendations:")
        for rec in result['recommendations']:
            print(f"      - {rec}")
    
    print()


def example_3_multiple_sessions():
    """Example 3: Managing multiple sessions"""
    print("=" * 60)
    print("EXAMPLE 3: Multiple Sessions")
    print("=" * 60)
    
    client = VerificationAPIClient()
    
    # Create multiple sessions
    print("\n[1] Creating Multiple Sessions")
    sessions = []
    for i, level in enumerate(['BASIC', 'STANDARD', 'COMPREHENSIVE'], 1):
        session = client.create_session(level=level)
        sessions.append(session)
        print(f"   Session {i}: {session['session_id'][:8]}... ({level})")
    
    # List all sessions
    print("\n[2] Listing All Sessions")
    all_sessions = client.list_sessions()
    print(f"✅ Total Sessions: {all_sessions['total']}")
    for sess in all_sessions['sessions']:
        print(f"   - {sess['session_id'][:8]}... ({sess['level']})")
    
    # Clean up
    print("\n[3] Cleaning Up")
    for session in sessions:
        client.delete_session(session['session_id'])
        print(f"   ✅ Deleted: {session['session_id'][:8]}...")
    
    print()


def example_4_error_handling():
    """Example 4: Error handling"""
    print("=" * 60)
    print("EXAMPLE 4: Error Handling")
    print("=" * 60)
    
    client = VerificationAPIClient()
    
    # Test 1: Invalid session ID
    print("\n[1] Testing Invalid Session ID")
    try:
        client.get_session("invalid-session-id")
    except requests.exceptions.HTTPError as e:
        print(f"✅ Caught error: {e.response.status_code}")
        print(f"   Message: {e.response.json()['error']}")
    
    # Test 2: Invalid intent data
    print("\n[2] Testing Invalid Intent Data")
    try:
        response = requests.post(
            f"{client.base_url}/api/v1/verify/intent",
            headers=client._headers(),
            json={}  # Empty data
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"✅ Caught error: {e.response.status_code}")
    
    # Test 3: Missing API key
    print("\n[3] Testing Missing API Key")
    try:
        response = requests.get(
            f"{client.base_url}/api/v1/health",
            headers={'Content-Type': 'application/json'}  # No API key
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"✅ Caught error: {e.response.status_code}")
        print(f"   Message: {e.response.json()['message']}")
    
    print()


def main():
    """Run all examples"""
    print("\n🌐 Agent Verification Framework - API Client Examples\n")
    
    try:
        example_1_basic_usage()
        input("Press Enter to continue...")
        
        example_2_complete_verification()
        input("Press Enter to continue...")
        
        example_3_multiple_sessions()
        input("Press Enter to continue...")
        
        example_4_error_handling()
        
        print("\n✨ All examples completed!\n")
    
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server")
        print("   Make sure the server is running:")
        print("   python -m src.api.server\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
