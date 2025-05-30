"""
FastAPI Endpoints for WitnessOS Engines

Provides REST API endpoints for all engines and integration workflows.
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime, date
import logging

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from integration.orchestrator import EngineOrchestrator
from integration.workflows import WorkflowManager
from integration.field_analyzer import FieldAnalyzer
from integration.synthesis import ResultSynthesizer
from formatters import MysticalFormatter, WitnessOSFormatter
from middleware import setup_middleware

# Initialize FastAPI app
app = FastAPI(
    title="WitnessOS Divination Engines API",
    description="Consciousness debugging and archetypal navigation through symbolic computation",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup middleware
setup_middleware(app)

# Initialize components
orchestrator = EngineOrchestrator()
workflow_manager = WorkflowManager()
field_analyzer = FieldAnalyzer()
synthesizer = ResultSynthesizer()
mystical_formatter = MysticalFormatter()
witnessOS_formatter = WitnessOSFormatter()

logger = logging.getLogger(__name__)

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

class WorkflowRequest(BaseModel):
    workflow_name: str = Field(..., description="Name of the workflow to run")
    birth_data: BirthData = Field(..., description="Birth data for the reading")
    options: Optional[Dict[str, Any]] = Field({}, description="Workflow options")
    format: Optional[str] = Field("witnessOS", description="Output format")

class MultiEngineRequest(BaseModel):
    engines: List[str] = Field(..., description="List of engines to run")
    birth_data: BirthData = Field(..., description="Birth data")
    parallel: bool = Field(True, description="Run engines in parallel")
    synthesize: bool = Field(True, description="Include synthesis")
    format: Optional[str] = Field("witnessOS", description="Output format")

class FieldAnalysisRequest(BaseModel):
    birth_data: BirthData = Field(..., description="Birth data")
    engines: Optional[List[str]] = Field(None, description="Engines to include (default: all)")
    analysis_depth: str = Field("standard", description="Analysis depth: basic, standard, deep")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "WitnessOS Divination Engines API",
        "version": "0.1.0",
        "description": "Consciousness debugging through symbolic computation",
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
    try:
        engines = orchestrator.get_available_engines()
        return {
            "available_engines": engines,
            "count": len(engines),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error listing engines: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/engines/run")
async def run_single_engine(request: EngineRequest):
    """Run a single engine"""
    try:
        # Convert input data to appropriate format
        # This would need proper input model conversion based on engine type
        result = orchestrator.run_single_engine(
            request.engine_name, 
            request.input_data, 
            request.config
        )
        
        # Format output based on request
        if request.format == "mystical":
            formatted_result = mystical_formatter.format_engine_result(result, request.engine_name)
        elif request.format == "witnessOS":
            formatted_result = witnessOS_formatter.format_engine_result(result, request.engine_name)
        else:
            formatted_result = result
        
        return {
            "engine": request.engine_name,
            "result": formatted_result,
            "timestamp": datetime.now().isoformat(),
            "format": request.format
        }
        
    except Exception as e:
        logger.error(f"Error running engine {request.engine_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/engines/multi")
async def run_multiple_engines(request: MultiEngineRequest):
    """Run multiple engines"""
    try:
        # Prepare engine configurations
        engine_configs = []
        for engine_name in request.engines:
            # Convert birth data to appropriate input format for each engine
            input_data = _convert_birth_data_to_engine_input(request.birth_data, engine_name)
            engine_configs.append({
                'name': engine_name,
                'input': input_data
            })
        
        # Run engines
        if request.parallel:
            results = orchestrator.run_parallel_engines(engine_configs)
        else:
            results = orchestrator.run_sequential_engines(engine_configs)
        
        # Synthesize if requested
        synthesis = None
        if request.synthesize:
            synthesis = synthesizer.synthesize_reading(results)
        
        # Format output
        if request.format == "witnessOS":
            formatted_results = witnessOS_formatter.format_multi_engine_results(
                results, synthesis, request.birth_data.dict()
            )
        else:
            formatted_results = {
                "results": results,
                "synthesis": synthesis
            }
        
        return {
            "engines": request.engines,
            "birth_data": request.birth_data.dict(),
            "results": formatted_results,
            "timestamp": datetime.now().isoformat(),
            "parallel_execution": request.parallel
        }
        
    except Exception as e:
        logger.error(f"Error running multiple engines: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Workflow endpoints
@app.get("/workflows")
async def list_workflows():
    """List all available workflows"""
    try:
        workflows = workflow_manager.get_available_workflows()
        workflow_descriptions = {}
        for workflow in workflows:
            workflow_descriptions[workflow] = workflow_manager.get_workflow_description(workflow)
        
        return {
            "available_workflows": workflows,
            "descriptions": workflow_descriptions,
            "count": len(workflows),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error listing workflows: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/workflows/run")
async def run_workflow(request: WorkflowRequest):
    """Run a predefined workflow"""
    try:
        # Convert birth data to dict
        birth_data_dict = request.birth_data.dict()
        
        # Run workflow
        result = workflow_manager.run_workflow(
            request.workflow_name,
            birth_data_dict,
            request.options
        )
        
        # Format output
        if request.format == "witnessOS":
            formatted_result = witnessOS_formatter.format_workflow_result(result)
        else:
            formatted_result = result
        
        return {
            "workflow": request.workflow_name,
            "result": formatted_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error running workflow {request.workflow_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Field analysis endpoints
@app.post("/field-analysis")
async def analyze_consciousness_field(request: FieldAnalysisRequest):
    """Analyze consciousness field signature"""
    try:
        # Run comprehensive reading first
        birth_data_dict = request.birth_data.dict()
        engines = request.engines or ['numerology', 'biorhythm', 'human_design', 'vimshottari', 'gene_keys']
        
        comprehensive_reading = orchestrator.create_comprehensive_reading(birth_data_dict, engines)
        
        # Analyze field signature
        field_signature = field_analyzer.analyze_field_signature(comprehensive_reading['results'])
        
        # Format for WitnessOS
        formatted_analysis = witnessOS_formatter.format_field_analysis(
            field_signature, 
            comprehensive_reading,
            request.analysis_depth
        )
        
        return {
            "field_analysis": formatted_analysis,
            "engines_analyzed": engines,
            "analysis_depth": request.analysis_depth,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error analyzing consciousness field: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Synthesis endpoints
@app.post("/synthesis")
async def synthesize_results(results: Dict[str, Any]):
    """Synthesize results from multiple engines"""
    try:
        synthesis = synthesizer.synthesize_reading(results)
        
        formatted_synthesis = witnessOS_formatter.format_synthesis(synthesis)
        
        return {
            "synthesis": formatted_synthesis,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error synthesizing results: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "engines_available": len(orchestrator.get_available_engines()),
        "workflows_available": len(workflow_manager.get_available_workflows())
    }

# Helper functions
def _convert_birth_data_to_engine_input(birth_data: BirthData, engine_name: str):
    """Convert birth data to appropriate engine input format"""
    from datetime import datetime
    import re

    # Parse birth date (DD.MM.YYYY format)
    try:
        day, month, year = birth_data.date.split('.')
        birth_date = datetime(int(year), int(month), int(day)).date()
    except ValueError:
        raise ValueError(f"Invalid birth date format. Expected DD.MM.YYYY, got: {birth_data.date}")

    # Parse birth time (HH:MM format)
    birth_time = None
    if birth_data.time:
        try:
            hour, minute = birth_data.time.split(':')
            birth_time = datetime.strptime(f"{hour}:{minute}", "%H:%M").time()
        except ValueError:
            raise ValueError(f"Invalid birth time format. Expected HH:MM, got: {birth_data.time}")

    # Parse birth location (for now, use a simple geocoding approach)
    # In production, you'd want to use a proper geocoding service
    birth_location = None
    timezone_str = birth_data.timezone or "UTC"

    # Simple location mapping for common cities (expand as needed)
    location_coords = {
        "bengaluru": (12.9716, 77.5946),
        "bangalore": (12.9716, 77.5946),
        "mumbai": (19.0760, 72.8777),
        "delhi": (28.7041, 77.1025),
        "new york": (40.7128, -74.0060),
        "london": (51.5074, -0.1278),
        "paris": (48.8566, 2.3522),
        "tokyo": (35.6762, 139.6503),
        "sydney": (-33.8688, 151.2093)
    }

    location_lower = birth_data.location.lower()
    for city, coords in location_coords.items():
        if city in location_lower:
            birth_location = coords
            break

    if not birth_location:
        # Default to Bengaluru if location not found (for testing)
        birth_location = (12.9716, 77.5946)
        logger.warning(f"Location '{birth_data.location}' not found, using default coordinates")

    # Convert based on engine type
    if engine_name == "numerology":
        return {
            "full_name": birth_data.name,
            "birth_date": birth_date,
            "system": "pythagorean"
        }

    elif engine_name == "biorhythm":
        return {
            "birth_date": birth_date,
            "include_extended_cycles": True,
            "forecast_days": 14
        }

    elif engine_name in ["human_design", "gene_keys"]:
        if not birth_time:
            raise ValueError(f"{engine_name} requires exact birth time")
        return {
            "birth_date": birth_date,
            "birth_time": birth_time,
            "birth_location": birth_location,
            "timezone": timezone_str
        }

    elif engine_name == "vimshottari":
        if not birth_time:
            raise ValueError("Vimshottari requires exact birth time")
        return {
            "birth_date": birth_date,
            "birth_time": birth_time,
            "birth_location": birth_location,
            "timezone": timezone_str
        }

    elif engine_name in ["tarot", "iching"]:
        return {
            "question": f"Guidance for {birth_data.name}",
            "context": f"Born {birth_data.date} in {birth_data.location}"
        }

    elif engine_name == "enneagram":
        return {
            "identification_method": "intuitive",
            "behavioral_description": f"Person born {birth_data.date} seeking personality insights"
        }

    elif engine_name == "sacred_geometry":
        return {
            "intention": f"Sacred geometry for {birth_data.name}",
            "birth_date": birth_date,
            "pattern_type": "personal"
        }

    elif engine_name == "sigil_forge":
        return {
            "intention": f"Manifestation sigil for {birth_data.name}",
            "generation_method": "traditional"
        }

    else:
        # Generic fallback
        return {
            "birth_date": birth_date,
            "birth_time": birth_time,
            "birth_location": birth_location,
            "name": birth_data.name
        }

# Error handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return HTTPException(status_code=400, detail=str(exc))

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return HTTPException(status_code=500, detail="Internal server error")

# Create router for modular use
from fastapi import APIRouter
router = APIRouter()

# Add all routes to router
router.add_api_route("/", root, methods=["GET"])
router.add_api_route("/engines", list_engines, methods=["GET"])
router.add_api_route("/engines/run", run_single_engine, methods=["POST"])
router.add_api_route("/engines/multi", run_multiple_engines, methods=["POST"])
router.add_api_route("/workflows", list_workflows, methods=["GET"])
router.add_api_route("/workflows/run", run_workflow, methods=["POST"])
router.add_api_route("/field-analysis", analyze_consciousness_field, methods=["POST"])
router.add_api_route("/synthesis", synthesize_results, methods=["POST"])
router.add_api_route("/health", health_check, methods=["GET"])
