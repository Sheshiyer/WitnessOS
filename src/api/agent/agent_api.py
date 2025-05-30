"""
WitnessOS AI Agent API

FastAPI endpoints for the AI agent layer that provides natural language
interpretation of divination engine calculations.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

# Add parent directory to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import get_config, is_openrouter_configured, get_openrouter_api_key, get_production_api_url

try:
    from .agent_service import WitnessOSAgent
except ImportError:
    # Fallback for direct execution
    from agent_service import WitnessOSAgent

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="WitnessOS AI Agent API",
    description="""
    ## Consciousness Interpretation Through AI Wisdom
    
    An intelligent agent layer that provides natural language interpretation
    of WitnessOS divination engine calculations using advanced language models.
    
    ### Features
    - Natural language translation of technical outputs
    - Dynamic LLM model selection via OpenRouter
    - WitnessOS consciousness framework integration
    - Mystical-technical balance in explanations
    - Archetypal pattern interpretation
    - Multi-engine synthesis and correlation analysis
    
    ### Agent Capabilities
    - **Single Engine Interpretation**: Get AI guidance for individual engine results
    - **Multi-Engine Synthesis**: Comprehensive analysis across multiple systems
    - **Workflow Interpretation**: AI guidance for predefined workflow results
    - **Dynamic Model Selection**: Choose optimal LLM for different interpretation tasks
    - **Consciousness Debugging**: Frame results as consciousness field analysis
    """,
    version="1.0.0",
    docs_url="/agent/docs",
    redoc_url="/agent/redoc",
    openapi_url="/agent/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent
agent = None

def get_agent() -> WitnessOSAgent:
    """Get or initialize the WitnessOS Agent"""
    global agent
    if agent is None:
        # Use the new configuration system
        config = get_config()

        if not config.is_openrouter_configured():
            env_status = config.get_env_file_status()
            available_files = [f for f, exists in env_status.items() if exists]

            raise HTTPException(
                status_code=503,
                detail={
                    "error": "OpenRouter API key not configured",
                    "message": "Set OPENROUTER_API_KEY environment variable",
                    "available_env_files": available_files,
                    "setup_instructions": [
                        "1. Get API key from https://openrouter.ai/keys",
                        "2. Add OPENROUTER_API_KEY to .env.local (recommended) or .env",
                        "3. Restart the agent API"
                    ],
                    "env_file_precedence": [".env.local", ".env", ".env.template"]
                }
            )

        agent = WitnessOSAgent(
            production_api_url=config.get('production_api_url'),
            openrouter_api_key=config.get('openrouter_api_key')
        )
        logger.info("WitnessOS Agent initialized with new config system")

    return agent

# Pydantic Models
class BirthData(BaseModel):
    """Birth data model for agent requests"""
    name: str = Field(..., min_length=1, max_length=100, description="Full birth name")
    date: str = Field(..., pattern=r"^\d{2}\.\d{2}\.\d{4}$", description="Birth date (DD.MM.YYYY)")
    time: str = Field(..., pattern=r"^\d{2}:\d{2}$", description="Birth time (HH:MM)")
    location: str = Field(..., min_length=1, max_length=100, description="Birth location")
    timezone: Optional[str] = Field(None, description="Timezone (e.g., Asia/Kolkata)")

class AgentSingleEngineRequest(BaseModel):
    """Request model for single engine interpretation"""
    engine_name: str = Field(..., description="Name of the engine to interpret")
    birth_data: BirthData = Field(..., description="Birth data for calculation")
    interpretation_style: str = Field("balanced", pattern="^(technical|mystical|witnessOS|balanced)$",
                                    description="Style of AI interpretation")
    model_type: Optional[str] = Field(None, pattern="^(fast|balanced|creative|reasoning)$",
                                    description="LLM model type to use")
    use_cache: bool = Field(True, description="Whether to use cached responses")

class AgentMultiEngineRequest(BaseModel):
    """Request model for multi-engine interpretation"""
    engines: List[str] = Field(..., min_items=1, max_items=10, description="List of engines to interpret")
    birth_data: BirthData = Field(..., description="Birth data for calculations")
    interpretation_style: str = Field("witnessOS", pattern="^(technical|mystical|witnessOS|balanced)$",
                                    description="Style of AI interpretation")
    model_type: Optional[str] = Field(None, pattern="^(fast|balanced|creative|reasoning)$",
                                    description="LLM model type to use")
    include_synthesis: bool = Field(True, description="Whether to include cross-engine synthesis")
    use_cache: bool = Field(True, description="Whether to use cached responses")

class AgentWorkflowRequest(BaseModel):
    """Request model for workflow interpretation"""
    workflow_name: str = Field(..., description="Name of the workflow to interpret")
    birth_data: BirthData = Field(..., description="Birth data for calculations")
    interpretation_style: str = Field("witnessOS", pattern="^(technical|mystical|witnessOS|balanced)$",
                                    description="Style of AI interpretation")
    model_type: Optional[str] = Field(None, pattern="^(fast|balanced|creative|reasoning)$",
                                    description="LLM model type to use")
    use_cache: bool = Field(True, description="Whether to use cached responses")

# API Endpoints

@app.get("/agent/")
async def agent_root():
    """Root endpoint with agent information"""
    return {
        "message": "WitnessOS AI Agent API",
        "version": "1.0.0",
        "description": "Consciousness interpretation through AI wisdom",
        "status": "active",
        "endpoints": {
            "single_engine": "/agent/interpret/single",
            "multi_engine": "/agent/interpret/multi",
            "workflow": "/agent/interpret/workflow",
            "status": "/agent/status",
            "models": "/agent/models",
            "documentation": "/agent/docs"
        },
        "features": [
            "Natural language interpretation",
            "Dynamic model selection",
            "WitnessOS consciousness framework",
            "Multi-engine synthesis",
            "Archetypal pattern analysis"
        ]
    }

@app.get("/agent/status")
async def agent_status(agent: WitnessOSAgent = Depends(get_agent)):
    """Get agent status and configuration"""
    try:
        status = agent.get_agent_status()
        
        # Add health check for production API
        try:
            engines = await agent.get_available_engines()
            status["production_api_status"] = "healthy" if "available_engines" in engines else "unhealthy"
        except Exception as e:
            status["production_api_status"] = f"error: {str(e)}"
        
        return status
    except Exception as e:
        logger.error(f"Error getting agent status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agent/models")
async def list_available_models(agent: WitnessOSAgent = Depends(get_agent)):
    """List available LLM models and their configurations"""
    try:
        models = agent.openrouter_client.list_available_models()
        
        return {
            "available_models": {
                model_type: {
                    "name": config.name,
                    "description": config.description,
                    "max_tokens": config.max_tokens,
                    "context_window": config.context_window,
                    "cost_per_1k_tokens": config.cost_per_1k_tokens
                }
                for model_type, config in models.items()
            },
            "model_selection_guide": {
                "fast": "Quick interpretations for simple queries",
                "balanced": "Comprehensive explanations for most use cases",
                "creative": "Mystical and poetic interpretations",
                "reasoning": "Complex synthesis and deep analysis"
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agent/engines")
async def list_available_engines(agent: WitnessOSAgent = Depends(get_agent)):
    """List available engines from production API"""
    try:
        engines = await agent.get_available_engines()
        return engines
    except Exception as e:
        logger.error(f"Error listing engines: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agent/workflows")
async def list_available_workflows(agent: WitnessOSAgent = Depends(get_agent)):
    """List available workflows from production API"""
    try:
        workflows = await agent.get_available_workflows()
        return workflows
    except Exception as e:
        logger.error(f"Error listing workflows: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agent/interpret/single")
async def interpret_single_engine(
    request: AgentSingleEngineRequest,
    agent: WitnessOSAgent = Depends(get_agent)
):
    """Get AI interpretation for a single engine calculation"""
    try:
        result = await agent.interpret_single_engine(
            engine_name=request.engine_name,
            birth_data=request.birth_data.model_dump(),
            interpretation_style=request.interpretation_style,
            model_type=request.model_type,
            use_cache=request.use_cache
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error in single engine interpretation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agent/interpret/multi")
async def interpret_multi_engine(
    request: AgentMultiEngineRequest,
    agent: WitnessOSAgent = Depends(get_agent)
):
    """Get AI interpretation for multiple engine calculations with synthesis"""
    try:
        result = await agent.interpret_multi_engine(
            engines=request.engines,
            birth_data=request.birth_data.model_dump(),
            interpretation_style=request.interpretation_style,
            model_type=request.model_type,
            include_synthesis=request.include_synthesis,
            use_cache=request.use_cache
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error in multi-engine interpretation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agent/interpret/workflow")
async def interpret_workflow(
    request: AgentWorkflowRequest,
    agent: WitnessOSAgent = Depends(get_agent)
):
    """Get AI interpretation for a workflow execution"""
    try:
        result = await agent.interpret_workflow(
            workflow_name=request.workflow_name,
            birth_data=request.birth_data.model_dump(),
            interpretation_style=request.interpretation_style,
            model_type=request.model_type,
            use_cache=request.use_cache
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error in workflow interpretation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": "HTTPException",
                "message": exc.detail,
                "status_code": exc.status_code,
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url)
            }
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception in agent API: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "InternalServerError",
                "message": "An internal server error occurred in the AI agent",
                "timestamp": datetime.now().isoformat(),
                "path": str(request.url)
            }
        }
    )

# Health check endpoint
@app.get("/agent/health")
async def health_check():
    """Comprehensive health check for the agent API"""
    try:
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "components": {}
        }

        # Use new configuration system
        config = get_config()

        # Check OpenRouter API key
        if config.is_openrouter_configured():
            health_status["components"]["openrouter_api_key"] = "configured"
        else:
            health_status["components"]["openrouter_api_key"] = "missing"
            health_status["status"] = "degraded"

        # Check production API URL
        health_status["components"]["production_api_url"] = config.get('production_api_url')

        # Add environment file status
        health_status["components"]["env_files"] = config.get_env_file_status()

        # Add configuration validation
        validation = config.validate_configuration()
        health_status["components"]["config_validation"] = {
            "valid": validation["valid"],
            "issues_count": len(validation["issues"]),
            "warnings_count": len(validation["warnings"])
        }

        # Try to initialize agent
        try:
            test_agent = get_agent()
            health_status["components"]["agent_initialization"] = "success"

            # Test production API connection
            try:
                engines = await test_agent.get_available_engines()
                health_status["components"]["production_api_connection"] = "healthy"
                health_status["components"]["available_engines"] = len(engines.get("available_engines", []))
            except Exception as e:
                health_status["components"]["production_api_connection"] = f"error: {str(e)}"
                health_status["status"] = "degraded"

        except Exception as e:
            health_status["components"]["agent_initialization"] = f"error: {str(e)}"
            health_status["status"] = "unhealthy"

        status_code = 200 if health_status["status"] == "healthy" else 503
        return JSONResponse(status_code=status_code, content=health_status)

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

# Server startup
if __name__ == "__main__":
    import argparse
    import uvicorn

    parser = argparse.ArgumentParser(description="WitnessOS AI Agent API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8003, help="Port to run on")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--log-level", default="info", help="Log level")

    args = parser.parse_args()

    logger.info("🤖 Starting WitnessOS AI Agent API")
    logger.info(f"🌐 Server: http://{args.host}:{args.port}")
    logger.info(f"📚 Documentation: http://{args.host}:{args.port}/agent/docs")
    logger.info("🧠 Mode: AI-powered consciousness interpretation")

    uvicorn.run(
        "agent_api:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level,
        access_log=True
    )
