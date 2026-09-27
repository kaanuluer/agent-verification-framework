# Security Policy and Best Practices

## 🔐 Security Overview

The Agent Verification Framework is designed with security as a top priority. This document outlines security features, best practices, and how to report vulnerabilities.

## 📋 Security Features

### 1. Authentication & Authorization

**API Key Authentication**
- All API endpoints (except `/health`) require authentication
- API keys are hashed using SHA-256
- Support for role-based access control (RBAC)

**Best Practices:**
```bash
# Generate a secure API key
python -c 'import secrets; print(secrets.token_urlsafe(32))'

# Set as environment variable
export API_KEY="your-secure-api-key-here"
```

### 2. Input Validation

**Comprehensive Validation:**
- String length limits
- Dictionary/list size limits
- Enum validation
- Type checking
- SQL injection prevention
- XSS prevention

**Validation Limits:**
```python
MAX_DESCRIPTION_LENGTH = 1000
MAX_TARGET_LENGTH = 500
MAX_CONTEXT_SIZE = 100
MAX_PARAMETERS_SIZE = 100
MAX_SIDE_EFFECTS = 50
```

### 3. Rate Limiting

**Default Limits:**
- 100 requests per minute per API key/IP
- 1000 requests per hour per API key/IP

**Configurable via environment:**
```bash
export RATE_LIMIT_PER_MINUTE=100
export RATE_LIMIT_PER_HOUR=1000
```

### 4. Security Headers

**Automatically Added:**
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `X-Request-ID` for request tracking

### 5. CORS Configuration

**Production Configuration:**
```bash
# Specify allowed origins (comma-separated)
export CORS_ORIGINS="https://your-app.com,https://api.your-app.com"
```

**Development:**
- Default allows all origins (`*`)
- Should be restricted in production

### 6. HTTPS Enforcement

```bash
# Require HTTPS in production
export REQUIRE_HTTPS=true
export SESSION_COOKIE_SECURE=true
```

### 7. Secret Management

**Environment Variables Required:**
```bash
# Flask secret key
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')

# API key
export API_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')

# Host binding (use 127.0.0.1 for localhost only)
export HOST=127.0.0.1

# Disable debug in production
export DEBUG=false
export FLASK_ENV=production
```

### 8. Audit Trail

**Cryptographic Integrity:**
- All logs are hashed with SHA-256
- Tamper detection built-in
- Immutable log records

**Verification:**
```python
framework.audit_logger.verify_integrity()  # Returns True if logs are intact
```

## 🚨 Security Warnings

### ⚠️ Development vs Production

**Development Mode Issues:**
- Debug mode enabled
- Weak default keys
- Binding to 0.0.0.0
- CORS allows all origins

**Production Checklist:**
- [ ] Set `FLASK_ENV=production`
- [ ] Set strong `SECRET_KEY`
- [ ] Set unique `API_KEY`
- [ ] Set `DEBUG=false`
- [ ] Set `HOST=127.0.0.1` or specific IP
- [ ] Configure `CORS_ORIGINS`
- [ ] Enable `REQUIRE_HTTPS=true`
- [ ] Use reverse proxy (nginx/apache)
- [ ] Enable rate limiting
- [ ] Set up monitoring/logging

### 🔥 Known Risks

1. **In-Memory Session Storage**
   - **Risk**: Sessions lost on restart
   - **Solution**: Use Redis or database in production
   - **Implementation**: See "Production Deployment" section

2. **In-Memory Rate Limiting**
   - **Risk**: Rate limits not shared across instances
   - **Solution**: Use Redis for distributed rate limiting
   - **Implementation**: See "Production Deployment" section

3. **No Built-in Encryption**
   - **Risk**: Data in transit not encrypted
   - **Solution**: Use HTTPS/TLS
   - **Implementation**: Deploy behind nginx with SSL

## 🛡️ Deployment Security

### Recommended Architecture

```
Internet
    │
    ▼
[Reverse Proxy - nginx/apache]
    │ (HTTPS/TLS)
    ▼
[Firewall]
    │
    ▼
[API Server - 127.0.0.1:5000]
    │
    ▼
[Redis - Session/Rate Limiting]
```

