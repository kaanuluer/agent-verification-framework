# Agent Verification Framework - API Guide

Complete guide for using the REST API.

## 🚀 Getting Started

### Starting the API Server

```bash
# Basic start
python -m src.api.server

# With custom configuration
python -m src.api.server --host 0.0.0.0 --port 8080

# With debug mode
python -m src.api.server --debug

# Production deployment with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "src.api.server:app"
```

### Authentication

All API endpoints (except `/health`) require authentication via API key.

**Methods:**

1. **X-API-Key header** (Recommended)
```bash
curl -H "X-API-Key: your-api-key" http://localhost:5000/api/v1/sessions
```

2. **Authorization Bearer token**
```bash
curl -H "Authorization: Bearer your-api-key" http://localhost:5000/api/v1/sessions
```

**Default API Key**: `dev-api-key-change-in-production`

**Environment Variable**: Set `API_KEY` environment variable for production.

## 📡 API Endpoints

### Health Check

**GET** `/api/v1/health`

Check API server health status.

**No authentication required**

**Response:**
```json
{
  "status": "healthy",
  "service": "agent-verification-framework",
  "version": "0.2.0",
  "timestamp": "2026-09-27T16:30:00.000Z",
  "active_sessions": 5
}
```

**cURL Example:**
```bash
curl http://localhost:5000/api/v1/health
```

---

### Session Management

#### Create Session

**POST** `/api/v1/sessions`

Create a new verification session.

**Request Body:**
```json
{
  "level": "STANDARD",
  "config": {
    "log_retention_days": 90,
    "require_approval_for_critical": true
  }
}
```

**Response:**
```json
{
  "session_id": "a1b2c3d4-5678-90ab-cdef-1234567890ab",
  "level": "STANDARD",
  "created_at": "2026-09-27T16:30:00.000Z",
  "config": {...}
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/v1/sessions \
  -H "X-API-Key: dev-api-key-change-in-production" \
  -H "Content-Type: application/json" \
  -d '{
    "level": "STANDARD",
    "config": {
      "log_retention_days": 90
    }
  }'
```

#### Get Session

**GET** `/api/v1/sessions/<session_id>`

Get information about a specific session.

**Response:**
```json
{
  "session_id": "a1b2c3d4-...",
  "level": "STANDARD",
  "report": {
    "framework_level": 2,
    "total_actions": 42,
    "successful_actions": 40,
    "success_rate": 0.95,
    "total_intents": 15,
    "log_integrity": true,
    "timestamp": "2026-09-27T16:35:00.000Z"
  }
}
```

#### List Sessions

**GET** `/api/v1/sessions`

List all active sessions.

**Response:**
```json
{
  "sessions": [
    {
      "session_id": "a1b2c3d4-...",
      "level": "STANDARD",
      "total_actions": 42,
      "success_rate": 0.95
    }
  ],
  "total": 3
}
```

#### Delete Session

**DELETE** `/api/v1/sessions/<session_id>`

Delete a verification session.

**Response:**
```json
{
  "message": "Session deleted",
  "session_id": "a1b2c3d4-..."
}
```

---

### Intent Verification

#### Verify Intent

**POST** `/api/v1/verify/intent`

Verify an intent before execution.

**Request Body:**
```json
{
  "session_id": "a1b2c3d4-...",
  "type": "READ",
  "description": "Read user data from database",
  "target": "database.users",
  "expected_outcome": "User list retrieved",
  "risk_level": "LOW",
  "context": {
    "user_id": 123,
    "requester": "admin"
  }
}
```

**Fields:**
- `session_id` (optional): Use existing session or create new one
- `type`: Intent type (READ, WRITE, DELETE, EXECUTE, NETWORK, SYSTEM, USER_INTERACTION)
- `description`: Human-readable description
- `target` (optional): Target resource
- `expected_outcome` (optional): Expected result
- `risk_level`: Risk level (SAFE, LOW, MEDIUM, HIGH, CRITICAL)
- `context` (optional): Additional context

