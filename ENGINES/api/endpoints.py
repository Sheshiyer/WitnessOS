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

from ..integration.orchestrator import EngineOrchestrator
from ..integration.workflows import WorkflowManager
from ..integration.field_analyzer import FieldAnalyzer
from ..integration.synthesis import ResultSynthesizer
from .formatters import MysticalFormatter, WitnessOSFormatter
from .middleware import setup_middleware

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
    # This would be implemented based on each engine's input model
    # For now, return a simplified conversion
    return {
        "name": birth_data.name,
        "birth_date": birth_data.date,
        "birth_time": birth_data.time,
        "birth_location": birth_data.location
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
