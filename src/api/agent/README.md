# WitnessOS AI Agent Layer

An intelligent agent layer that sits above the WitnessOS production API, providing natural language interpretation and contextual explanations of divination engine calculations using advanced language models via OpenRouter.

## 🌟 Features

- **Natural Language Translation**: Converts technical calculation outputs into human-readable wisdom
- **Dynamic LLM Model Selection**: Choose optimal models for different interpretation tasks
- **WitnessOS Consciousness Framework**: Maintains mystical-technical balance in explanations
- **Multi-Engine Synthesis**: Correlates insights across multiple divination systems
- **Archetypal Pattern Interpretation**: Identifies and explains archetypal themes
- **Reality Patch Generation**: Provides actionable consciousness optimization suggestions

## 🏗️ Architecture

```
WitnessOS AI Agent Layer
├── agent_service.py         # Main agent service
├── openrouter_client.py     # OpenRouter API integration
├── prompt_templates.py      # Scaffolding system prompts
├── response_formatter.py    # WitnessOS response formatting
├── agent_api.py            # FastAPI endpoints
├── start_agent.py          # Startup script
├── demo_agent.py           # Demo and testing
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Set your OpenRouter API key
export OPENROUTER_API_KEY="your_openrouter_api_key_here"

# Optional: Set production API URL (defaults to localhost:8002)
export WITNESSOS_PRODUCTION_API_URL="http://localhost:8002"
```

### 2. Install Dependencies

```bash
# Install required packages
pip install httpx fastapi uvicorn pydantic
```

### 3. Start the Production API

```bash
# Start the WitnessOS production API first
cd ENGINES
python api/production_api.py --port 8002
```

### 4. Start the Agent API

```bash
# Start the AI agent API
cd ENGINES/agent
python start_agent.py --port 8003
```

### 5. Access the API

- **Agent API**: http://localhost:8003/agent/
- **Documentation**: http://localhost:8003/agent/docs
- **Health Check**: http://localhost:8003/agent/health

## 🎯 Available Models

The agent supports multiple LLM models via OpenRouter:

- **fast**: `openrouter/google/gemini-2.0-flash-001` - Quick interpretations
- **balanced**: `deepseek/deepseek-chat` - Comprehensive explanations
- **creative**: `openrouter/deepseek/deepseek-r1-distill-qwen-32b` - Mystical interpretations
- **reasoning**: `deepseek/deepseek-reasoner` - Complex synthesis and analysis

## 📖 Usage Examples

### Single Engine Interpretation

```python
import asyncio
from agent.agent_service import WitnessOSAgent

async def example():
    agent = WitnessOSAgent()
    
    birth_data = {
        "name": "John Doe",
        "date": "15.06.1990",
        "time": "14:30",
        "location": "New York",
        "timezone": "America/New_York"
    }
    
    result = await agent.interpret_single_engine(
        engine_name="numerology",
        birth_data=birth_data,
        interpretation_style="balanced",
        model_type="balanced"
    )
    
    print(result["consciousness_interpretation"]["ai_guidance"])

asyncio.run(example())
```

### Multi-Engine Analysis

```python
async def multi_engine_example():
    agent = WitnessOSAgent()
    
    result = await agent.interpret_multi_engine(
        engines=["numerology", "human_design", "gene_keys"],
        birth_data=birth_data,
        interpretation_style="witnessOS",
        include_synthesis=True
    )
    
    # Access synthesis
    synthesis = result["consciousness_synthesis"]["unified_field_analysis"]
    print(synthesis)

asyncio.run(multi_engine_example())
```

### API Requests

```bash
# Single engine interpretation
curl -X POST "http://localhost:8003/agent/interpret/single" \
  -H "Content-Type: application/json" \
  -d '{
    "engine_name": "numerology",
    "birth_data": {
      "name": "John Doe",
      "date": "15.06.1990",
      "time": "14:30",
      "location": "New York"
    },
    "interpretation_style": "balanced"
  }'

# Multi-engine analysis
curl -X POST "http://localhost:8003/agent/interpret/multi" \
  -H "Content-Type: application/json" \
  -d '{
    "engines": ["numerology", "biorhythm"],
    "birth_data": {
      "name": "John Doe",
      "date": "15.06.1990",
      "time": "14:30",
      "location": "New York"
    },
    "interpretation_style": "witnessOS",
    "include_synthesis": true
  }'
```

## 🎨 Interpretation Styles

- **technical**: Precise, scientific explanations
- **mystical**: Poetic, archetypal interpretations
- **witnessOS**: Consciousness debugging framework
- **balanced**: Mystical-technical balance (default)

## 🔧 Configuration

### Environment Variables

- `OPENROUTER_API_KEY`: Your OpenRouter API key (required)
- `WITNESSOS_PRODUCTION_API_URL`: Production API URL (default: http://localhost:8002)

### Model Selection

The agent automatically selects optimal models based on task type:

- **Interpretation tasks**: `balanced` model
- **Synthesis tasks**: `reasoning` model  
- **Creative tasks**: `creative` model
- **Quick responses**: `fast` model

## 🧪 Testing

Run the demo script to test all agent capabilities:

```bash
cd ENGINES/agent
python demo_agent.py
```

The demo will test:
- Single engine interpretation
- Multi-engine analysis with synthesis
- Workflow interpretation
- Different model types

## 🌊 Integration with WitnessOS

The agent maintains WitnessOS's core principles:

- **Mystical-Technical Balance**: Blends precision with spiritual insight
- **Consciousness Framework**: Uses WitnessOS terminology naturally
- **Archetypal Navigation**: Identifies and explains archetypal patterns
- **Reality Patches**: Provides actionable consciousness optimization
- **Witness Protocol**: Guides awareness cultivation practices

## 🔍 Response Format

Agent responses follow the WitnessOS consciousness framework:

```json
{
  "consciousness_session": {
    "session_type": "single_engine_interpretation",
    "engine_deployed": "numerology",
    "subject_profile": {...},
    "field_coherence": 0.85
  },
  "calculation_data": {
    "engine": "numerology",
    "raw_results": {...},
    "field_signature": "NUMEROLOGY_FIELD_ACTIVE_COHERENT"
  },
  "consciousness_interpretation": {
    "ai_guidance": "Your life path reveals...",
    "archetypal_resonance": ["Seeker", "Creator"],
    "integration_pathway": [...]
  },
  "witness_protocol": {
    "awareness_cultivation": [...],
    "reality_patches": [...],
    "next_steps": [...]
  }
}
```

## 🚨 Error Handling

The agent includes comprehensive error handling:

- OpenRouter API failures
- Production API connectivity issues
- Invalid birth data
- Model selection errors
- Response formatting errors

## 📊 Monitoring

- Health check endpoint: `/agent/health`
- Status endpoint: `/agent/status`
- Model information: `/agent/models`
- Available engines: `/agent/engines`

## 🔮 Future Enhancements

- Streaming responses for real-time interpretation
- Custom prompt template creation
- Advanced semantic analysis for correlations
- Integration with vector databases for context
- Multi-language support
- Voice-based interpretations

---

*The WitnessOS AI Agent bridges the gap between precise symbolic computation and profound spiritual insight, maintaining the mystical-technical balance that defines the WitnessOS consciousness debugging experience.*
