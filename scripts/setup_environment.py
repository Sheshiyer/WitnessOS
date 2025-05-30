#!/usr/bin/env python3
"""
WitnessOS Environment Setup Script

This script helps set up the environment for running WitnessOS APIs.
It creates the .env file and validates the configuration.
"""

import os
import sys
from pathlib import Path
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'httpx',
        'pydantic'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n📦 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    env_file = Path(".env")
    template_file = Path(".env.template")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if not template_file.exists():
        print("❌ .env.template file not found")
        return False
    
    # Copy template to .env
    with open(template_file, 'r') as f:
        template_content = f.read()
    
    with open(env_file, 'w') as f:
        f.write(template_content)
    
    print("✅ Created .env file from template")
    print("⚠️  Please edit .env file and add your OpenRouter API key")
    return True

def validate_env_file():
    """Validate the .env file configuration"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    # Load environment variables from .env file
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value
    
    # Check OpenRouter API key
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_key or openrouter_key == "your_openrouter_api_key_here":
        print("❌ OpenRouter API key not configured")
        print("   Please edit .env file and set OPENROUTER_API_KEY")
        return False
    
    print("✅ OpenRouter API key configured")
    return True

def check_ports():
    """Check if required ports are available"""
    import socket
    
    ports = {
        8001: "Simple API",
        8002: "Production API", 
        8003: "Agent API"
    }
    
    for port, service in ports.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        
        if result == 0:
            print(f"⚠️  Port {port} ({service}) is already in use")
        else:
            print(f"✅ Port {port} ({service}) is available")

def main():
    """Main setup function"""
    print("🌟 WitnessOS Environment Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first")
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Validate configuration
    env_valid = validate_env_file()
    
    # Check ports
    print("\n🔍 Checking port availability:")
    check_ports()
    
    print("\n" + "=" * 40)
    if env_valid:
        print("✅ Environment setup complete!")
        print("\n🚀 You can now start the APIs:")
        print("   Simple API:     python ENGINES/simple_api.py")
        print("   Production API: python ENGINES/api/production_api.py")
        print("   Agent API:      python ENGINES/agent/start_agent.py")
    else:
        print("⚠️  Environment setup incomplete")
        print("   Please configure your OpenRouter API key in .env file")
        print("   Then run this script again to validate")

if __name__ == "__main__":
    main()
