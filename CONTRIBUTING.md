# 🤝 Contributing to AI Travel Planner

Thank you for your interest in contributing to the AI Travel Planner project! This document provides guidelines for contributing to the project.

## 🎯 How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **🐛 Bug Reports**: Report issues you encounter
- **💡 Feature Requests**: Suggest new features or improvements
- **📝 Documentation**: Improve or add documentation
- **🔧 Code Contributions**: Submit code improvements or new features
- **🧪 Testing**: Help with testing and quality assurance
- **🌍 Localization**: Help translate the application

### Before You Start

1. **Check Existing Issues**: Search existing issues to avoid duplicates
2. **Read Documentation**: Familiarize yourself with the project structure
3. **Set Up Development Environment**: Follow the setup instructions below

## 🛠️ Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- API keys for testing (Google Gemini, Google Maps)

### Setup Steps

```bash
# Fork and clone the repository
git clone https://github.com/your-username/travel-planner-ai-agent.git
cd travel-planner-ai-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy pre-commit

# Set up pre-commit hooks
pre-commit install

# Create .env file for API keys
cp .env.example .env
# Edit .env with your API keys
```

### Environment Variables

Create a `.env` file with your API keys:

```env
GOOGLE_GEMINI_API_KEY=your_gemini_api_key
GOOGLE_MAPS_API_KEY=your_maps_api_key
DEBUG=True
LOG_LEVEL=DEBUG
```

## 📋 Contribution Guidelines

### Code Style

- **Python**: Follow PEP 8 guidelines
- **Type Hints**: Use type hints for all functions
- **Docstrings**: Add docstrings to all functions and classes
- **Comments**: Add comments for complex logic

### Example Code Style

```python
from typing import List, Optional
from langchain_core.messages import HumanMessage, AIMessage

def suggest_destinations(
    interests: List[str], 
    budget: str, 
    destination_names: List[str]
) -> List[str]:
    """Suggest destinations based on user interests and budget.
    
    Args:
        interests: List of user interests (e.g., ['history', 'food'])
        budget: Budget level ('low', 'medium', 'high')
        destination_names: Available destination names
        
    Returns:
        List of suggested destination names
        
    Raises:
        ValueError: If budget is not one of the allowed values
    """
    if budget not in ['low', 'medium', 'high']:
        raise ValueError("Budget must be 'low', 'medium', or 'high'")
    
    # Implementation here
    return suggested_destinations
```

### Testing

- Write tests for new features
- Ensure all tests pass before submitting
- Aim for good test coverage

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=planner --cov-report=html

# Run specific test file
pytest tests/test_tools.py
```

### Code Quality

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy planner/

# Security check
bandit -r .
```

## 🔄 Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Write your code following the style guidelines
- Add tests for new functionality
- Update documentation if needed

### 3. Test Your Changes

```bash
# Run tests
pytest

# Test the application
streamlit run app_streamlit.py

# Check code quality
black .
flake8 .
mypy planner/
```

### 4. Commit Your Changes

```bash
# Add your changes
git add .

# Commit with a descriptive message
git commit -m "feat: add new weather tool functionality

- Add seasonal weather predictions
- Include packing recommendations
- Update documentation"
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:

- **Clear title**: Describe the change
- **Description**: Explain what and why
- **Related issues**: Link to any related issues
- **Screenshots**: If UI changes are involved

## 📝 Pull Request Guidelines

### PR Title Format

Use conventional commit format:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions or changes
- `chore:` Maintenance tasks

### PR Description Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Test addition

## Testing
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Clear description** of the issue
2. **Steps to reproduce**
3. **Expected vs actual behavior**
4. **Environment details** (OS, Python version, etc.)
5. **Screenshots** if applicable
6. **Error messages** and stack traces

## 💡 Feature Requests

When suggesting features:

1. **Clear description** of the feature
2. **Use case** and benefits
3. **Implementation ideas** (optional)
4. **Mockups** or examples (if applicable)

## 📚 Documentation

Help improve documentation by:

- Fixing typos or unclear explanations
- Adding missing information
- Creating tutorials or guides
- Translating to other languages

## 🏷️ Issue Labels

We use the following labels:

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested

## 🎉 Recognition

Contributors will be recognized in:

- Project README
- Release notes
- GitHub contributors page

## 📞 Getting Help

If you need help:

1. **Check documentation**: [docs/](docs/)
2. **Search issues**: Look for similar problems
3. **Ask questions**: Use GitHub Discussions
4. **Join community**: Connect with other contributors

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to AI Travel Planner! 🌍✈️** 