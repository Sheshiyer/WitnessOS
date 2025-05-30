# WitnessOS Divination Engines

> **Consciousness debugging and archetypal navigation through symbolic computation**

A modular collection of consciousness exploration and divination engines for the WitnessOS reality debugging framework. Includes a production-ready REST API for programmatic access to all engines and workflows.

## 🏗️ Project Structure

```
ENGINES/
├── README.md                    # This file - Project overview
├── start_api.py                 # Quick API server launcher
├── requirements.txt             # Python dependencies
├── __init__.py                  # Main package initialization and engine registry
│
├── api/                         # REST API Layer
│   ├── README.md                # 📡 API Documentation & Usage Guide
│   ├── main.py                  # FastAPI server with full configuration
│   ├── test_api.py              # Comprehensive API test suite
│   ├── endpoints.py             # All REST endpoints and request handlers
│   ├── formatters.py            # Output formatting (Standard, Mystical, WitnessOS)
│   └── middleware.py            # Authentication, rate limiting, CORS
│
├── base/                        # Foundation Architecture
│   ├── engine_interface.py      # Abstract base class for all engines
│   ├── data_models.py           # Pydantic models for standardized I/O
│   └── utils.py                 # Shared utilities and helper functions
│
├── calculations/                # Shared Calculation Modules
│   ├── astrology.py             # Swiss Ephemeris astronomical calculations
│   ├── biorhythm.py             # Sine wave mathematics for biorhythms
│   ├── numerology.py            # Pythagorean & Chaldean number systems
│   ├── divination.py            # Randomization and symbolic mapping
│   ├── sacred_geometry.py       # Mathematical pattern generation
│   └── sigil_generation.py      # Symbolic creation algorithms
│
├── engines/                     # Individual Engine Implementations
│   ├── numerology.py            # ✅ Numerology Field Extractor
│   ├── biorhythm.py             # ✅ Biorhythm Synchronizer
│   ├── human_design.py          # ✅ Human Design Scanner
│   ├── vimshottari.py           # ✅ Vimshottari Timeline Mapper
│   ├── tarot.py                 # ✅ Tarot Sequence Decoder
│   ├── iching.py                # ✅ I-Ching Mutation Oracle
│   ├── gene_keys.py             # ✅ Gene Keys Compass
│   ├── enneagram.py             # ✅ Enneagram Resonator
│   ├── sacred_geometry.py       # ✅ Sacred Geometry Mapper
│   ├── sigil_forge.py           # ✅ Sigil Forge Synthesizer
│   └── *_models.py              # Data models for each engine
│
├── integration/                 # Multi-Engine Workflows
│   ├── README.md                # Integration layer documentation
│   ├── orchestrator.py          # Engine coordination and parallel execution
│   ├── workflows.py             # Predefined multi-engine reading patterns
│   ├── synthesis.py             # Cross-engine result correlation
│   └── field_analyzer.py        # Consciousness field signature analysis
│
├── data/                        # Static Data Files
│   ├── astrology/               # Astronomical reference data
│   ├── tarot/                   # Tarot card definitions and spreads
│   ├── iching/                  # I-Ching hexagram data and interpretations
│   ├── gene_keys/               # Gene Keys archetypal mappings
│   ├── enneagram/               # Enneagram type definitions
│   ├── human_design/            # Human Design system data
│   └── sacred_geometry/         # Sacred geometry patterns and templates
│
├── tests/                       # Unit and Integration Tests
├── demos/                       # Demonstration Scripts
├── validation/                  # Validation Framework
├── research/                    # Research and Development Scripts
├── scripts/                     # Utility Scripts
└── docs/                        # Documentation
    ├── API_USAGE.md             # Extended API usage examples
    ├── TECHNICAL_SPECS.md       # Detailed engine specifications
    └── IMPLEMENTATION_ROADMAP.md # Development roadmap and progress
```

## 🎯 Current Status

### ✅ All Phases Complete!
- **Phase 1**: Foundation Architecture ✅
- **Phase 2**: Simple Engines (Numerology, Biorhythm) ✅
- **Phase 3**: Astronomical Engines (Human Design, Vimshottari) ✅
- **Phase 4**: Symbolic Engines (Tarot, I-Ching, Gene Keys) ✅
- **Phase 5**: Psychological Engines (Enneagram) ✅
- **Phase 6**: Creative/Generative Engines (Sacred Geometry, Sigil Forge) ✅
- **Phase 7**: Integration & API (Multi-engine workflows, REST API) ✅

