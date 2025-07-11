# 👨‍💻 Development Guide - AI Travel Planner

## 🎯 Overview

This guide is for developers who want to contribute to or extend the AI Travel Planner project. It covers the codebase structure, development setup, and best practices.

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+
- Git
- Virtual environment (recommended)
- API keys for testing

### Environment Setup
```bash
# Clone repository
git clone <repository-url>
cd travel-planner-ai-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy

# Set up pre-commit hooks
pre-commit install
```

### Environment Variables
Create `.env` file for development:
```env
GOOGLE_GEMINI_API_KEY=your_test_key
GOOGLE_MAPS_API_KEY=your_test_key
DEBUG=True
LOG_LEVEL=DEBUG
```

## 📁 Codebase Architecture

### Project Structure
```
travel-planner-ai-agent/
├── app_streamlit.py          # Main Streamlit application
├── app.py                    # Terminal version
├── demo.py                   # Data generation
├── visualize_graph.py        # Graph visualization generator
├── requirements.txt          # Dependencies
├── planner/                  # Core logic
│   ├── __init__.py
│   ├── graph.py             # LangGraph workflow
│   ├── nodes.py             # Processing nodes
│   ├── tools.py             # External API tools
│   └── rag.py               # RAG implementation
├── data/                     # Static data
├── travel_data/             # Dynamic data
├── docs/                    # Documentation
└── tests/                   # Test files
```

### 🎨 LangGraph Workflow Visualization

The application uses a sophisticated LangGraph workflow with 8 interconnected nodes. To understand the workflow structure:

1. **Generate Visual Diagrams**:
   ```bash
   python visualize_graph.py
   ```

2. **View Documentation**: See [docs/GRAPH_VISUALIZATION.md](GRAPH_VISUALIZATION.md) for detailed workflow documentation.

3. **Workflow Overview**:
   ```
   🚀 START → 💰 ask_budget → 📅 ask_duration → 🌟 ask_interests
   ↓
   🔍 suggest_destinations → 🎯 select_city
   ↓
   📝 create_itinerary → 🛠️ call_tools → 📚 rag_follow_up → ✅ END
   ```

### Key Components

#### 1. Streamlit Application (`app_streamlit.py`)
- **Purpose**: Web interface for travel planning
- **Key Features**: 
  - Step-by-step workflow
  - Real-time data integration
  - Caching and optimization
  - Error handling

#### 2. Core Planning Logic (`planner/`)
- **graph.py**: LangGraph workflow definition
- **nodes.py**: Individual processing steps
- **tools.py**: External API integrations
- **rag.py**: Retrieval Augmented Generation

#### 3. Data Management
- **Static Data**: `data/destinations.json`
- **Dynamic Data**: `travel_data/traveldata.json`
- **Caching**: Streamlit cache with TTL

## 🔧 Development Workflow

### Code Style
Follow PEP 8 with these additions:
```python
# Type hints for all functions
def suggest_destinations(
    interests: List[str], 
    budget: str, 
    destination_names: List[str]
) -> List[str]:
    """Suggest destinations based on interests and budget.
    
    Args:
        interests: List of user interests
        budget: Budget level (low/medium/high)
        destination_names: Available destinations
        
    Returns:
        List of suggested destinations
    """
    pass
```

### Testing Strategy
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_streamlit.py

# Run with coverage
pytest --cov=planner --cov-report=html

# Run performance tests
python performance_test.py
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

## 🧪 Testing

### Test Structure
```
tests/
├── test_streamlit.py        # Streamlit app tests
├── test_planner.py          # Core logic tests
├── test_tools.py            # API tools tests
├── test_performance.py      # Performance tests
└── conftest.py              # Test configuration
```

### Writing Tests
```python
import pytest
from planner.tools import weather_tool

def test_weather_tool():
    """Test weather tool functionality."""
    result = weather_tool.call("London")
    assert "temperature" in result.lower()
    assert "wind" in result.lower()

def test_weather_tool_with_month():
    """Test weather tool with seasonal data."""
    result = weather_tool.call("Paris", "July")
    assert "july" in result.lower()
    assert "average" in result.lower()

@pytest.mark.parametrize("location", ["London", "Paris", "Tokyo"])
def test_weather_tool_multiple_locations(location):
    """Test weather tool with multiple locations."""
    result = weather_tool.call(location)
    assert result is not None
    assert len(result) > 0
```

### Mocking External APIs
```python
import pytest
from unittest.mock import patch, Mock

@patch('planner.tools.requests.get')
def test_weather_tool_mock(mock_get):
    """Test weather tool with mocked API."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "current_weather": {
            "temperature": 20.0,
            "windspeed": 10.0
        }
    }
    mock_get.return_value = mock_response
    
    result = weather_tool.call("London")
    assert "20.0°C" in result
```

