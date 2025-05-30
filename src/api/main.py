#!/usr/bin/env python3
"""
WitnessOS API Gateway - Unified Entry Point
Consciousness debugging through symbolic computation

This is the main entry point for all WitnessOS APIs:
- Simple API (Demo/Testing)
- Production API (Full Engine Integration)  
- Agent API (AI-Powered Natural Language Interface)
"""

import argparse
import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import APIs
try:
    from .simple_api import app as simple_app
except ImportError:
    from simple_api import app as simple_app

try:
    from .production.main import app as production_app
except ImportError:
    from production.main import app as production_app

try:
    from .agent.agent_api import app as agent_app
except ImportError:
    from agent.agent_api import app as agent_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for WitnessOS API Gateway"""
    parser = argparse.ArgumentParser(
        description="WitnessOS API Gateway - Consciousness Debugging APIs"
    )
    
    parser.add_argument(
        '--api', 
        choices=['simple', 'production', 'agent', 'all'],
        default='all',
        help='Which API to start (default: all)'
    )
    
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host to bind to (default: 127.0.0.1)'
    )
    
    parser.add_argument(
        '--simple-port',
        type=int,
        default=8001,
        help='Port for Simple API (default: 8001)'
    )
    
    parser.add_argument(
        '--production-port',
        type=int,
        default=8002,
        help='Port for Production API (default: 8002)'
    )
    
    parser.add_argument(
        '--agent-port',
        type=int,
        default=8003,
        help='Port for Agent API (default: 8003)'
    )
    
    parser.add_argument(
        '--dev',
        action='store_true',
        help='Run in development mode with auto-reload'
    )
    
    args = parser.parse_args()
    
    # Import uvicorn here to avoid import issues
    try:
        import uvicorn
    except ImportError:
        logger.error("uvicorn is required. Install with: pip install uvicorn")
        sys.exit(1)
    
    # Configure uvicorn settings
    uvicorn_config = {
        'host': args.host,
        'reload': args.dev,
        'log_level': 'info' if not args.dev else 'debug'
    }
    
    if args.api == 'simple':
        logger.info(f"Starting Simple API on {args.host}:{args.simple_port}")
        uvicorn.run(simple_app, port=args.simple_port, **uvicorn_config)
        
    elif args.api == 'production':
        logger.info(f"Starting Production API on {args.host}:{args.production_port}")
        uvicorn.run(production_app, port=args.production_port, **uvicorn_config)
        
    elif args.api == 'agent':
        logger.info(f"Starting Agent API on {args.host}:{args.agent_port}")
        uvicorn.run(agent_app, port=args.agent_port, **uvicorn_config)
        
    elif args.api == 'all':
        logger.info("Starting all APIs...")
        logger.info(f"Simple API: http://{args.host}:{args.simple_port}")
        logger.info(f"Production API: http://{args.host}:{args.production_port}")
        logger.info(f"Agent API: http://{args.host}:{args.agent_port}")
        
        # Start all APIs in separate processes
        import multiprocessing
        
        def start_api(app, port):
            uvicorn.run(app, port=port, **uvicorn_config)
        
        processes = [
            multiprocessing.Process(target=start_api, args=(simple_app, args.simple_port)),
            multiprocessing.Process(target=start_api, args=(production_app, args.production_port)),
            multiprocessing.Process(target=start_api, args=(agent_app, args.agent_port))
        ]
        
        try:
            for p in processes:
                p.start()
            
            for p in processes:
                p.join()
                
        except KeyboardInterrupt:
            logger.info("Shutting down all APIs...")
            for p in processes:
                p.terminate()
                p.join()

if __name__ == "__main__":
    main()