### nginx Configuration Example

```nginx
server {
    listen 443 ssl http2;
    server_name api.example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Docker Security

```dockerfile
FROM python:3.10-slim

# Run as non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Install dependencies
COPY requirements.txt requirements-api.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-api.txt

# Copy application
COPY . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:5000/api/v1/health')"

# Run with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "30", "--access-logfile", "-", "src.api.server:app"]
```

### Environment File (.env)

```bash
# NEVER commit this file to version control
# Add .env to .gitignore

FLASK_ENV=production
DEBUG=false

# Generate with: python -c 'import secrets; print(secrets.token_hex(32))'
SECRET_KEY=your-secret-key-here

# Generate with: python -c 'import secrets; print(secrets.token_urlsafe(32))'
API_KEY=your-api-key-here

# Network
HOST=127.0.0.1
PORT=5000

# Security
REQUIRE_HTTPS=true
CORS_ORIGINS=https://your-app.com

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_PER_HOUR=1000

# Limits
MAX_CONTENT_LENGTH=10485760  # 10MB
```

## 🔍 Security Scanning

### Automated Scanning

```bash
# Install security tools
pip install bandit safety

# Run Bandit (static analysis)
bandit -r src/ -f json -o security_report.json

# Check dependencies for vulnerabilities
safety check --json

# Run tests with security focus
pytest tests/ -v -k security
```

### Manual Code Review

**Focus Areas:**
1. Authentication bypass
2. SQL injection vectors
3. XSS vulnerabilities
4. CSRF protection
5. Rate limiting effectiveness
6. Input validation coverage
7. Secrets in code
8. Insecure dependencies

## 🐛 Vulnerability Reporting

### Responsible Disclosure

**DO NOT** open public GitHub issues for security vulnerabilities.

**Instead:**
1. Email: security@example.com (if available)
2. Or create a private GitHub security advisory
3. Include:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Time

- **Critical**: Response within 24 hours
- **High**: Response within 3 days
- **Medium**: Response within 1 week
- **Low**: Response within 2 weeks

### Bug Bounty

Currently, we do not have a bug bounty program. Contributions are welcome and credited.

## 📚 Security Resources

### Standards & Compliance

- **OWASP Top 10**: Common web vulnerabilities
- **CWE/SANS Top 25**: Most dangerous software errors
- **NIST Cybersecurity Framework**: Security best practices

### Tools

- **Bandit**: Python security linter
- **Safety**: Dependency vulnerability checker
- **OWASP ZAP**: Web application security scanner
- **Semgrep**: Static analysis tool

### References

- [Flask Security Best Practices](https://flask.palletsprojects.com/en/latest/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [OWASP API Security Project](https://owasp.org/www-project-api-security/)

## 🔄 Security Updates

### Update Policy

- Security patches released ASAP
- Minor versions for low-risk fixes
- Major versions for breaking changes

### Staying Updated

```bash
# Check for updates
pip list --outdated

# Update framework
pip install --upgrade agent-verification-framework

# Check release notes
https://github.com/kaanuluer/agent-verification-framework/releases
```

## ✅ Security Checklist

### Development
- [ ] Use unique API keys per developer
- [ ] Never commit secrets to version control
- [ ] Use `.env` files with `.gitignore`
- [ ] Run security scanners regularly
- [ ] Review dependency vulnerabilities

### Production
- [ ] Strong secrets (32+ bytes)
- [ ] HTTPS/TLS enabled
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Monitoring and alerting
- [ ] Regular security audits
- [ ] Incident response plan
- [ ] Backup and recovery tested

### API Keys
- [ ] Rotate regularly (every 90 days)
- [ ] Revoke on suspected compromise
- [ ] Use different keys per environment
- [ ] Monitor usage patterns
- [ ] Set expiration dates

## 📞 Contact

For security concerns:
- Email: security@example.com
- GitHub: https://github.com/kaanuluer/agent-verification-framework/security

---

**Last Updated**: September 27, 2026
**Version**: 0.2.1
