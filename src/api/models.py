"""
Agent Verification Framework - API Models
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List


@dataclass
class IntentRequest:
    """Intent verification request model"""
    type: str
    description: str
    target: Optional[str] = None
    expected_outcome: Optional[str] = None
    risk_level: str = "MEDIUM"
    context: Dict[str, Any] = None
    session_id: Optional[str] = None
    level: str = "STANDARD"
    config: Dict[str, Any] = None


@dataclass
class ActionRequest:
    """Action verification request model"""
    session_id: str
    intent: Dict[str, Any]
    action: Dict[str, Any]


@dataclass
class VerificationResponse:
    """Verification response model"""
    session_id: str
    intent_id: str
    action_id: Optional[str] = None
    verified: bool = True
    alignment_score: Optional[float] = None
    risk_assessment: Optional[str] = None
    security_violations: List[str] = None
    behavior_anomalies: List[str] = None
    recommendations: List[str] = None
    timestamp: Optional[str] = None


@dataclass
class ErrorResponse:
    """Error response model"""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