**Response:**
```json
{
  "session_id": "a1b2c3d4-...",
  "intent_id": "intent-xyz-...",
  "valid": true,
  "warnings": [],
  "intent": {
    "type": "read",
    "description": "Read user data from database",
    "risk_level": "low",
    "requires_approval": false
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/v1/verify/intent \
  -H "X-API-Key: dev-api-key-change-in-production" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "READ",
    "description": "Read user data",
    "target": "database.users",
    "risk_level": "LOW"
  }'
```

---

### Action Verification

#### Verify Action

**POST** `/api/v1/verify/action`

Verify an action after execution.

**Request Body:**
```json
{
  "session_id": "a1b2c3d4-...",
  "intent": {
    "type": "WRITE",
    "description": "Update user profile",
    "target": "users/123/profile",
    "risk_level": "MEDIUM"
  },
  "action": {
    "type": "database_update",
    "description": "UPDATE users SET name='John'",
    "parameters": {
      "user_id": 123,
      "field": "name",
      "value": "John"
    },
    "success": true,
    "duration_ms": 45.3,
    "side_effects": ["cache_invalidated"]
  }
}
```

**Response:**
```json
{
  "session_id": "a1b2c3d4-...",
  "intent_id": "intent-xyz-...",
  "action_id": "action-abc-...",
  "verified": true,
  "alignment_score": 0.95,
  "risk_assessment": "medium",
  "security_violations": [],
  "behavior_anomalies": [],
  "recommendations": [],
  "timestamp": "2026-09-27T16:30:00.000Z"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/v1/verify/action \
  -H "X-API-Key: dev-api-key-change-in-production" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "a1b2c3d4-...",
    "intent": {
      "type": "WRITE",
      "description": "Update user",
      "risk_level": "MEDIUM"
    },
    "action": {
      "type": "update",
      "description": "Updated user",
      "success": true
    }
  }'
```

---

### Reports and Audit

#### Get Report

**GET** `/api/v1/reports/<session_id>`

Get verification report for a session.

**Response:**
```json
{
  "session_id": "a1b2c3d4-...",
  "report": {
    "framework_level": 2,
    "total_actions": 42,
    "successful_actions": 40,
    "success_rate": 0.95,
    "total_intents": 15,
    "log_integrity": true,
    "timestamp": "2026-09-27T16:35:00.000Z"
  }
}
```

#### Get Actions

**GET** `/api/v1/reports/<session_id>/actions?limit=10&offset=0`

Get actions for a session with pagination.

**Query Parameters:**
- `limit` (default: 10): Number of actions to return
- `offset` (default: 0): Offset for pagination

**Response:**
```json
{
  "session_id": "a1b2c3d4-...",
  "actions": [
    {
      "id": "action-123",
      "type": "database_update",
      "description": "...",
      "success": true,
      "timestamp": "...",
      ...
    }
  ],
  "total": 42,
  "limit": 10,
  "offset": 0
}
```

#### Get Audit Logs

**GET** `/api/v1/reports/<session_id>/audit?limit=10&offset=0`

Get audit logs for a session.

**Response:**
```json
{
  "session_id": "a1b2c3d4-...",
  "logs": [
    {
      "type": "intent",
      "data": {...},
      "hash": "sha256-hash..."
    }
  ],
  "total": 50,
  "limit": 10,
  "offset": 0,
  "integrity_verified": true
}
```

---

## 🐍 Python Client

### Installation

```python
pip install requests
```

### Usage

