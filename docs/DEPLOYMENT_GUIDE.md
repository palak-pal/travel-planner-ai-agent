# 🚀 Deployment Guide - AI Travel Planner

## 📋 Overview

This guide covers deploying the AI Travel Planner application to various platforms and environments.

## 🛠️ Prerequisites

### Required
- Python 3.8 or higher
- Google Gemini API key
- Git repository access

### Optional
- Google Maps API key (for enhanced features)
- Domain name (for production)
- SSL certificate (for HTTPS)

## 🏠 Local Deployment

### Development Environment
```bash
# Clone repository
git clone <repository-url>
cd travel-planner-ai-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GOOGLE_GEMINI_API_KEY=your_key_here
export GOOGLE_MAPS_API_KEY=your_key_here  # Optional

# Run application
streamlit run app_streamlit.py
```

### Production Local Setup
```bash
# Install production dependencies
pip install gunicorn

# Run with production settings
streamlit run app_streamlit.py \
  --server.headless true \
  --server.port 8501 \
  --server.address 0.0.0.0
```

## ☁️ Cloud Deployment

### Streamlit Cloud (Recommended)

#### Step 1: Prepare Repository
```bash
# Ensure requirements.txt is up to date
pip freeze > requirements.txt

# Create .streamlit/config.toml
mkdir .streamlit
```

Create `.streamlit/config.toml`:
```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

#### Step 2: Deploy to Streamlit Cloud
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Set deployment settings:
   - **Main file path**: `app_streamlit.py`
   - **Python version**: 3.9
4. Add secrets in Streamlit Cloud:
   - `GOOGLE_GEMINI_API_KEY`
   - `GOOGLE_MAPS_API_KEY` (optional)

#### Step 3: Configure Environment
In Streamlit Cloud dashboard:
- Go to Settings → Secrets
- Add your API keys:
```toml
GOOGLE_GEMINI_API_KEY = "your_key_here"
GOOGLE_MAPS_API_KEY = "your_key_here"
```

### Heroku Deployment

#### Step 1: Create Heroku App
```bash
# Install Heroku CLI
# Create app
heroku create your-travel-planner-app

# Add buildpack
heroku buildpacks:add heroku/python
```

#### Step 2: Create Procfile
Create `Procfile`:
```
web: streamlit run app_streamlit.py --server.port=$PORT --server.address=0.0.0.0
```

#### Step 3: Deploy
```bash
# Set environment variables
heroku config:set GOOGLE_GEMINI_API_KEY=your_key_here
heroku config:set GOOGLE_MAPS_API_KEY=your_key_here

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Docker Deployment

#### Step 1: Create Dockerfile
```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Set environment variables
ENV PYTHONPATH=/app
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run application
CMD ["streamlit", "run", "app_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Step 2: Create Docker Compose
Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  travel-planner:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GOOGLE_GEMINI_API_KEY=${GOOGLE_GEMINI_API_KEY}
      - GOOGLE_MAPS_API_KEY=${GOOGLE_MAPS_API_KEY}
    volumes:
      - ./data:/app/data
      - ./travel_data:/app/travel_data
    restart: unless-stopped
```

#### Step 3: Build and Run
```bash
# Build image
docker build -t travel-planner .

# Run container
docker run -p 8501:8501 \
  -e GOOGLE_GEMINI_API_KEY=your_key_here \
  -e GOOGLE_MAPS_API_KEY=your_key_here \
  travel-planner

# Or use Docker Compose
docker-compose up -d
```

### AWS Deployment

#### EC2 Instance
```bash
# Launch EC2 instance (Ubuntu 20.04)
# Connect via SSH
ssh -i your-key.pem ubuntu@your-instance-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Clone repository
git clone <repository-url>
cd travel-planner-ai-agent

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables
export GOOGLE_GEMINI_API_KEY=your_key_here
export GOOGLE_MAPS_API_KEY=your_key_here

# Run application
streamlit run app_streamlit.py --server.port=8501 --server.address=0.0.0.0
```

#### Nginx Configuration
Create `/etc/nginx/sites-available/travel-planner`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/travel-planner /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Google Cloud Platform

#### App Engine
Create `app.yaml`:
```yaml
runtime: python39

env_variables:
  GOOGLE_GEMINI_API_KEY: "your_key_here"
  GOOGLE_MAPS_API_KEY: "your_key_here"

handlers:
  - url: /.*
    script: auto
    secure: always
```

Deploy:
```bash
gcloud app deploy
```

#### Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/travel-planner
gcloud run deploy travel-planner \
  --image gcr.io/PROJECT_ID/travel-planner \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_GEMINI_API_KEY=your_key_here
```

## 🔧 Environment Configuration

### Environment Variables
```bash
# Required
GOOGLE_GEMINI_API_KEY=your_gemini_api_key

# Optional
GOOGLE_MAPS_API_KEY=your_maps_api_key
DEBUG=False
LOG_LEVEL=INFO
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Configuration Files
Create `.streamlit/config.toml`:
```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false
maxUploadSize = 200

[browser]
gatherUsageStats = false
serverAddress = "0.0.0.0"
serverPort = 8501

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

## 🔒 Security Considerations

### API Key Management
```bash
# Use environment variables (recommended)
export GOOGLE_GEMINI_API_KEY=your_key

# Or use secrets management
# AWS Secrets Manager
aws secretsmanager create-secret --name travel-planner-keys --secret-string '{"GEMINI_KEY":"your_key"}'

# Google Secret Manager
echo -n "your_key" | gcloud secrets create gemini-api-key --data-file=-
```

### HTTPS Configuration
```nginx
# Nginx SSL configuration
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    # ... rest of configuration
}
```

### Firewall Rules
```bash
# Allow only necessary ports
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

## 📊 Monitoring and Logging

### Application Logs
```python
# Add logging to app_streamlit.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Health Checks
```python
# Add health check endpoint
import streamlit as st

def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# In your app
if st.sidebar.button("Health Check"):
    st.json(health_check())
```

### Performance Monitoring
```python
# Monitor API response times
import time

def monitor_api_call(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        logging.info(f"API call {func.__name__} took {duration:.2f}s")
        return result
    return wrapper
```

## 🚨 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port
lsof -i :8501

# Kill process
kill -9 <PID>

# Or use different port
streamlit run app_streamlit.py --server.port 8502
```

#### Memory Issues
```bash
# Monitor memory usage
htop

# Increase swap space
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### API Rate Limits
```python
# Implement rate limiting
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

### Debug Mode
```bash
# Enable debug logging
export DEBUG=True
export LOG_LEVEL=DEBUG

# Run with debug
streamlit run app_streamlit.py --logger.level=debug
```

## 📈 Scaling

### Horizontal Scaling
```yaml
# Docker Compose with multiple instances
version: '3.8'

services:
  travel-planner:
    build: .
    ports:
      - "8501-8510:8501"
    deploy:
      replicas: 3
    environment:
      - GOOGLE_GEMINI_API_KEY=${GOOGLE_GEMINI_API_KEY}
```

### Load Balancing
```nginx
# Nginx load balancer configuration
upstream travel_planner {
    server localhost:8501;
    server localhost:8502;
    server localhost:8503;
}

server {
    listen 80;
    location / {
        proxy_pass http://travel_planner;
    }
}
```

## 📞 Support

### Deployment Issues
1. Check logs: `docker logs <container_id>`
2. Verify environment variables
3. Test API connectivity
4. Check firewall settings

### Performance Issues
1. Monitor resource usage
2. Check API rate limits
3. Optimize caching
4. Scale horizontally

---

*For development setup, see [Development Guide](DEVELOPMENT_GUIDE.md).* 