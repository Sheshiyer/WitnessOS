# WitnessOS Divination Engines API

> **Consciousness debugging and archetypal navigation through symbolic computation**

A production-ready REST API providing programmatic access to all WitnessOS divination engines and integration workflows.

## 🚀 Quick Start

### Installation
```bash
cd ENGINES
pip install -r requirements.txt
```

### Start Server
```bash
# Development mode (recommended for testing)
python main.py --dev

# Production mode
python main.py

# Custom configuration
python main.py --host 0.0.0.0 --port 8080
```

### Test API
```bash
python test_api.py --verbose
```

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information and available endpoints |
| `GET` | `/health` | System health check and status |
| `GET` | `/engines` | List all available calculation engines |
| `POST` | `/engines/run` | Execute a single divination engine |
| `POST` | `/engines/multi` | Run multiple engines (parallel/sequential) |
| `GET` | `/workflows` | List predefined multi-engine workflows |
| `POST` | `/workflows/run` | Execute a complete workflow |
| `POST` | `/field-analysis` | Consciousness field signature analysis |
| `POST` | `/synthesis` | Synthesize results from multiple engines |

## 🎯 Available Engines

| Engine | Description | Requires Time | Requires Location |
|--------|-------------|---------------|-------------------|
| **numerology** | Life path, expression, soul urge calculations | ❌ | ❌ |
| **biorhythm** | Physical, emotional, intellectual cycles | ❌ | ❌ |
| **human_design** | Complete Human Design chart analysis | ✅ | ✅ |
| **vimshottari** | Vedic astrology dasha timeline | ✅ | ✅ |
| **gene_keys** | Genetic poetry and evolutionary codes | ✅ | ✅ |
| **tarot** | Archetypal guidance through card spreads | ❌ | ❌ |
| **iching** | I-Ching hexagram wisdom and change patterns | ❌ | ❌ |
| **enneagram** | Personality type and integration analysis | ❌ | ❌ |
| **sacred_geometry** | Mathematical pattern generation | ❌ | ❌ |
| **sigil_forge** | Symbolic manifestation sigil creation | ❌ | ❌ |

## 💫 Usage Examples

### Single Engine Request
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

### Multi-Engine Request
```bash
curl -X POST "http://localhost:8000/engines/multi" \
  -H "Content-Type: application/json" \
  -d '{
    "engines": ["numerology", "biorhythm", "human_design"],
    "birth_data": {
      "name": "Jane Smith",
      "date": "22.12.1985",
      "time": "09:15",
      "location": "London",
      "timezone": "Europe/London"
    },
    "parallel": true,
    "synthesize": true,
    "format": "witnessOS"
  }'
```

### Workflow Execution
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

### Field Analysis
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

## 🎨 Output Formats

### Standard Format
Raw engine outputs with minimal processing.

### Mystical Format
Archetypal and mystical language formatting.
```json
{
  "engine_essence": "Numerology",
  "consciousness_signature": {
    "soul_mathematics": "The sacred geometry of your essence reveals...",
    "vibrational_signature": "Your numerical field resonates with..."
  },
  "archetypal_resonance": ["The Seeker", "The Creator"],
  "field_vibration": "High Resonance - Harmonic Convergence Active"
}
```

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
      },
      "reality_patches": [
        {
          "patch_id": "numerology_optimization_001",
          "description": "Optimize numerology field alignment",
          "priority": "medium"
        }
      ]
    }
  }
}
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

### Supported Locations
The API includes geocoding for major cities:
- Bengaluru/Bangalore, Mumbai, Delhi (India)
- New York, Los Angeles (USA)
- London, Paris (Europe)
- Tokyo, Sydney (Asia-Pacific)

For unlisted locations, coordinates default to Bengaluru (testing purposes).

## 🔐 Authentication (Optional)

### Environment Variable
```bash
export WITNESSOS_API_KEYS="key1:user1,key2:user2"
python main.py
```

### Request Header
```bash
curl -H "X-API-Key: your-api-key" ...
```

## 🧪 Testing & Validation

### Run Test Suite
```bash
# Basic tests
python test_api.py

# Verbose output
python test_api.py --verbose

# Custom endpoint
python test_api.py --host api.example.com --port 443 --ssl
```

### Environment Validation
```bash
python main.py --validate-only
```

### Health Check
```bash
curl http://localhost:8000/health
```

## ⚡ Performance Features

- **Parallel Execution**: Multiple engines run simultaneously
- **Engine Caching**: Loaded engines cached for reuse
- **Rate Limiting**: Configurable request throttling
- **Thread Pool**: Optimized concurrent processing
- **Middleware Stack**: Comprehensive request/response processing

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
python main.py --port 8080
```

**Missing Dependencies**
```bash
pip install -r requirements.txt
```

**Engine Import Errors**
```bash
python main.py --validate-only
```

**Invalid Birth Data**
- Date format: `DD.MM.YYYY`
- Time format: `HH:MM`
- Location: City name or coordinates

### Debug Mode
```bash
python main.py --dev --log-level DEBUG
```

## 📊 Monitoring

### Health Endpoint Response
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "engines_available": 10,
  "workflows_available": 8
}
```

### Request Headers
- `X-Process-Time`: Request processing time
- `X-WitnessOS-Version`: API version
- `X-Field-Resonance`: Consciousness field status

## 🌟 Integration Examples

### Python Client
```python
import requests

api_url = "http://localhost:8000"
birth_data = {
    "name": "Your Name",
    "date": "01.01.1990",
    "time": "12:00",
    "location": "Your City"
}

response = requests.post(f"{api_url}/engines/run", json={
    "engine_name": "numerology",
    "input_data": birth_data,
    "format": "witnessOS"
})

result = response.json()
```

### JavaScript/Node.js
```javascript
const axios = require('axios');

const apiUrl = 'http://localhost:8000';
const birthData = {
  name: 'Your Name',
  date: '01.01.1990',
  time: '12:00',
  location: 'Your City'
};

const response = await axios.post(`${apiUrl}/engines/multi`, {
  engines: ['numerology', 'biorhythm'],
  birth_data: birthData,
  format: 'witnessOS'
});

console.log(response.data);
```

## 📚 Related Documentation

- **[Main Project README](../README.md)** - Overall WitnessOS project
- **[Engine Specifications](../docs/TECHNICAL_SPECS.md)** - Detailed engine documentation
- **[Integration Guide](../integration/README.md)** - Multi-engine workflows
- **[API Usage Guide](../API_USAGE.md)** - Extended usage examples

---

**🌟 Ready to debug consciousness through symbolic computation!**