```python
import requests

API_URL = "http://localhost:5000"
API_KEY = "dev-api-key-change-in-production"

headers = {
    'X-API-Key': API_KEY,
    'Content-Type': 'application/json'
}

# Create session
response = requests.post(
    f"{API_URL}/api/v1/sessions",
    headers=headers,
    json={'level': 'STANDARD'}
)
session = response.json()
session_id = session['session_id']

# Verify intent
response = requests.post(
    f"{API_URL}/api/v1/verify/intent",
    headers=headers,
    json={
        'session_id': session_id,
        'type': 'READ',
        'description': 'Read user data',
        'risk_level': 'LOW'
    }
)
intent_result = response.json()

# Get report
response = requests.get(
    f"{API_URL}/api/v1/reports/{session_id}",
    headers=headers
)
report = response.json()
```

### Client Class

See [api_client_example.py](../examples/api_client_example.py) for a complete client implementation.

---

## 🔐 Security

### API Key Management

**Generate API Key:**
```python
from src.api.auth import AuthManager

auth = AuthManager()
new_key = auth.generate_api_key()
print(f"New API Key: {new_key}")
```

**Add API Key:**
```python
auth.add_api_key(
    api_key="your-new-key",
    name="production-key",
    role="admin",
    metadata={'created_by': 'admin'}
)
```

**Revoke API Key:**
```python
auth.revoke_api_key("old-key")
```

### Best Practices

1. **Use HTTPS in production**
2. **Rotate API keys regularly**
3. **Use environment variables for secrets**
4. **Implement rate limiting**
5. **Monitor API usage**
6. **Enable audit logging**

---

## 🚀 Deployment

### Development

```bash
python -m src.api.server --debug
```

### Production with Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "src.api.server:app"
```

### Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt -r requirements-api.txt

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.api.server:app"]
```

### Environment Variables

```bash
# API Configuration
API_KEY=your-secret-api-key
SECRET_KEY=your-flask-secret-key
HOST=0.0.0.0
PORT=5000
DEBUG=false

# CORS
CORS_ORIGINS=https://your-domain.com

# Session
SESSION_TIMEOUT=3600
MAX_SESSIONS=100
```

---

## 📊 Response Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Invalid or missing API key |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error |

---

## 🔍 Error Handling

All errors follow this format:

```json
{
  "error": "Error Type",
  "message": "Detailed error message",
  "details": {
    "additional": "context"
  }
}
```

**Example:**
```json
{
  "error": "Unauthorized",
  "message": "Invalid API key"
}
```

---

## 📈 Rate Limiting

Rate limiting is configurable in `config/api_config.json`:

```json
{
  "rate_limiting": {
    "enabled": true,
    "requests_per_minute": 100,
    "requests_per_hour": 1000
  }
}
```

When rate limit is exceeded:
```json
{
  "error": "Rate Limit Exceeded",
  "message": "Too many requests",
  "retry_after": 60
}
```

---

## 🧪 Testing

### Manual Testing with cURL

```bash
# Health check
curl http://localhost:5000/api/v1/health

# Create session
curl -X POST http://localhost:5000/api/v1/sessions \
  -H "X-API-Key: dev-api-key-change-in-production" \
  -H "Content-Type: application/json" \
  -d '{"level":"STANDARD"}'

# Verify intent
curl -X POST http://localhost:5000/api/v1/verify/intent \
  -H "X-API-Key: dev-api-key-change-in-production" \
  -H "Content-Type: application/json" \
  -d '{
    "type":"READ",
    "description":"Test intent",
    "risk_level":"LOW"
  }'
```

### Automated Testing

```bash
# Run API examples
python examples/api_client_example.py

# Run integration tests
pytest tests/test_api.py -v
```

---

## 💡 Examples

See [examples/api_client_example.py](../examples/api_client_example.py) for:

- Basic API usage
- Complete verification workflow
- Managing multiple sessions
- Error handling

---

## 📞 Support

- **Documentation**: [GitHub Repository](https://github.com/kaanuluer/agent-verification-framework)
- **Issues**: [GitHub Issues](https://github.com/kaanuluer/agent-verification-framework/issues)
- **API Reference**: [api-reference.md](api-reference.md)
