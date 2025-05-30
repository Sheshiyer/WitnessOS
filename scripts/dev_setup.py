#!/usr/bin/env python3
"""
WitnessOS Development Environment Setup
Sets up the complete development environment for WitnessOS
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description, check=True):
    """Run a command with error handling"""
    print(f"\n🔧 {description}")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
        else:
            print(f"⚠️ {description} - WARNING")
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        if e.stderr:
            print("Error:", e.stderr)
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.11+")
        return False

def setup_environment():
    """Set up the development environment"""
    print("🌟 WitnessOS Development Environment Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    print(f"📁 Working directory: {project_root}")
    
    # Install dependencies
    run_command(
        ['pip', 'install', '-r', 'requirements.txt'],
        "Installing Python dependencies"
    )
    
    # Install development dependencies
    dev_packages = [
        'pytest>=7.0.0',
        'pytest-cov>=4.0.0',
        'pytest-asyncio>=0.21.0',
        'flake8>=6.0.0',
        'black>=23.0.0',
        'isort>=5.12.0',
        'mypy>=1.0.0'
    ]
    
    for package in dev_packages:
        run_command(
            ['pip', 'install', package],
            f"Installing {package}",
            check=False
        )
    
    # Set up pre-commit hooks (if available)
    run_command(
        ['pip', 'install', 'pre-commit'],
        "Installing pre-commit",
        check=False
    )
    
    # Create .env file if it doesn't exist
    env_file = project_root / '.env'
    if not env_file.exists():
        print("\n📝 Creating .env file")
        env_content = """# WitnessOS Environment Configuration
# OpenRouter API Key for AI Agent
OPENROUTER_API_KEY=your_openrouter_api_key_here

# API Configuration
SIMPLE_API_PORT=8001
PRODUCTION_API_PORT=8002
AGENT_API_PORT=8003

# Development Settings
DEBUG=true
LOG_LEVEL=INFO
"""
        env_file.write_text(env_content)
        print("✅ Created .env file - Please update with your API keys")
    
    # Run initial tests
    print("\n🧪 Running initial test suite")
    run_command(
        ['python', '-m', 'pytest', 'tests/', '--tb=short'],
        "Initial test run",
        check=False
    )
    
    print("\n" + "=" * 50)
    print("🎉 Development environment setup complete!")
    print("\n📋 Next steps:")
    print("1. Update .env file with your API keys")
    print("2. Run: python src/api/main.py --dev")
    print("3. Visit: http://localhost:8001/docs (Simple API)")
    print("4. Visit: http://localhost:8002/docs (Production API)")
    print("5. Visit: http://localhost:8003/docs (Agent API)")

if __name__ == "__main__":
    setup_environment()