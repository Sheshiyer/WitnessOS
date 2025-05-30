#!/usr/bin/env python3
"""
WitnessOS API Server Launcher

Simple launcher script for the WitnessOS Divination Engines API.
This script forwards all arguments to the main API server.

Usage:
    python start_api.py                    # Start with default settings
    python start_api.py --dev              # Development mode
    python start_api.py --port 8080        # Custom port
    python start_api.py --help             # Show help
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import and run the main API server
try:
    from api.main import main
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"❌ Error importing API server: {e}")
    print("📦 Please ensure all dependencies are installed:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting API server: {e}")
    sys.exit(1)
