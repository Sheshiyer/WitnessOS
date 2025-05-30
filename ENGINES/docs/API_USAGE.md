# WitnessOS Divination Engines API Usage Guide

## 🌟 Overview

The WitnessOS API provides REST endpoints for accessing all divination engines and integration workflows. This guide covers installation, startup, and usage examples.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ENGINES
pip install -r requirements.txt
```

### 2. Start the API Server

```bash
# Basic startup
python main.py

# Development mode (no rate limiting, CORS enabled)
python main.py --dev

# Custom port
python main.py --port 8080

# Custom host (listen on all interfaces)
python main.py --host 0.0.0.0 --port 8000
```

### 3. Access Documentation

- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📡 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and endpoint listing |
| GET | `/health` | Health check and system status |
| GET | `/engines` | List all available engines |
| POST | `/engines/run` | Run a single engine |
| POST | `/engines/multi` | Run multiple engines |
| GET | `/workflows` | List available workflows |
| POST | `/workflows/run` | Execute predefined workflow |
| POST | `/field-analysis` | Analyze consciousness field |
| POST | `/synthesis` | Synthesize engine results |

## 🎯 Usage Examples

### List Available Engines

```bash
curl -X GET "http://localhost:8000/engines"
```

**Response:**
```json
{
  "available_engines": ["numerology", "biorhythm", "human_design", "vimshottari"],
  "count": 4,
  "timestamp": "2024-01-15T10:30:00"
}
```

### Run Single Engine

```bash
curl -X POST "http://localhost:8000/engines/run" \
  -H "Content-Type: application/json" \
  -d '{
    "engine_name": "numerology",
    "input_data": {
      "name": "John Doe",
      "date": "15.05.1990",
      "time": "14:30",
      "location": "New York"
    },
    "format": "witnessOS"
  }'
```

### Run Multiple Engines

```bash
curl -X POST "http://localhost:8000/engines/multi" \
  -H "Content-Type: application/json" \
  -d '{
    "engines": ["numerology", "biorhythm"],
    "birth_data": {
      "name": "Jane Smith",
      "date": "22.12.1985",
      "time": "09:15",
      "location": "London"
    },
    "parallel": true,
    "synthesize": true,
    "format": "witnessOS"
  }'
```

### Execute Workflow

```bash
curl -X POST "http://localhost:8000/workflows/run" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_name": "complete_natal",
    "birth_data": {
      "name": "Alex Johnson",
      "date": "08.03.1992",
      "time": "16:45",
      "location": "Sydney"
    },
    "format": "witnessOS"
  }'
```

### Consciousness Field Analysis

```bash
curl -X POST "http://localhost:8000/field-analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "name": "Maria Garcia",
      "date": "11.07.1988",
      "time": "11:20",
      "location": "Madrid"
    },
    "engines": ["numerology", "human_design", "gene_keys"],
    "analysis_depth": "deep"
  }'
```

## 🔧 Input Data Format

### Birth Data Structure

```json
{
  "name": "Full Birth Name",
  "date": "DD.MM.YYYY",
  "time": "HH:MM",
  "location": "City Name",
  "timezone": "Timezone/Region"
}
```

### Engine-Specific Requirements

| Engine | Requires Time | Requires Location | Notes |
|--------|---------------|-------------------|-------|
| Numerology | No | No | Name and birth date only |
| Biorhythm | No | No | Birth date for cycle calculation |
| Human Design | Yes | Yes | Exact time and coordinates required |
| Vimshottari | Yes | Yes | Vedic astrology calculations |
| Gene Keys | Yes | Yes | Based on Human Design |
| Tarot | No | No | Question-based divination |
| I-Ching | No | No | Symbolic guidance |
| Enneagram | No | No | Personality analysis |

## 🎨 Output Formats

### Standard Format
Raw engine outputs with minimal processing.

### Mystical Format
Archetypal and mystical language formatting.

### WitnessOS Format (Recommended)
Consciousness debugging and field analysis format.

```json
{
  "consciousness_scan": {
    "subject_id": "John Doe",
    "scan_timestamp": "2024-01-15T10:30:00",
    "engines_deployed": ["numerology", "biorhythm"],
    "field_coherence": 0.78,
    "debug_status": "COMPLETE"
  },
  "engine_outputs": {
    "numerology": {
      "consciousness_debug": {
        "numerical_field_analysis": "Core frequency patterns identified",
        "reality_creation_codes": "Manifestation algorithms extracted"
      }
    }
  }
}
```

## 🔐 Authentication (Optional)

Set API keys via environment variable:

```bash
export WITNESSOS_API_KEYS="key1:user1,key2:user2"
python main.py
```

Include API key in requests:

```bash
curl -X POST "http://localhost:8000/engines/run" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '...'
```

## 🧪 Testing

### Run API Tests

```bash
# Test against default localhost:8000
python test_api.py

# Test with verbose output
python test_api.py --verbose

# Test against custom endpoint
python test_api.py --host api.example.com --port 443 --ssl
```

### Validate Environment

```bash
# Check if all engines are working
python main.py --validate-only
```

## ⚡ Performance Tips

1. **Use Parallel Execution**: Set `"parallel": true` for multi-engine requests
2. **Cache Results**: Identical birth data will produce identical results
3. **Limit Engines**: Only request engines you need for better performance
4. **Use Appropriate Format**: WitnessOS format provides the richest output

## 🐛 Troubleshooting

### Common Issues

1. **Missing Dependencies**: Run `pip install -r requirements.txt`
2. **Port Already in Use**: Use `--port` to specify different port
3. **Engine Import Errors**: Check that all engine files are present
4. **Invalid Birth Data**: Ensure date format is DD.MM.YYYY and time is HH:MM

### Debug Mode

```bash
python main.py --dev --log-level DEBUG
```

### Health Check

```bash
curl http://localhost:8000/health
```

## 📚 Advanced Usage

### Custom Middleware Configuration

```python
from ENGINES.api.endpoints import app
from ENGINES.api.middleware import setup_middleware

config = {
    "cors_origins": ["https://myapp.com"],
    "rate_limit": 120,
    "api_keys": {"secret-key": "admin-user"}
}

setup_middleware(app, config)
```

### Integration with Other Applications

The API can be easily integrated into web applications, mobile apps, or other services that need divination calculations.

## 🌟 Next Steps

1. **Explore Interactive Docs**: Visit `/docs` for hands-on API exploration
2. **Try Different Engines**: Each engine provides unique insights
3. **Use Workflows**: Pre-configured multi-engine readings
4. **Implement Field Analysis**: Deep consciousness debugging capabilities

For more information, see the main WitnessOS documentation and engine specifications.
