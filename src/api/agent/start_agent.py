#!/usr/bin/env python3
"""
WitnessOS AI Agent Startup Script

Starts the AI agent API server with proper configuration and environment setup.
"""

import os
import sys
import logging
import argparse
from pathlib import Path

# Add ENGINES directory to path
current_dir = Path(__file__).parent
engines_dir = current_dir.parent
sys.path.insert(0, str(engines_dir))

# Import configuration system
from config import get_config, validate_environment

def setup_logging(log_level: str = "info"):
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def check_environment():
    """Check required environment variables and dependencies using new config system"""

    # Use new configuration system
    config = get_config()
    validation = validate_environment()

    print(f"🔗 Production API URL: {config.get('production_api_url')}")

    # Check environment files
    env_status = config.get_env_file_status()
    available_files = [f for f, exists in env_status.items() if exists]
    print(f"📁 Available env files: {', '.join(available_files)}")

    # Check OpenRouter API key
    if config.is_openrouter_configured():
        print("✅ OpenRouter API key configured")
    else:
        print("❌ OpenRouter API key not configured")

    # Check required packages
    try:
        import httpx
        import fastapi
        import uvicorn
        print("✅ Required packages available")
    except ImportError as e:
        validation['issues'].append(f"Missing required package: {e}")

    # Display validation results
    if validation['warnings']:
        print("\n⚠️  Warnings:")
        for warning in validation['warnings']:
            print(f"   ⚠️  {warning}")

    if validation['issues']:
        print("\n⚠️  Environment Issues:")
        for issue in validation['issues']:
            print(f"   ❌ {issue}")
        print("\nPlease resolve these issues before starting the agent.")
        return False

    return True

def main():
    """Main startup function"""
    parser = argparse.ArgumentParser(description="WitnessOS AI Agent API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8003, help="Port to run on")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--log-level", default="info", help="Log level")
    parser.add_argument("--check-only", action="store_true", help="Only check environment, don't start server")
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    print("🤖 WitnessOS AI Agent Startup")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    if args.check_only:
        print("\n✅ Environment check passed!")
        return
    
    print("\n🚀 Starting WitnessOS AI Agent API...")
    print(f"🌐 Server will be available at: http://{args.host}:{args.port}")
    print(f"📚 API Documentation: http://{args.host}:{args.port}/agent/docs")
    print(f"🔍 Health Check: http://{args.host}:{args.port}/agent/health")
    print("\n" + "=" * 50)
    
    try:
        import uvicorn
        from agent_api import app
        
        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level=args.log_level,
            access_log=True
        )
        
    except KeyboardInterrupt:
        logger.info("Agent API server stopped by user")
    except Exception as e:
        logger.error(f"Failed to start agent API server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
