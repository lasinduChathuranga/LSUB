# Contributing to LSUB v1

Thank you for your interest in contributing to LSUB v1! This document provides guidelines and information for contributors.

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- **Clear description** of the problem
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Python version, etc.)
- **Error messages** or logs if applicable

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- **Clear description** of the enhancement
- **Use case** explaining why this would be useful
- **Possible implementation** approach if you have ideas

### Pull Requests

1. **Fork** the repository
2. **Create a branch** from `develop` for new features or `main` for hotfixes
3. **Make your changes** following the coding standards
4. **Test your changes** thoroughly
5. **Update documentation** if needed
6. **Submit a pull request**

#### Pull Request Guidelines

- Use clear, descriptive commit messages
- Include tests for new functionality
- Update README.md if adding new features
- Follow the existing code style
- Keep changes focused and atomic

## Development Setup

### Prerequisites

```bash
# Clone your fork
git clone https://github.com/yourusername/lsub-v1.git
cd lsub-v1

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Development Dependencies

Create a `requirements-dev.txt` file:
```
pytest>=6.0.0
pytest-cov>=2.10.0
flake8>=3.8.0
black>=21.0.0
isort>=5.0.0
bandit>=1.7.0
```

### Code Style

We use the following tools for code formatting and linting:

```bash
# Format code
black lsub.py

# Sort imports
isort lsub.py

# Lint code
flake8 lsub.py

# Security scan
bandit -r lsub.py
```

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=lsub

# Test specific functionality
python lsub.py --help
python lsub.py --show-engines
```

## Project Structure

```
lsub-v1/
├── lsub.py              # Main application file
├── README.md            # Project documentation
├── requirements.txt     # Production dependencies
├── requirements-dev.txt # Development dependencies
├── setup.py            # Package setup
├── LICENSE             # License file
├── .gitignore          # Git ignore rules
├── CONTRIBUTING.md     # This file
├── .github/
│   └── workflows/
│       └── ci.yml      # GitHub Actions CI
└── docs/               # Additional documentation
```

## Adding New Enumeration Engines

To add a new enumeration engine:

1. **Create a new class** inheriting from `EnumeratorBaseThreaded`
2. **Implement required methods**:
   - `__init__()`
   - `enumerate()` or `extract_domains()`
   - `generate_query()` (if needed)

3. **Example structure**:
```python
class NewEngineEnum(EnumeratorBaseThreaded):
    def __init__(self, domain, subdomains=None, q=None, silent=False, verbose=True):
        base_url = 'https://example.com/api/search?q={query}'
        self.engine_name = "New Engine"
        super(NewEngineEnum, self).__init__(base_url, self.engine_name, domain, subdomains, q=q, silent=silent, verbose=verbose)
    
    def enumerate(self):
        # Implementation here
        return self.subdomains
```

4. **Add to engine groups** in the main function
5. **Test thoroughly** with various domains
6. **Update documentation**

## Performance Considerations

When contributing code:

- **Optimize for concurrent execution**
- **Handle timeouts and errors gracefully**
- **Minimize API calls** where possible
- **Use appropriate delays** to avoid rate limiting
- **Test with different thread counts**

## Documentation Updates

When adding features:

- Update README.md with new options
- Add usage examples
- Update the engine count if adding new engines
- Include any new dependencies

## Release Process

1. Update version number in `setup.py`
2. Update CHANGELOG.md with new features/fixes
3. Create release notes
4. Tag the release
5. Update documentation

## Questions or Need Help?

- Open an issue for bugs or feature requests
- Start a discussion for general questions
- Check existing issues and documentation first

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to LSUB v1!