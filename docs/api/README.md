# WitnessOS API Documentation

This directory contains comprehensive documentation for all WitnessOS APIs.

## 📡 Available APIs

### Simple API (Port 8001)
**Purpose**: Demo and testing API with mock data  
**Documentation**: http://localhost:8001/docs  
**Use Case**: Frontend development, testing, demonstrations

### Production API (Port 8002)  
**Purpose**: Full-featured API with real engine calculations  
**Documentation**: http://localhost:8002/docs  
**Use Case**: Production applications, real divination calculations

### Agent API (Port 8003)
**Purpose**: AI-powered natural language interface  
**Documentation**: http://localhost:8003/docs  
**Use Case**: Natural language interpretation of calculation results

## 🚀 Quick Start

### Start All APIs
```bash
# Development mode (auto-reload)
python src/api/main.py --dev

# Production mode
python src/api/main.py

# Start specific API
python src/api/main.py --api simple
python src/api/main.py --api production  
python src/api/main.py --api agent
```

### Test APIs
```bash
# Test all APIs
python scripts/run_tests.py --type api

# Test specific endpoints
curl http://localhost:8001/
curl http://localhost:8002/engines
curl http://localhost:8003/health
```

## 📋 API Endpoints Overview

### Common Endpoints (All APIs)
- `GET /` - API information and status
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation
- `GET /redoc` - Alternative API documentation

### Engine Endpoints
- `GET /engines` - List available calculation engines
- `POST /engines/run` - Execute single engine calculation
- `POST /engines/multi` - Run multiple engines

### Workflow Endpoints  
- `GET /workflows` - List predefined workflows
- `POST /workflows/run` - Execute complete workflow

### Advanced Features (Production API)
- `POST /field-analysis` - Consciousness field analysis
- `POST /synthesis` - Multi-engine result synthesis

### AI Features (Agent API)
- `POST /interpret` - Natural language interpretation
- `POST /explain` - Detailed explanations
- `POST /synthesize` - AI-powered synthesis

## 🔧 Configuration

### Environment Variables
```bash
# API Ports
SIMPLE_API_PORT=8001
PRODUCTION_API_PORT=8002  
AGENT_API_PORT=8003

# AI Configuration
OPENROUTER_API_KEY=your_key_here

# Development
DEBUG=true
LOG_LEVEL=INFO
```

### API Keys
The Agent API requires an OpenRouter API key for AI functionality. Set this in your `.env` file or environment variables.

## 📊 Response Formats

### Standard Response
```json
{
  "status": "success",
  "data": {...},
  "timestamp": "2024-01-01T00:00:00Z",
  "engine": "engine_name"
}
```

### Error Response
```json
{
  "status": "error", 
  "error": "Error description",
  "code": "ERROR_CODE",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Mystical Format (WitnessOS Style)
```json
{
  "field_signature": "...",
  "consciousness_state": "...",
  "archetypal_patterns": [...],
  "guidance": "...",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 🧪 Testing

### Manual Testing
Use the interactive documentation at `/docs` endpoints for manual testing.

### Automated Testing  
```bash
# Run API tests
python scripts/run_tests.py --type api

# Run with coverage
python scripts/run_tests.py --type api --coverage
```

### Load Testing
```bash
# Install locust
pip install locust

# Run load tests (coming soon)
locust -f tests/load/locustfile.py
```

## 🔒 Security

### Rate Limiting
- Simple API: 100 requests/minute
- Production API: 60 requests/minute  
- Agent API: 30 requests/minute

### Authentication
Currently using API key authentication for Agent API. Full authentication system coming soon.

### CORS
All APIs are configured with CORS for development. Production deployment should restrict origins.

## 📈 Monitoring

### Health Checks
All APIs provide health check endpoints for monitoring:
- `GET /health` - Basic health status
- `GET /health/detailed` - Detailed system status

### Logging
Structured logging is available at different levels:
- `DEBUG` - Detailed debugging information
- `INFO` - General operational information  
- `WARNING` - Warning conditions
- `ERROR` - Error conditions

---

*For detailed endpoint documentation, visit the interactive docs at `/docs` for each API.*