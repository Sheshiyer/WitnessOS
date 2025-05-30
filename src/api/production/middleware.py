"""
API Middleware for WitnessOS Engines

Provides authentication, rate limiting, logging, and other middleware
for the WitnessOS API endpoints.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time
import logging
from typing import Dict, Optional
from collections import defaultdict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware to prevent API abuse
    """
    
    def __init__(self, app, calls_per_minute: int = 60):
        super().__init__(app)
        self.calls_per_minute = calls_per_minute
        self.client_calls = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = datetime.now()
        
        # Clean old entries
        cutoff = now - timedelta(minutes=1)
        self.client_calls[client_ip] = [
            call_time for call_time in self.client_calls[client_ip] 
            if call_time > cutoff
        ]
        
        # Check rate limit
        if len(self.client_calls[client_ip]) >= self.calls_per_minute:
            raise HTTPException(
                status_code=429, 
                detail="Rate limit exceeded. Please try again later."
            )
        
        # Record this call
        self.client_calls[client_ip].append(now)
        
        response = await call_next(request)
        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Request/response logging middleware
    """
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url}")
        
        response = await call_next(request)
        
        # Log response
        process_time = time.time() - start_time
        logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
        
        # Add timing header
        response.headers["X-Process-Time"] = str(process_time)
        
        return response

class WitnessOSMiddleware(BaseHTTPMiddleware):
    """
    WitnessOS-specific middleware for consciousness field tracking
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.field_interactions = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        # Track consciousness field interactions
        client_ip = request.client.host
        endpoint = str(request.url.path)
        timestamp = datetime.now()
        
        # Record field interaction
        self.field_interactions[client_ip].append({
            'endpoint': endpoint,
            'timestamp': timestamp,
            'method': request.method
        })
        
        # Add WitnessOS headers
        response = await call_next(request)
        response.headers["X-WitnessOS-Version"] = "0.1.0"
        response.headers["X-Field-Resonance"] = "active"
        response.headers["X-Consciousness-Debug"] = "enabled"
        
        return response

class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Simple API key authentication middleware
    """
    
    def __init__(self, app, api_keys: Optional[Dict[str, str]] = None):
        super().__init__(app)
        self.api_keys = api_keys or {}
        self.public_endpoints = {
            "/", "/docs", "/redoc", "/openapi.json", "/health"
        }
    
    async def dispatch(self, request: Request, call_next):
        # Skip auth for public endpoints
        if request.url.path in self.public_endpoints:
            return await call_next(request)
        
        # Skip auth if no API keys configured
        if not self.api_keys:
            return await call_next(request)
        
        # Check for API key
        api_key = request.headers.get("X-API-Key")
        if not api_key or api_key not in self.api_keys:
            raise HTTPException(
                status_code=401,
                detail="Invalid or missing API key"
            )
        
        # Add user info to request state
        request.state.user = self.api_keys[api_key]
        
        return await call_next(request)

def setup_middleware(app: FastAPI, config: Optional[Dict] = None):
    """
    Setup all middleware for the WitnessOS API
    
    Args:
        app: FastAPI application instance
        config: Optional configuration dictionary
    """
    config = config or {}
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.get("cors_origins", ["*"]),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Trusted host middleware
    if config.get("trusted_hosts"):
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=config["trusted_hosts"]
        )
    
    # Rate limiting
    if config.get("enable_rate_limiting", True):
        app.add_middleware(
            RateLimitMiddleware,
            calls_per_minute=config.get("rate_limit", 60)
        )
    
    # Authentication
    if config.get("api_keys"):
        app.add_middleware(
            AuthenticationMiddleware,
            api_keys=config["api_keys"]
        )
    
    # WitnessOS-specific middleware
    app.add_middleware(WitnessOSMiddleware)
    
    # Logging middleware
    app.add_middleware(LoggingMiddleware)
    
    logger.info("WitnessOS API middleware setup complete")

def get_field_interaction_stats(client_ip: str = None) -> Dict:
    """
    Get consciousness field interaction statistics
    
    Args:
        client_ip: Optional client IP to filter by
        
    Returns:
        Dictionary with interaction statistics
    """
    # This would be implemented to return actual stats
    # For now, return placeholder data
    return {
        "total_interactions": 42,
        "unique_clients": 7,
        "most_active_endpoint": "/field-analysis",
        "field_resonance_level": "high",
        "consciousness_debug_sessions": 12
    }

def reset_rate_limits():
    """Reset all rate limit counters"""
    # This would be implemented to reset rate limiting
    logger.info("Rate limits reset")

def get_api_health() -> Dict:
    """Get API health and middleware status"""
    return {
        "middleware_status": "active",
        "rate_limiting": "enabled",
        "field_tracking": "active",
        "consciousness_debug": "enabled",
        "timestamp": datetime.now().isoformat()
    }
