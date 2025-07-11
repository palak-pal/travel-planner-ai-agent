# 🌟 AI Travel Planner - Professional Edition

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.5.2-green.svg)](https://langchain-ai.github.io/langgraph/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A sophisticated AI-powered travel planning application that creates personalized itineraries using Google Gemini AI, enhanced with real-time data from Google Places API and dynamic weather information.

## 🚀 Live Demo

**[Try the Live App](https://travel-planner-ai-agent.streamlit.app/)**

## ✨ Features

### 🎯 Core Functionality
- **AI-Powered Itinerary Generation**: Personalized travel plans using Google Gemini
- **Smart Destination Recommendations**: ML-based destination matching using embeddings
- **Real-Time Weather Data**: Current and seasonal weather information
- **Google Places Integration**: Live data for attractions, restaurants, hotels, and transportation
- **Seasonal Planning**: Month-based recommendations with weather insights

### 🚀 Performance Optimizations
- **Fast Startup**: 2-3 seconds vs 30+ seconds (optimized with lazy loading)
- **Smart Caching**: Data cached for 1 hour with automatic cleanup
- **Memory Efficient**: Lazy loading of embeddings and models
- **Warning-Free**: Clean console output with suppressed warnings

### 🎨 User Experience
- **Interactive Web Interface**: Built with Streamlit
- **Step-by-Step Planning**: 7-step guided process
- **Progress Tracking**: Visual progress indicator
- **Real-Time Information**: Live weather, attractions, and local data
- **Responsive Design**: Works on desktop and mobile

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [API Configuration](#api-configuration)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key
- Google Maps API key (optional, for enhanced data)

### Step 1: Clone the Repository
```bash
git clone https://github.com/palak-pal/travel-planner-ai-agent.git
cd travel-planner-ai-agent
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up API Keys
Create a `.env` file in the project root:
```env
GOOGLE_GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_MAPS_API_KEY=your_maps_api_key_here
```

### Step 4: Generate Data (Optional)
For enhanced experience with real data:
```bash
python demo.py
```

## 🚀 Quick Start

### Run the Streamlit App
```bash
streamlit run app_streamlit.py
```

The app will open at `http://localhost:8501`

### Run the Terminal Version
```bash
python app.py
```

## 📖 Usage Guide

### Web Interface (Streamlit)

1. **Trip Idea** - Describe your travel request
2. **Budget Selection** - Choose low, medium, or high budget
3. **Duration** - Select number of days (1-60)
4. **Interests** - Enter comma-separated interests
5. **Travel Month** - Choose month for seasonal planning
6. **Destination Selection** - AI suggests destinations
7. **Itinerary Generation** - Get personalized travel plan

### Features Available

#### 🌤️ Weather Information
- Current weather conditions
- Seasonal averages for your travel month
- Packing recommendations based on weather

#### 🏛️ Local Information
- Top attractions with ratings
- Popular restaurants and cuisine
- Accommodation options
- Transportation details

#### 📅 Seasonal Planning
- Month-specific recommendations
- Weather-based packing lists
- Seasonal activities and festivals

## 🔧 API Configuration

### Google Gemini API
Required for AI itinerary generation:
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Add to `.env` file or update in code

### Google Maps API (Optional)
Enhances local data with real information:
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Places API
3. Create API key
4. Add to `.env` file

## 📁 Project Structure

```
travel-planner-ai-agent/
├── app_streamlit.py          # Main Streamlit application
├── app.py                    # Terminal version
├── demo.py                   # Data generation script
├── visualize_graph.py        # Graph visualization generator
├── requirements.txt          # Python dependencies
├── planner/                  # Core planning logic
│   ├── __init__.py
│   ├── graph.py             # Workflow definition
│   ├── nodes.py             # Processing nodes
│   ├── tools.py             # External API tools
│   └── rag.py               # RAG implementation
├── data/                     # Static data
│   └── destinations.json    # Fallback destinations
├── travel_data/             # Dynamic data
│   └── traveldata.json     # Generated with real API data
├── docs/                    # Documentation
│   ├── README.md           # Documentation index
│   ├── API_DOCUMENTATION.md # API usage guide
│   ├── USER_GUIDE.md       # User instructions
│   ├── DEVELOPMENT_GUIDE.md # Developer guide
│   ├── DEPLOYMENT_GUIDE.md # Deployment instructions
│   └── GRAPH_VISUALIZATION.md # Workflow diagrams
└── README.md               # This file
```

## 🔬 Technical Details

### Architecture
- **Frontend**: Streamlit web interface
- **AI Engine**: Google Gemini for itinerary generation
- **ML Pipeline**: Sentence Transformers + FAISS for destination matching
- **Data Sources**: Google Places API, Open-Meteo Weather API
- **Caching**: Streamlit cache with TTL for performance

### 🎨 LangGraph Workflow Visualization

The application uses a sophisticated LangGraph workflow with 8 interconnected nodes:

```
🚀 START
   ↓
💰 ask_budget → 📅 ask_duration → 🌟 ask_interests
   ↓
🔍 suggest_destinations → 🎯 select_city
   ↓
📝 create_itinerary → 🛠️ call_tools → 📚 rag_follow_up
   ↓
✅ END
```

#### Workflow Phases:
1. **User Input Collection**: Budget, duration, interests
2. **AI-Powered Selection**: Vector-based destination suggestions
3. **Planning & Tools**: Itinerary generation + external APIs
4. **Knowledge Enhancement**: RAG-based follow-up information

#### Generate Visual Diagrams:
```bash
# Install Graphviz dependency
pip install graphviz

# Generate workflow diagrams
python visualize_graph.py
```

This creates three visualization types:
- **Basic Workflow**: Simple node-to-node flow
- **Detailed View**: Phase-based organization with state labels
- **State Flow**: State transition diagram

📖 **Detailed Documentation**: See [docs/GRAPH_VISUALIZATION.md](docs/GRAPH_VISUALIZATION.md) for complete workflow documentation.

### Key Components

#### AI Itinerary Generation
```python
def create_itinerary_streamlit(city, interests, duration, budget, travel_month):
    # Uses Google Gemini to generate personalized itineraries
    # Includes seasonal context and budget-specific recommendations
```

#### Destination Matching
```python
def suggest_destinations_streamlit(interests, budget, destination_names, descriptions):
    # Uses sentence embeddings to match interests with destinations
    # Filters by budget level for appropriate suggestions
```

#### Real-Time Data Integration
```python
class WeatherTool:
    # Open-Meteo API for current and historical weather
    # Seasonal recommendations and packing advice

class AttractionsTool:
    # Google Places API for real attraction data
    # Ratings, reviews, and location information
```

### Performance Optimizations

#### Caching Strategy
- `@st.cache_resource`: Heavy objects (models)
- `@st.cache_data`: Data with TTL (1 hour)
- Lazy loading: Embeddings only when needed

#### Memory Management
- Embeddings created on-demand
- Automatic cache cleanup
- Efficient data processing

## 🚀 Deployment

### Local Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app_streamlit.py
```

### Cloud Deployment

#### Streamlit Cloud
1. Fork this repository
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy with your API keys

#### Heroku
```bash
# Create Procfile
echo "web: streamlit run app_streamlit.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

#### Docker
```bash
# Build image
docker build -t travel-planner .

# Run container
docker run -p 8501:8501 travel-planner
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Fork and clone
git clone https://github.com/your-username/travel-planner-ai-agent.git
cd travel-planner-ai-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

### Code Style
- Follow PEP 8
- Use type hints
- Add docstrings
- Write tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Google Gemini](https://ai.google.dev/) for AI capabilities
- [Streamlit](https://streamlit.io/) for the web framework
- [LangGraph](https://langchain-ai.github.io/langgraph/) for workflow management
- [Open-Meteo](https://open-meteo.com/) for weather data
- [Google Places API](https://developers.google.com/maps/documentation/places/web-service) for location data

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/palak-pal/travel-planner-ai-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/palak-pal/travel-planner-ai-agent/discussions)
- **Documentation**: [docs/](docs/)

---

**Happy Traveling! 🌍✈️**

*Made with ❤️ by [Palak Pal](https://github.com/palak-pal)*