## 🚀 Performance Optimization

### Caching Strategy
```python
# Resource caching (heavy objects)
@st.cache_resource
def get_embedding_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

# Data caching with TTL
@st.cache_data(ttl=3600)
def load_destination_data():
    # Cache for 1 hour
    pass

# Computed value caching
@st.cache_data
def expensive_computation(data):
    # Cache based on input parameters
    pass
```

### Memory Management
```python
# Lazy loading
def get_embeddings_when_needed():
    if not hasattr(get_embeddings_when_needed, '_embeddings'):
        get_embeddings_when_needed._embeddings = create_embeddings()
    return get_embeddings_when_needed._embeddings

# Cleanup
def cleanup_resources():
    if hasattr(get_embeddings_when_needed, '_embeddings'):
        del get_embeddings_when_needed._embeddings
```

### API Optimization
```python
# Batch requests
def batch_api_calls(locations):
    """Make multiple API calls efficiently."""
    results = {}
    for location in locations:
        try:
            results[location] = api_call(location)
            time.sleep(0.1)  # Rate limiting
        except Exception as e:
            results[location] = f"Error: {e}"
    return results

# Retry logic
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def api_call_with_retry(url):
    """API call with exponential backoff retry."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
```

## 🔧 Adding New Features

### 1. New API Tool
```python
# In planner/tools.py
class NewTool:
    def call(self, location: str) -> str:
        """New tool implementation."""
        try:
            # API call logic
            result = self._make_api_call(location)
            return self._format_result(result)
        except Exception as e:
            return f"Error: {e}"
    
    def _make_api_call(self, location: str):
        """Make the actual API call."""
        pass
    
    def _format_result(self, data):
        """Format API response."""
        pass

# Add to tools module
new_tool = NewTool()
```

### 2. New Streamlit Step
```python
# In app_streamlit.py
elif st.session_state.step == 7:  # New step
    st.subheader("Step 8: New Feature")
    
    # User input
    user_input = st.text_input("Enter information:")
    
    if st.button("Continue"):
        # Process input
        st.session_state.state["new_data"] = user_input
        st.session_state.step = 8
        st.rerun()
```

### 3. New AI Prompt
```python
# In planner/nodes.py
new_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a travel assistant..."),
    ("human", "Generate {type} for {destination}")
])

def new_ai_function(state):
    """New AI-powered function."""
    response = llm.invoke(new_prompt.format_messages(
        type=state["type"],
        destination=state["destination"]
    ))
    return {**state, "result": response.content}
```

## 🐛 Debugging

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Debug Streamlit
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)
```

### Common Issues

#### Performance Issues
```python
# Profile code
import cProfile
import pstats

def profile_function(func):
    profiler = cProfile.Profile()
    profiler.enable()
    result = func()
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
    return result
```

#### Memory Issues
```python
# Monitor memory usage
import psutil
import os

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # MB

print(f"Memory usage: {get_memory_usage():.2f} MB")
```

#### API Issues
```python
# Test API connectivity
def test_api_connectivity():
    try:
        response = requests.get(api_url, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"API error: {e}")
        return False
```

## 📦 Deployment

### Local Development
```bash
# Run with hot reload
streamlit run app_streamlit.py --server.runOnSave true

# Run on specific port
streamlit run app_streamlit.py --server.port 8501
```

### Production Deployment
```bash
# Build requirements
pip freeze > requirements.txt

# Set environment variables
export GOOGLE_GEMINI_API_KEY=production_key
export GOOGLE_MAPS_API_KEY=production_key

# Run with production settings
streamlit run app_streamlit.py --server.headless true
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🤝 Contributing

### Pull Request Process
1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Make changes and add tests
4. Run tests: `pytest`
5. Format code: `black .`
6. Commit: `git commit -m "Add new feature"`
7. Push: `git push origin feature/new-feature`
8. Create pull request

### Code Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Performance considered
- [ ] Security reviewed

### Commit Message Format
```
type(scope): description

feat(tools): add new weather API integration
fix(streamlit): resolve caching issue
docs(readme): update installation instructions
test(planner): add unit tests for destination matching
```

## 📚 Resources

### Documentation
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Google Gemini API](https://ai.google.dev/docs)
- [Google Places API](https://developers.google.com/maps/documentation/places/web-service)

### Tools
- [Black](https://black.readthedocs.io/) - Code formatting
- [Flake8](https://flake8.pycqa.org/) - Linting
- [MyPy](https://mypy.readthedocs.io/) - Type checking
- [Pytest](https://docs.pytest.org/) - Testing

---

*For user documentation, see [User Guide](USER_GUIDE.md). For API details, see [API Documentation](API_DOCUMENTATION.md).* 