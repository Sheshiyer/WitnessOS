"""
OpenRouter API Client for WitnessOS Agent

Handles communication with OpenRouter API for accessing various language models.
Supports dynamic model selection and response streaming.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, AsyncGenerator
from dataclasses import dataclass
import httpx


logger = logging.getLogger(__name__)


@dataclass
class ModelConfig:
    """Configuration for a specific language model"""
    name: str
    max_tokens: int
    temperature: float
    top_p: float
    description: str
    cost_per_1k_tokens: float
    context_window: int


class OpenRouterClient:
    """
    Client for interacting with OpenRouter API
    
    Provides access to multiple language models with dynamic selection
    based on task requirements and cost considerations.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenRouter client
        
        Args:
            api_key: OpenRouter API key (defaults to OPENROUTER_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key not provided. Set OPENROUTER_API_KEY environment variable.")
        
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://witnessOS.com",
            "X-Title": "WitnessOS Consciousness Agent"
        }
        
        # Available free models with fallback order
        self.models = {
            "primary": ModelConfig(
                name="microsoft/phi-4-reasoning-plus:free",
                max_tokens=4096,
                temperature=0.7,
                top_p=0.9,
                description="Primary free model - Microsoft Phi-4 Reasoning Plus",
                cost_per_1k_tokens=0.0,
                context_window=16384
            ),
            "fallback1": ModelConfig(
                name="google/gemma-3n-e4b-it:free",
                max_tokens=4096,
                temperature=0.7,
                top_p=0.9,
                description="Fallback 1 - Google Gemma 3N",
                cost_per_1k_tokens=0.0,
                context_window=8192
            ),
            "fallback2": ModelConfig(
                name="deepseek/deepseek-v3-base:free",
                max_tokens=4096,
                temperature=0.7,
                top_p=0.9,
                description="Fallback 2 - DeepSeek V3 Base",
                cost_per_1k_tokens=0.0,
                context_window=32768
            ),
            "fallback3": ModelConfig(
                name="deepseek/deepseek-r1-0528-qwen3-8b:free",
                max_tokens=4096,
                temperature=0.7,
                top_p=0.9,
                description="Fallback 3 - DeepSeek R1 Qwen3",
                cost_per_1k_tokens=0.0,
                context_window=32768
            )
        }

        # Model fallback order
        self.fallback_order = ["primary", "fallback1", "fallback2", "fallback3"]
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        model_type: str = "primary",
        stream: bool = False,
        timeout: float = 30.0,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate response using specified model with automatic fallback

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model_type: Type of model to use (defaults to 'primary')
            stream: Whether to stream the response
            **kwargs: Additional parameters to override model config

        Returns:
            Response dictionary with generated content
        """
        # If specific model type requested, try it first, then fallback
        if model_type in self.models:
            models_to_try = [model_type] + [m for m in self.fallback_order if m != model_type]
        else:
            # Use fallback order if unknown model type
            models_to_try = self.fallback_order

        last_error = None

        for attempt, current_model_type in enumerate(models_to_try):
            model_config = self.models[current_model_type]

            # Prepare request payload
            payload = {
                "model": model_config.name,
                "messages": messages,
                "max_tokens": kwargs.get("max_tokens", model_config.max_tokens),
                "temperature": kwargs.get("temperature", model_config.temperature),
                "top_p": kwargs.get("top_p", model_config.top_p),
                "stream": stream
            }

            try:
                logger.info(f"Attempting request with {current_model_type} model: {model_config.name}")

                async with httpx.AsyncClient(timeout=timeout) as client:
                    if stream:
                        return await self._stream_response(client, payload)
                    else:
                        response = await client.post(
                            f"{self.base_url}/chat/completions",
                            headers=self.headers,
                            json=payload
                        )
                        response.raise_for_status()
                        result = response.json()

                        # Add metadata about which model was used
                        result["_model_used"] = current_model_type
                        result["_model_name"] = model_config.name
                        result["_attempt"] = attempt + 1

                        logger.info(f"Successfully generated response with {current_model_type} model")
                        return result

            except (httpx.TimeoutException, httpx.ConnectTimeout, httpx.ReadTimeout) as e:
                last_error = f"Timeout with {current_model_type}: {e}"
                logger.warning(f"Timeout with {current_model_type} model, trying next fallback...")
                continue

            except httpx.HTTPStatusError as e:
                if e.response.status_code in [429, 503, 502, 504]:  # Rate limit or server errors
                    last_error = f"Server error {e.response.status_code} with {current_model_type}: {e}"
                    logger.warning(f"Server error {e.response.status_code} with {current_model_type} model, trying next fallback...")
                    continue
                else:
                    last_error = f"HTTP error {e.response.status_code} with {current_model_type}: {e}"
                    logger.error(f"HTTP error {e.response.status_code} with {current_model_type} model: {e}")
                    continue

            except Exception as e:
                last_error = f"Unexpected error with {current_model_type}: {e}"
                logger.error(f"Unexpected error with {current_model_type} model: {e}")
                continue

        # If all models failed
        raise Exception(f"All models failed. Last error: {last_error}")
    
    async def _stream_response(self, client: httpx.AsyncClient, payload: Dict) -> AsyncGenerator[str, None]:
        """Stream response from OpenRouter API"""
        async with client.stream(
            "POST",
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            json=payload
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                        if "choices" in chunk and chunk["choices"]:
                            delta = chunk["choices"][0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
                    except json.JSONDecodeError:
                        continue
    
    def get_model_info(self, model_type: str) -> ModelConfig:
        """Get information about a specific model"""
        if model_type not in self.models:
            raise ValueError(f"Unknown model type: {model_type}")
        return self.models[model_type]
    
    def list_available_models(self) -> Dict[str, ModelConfig]:
        """List all available models"""
        return self.models.copy()
    
    def select_optimal_model(self, task_type: str = "interpretation", complexity: str = "medium") -> str:
        """
        Select optimal model based on task type and complexity

        Args:
            task_type: Type of task ('interpretation', 'synthesis', 'creative', 'analysis')
            complexity: Complexity level ('low', 'medium', 'high')

        Returns:
            Model type string
        """
        # Always use primary model first (Microsoft Phi-4) with automatic fallback
        # Parameters kept for API compatibility but not used since we have a single fallback chain
        _ = task_type, complexity  # Acknowledge parameters to avoid warnings
        return "primary"
