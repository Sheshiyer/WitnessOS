"""
WitnessOS AI Agent Service

Main agent service that wraps the production API and provides natural language
interpretation of divination engine calculations using OpenRouter LLMs.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import httpx

try:
    from .openrouter_client import OpenRouterClient
    from .prompt_templates import PromptTemplateManager, EngineType, InterpretationStyle
    from .response_formatter import AgentResponseFormatter
except ImportError:
    # Fallback for direct execution
    from openrouter_client import OpenRouterClient
    from prompt_templates import PromptTemplateManager, EngineType, InterpretationStyle
    from response_formatter import AgentResponseFormatter

logger = logging.getLogger(__name__)


class WitnessOSAgent:
    """
    Main AI agent that provides natural language interpretation of
    WitnessOS divination engine calculations.
    
    Integrates with the production API to fetch calculation results,
    then uses OpenRouter LLMs to generate contextual explanations.
    """
    
    def __init__(
        self,
        production_api_url: str = "http://localhost:8002",
        openrouter_api_key: Optional[str] = None,
        default_model_type: str = "balanced",
        use_local_engines: bool = True
    ):
        """
        Initialize the WitnessOS Agent

        Args:
            production_api_url: URL of the WitnessOS production API
            openrouter_api_key: OpenRouter API key
            default_model_type: Default model type for interpretations
            use_local_engines: Whether to use local engines when API fails
        """
        self.production_api_url = production_api_url.rstrip('/')
        self.openrouter_client = OpenRouterClient(openrouter_api_key)
        self.prompt_manager = PromptTemplateManager()
        self.response_formatter = AgentResponseFormatter()
        self.default_model_type = default_model_type or "primary"
        self.use_local_engines = use_local_engines

        # Cache for agent responses
        self.response_cache = {}
        self.cache_max_size = 100

        # Local engine instances (lazy loaded)
        self.local_engines = {}

        # Initialize Aletheos context extractor
        try:
            from .aletheos_muses import AletheosContextExtractor
        except ImportError:
            from aletheos_muses import AletheosContextExtractor
        self.aletheos = AletheosContextExtractor()

        logger.info("WitnessOS Agent initialized with Aletheos + 10 Muses")
    
    async def interpret_single_engine(
        self,
        engine_name: str,
        birth_data: Dict[str, Any],
        interpretation_style: str = "balanced",
        model_type: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Get calculation from production API and provide AI interpretation
        
        Args:
            engine_name: Name of the engine to run
            birth_data: Birth data for calculation
            interpretation_style: Style of interpretation ('technical', 'mystical', 'witnessOS', 'balanced')
            model_type: LLM model type to use
            use_cache: Whether to use cached responses
            
        Returns:
            Dictionary containing calculation results and AI interpretation
        """
        try:
            # Generate cache key
            cache_key = self._generate_cache_key({
                "engine": engine_name,
                "birth_data": birth_data,
                "style": interpretation_style,
                "model": model_type or self.default_model_type
            })
            
            # Check cache
            if use_cache and cache_key in self.response_cache:
                logger.info(f"Cache hit for agent interpretation: {engine_name}")
                return self.response_cache[cache_key]
            
            # Get calculation from production API
            calculation_result = await self._call_production_api(
                endpoint=f"/calculate/{engine_name}",
                data={
                    "birth_data": {
                        "name": birth_data.get("name", ""),
                        "date": birth_data.get("date", ""),
                        "time": birth_data.get("time"),
                        "location": birth_data.get("location"),
                        "timezone": birth_data.get("timezone")
                    },
                    "system": "pythagorean" if engine_name == "numerology" else None,
                    "current_year": birth_data.get("current_year"),
                    "target_date": birth_data.get("target_date")
                }
            )
            
            if calculation_result.get("status") != "success":
                raise Exception(f"Engine calculation failed: {calculation_result.get('error', 'Unknown error')}")
            
            # Generate AI interpretation
            interpretation = await self._generate_interpretation(
                engine_name=engine_name,
                calculation_data=calculation_result,
                birth_data=birth_data,
                style=interpretation_style,
                model_type=model_type
            )
            
            # Format response
            response = self.response_formatter.format_single_engine_response(
                engine_name=engine_name,
                calculation_result=calculation_result,
                ai_interpretation=interpretation,
                birth_data=birth_data
            )
            
            # Cache response
            if use_cache:
                self._cache_response(cache_key, response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in single engine interpretation: {e}")
            return {
                "error": str(e),
                "engine": engine_name,
                "status": "agent_error",
                "timestamp": datetime.now().isoformat()
            }
    
    async def interpret_multi_engine(
        self,
        engines: List[str],
        birth_data: Dict[str, Any],
        interpretation_style: str = "witnessOS",
        model_type: Optional[str] = None,
        include_synthesis: bool = True,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Get multi-engine calculation and provide comprehensive AI interpretation
        
        Args:
            engines: List of engine names to run
            birth_data: Birth data for calculations
            interpretation_style: Style of interpretation
            model_type: LLM model type to use
            include_synthesis: Whether to include cross-engine synthesis
            use_cache: Whether to use cached responses
            
        Returns:
            Dictionary containing all calculations and AI interpretations
        """
        try:
            # Generate cache key
            cache_key = self._generate_cache_key({
                "engines": sorted(engines),
                "birth_data": birth_data,
                "style": interpretation_style,
                "model": model_type or self.default_model_type,
                "synthesis": include_synthesis
            })
            
            # Check cache
            if use_cache and cache_key in self.response_cache:
                logger.info(f"Cache hit for multi-engine interpretation")
                return self.response_cache[cache_key]
            
            # Get calculations from production API (call each engine separately)
            calculation_results = {}
            for engine in engines:
                try:
                    result = await self._call_production_api(
                        endpoint=f"/calculate/{engine}",
                        data={
                            "birth_data": {
                                "name": birth_data.get("name", ""),
                                "date": birth_data.get("date", ""),
                                "time": birth_data.get("time"),
                                "location": birth_data.get("location"),
                                "timezone": birth_data.get("timezone")
                            },
                            "system": "pythagorean" if engine == "numerology" else None,
                            "current_year": birth_data.get("current_year"),
                            "target_date": birth_data.get("target_date")
                        }
                    )
                    calculation_results[engine] = result
                except Exception as e:
                    logger.error(f"Error calculating {engine}: {e}")
                    calculation_results[engine] = {"status": "error", "error": str(e)}

            # Create a combined result structure
            calculation_result = {
                "status": "success",
                "results": {
                    "engine_outputs": calculation_results
                },
                "timestamp": datetime.now().isoformat()
            }
            
            # Generate individual interpretations
            engine_interpretations = {}
            for engine_name in engines:
                if engine_name in calculation_result.get("results", {}).get("engine_outputs", {}):
                    engine_data = calculation_result["results"]["engine_outputs"][engine_name]
                    if engine_data.get("status") == "success":
                        interpretation = await self._generate_interpretation(
                            engine_name=engine_name,
                            calculation_data=engine_data,
                            birth_data=birth_data,
                            style=interpretation_style,
                            model_type=model_type
                        )
                        engine_interpretations[engine_name] = interpretation
            
            # Generate synthesis if requested
            synthesis_interpretation = None
            if include_synthesis and len(engine_interpretations) > 1:
                synthesis_interpretation = await self._generate_synthesis(
                    engine_results=calculation_result["results"]["engine_outputs"],
                    interpretations=engine_interpretations,
                    birth_data=birth_data,
                    style=interpretation_style,
                    model_type=model_type or "reasoning"  # Use reasoning model for synthesis
                )
            
            # Format response
            response = self.response_formatter.format_multi_engine_response(
                calculation_result=calculation_result,
                engine_interpretations=engine_interpretations,
                synthesis_interpretation=synthesis_interpretation,
                birth_data=birth_data
            )
            
            # Cache response
            if use_cache:
                self._cache_response(cache_key, response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in multi-engine interpretation: {e}")
            return {
                "error": str(e),
                "engines": engines,
                "status": "agent_error",
                "timestamp": datetime.now().isoformat()
            }
    
    async def interpret_workflow(
        self,
        workflow_name: str,
        birth_data: Dict[str, Any],
        interpretation_style: str = "witnessOS",
        model_type: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Execute workflow and provide AI interpretation
        
        Args:
            workflow_name: Name of the workflow to execute
            birth_data: Birth data for calculations
            interpretation_style: Style of interpretation
            model_type: LLM model type to use
            use_cache: Whether to use cached responses
            
        Returns:
            Dictionary containing workflow results and AI interpretation
        """
        try:
            # Get workflow execution from production API
            workflow_result = await self._call_production_api(
                endpoint="/v1/workflows/run",
                data={
                    "workflow_name": workflow_name,
                    "birth_data": birth_data,
                    "format": "standard",
                    "use_cache": use_cache
                }
            )
            
            # Extract engines used in workflow
            engines = workflow_result.get("workflow", {}).get("engines_used", [])
            
            # Use multi-engine interpretation for workflow results
            return await self.interpret_multi_engine(
                engines=engines,
                birth_data=birth_data,
                interpretation_style=interpretation_style,
                model_type=model_type,
                include_synthesis=True,
                use_cache=use_cache
            )
            
        except Exception as e:
            logger.error(f"Error in workflow interpretation: {e}")
            return {
                "error": str(e),
                "workflow": workflow_name,
                "status": "agent_error",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _call_production_api(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Call the WitnessOS production API with local engine fallback"""
        try:
            url = f"{self.production_api_url}{endpoint}"

            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, json=data)
                response.raise_for_status()
                return response.json()

        except Exception as api_error:
            logger.warning(f"Production API call failed: {api_error}")

            # Try local engine fallback if enabled
            if self.use_local_engines and endpoint.startswith("/calculate/"):
                engine_name = endpoint.split("/")[-1]
                logger.info(f"Attempting local engine fallback for {engine_name}")
                return await self._call_local_engine(engine_name, data)
            else:
                raise api_error

    async def _call_local_engine(self, engine_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Call local engine directly as fallback"""
        try:
            # Import local engines
            try:
                from .local_engines import SimpleNumerologyEngine, SimpleBiorhythmEngine, MockEngineFactory
            except ImportError:
                from local_engines import SimpleNumerologyEngine, SimpleBiorhythmEngine, MockEngineFactory

            birth_data = data.get("birth_data", {})

            if engine_name == "numerology":
                if engine_name not in self.local_engines:
                    self.local_engines[engine_name] = SimpleNumerologyEngine()

                input_data = {
                    "full_name": birth_data.get("name", ""),
                    "birth_date": birth_data.get("date", "1990-01-01"),
                    "system": data.get("system", "pythagorean"),
                    "current_year": data.get("current_year")
                }

                return self.local_engines[engine_name].calculate(input_data)

            elif engine_name == "biorhythm":
                if engine_name not in self.local_engines:
                    self.local_engines[engine_name] = SimpleBiorhythmEngine()

                input_data = {
                    "birth_date": birth_data.get("date", "1990-01-01"),
                    "target_date": data.get("target_date")
                }

                return self.local_engines[engine_name].calculate(input_data)

            else:
                # Use mock factory for other engines
                return MockEngineFactory.create_mock_engine(engine_name)

        except Exception as e:
            logger.error(f"Local engine {engine_name} failed: {e}")
            return self._create_mock_response(engine_name, data)

    def _create_mock_response(self, engine_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a mock response for engines that aren't available"""
        birth_data = data.get("birth_data", {})

        return {
            "engine": engine_name,
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "input": birth_data,
            "interpretation": f"Mock {engine_name} analysis for {birth_data.get('name', 'User')}. This is a demonstration of the AI agent's interpretation capabilities.",
            "recommendations": [
                f"This is a mock {engine_name} recommendation",
                "The AI agent is working correctly",
                "Real calculations would provide detailed insights"
            ],
            "mock_data": True
        }
    
    async def _generate_interpretation(
        self,
        engine_name: str,
        calculation_data: Dict[str, Any],
        birth_data: Dict[str, Any],
        style: str,
        model_type: Optional[str] = None
    ) -> str:
        """Generate AI interpretation for a single engine result with Aletheos context"""
        try:
            # Extract context through Aletheos and the 10 Muses
            engine_results = {engine_name: calculation_data}
            muse_insights = self.aletheos.extract_context(engine_results, birth_data)
            aletheos_context = self.aletheos.format_context_for_agent(muse_insights)

            # Map engine name to EngineType enum
            engine_type = EngineType(engine_name)
            interpretation_style = InterpretationStyle(style)

            # Prepare context for prompt template with Aletheos insights
            context = {
                "name": birth_data.get("name", "User"),
                "birth_date": birth_data.get("date", ""),
                "birth_time": birth_data.get("time", ""),
                "location": birth_data.get("location", ""),
                "calculation_data": json.dumps(calculation_data, indent=2),
                "aletheos_context": aletheos_context,
                "context": f"Consciousness guidance for {birth_data.get('name', 'User')} with Muse insights"
            }
            
            # Generate prompt
            prompt = self.prompt_manager.get_prompt(
                engine_type=engine_type,
                style=interpretation_style,
                context=context
            )
            
            # Generate response using OpenRouter
            messages = [
                {"role": "system", "content": prompt["system"]},
                {"role": "user", "content": prompt["user"]}
            ]
            
            response = await self.openrouter_client.generate_response(
                messages=messages,
                model_type=model_type or self.default_model_type
            )
            
            return response["choices"][0]["message"]["content"]
            
        except Exception as e:
            logger.error(f"Error generating interpretation for {engine_name}: {e}")
            return f"Unable to generate interpretation: {str(e)}"

    async def _generate_synthesis(
        self,
        engine_results: Dict[str, Any],
        interpretations: Dict[str, str],
        birth_data: Dict[str, Any],
        style: str,
        model_type: str = "reasoning"
    ) -> str:
        """Generate AI synthesis of multiple engine results"""
        try:
            interpretation_style = InterpretationStyle(style)

            # Prepare synthesis data
            synthesis_data = {
                "engine_results": engine_results,
                "interpretations": interpretations,
                "birth_data": birth_data
            }

            # Generate synthesis prompt
            prompt = self.prompt_manager.get_synthesis_prompt(
                engine_results=synthesis_data,
                style=interpretation_style
            )

            # Generate response using OpenRouter
            messages = [
                {"role": "system", "content": prompt["system"]},
                {"role": "user", "content": prompt["user"]}
            ]

            response = await self.openrouter_client.generate_response(
                messages=messages,
                model_type=model_type
            )

            return response["choices"][0]["message"]["content"]

        except Exception as e:
            logger.error(f"Error generating synthesis: {e}")
            return f"Unable to generate synthesis: {str(e)}"

    def _generate_cache_key(self, data: Dict[str, Any]) -> str:
        """Generate cache key from request data"""
        import hashlib
        data_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(data_str.encode()).hexdigest()

    def _cache_response(self, cache_key: str, response: Dict[str, Any]):
        """Cache agent response with size limit"""
        if len(self.response_cache) >= self.cache_max_size:
            # Remove oldest entry
            oldest_key = next(iter(self.response_cache))
            del self.response_cache[oldest_key]

        self.response_cache[cache_key] = {
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "cached": True
        }

    async def get_available_engines(self) -> Dict[str, Any]:
        """Get list of available engines from production API"""
        try:
            return await self._call_production_api("/v1/engines", {})
        except Exception as e:
            logger.error(f"Error getting available engines: {e}")
            return {"error": str(e)}

    async def get_available_workflows(self) -> Dict[str, Any]:
        """Get list of available workflows from production API"""
        try:
            return await self._call_production_api("/v1/workflows", {})
        except Exception as e:
            logger.error(f"Error getting available workflows: {e}")
            return {"error": str(e)}

    def get_agent_status(self) -> Dict[str, Any]:
        """Get agent status and configuration"""
        return {
            "status": "active",
            "production_api_url": self.production_api_url,
            "default_model_type": self.default_model_type,
            "available_models": list(self.openrouter_client.list_available_models().keys()),
            "cache_size": len(self.response_cache),
            "cache_max_size": self.cache_max_size,
            "timestamp": datetime.now().isoformat()
        }
