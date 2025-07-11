# 🔧 API Documentation

## Overview

The AI Travel Planner uses multiple APIs to provide comprehensive travel planning services. This document details the API integrations, configuration, and usage.

## 🔑 API Keys Required

### 1. Google Gemini API
**Required for**: AI itinerary generation
- **Service**: Google AI Studio
- **URL**: https://makersuite.google.com/app/apikey
- **Usage**: Generates personalized travel itineraries
- **Rate Limits**: Varies by plan

### 2. Google Maps API (Optional)
**Required for**: Real-time location data
- **Service**: Google Cloud Console
- **URL**: https://console.cloud.google.com/
- **Usage**: Attractions, restaurants, hotels, transportation
- **Rate Limits**: 1000 requests/day (free tier)

## 🌐 External APIs Used

### Open-Meteo Weather API
**Service**: Free weather data
**URL**: https://open-meteo.com/
**Features**:
- Current weather conditions
- Historical weather data
- No API key required
- Global coverage

**Endpoints Used**:
```python
# Geocoding
GET https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1

# Current weather
GET https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true

# Historical weather
GET https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={date}&end_date={date}&daily=temperature_2m_mean,precipitation_sum
```

### Google Places API
**Service**: Location and business data
**URL**: https://developers.google.com/maps/documentation/places/web-service
**Features**:
- Tourist attractions
- Restaurants and dining
- Hotels and accommodations
- Transportation options

**Endpoints Used**:
```python
# Text search for places
GET https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={api_key}
```

## 🛠️ Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Required
GOOGLE_GEMINI_API_KEY=your_gemini_api_key_here

# Optional (for enhanced data)
GOOGLE_MAPS_API_KEY=your_maps_api_key_here
```

### Code Configuration
Update API keys in the code if not using environment variables:

```python
# In app_streamlit.py
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    google_api_key="your_key_here",
    temperature=0.5
)

# In planner/tools.py
api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
```

## 📊 API Usage Examples

### Weather Information
```python
from planner.tools import weather_tool

# Current weather
weather = weather_tool.call("Paris, France")
print(weather)
# Output: "Current temperature: 18.5°C, wind speed: 12.3 km/h."

# Seasonal weather
seasonal = weather_tool.call("Paris, France", "July")
print(seasonal)
# Output: "Current temperature: 18.5°C, wind speed: 12.3 km/h.
#         July average: 23.2°C, 45.6mm precipitation. ☀️ Hot weather - pack light clothes and stay hydrated!"
```

### Attractions Data
```python
from planner.tools import attractions_tool

attractions = attractions_tool.call("Rome, Italy")
print(attractions)
# Output: "Top attractions in Rome, Italy:
#           1. Colosseum (Rating: 4.6) - Piazza del Colosseo
#           2. Vatican Museums (Rating: 4.5) - Viale Vaticano
#           ..."
```

### Restaurant Information
```python
from planner.tools import restaurant_tool

restaurants = restaurant_tool.call("Tokyo, Japan")
print(restaurants)
# Output: "Popular restaurants in Tokyo, Japan:
#           1. Sukiyabashi Jiro (Rating: 4.8) - Sushi
#           2. Narisawa (Rating: 4.7) - French-Japanese
#           ..."
```

## 🔄 Error Handling

### API Rate Limits
The application includes fallback mechanisms:

```python
# If Google Maps API is unavailable
if not api_key:
    return f"[Demo] Top attractions in {location}: Museum, Park, Historic Site. (Set GOOGLE_MAPS_API_KEY for real data)"

# If weather API fails
except Exception as e:
    return f"Weather unavailable for {location}."
```

### Graceful Degradation
- Weather: Falls back to demo data
- Places: Uses cached data or demo information
- AI: Returns error message with suggestions

## 📈 Performance Considerations

### Caching Strategy
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_destination_data():
    # Data is cached to reduce API calls

@st.cache_resource
def get_embedding_model():
    # Heavy models are cached
```

### API Call Optimization
- Batch requests where possible
- Cache frequently accessed data
- Use lazy loading for expensive operations

## 🧪 Testing APIs

### Test API Connectivity
```bash
# Test weather API
python -c "from planner.tools import weather_tool; print(weather_tool.call('London'))"

# Test places API (requires API key)
python -c "from planner.tools import attractions_tool; print(attractions_tool.call('Paris'))"
```

### Monitor API Usage
```python
import time

start_time = time.time()
result = api_call()
duration = time.time() - start_time
print(f"API call took {duration:.2f} seconds")
```

## 🔒 Security Best Practices

### API Key Management
1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive data
3. **Rotate keys regularly** for production use
4. **Monitor usage** to detect abuse

### Rate Limiting
```python
import time
from functools import wraps

def rate_limit(calls_per_second=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(1/calls_per_second)
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## 📋 API Response Formats

### Weather API Response
```json
{
  "current_weather": {
    "temperature": 18.5,
    "windspeed": 12.3,
    "weathercode": 1
  }
}
```

### Places API Response
```json
{
  "results": [
    {
      "name": "Colosseum",
      "rating": 4.6,
      "vicinity": "Piazza del Colosseo",
      "types": ["tourist_attraction", "establishment"]
    }
  ]
}
```

## 🚨 Troubleshooting

### Common API Issues

#### "API key not valid"
- Verify API key is correct
- Check if API is enabled in Google Cloud Console
- Ensure billing is set up (for Google APIs)

#### "Rate limit exceeded"
- Implement exponential backoff
- Cache responses
- Monitor usage patterns

#### "No results found"
- Check location spelling
- Verify API service is available
- Use fallback data sources

### Debug Mode
Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📞 Support

For API-related issues:
1. Check API documentation
2. Verify API key configuration
3. Monitor rate limits and quotas
4. Test with simple examples first

---

*For more information, see the main [README.md](../README.md)* 