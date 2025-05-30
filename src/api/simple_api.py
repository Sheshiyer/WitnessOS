#!/usr/bin/env python3
"""
Simple WitnessOS API Server

A simplified version of the WitnessOS API that works without complex imports.
This demonstrates the API structure and endpoints for testing purposes.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="WitnessOS Divination Engines API",
    description="Consciousness debugging and archetypal navigation through symbolic computation",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API
class BirthData(BaseModel):
    name: str = Field(..., description="Full birth name")
    date: str = Field(..., description="Birth date (DD.MM.YYYY)")
    time: str = Field(..., description="Birth time (HH:MM)")
    location: str = Field(..., description="Birth location")
    timezone: Optional[str] = Field(None, description="Timezone (optional)")

class EngineRequest(BaseModel):
    engine_name: str = Field(..., description="Name of the engine to run")
    input_data: Dict[str, Any] = Field(..., description="Input data for the engine")
    config: Optional[Dict[str, Any]] = Field(None, description="Optional engine configuration")
    format: Optional[str] = Field("standard", description="Output format: standard, mystical, witnessOS")

class MultiEngineRequest(BaseModel):
    engines: List[str] = Field(..., description="List of engines to run")
    birth_data: BirthData = Field(..., description="Birth data")
    parallel: bool = Field(True, description="Run engines in parallel")
    synthesize: bool = Field(True, description="Include synthesis")
    format: Optional[str] = Field("witnessOS", description="Output format")

# Available engines (mock data for demo)
AVAILABLE_ENGINES = [
    "numerology", "biorhythm", "human_design", "vimshottari", 
    "gene_keys", "tarot", "iching", "enneagram", 
    "sacred_geometry", "sigil_forge"
]

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "WitnessOS Divination Engines API",
        "version": "0.1.0",
        "description": "Consciousness debugging through symbolic computation",
        "status": "Demo Mode - Simplified API for testing",
        "endpoints": {
            "engines": "/engines",
            "workflows": "/workflows", 
            "field_analysis": "/field-analysis",
            "documentation": "/docs"
        }
    }

# Engine endpoints
@app.get("/engines")
async def list_engines():
    """List all available engines"""
    return {
        "available_engines": AVAILABLE_ENGINES,
        "count": len(AVAILABLE_ENGINES),
        "timestamp": datetime.now().isoformat(),
        "note": "Demo mode - engines return mock data"
    }

@app.post("/engines/run")
async def run_single_engine(request: EngineRequest):
    """Run a single engine (demo mode)"""
    if request.engine_name not in AVAILABLE_ENGINES:
        raise HTTPException(
            status_code=400, 
            detail=f"Engine '{request.engine_name}' not available. Available engines: {AVAILABLE_ENGINES}"
        )
    
    # Mock response for demo
    mock_result = {
        "engine": request.engine_name,
        "result": {
            "consciousness_debug": {
                f"{request.engine_name}_field_analysis": f"Mock {request.engine_name} analysis complete",
                "reality_creation_codes": f"Mock {request.engine_name} patterns identified",
                "field_signature": f"{request.engine_name.upper()}_FIELD_ACTIVE_RESONANCE_HIGH"
            },
            "interpretation": f"This is a mock {request.engine_name} reading for demonstration purposes.",
            "recommendations": [
                f"Explore {request.engine_name} patterns in your daily life",
                f"Meditate on {request.engine_name} insights",
                "Trust the unfolding process"
            ],
            "confidence": 0.95
        },
        "timestamp": datetime.now().isoformat(),
        "format": request.format,
        "demo_mode": True
    }
    
    return mock_result

@app.post("/engines/multi")
async def run_multiple_engines(request: MultiEngineRequest):
    """Run multiple engines (demo mode)"""
    # Validate engines
    invalid_engines = [e for e in request.engines if e not in AVAILABLE_ENGINES]
    if invalid_engines:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid engines: {invalid_engines}. Available: {AVAILABLE_ENGINES}"
        )
    
    # Mock multi-engine response
    results = {}
    for engine in request.engines:
        results[engine] = {
            "consciousness_debug": {
                f"{engine}_field_analysis": f"Mock {engine} analysis complete",
                "reality_creation_codes": f"Mock {engine} patterns identified"
            },
            "field_signature": f"{engine.upper()}_FIELD_ACTIVE",
            "confidence": 0.90 + (len(engine) % 10) * 0.01  # Vary confidence slightly
        }
    
    mock_response = {
        "engines": request.engines,
        "birth_data": request.birth_data.model_dump(),
        "results": {
            "consciousness_scan": {
                "subject_id": request.birth_data.name,
                "scan_timestamp": datetime.now().isoformat(),
                "engines_deployed": request.engines,
                "field_coherence": 0.78,
                "debug_status": "COMPLETE"
            },
            "engine_outputs": results,
            "synthesis": {
                "field_correlation_analysis": "High coherence detected across all engines",
                "consciousness_integration_map": ["Seeker", "Creator", "Transformer"],
                "reality_optimization_protocol": ["Align with natural timing", "Trust intuitive guidance"]
            } if request.synthesize else None
        },
        "timestamp": datetime.now().isoformat(),
        "parallel_execution": request.parallel,
        "demo_mode": True
    }
    
    return mock_response

@app.get("/workflows")
async def list_workflows():
    """List available workflows (demo mode)"""
    workflows = [
        "complete_natal", "relationship_compatibility", "career_guidance",
        "spiritual_development", "life_transition", "daily_guidance",
        "shadow_work", "manifestation_timing"
    ]
    
    return {
        "available_workflows": workflows,
        "count": len(workflows),
        "timestamp": datetime.now().isoformat(),
        "demo_mode": True
    }

@app.post("/field-analysis")
async def analyze_consciousness_field(birth_data: BirthData):
    """Analyze consciousness field signature (demo mode)"""
    mock_analysis = {
        "field_analysis": {
            "field_diagnostic": {
                "analysis_depth": "standard",
                "field_coherence": {"overall": 0.82, "stability": 0.75},
                "consciousness_level": {"awareness": "expanding", "integration": "active"},
                "evolution_vector": {"direction": "ascending", "velocity": "moderate"},
                "diagnostic_timestamp": datetime.now().isoformat()
            },
            "reality_patches": [
                {
                    "patch_id": "consciousness_optimization_001",
                    "description": "Enhance awareness practices",
                    "priority": "high"
                }
            ],
            "consciousness_map": {
                "primary_patterns": ["Seeker", "Creator"],
                "secondary_influences": ["Transformer", "Healer"],
                "integration_points": ["Heart-Mind", "Intuition-Logic"]
            },
            "witness_recommendations": [
                "Cultivate witness consciousness",
                "Observe patterns without attachment",
                "Trust the intelligence of awareness"
            ]
        },
        "engines_analyzed": ["numerology", "biorhythm", "human_design"],
        "analysis_depth": "standard",
        "timestamp": datetime.now().isoformat(),
        "demo_mode": True
    }
    
    return mock_analysis

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "engines_available": len(AVAILABLE_ENGINES),
        "workflows_available": 8,
        "demo_mode": True,
        "message": "WitnessOS API is running in demo mode"
    }

if __name__ == "__main__":
    import uvicorn
    print("🌟 Starting WitnessOS Simple API Demo")
    print("🌐 Server: http://localhost:8001")
    print("📚 Documentation: http://localhost:8001/docs")
    print("⚠️  Demo Mode: Returns mock data for testing")

    uvicorn.run(
        "simple_api:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
