#!/usr/bin/env python3
"""
WitnessOS Divination Engines API Server

Main entry point for running the FastAPI server that provides REST API access
to all WitnessOS calculation engines and integration workflows.

Usage:
    python main.py                    # Run with default settings
    python main.py --port 8080        # Run on custom port
    python main.py --dev              # Run in development mode
    python main.py --help             # Show help
"""

import argparse
import logging
import sys
import os
from pathlib import Path

# Add ENGINES directory to Python path
engines_dir = Path(__file__).parent
sys.path.insert(0, str(engines_dir))

try:
    import uvicorn
    from fastapi import FastAPI
except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
    print("📦 Please install required packages:")
    print("   pip install fastapi uvicorn[standard]")
    print("   or: pip install -r requirements.txt")
    sys.exit(1)

from api.endpoints import app
from api.middleware import setup_middleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_api_config(dev_mode: bool = False) -> dict:
    """
    Setup API configuration based on environment
    
    Args:
        dev_mode: Whether to run in development mode
        
    Returns:
        Configuration dictionary for middleware
    """
    config = {
        "cors_origins": ["*"] if dev_mode else ["http://localhost:3000", "http://localhost:8000"],
        "enable_rate_limiting": not dev_mode,
        "rate_limit": 120 if dev_mode else 60,
        "trusted_hosts": None if dev_mode else ["localhost", "127.0.0.1"]
    }
    
    # Add API keys if environment variable is set
    api_keys_env = os.getenv("WITNESSOS_API_KEYS")
    if api_keys_env:
        # Format: "key1:user1,key2:user2"
        api_keys = {}
        for pair in api_keys_env.split(","):
            if ":" in pair:
                key, user = pair.split(":", 1)
                api_keys[key.strip()] = user.strip()
        config["api_keys"] = api_keys
    
    return config

def validate_environment():
    """Validate that all required engines and components are available"""
    try:
        # Test engine imports
        from engines import NumerologyEngine, BiorhythmEngine
        from integration.orchestrator import EngineOrchestrator
        from integration.workflows import WorkflowManager
        
        # Test orchestrator initialization
        orchestrator = EngineOrchestrator()
        available_engines = orchestrator.get_available_engines()
        
        logger.info(f"✅ Environment validation successful")
        logger.info(f"📊 Available engines: {len(available_engines)}")
        logger.info(f"🔧 Engines: {', '.join(available_engines)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Environment validation failed: {e}")
        return False

def main():
    """Main entry point for the API server"""
    parser = argparse.ArgumentParser(
        description="WitnessOS Divination Engines API Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Run on default port 8000
  python main.py --port 8080        # Run on port 8080
  python main.py --dev              # Development mode (no rate limiting)
  python main.py --host 0.0.0.0     # Listen on all interfaces
  
Environment Variables:
  WITNESSOS_API_KEYS               # API keys in format "key1:user1,key2:user2"
  WITNESSOS_LOG_LEVEL              # Logging level (DEBUG, INFO, WARNING, ERROR)
        """
    )
    
    parser.add_argument(
        "--host", 
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000,
        help="Port to run on (default: 8000)"
    )
    parser.add_argument(
        "--dev", 
        action="store_true",
        help="Run in development mode (disables rate limiting, enables CORS)"
    )
    parser.add_argument(
        "--reload", 
        action="store_true",
        help="Enable auto-reload on code changes (development only)"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default=os.getenv("WITNESSOS_LOG_LEVEL", "INFO"),
        help="Set logging level"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate environment and exit"
    )
    
    args = parser.parse_args()
    
    # Set logging level
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    # Validate environment
    logger.info("🔍 Validating WitnessOS environment...")
    if not validate_environment():
        logger.error("❌ Environment validation failed. Please check your installation.")
        sys.exit(1)
    
    if args.validate_only:
        logger.info("✅ Environment validation complete. Exiting.")
        return
    
    # Setup middleware with configuration
    config = setup_api_config(args.dev)
    setup_middleware(app, config)
    
    # Display startup information
    logger.info("🌟 Starting WitnessOS Divination Engines API")
    logger.info(f"🌐 Server: http://{args.host}:{args.port}")
    logger.info(f"📚 Documentation: http://{args.host}:{args.port}/docs")
    logger.info(f"🔧 Mode: {'Development' if args.dev else 'Production'}")
    
    if args.dev:
        logger.info("⚠️  Development mode: Rate limiting disabled, CORS enabled for all origins")
    
    if config.get("api_keys"):
        logger.info(f"🔐 API authentication enabled ({len(config['api_keys'])} keys)")
    else:
        logger.info("🔓 API authentication disabled")
    
    # Run the server
    try:
        uvicorn.run(
            "main:app",
            host=args.host,
            port=args.port,
            reload=args.reload and args.dev,
            log_level=args.log_level.lower(),
            access_log=True
        )
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
