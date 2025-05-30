# WitnessOS Backend Setup Guide

This guide covers setting up and running the WitnessOS backend APIs.

## 🏗️ Architecture Overview

WitnessOS consists of three main API layers:

1. **Simple API** (Port 8001) - Demo API with mock data for testing
2. **Production API** (Port 8002) - Full-featured API with real engine calculations  
3. **Agent API** (Port 8003) - AI-powered natural language interface

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Navigate to ENGINES directory
cd ENGINES

# Run the setup script
python setup_environment.py
```

This will:
- Check Python version and dependencies
- Create `.env` file from template
- Validate configuration
- Check port availability

### 2. Configure OpenRouter API Key

Edit the `.env` file and add your OpenRouter API key:

```bash
# Get your API key from: https://openrouter.ai/keys
OPENROUTER_API_KEY=your_actual_api_key_here
```

### 3. Start All APIs

```bash
# Start all APIs at once
python start_all_apis.py

# Or start individual APIs
python start_all_apis.py --api simple      # Simple API only
python start_all_apis.py --api production  # Production API only  
python start_all_apis.py --api agent       # Agent API only
```

### 4. Verify Setup

Check API status:
```bash
python start_all_apis.py --status
```

## 📡 API Endpoints

### Simple API (Port 8001)
- **Base URL**: http://localhost:8001
- **Documentation**: http://localhost:8001/docs
- **Purpose**: Demo API with mock data for testing

### Production API (Port 8002)  
- **Base URL**: http://localhost:8002
- **Versioned URL**: http://localhost:8002/v1/
- **Documentation**: http://localhost:8002/v1/docs
- **Purpose**: Production API with real engine calculations

### Agent API (Port 8003)
- **Base URL**: http://localhost:8003/agent/
- **Documentation**: http://localhost:8003/agent/docs
- **Purpose**: AI-powered natural language interface

## 🔧 Manual API Startup

If you prefer to start APIs individually:

```bash
# Simple API
python simple_api.py

# Production API  
python api/production_api.py

# Agent API
python agent/start_agent.py
```

## 🩺 Health Checks

Each API provides health check endpoints:

```bash
# Simple API
curl http://localhost:8001/health

# Production API
curl http://localhost:8002/v1/health

# Agent API  
curl http://localhost:8003/agent/health
```

## 🐛 Troubleshooting

### Common Issues

**1. OpenRouter API Key Not Configured**
```
Error: OpenRouter API key not configured
Solution: Edit .env file and set OPENROUTER_API_KEY
```

**2. Port Already in Use**
```
Error: Port 8001 is already in use
Solution: Stop existing process or use different port
```

**3. Import Errors**
```
Error: ModuleNotFoundError
Solution: Install dependencies with pip install -r requirements.txt
```

**4. Agent API 503 Errors**
```
Error: Service Unavailable
Solution: Configure OpenRouter API key in .env file
```

### Debug Commands

```bash
# Check environment
python setup_environment.py

# Check API status
python start_all_apis.py --status

# Stop all APIs
python start_all_apis.py --stop

# Test individual components
python agent/quick_local_test.py
```

## 📁 File Structure

```
ENGINES/
├── .env.template              # Environment template
├── .env                       # Your environment config
├── setup_environment.py       # Environment setup script
├── start_all_apis.py          # Multi-API manager
├── simple_api.py              # Simple demo API
├── api/
│   ├── production_api.py      # Production API
│   └── simple_api.py          # Alternative simple API
└── agent/
    ├── start_agent.py         # Agent API startup
    └── agent_api.py           # Agent API implementation
```

## 🔐 Security Notes

- The `.env` file contains sensitive API keys - never commit it to version control
- APIs run on localhost by default for security
- Production deployment requires additional security configuration

## 📚 Next Steps

Once the backend is running:

1. Test the APIs using the interactive documentation
2. Try the AI agent with natural language queries
3. Explore the engine calculations with your birth data
4. Check the frontend documentation for UI setup
