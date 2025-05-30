"""
WitnessOS AI Agent Layer

An intelligent agent layer that sits above the WitnessOS production API,
providing natural language interpretation and contextual explanations
of divination engine calculations.

Features:
- Natural language translation of technical outputs
- Dynamic LLM model selection via OpenRouter
- WitnessOS consciousness framework integration
- Mystical-technical balance in explanations
- Archetypal pattern interpretation
"""

from .agent_service import WitnessOSAgent
from .openrouter_client import OpenRouterClient
from .prompt_templates import PromptTemplateManager
from .response_formatter import AgentResponseFormatter

__all__ = [
    "WitnessOSAgent",
    "OpenRouterClient", 
    "PromptTemplateManager",
    "AgentResponseFormatter"
]

__version__ = "1.0.0"
