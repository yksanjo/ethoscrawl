# Contributing to EthosCrawl

Thank you for your interest in contributing to EthosCrawl! We're building tools for ethical web scraping and appreciate all contributions.

## 🎯 How to Contribute

### 1. Report Bugs
- Check if the bug already exists in [Issues](https://github.com/yourusername/ethoscrawl/issues)
- Use the bug report template
- Include steps to reproduce, expected vs actual behavior

### 2. Suggest Features
- Check if the feature already exists in [Issues](https://github.com/yourusername/ethoscrawl/issues)
- Explain the use case and benefits
- Consider if it aligns with EthosCrawl's ethical principles

### 3. Submit Code Changes
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add or update tests
5. Ensure code passes all checks
6. Submit a pull request

## 🏗️ Development Setup

### Prerequisites
- Python 3.8+
- Git

### Installation
```bash
# Clone your fork
git clone https://github.com/yourusername/ethoscrawl.git
cd ethoscrawl

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ethoscrawl

# Run specific test file
pytest tests/test_crawler.py
```

### Code Quality
```bash
# Format code
black src/ tests/

# Check linting
flake8 src/ tests/

# Type checking
mypy src/
```

## 📁 Project Structure

```
ethoscrawl/
├── src/ethoscrawl/          # Main source code
│   ├── core/               # Core components
│   ├── analytics/          # Analytics and reporting
│   ├── ai/                 # AI integration
│   └── cli.py              # Command line interface
├── tests/                  # Test files
├── examples/               # Usage examples
├── docs/                   # Documentation
└── scripts/                # Development scripts
```

## 📝 Code Style

### Python Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints for all functions
- Document public APIs with docstrings
- Keep functions focused and small

### Docstring Format
```python
def example_function(param1: str, param2: int) -> List[str]:
    """
    Brief description of the function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        List of strings with results
        
    Raises:
        ValueError: If parameters are invalid
        
    Example:
        >>> example_function("test", 5)
        ["result1", "result2"]
    """
```

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):
```
feat: add new privacy level
fix: handle edge case in selector parsing
docs: update installation instructions
test: add tests for ethical framework
refactor: simplify adaptive engine
chore: update dependencies
```

## 🧪 Testing Guidelines

### Test Structure
- Place tests in `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names

### Example Test
```python
import pytest
from ethoscrawl import EthosCrawler

class TestEthosCrawler:
    @pytest.mark.asyncio
    async def test_scrape_with_privacy(self):
        """Test that scraping applies privacy correctly."""
        crawler = EthosCrawler()
        result = await crawler.scrape(...)
        assert result.privacy_applied is True
```

### Mocking
- Mock external API calls
- Use fixtures for common setup
- Test edge cases and error conditions

## 🔒 Security Considerations

EthosCrawl handles web scraping ethically. When contributing:

1. **Respect Privacy**: Never add features that bypass privacy protections
2. **Follow Laws**: Ensure compliance with GDPR, CCPA, and other regulations
3. **Rate Limiting**: Always implement respectful rate limiting
4. **Transparency**: Be clear about what data is collected

## 📚 Documentation

### Updating Documentation
- Update README.md for user-facing changes
- Add docstrings for new functions/classes
- Update examples if API changes
- Consider adding to docs/ for complex features

### Building Documentation
```bash
# Install docs dependencies
pip install -e ".[docs]"

# Build documentation
cd docs && make html
```

## 🚀 Release Process

1. Update version in `setup.py`
2. Update CHANGELOG.md
3. Create release notes
4. Tag the release
5. Build and publish to PyPI

## ❓ Getting Help

- Check existing documentation
- Search existing issues
- Join our [Discussions](https://github.com/yourusername/ethoscrawl/discussions)
- Ask in pull request comments

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make EthosCrawl better! 🙏