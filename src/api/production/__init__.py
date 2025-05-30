"""
WitnessOS API Layer - Phase 7

Provides FastAPI endpoints for all engines and integration workflows.
Includes mystical output formatting and WitnessOS-specific features.
"""

from .endpoints import app, router
from .middleware import setup_middleware
from .formatters import MysticalFormatter, WitnessOSFormatter

__all__ = [
    "app",
    "router", 
    "setup_middleware",
    "MysticalFormatter",
    "WitnessOSFormatter"
]
