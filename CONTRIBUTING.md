# Contributing to Agent Verification Framework

Agent Verification Framework'e katkıda bulunmak istediğiniz için teşekkürler! 

## 🤝 Katkı Süreci

### 1. Fork ve Clone

```bash
# Repository'yi fork edin, sonra:
git clone https://github.com/YOUR_USERNAME/agent-verification-framework.git
cd agent-verification-framework
```

### 2. Development Environment Kurulumu

```bash
# Virtual environment oluştur
python -m venv venv
source venv/bin/activate  # Linux/Mac

# Development dependencies yükle
pip install -e ".[dev]"
```

### 3. Branch Oluştur

```bash
git checkout -b feature/your-feature-name
# veya
git checkout -b bugfix/issue-number
```

### 4. Değişikliklerinizi Yapın

- Code'u yazın
- Test'leri ekleyin
- Dokümantasyonu güncelleyin

### 5. Test Edin

```bash
# Testleri çalıştır
pytest tests/ -v

# Coverage kontrol et
pytest tests/ --cov=src --cov-report=html

# Code style kontrol et
black src/ tests/
flake8 src/ tests/
mypy src/
```

### 6. Commit ve Push

```bash
git add .
git commit -m "feat: Add new feature"
git push origin feature/your-feature-name
```

### 7. Pull Request Oluştur

GitHub'da Pull Request açın ve şablon'u doldurun.

## 📝 Commit Message Convention

Conventional Commits kullanıyoruz:

```
type(scope): subject

body (optional)

footer (optional)
```

### Types:

- `feat`: Yeni feature
- `fix`: Bug fix
- `docs`: Dokümantasyon değişikliği
- `test`: Test ekleme/değiştirme
- `refactor`: Code refactoring
- `style`: Code style (formatting, etc.)
- `perf`: Performance improvement
- `chore`: Build, dependencies, etc.

### Örnekler:

```
feat(validator): Add custom validation rules support

Add ability to register custom validation rules for intents.

Closes #123
```

```
fix(tracker): Fix action chain tracking bug

Fixed issue where action chains were not properly linked
when intent_id was None.
```

## 🧪 Testing Guidelines

### Test Yazma

```python
# tests/test_my_feature.py
import pytest
from src.core import VerificationFramework

class TestMyFeature:
    def test_feature_works(self):
        framework = VerificationFramework()
        # Test code
        assert result == expected
    
    def test_feature_handles_error(self):
        with pytest.raises(ValueError):
            # Test error case
            pass
```

### Test Coverage

- Yeni feature'lar için %80+ coverage hedefleyin
- Edge case'leri test edin
- Error handling'i test edin

## 📚 Documentation Guidelines

### Docstring Format

```python
def my_function(param1: str, param2: int) -> bool:
    """
    Brief description of what the function does.
    
    Longer description if needed, explaining the behavior,
    algorithm, or any important details.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is negative
    
    Example:
        >>> my_function("test", 42)
        True
    """
    pass
```

### Markdown Docs

- README.md: Genel bakış ve quick start
- docs/: Detaylı dokümantasyon
- examples/: Çalışan kod örnekleri
- Türkçe ve İngilizce destekleniyor

## 🎨 Code Style

### Python Style Guide

- PEP 8 kurallarını takip edin
- Black formatter kullanın
- Type hints kullanın
- Docstring'ler yazın

### Örnek:

```python
from typing import List, Optional, Dict, Any

class MyClass:
    """Class description."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize with config."""
        self.config = config
    
    def process(
        self, 
        data: List[str], 
        options: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Process the data.
        
        Args:
            data: List of items to process
            options: Optional processing options
        
        Returns:
            Success status
        """
        # Implementation
        return True
```

## 🔍 Code Review Process

### PR Checklist

- [ ] Tests pass
- [ ] Coverage maintained/improved
- [ ] Documentation updated
- [ ] Code style compliant
- [ ] Commit messages follow convention
- [ ] No merge conflicts

### Review Criteria

1. **Functionality**: Does it work as intended?
2. **Tests**: Are there adequate tests?
3. **Code Quality**: Is it readable and maintainable?
4. **Documentation**: Is it well documented?
5. **Performance**: Any performance impact?
6. **Security**: Any security concerns?

## 🐛 Bug Reports

### Bug Report Template

```markdown
**Describe the bug**
A clear description of the bug.

**To Reproduce**
Steps to reproduce:
1. ...
2. ...

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment**
- OS: [e.g. Ubuntu 22.04]
- Python version: [e.g. 3.10]
- Framework version: [e.g. 0.1.0]

**Additional context**
Any other relevant information.
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Any alternative solutions or features.

**Additional context**
Any other context or screenshots.
```

## 🏗️ Architecture Guidelines

### Adding New Components

1. **Plan**: Discuss in an issue first
2. **Design**: Follow existing patterns
3. **Implement**: Write clean, testable code
4. **Document**: Add comprehensive docs
5. **Test**: Write thorough tests

### Component Structure

```
src/core/
├── __init__.py
├── verification_framework.py  # Core framework
├── validators/               # Intent validators
├── trackers/                # Action trackers
├── analyzers/               # Behavior analyzers
├── guards/                  # Security guards
└── reporters/               # Report generators
```

## 🔐 Security Guidelines

### Security Considerations

- Never commit secrets
- Validate all inputs
- Handle errors securely
- Follow principle of least privilege
- Document security implications

### Reporting Security Issues

**DO NOT** open public issues for security vulnerabilities.

Email: security@example.com

## 📊 Performance Guidelines

### Performance Considerations

- Profile before optimizing
- Document performance impact
- Add benchmarks for critical paths
- Consider different verification levels

### Benchmarking

```python
import time

def benchmark_feature():
    start = time.time()
    # Run feature
    elapsed = time.time() - start
    print(f"Feature took {elapsed:.4f}s")
```

## 🌍 Internationalization

### Adding Translations

```python
# For Turkish documentation
docs/tr/quickstart.md

# For English documentation  
docs/en/quickstart.md
```

## 📦 Release Process

### Version Numbers

Semantic Versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### Release Checklist

- [ ] Update version in setup.py
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create git tag
- [ ] Build package
- [ ] Upload to PyPI

## 🎓 Learning Resources

### For Contributors

- [Python Best Practices](https://docs.python-guide.org/)
- [Testing in Python](https://docs.pytest.org/)
- [Type Hints](https://docs.python.org/3/library/typing.html)
- [Git Workflow](https://guides.github.com/introduction/flow/)

## 🙏 Recognition

Contributors are recognized in:
- README.md
- Release notes
- Contributors page

## ❓ Questions?

- Open a Discussion on GitHub
- Join our Slack channel
- Email: dev@example.com

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