### 🌟 Available Engines (10/10)
All divination engines are implemented and accessible via REST API:

| Engine | Status | Description |
|--------|--------|-------------|
| **Numerology** | ✅ | Life path, expression, soul urge calculations |
| **Biorhythm** | ✅ | Physical, emotional, intellectual cycles |
| **Human Design** | ✅ | Complete chart with type, strategy, authority |
| **Vimshottari** | ✅ | Vedic astrology dasha timeline |
| **Gene Keys** | ✅ | Genetic poetry and evolutionary codes |
| **Tarot** | ✅ | Archetypal guidance through card spreads |
| **I-Ching** | ✅ | Change pattern analysis and wisdom |
| **Enneagram** | ✅ | Personality type and integration analysis |
| **Sacred Geometry** | ✅ | Mathematical pattern generation |
| **Sigil Forge** | ✅ | Symbolic manifestation sigil creation |

## 🚀 Quick Start

### Option 1: REST API (Recommended)

```bash
# Install dependencies
pip install -r requirements.txt

# Start API server
python start_api.py --dev

# Test the API
python api/test_api.py --verbose

# Visit interactive docs
open http://localhost:8000/docs
```

### Option 2: Direct Python Usage

```python
from ENGINES import get_engine

# Get a specific engine
numerology = get_engine("numerology")

# Run calculation with your data
result = numerology.calculate({
    "full_name": "Your Name",
    "birth_date": "1991-08-13",
    "system": "pythagorean"
})

print(result.formatted_output)
```

### Option 3: Multi-Engine Workflow

```python
from ENGINES.integration.orchestrator import EngineOrchestrator

orchestrator = EngineOrchestrator()

# Run multiple engines
birth_data = {
    "name": "Your Name",
    "date": "13.08.1991",
    "time": "13:31",
    "location": "Bengaluru"
}

reading = orchestrator.create_comprehensive_reading(
    birth_data,
    engines=['numerology', 'biorhythm', 'human_design']
)
```

## 📡 REST API

The WitnessOS API provides programmatic access to all engines and workflows.

### Quick API Examples

```bash
# List available engines
curl http://localhost:8000/engines

# Run single engine
curl -X POST http://localhost:8000/engines/run \
  -H "Content-Type: application/json" \
  -d '{"engine_name": "numerology", "input_data": {...}}'

# Run multiple engines
curl -X POST http://localhost:8000/engines/multi \
  -H "Content-Type: application/json" \
  -d '{"engines": ["numerology", "biorhythm"], "birth_data": {...}}'
```

**📖 Full API Documentation**: [api/README.md](api/README.md)

## 🧪 Testing & Validation

### API Testing
```bash
python api/test_api.py --verbose
```

### Engine Testing
```bash
python -m pytest tests/
```

### Validation with Real Data
```bash
cd validation
python run_validation_tests.py
```

### Demo Scripts
```bash
cd demos
python demo_numerology.py
python demo_human_design.py
python demo_phase7_integration.py  # Multi-engine workflows
```

## 🔮 Validation Data

All engines tested with verified Human Design data:
- **Subject**: Cumbipuram Nateshan Sheshnarayan
- **Birth**: August 13, 1991, 13:31, Bengaluru, India
- **Known Chart**: 2/4 Generator, Sacral Authority, Split Definition

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[api/README.md](api/README.md)** | 📡 Complete API documentation and usage guide |
| **[docs/API_USAGE.md](docs/API_USAGE.md)** | Extended API examples and integration patterns |
| **[docs/TECHNICAL_SPECS.md](docs/TECHNICAL_SPECS.md)** | Detailed engine specifications and algorithms |
| **[integration/README.md](integration/README.md)** | Multi-engine workflows and field analysis |

## 🌟 Philosophy

These engines are designed as **consciousness exploration tools**, not prediction systems. They provide pattern recognition and archetypal guidance for conscious navigation of reality fields through symbolic computation.

## 🎯 Next Steps

1. **Start the API**: `python start_api.py --dev`
2. **Explore Documentation**: Visit http://localhost:8000/docs
3. **Test with Your Data**: Use the interactive API docs
4. **Build Applications**: Integrate the API into your projects
5. **Explore Workflows**: Try multi-engine consciousness debugging

---

**🌟 Ready for consciousness debugging through symbolic computation!**

*Part of the WitnessOS reality debugging framework*
