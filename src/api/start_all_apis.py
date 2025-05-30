#!/usr/bin/env python3
"""
WitnessOS All APIs Startup Script

This script starts all WitnessOS APIs with proper port management and environment setup.
"""

import os
import sys
import time
import signal
import subprocess
from pathlib import Path
from typing import List, Dict
import argparse

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

class APIManager:
    """Manages multiple API processes"""
    
    def __init__(self):
        self.processes: Dict[str, subprocess.Popen] = {}
        self.api_configs = {
            "simple": {
                "name": "Simple API",
                "script": "simple_api.py",
                "port": 8001,
                "description": "Demo API with mock data"
            },
            "production": {
                "name": "Production API", 
                "script": "api/production_api.py",
                "port": 8002,
                "description": "Production API with real engines"
            },
            "agent": {
                "name": "Agent API",
                "script": "agent/start_agent.py", 
                "port": 8003,
                "description": "AI Agent API with OpenRouter integration"
            }
        }
    
    def check_environment(self) -> bool:
        """Check if environment is properly configured"""
        env_file = current_dir / ".env"
        if not env_file.exists():
            print("❌ .env file not found")
            print("   Run: python setup_environment.py")
            return False
        
        # Load environment variables
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        
        # Check OpenRouter API key for agent
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if not openrouter_key or openrouter_key == "your_openrouter_api_key_here":
            print("⚠️  OpenRouter API key not configured")
            print("   Agent API will not work properly")
            return False
        
        return True
    
    def start_api(self, api_name: str) -> bool:
        """Start a specific API"""
        if api_name not in self.api_configs:
            print(f"❌ Unknown API: {api_name}")
            return False
        
        config = self.api_configs[api_name]
        script_path = current_dir / config["script"]
        
        if not script_path.exists():
            print(f"❌ Script not found: {script_path}")
            return False
        
        try:
            print(f"🚀 Starting {config['name']} on port {config['port']}...")
            
            # Start the process
            process = subprocess.Popen(
                [sys.executable, str(script_path), "--port", str(config["port"])],
                cwd=current_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes[api_name] = process
            
            # Give it a moment to start
            time.sleep(2)
            
            # Check if process is still running
            if process.poll() is None:
                print(f"✅ {config['name']} started successfully")
                print(f"   🌐 URL: http://localhost:{config['port']}")
                print(f"   📚 Docs: http://localhost:{config['port']}/docs")
                return True
            else:
                stdout, stderr = process.communicate()
                print(f"❌ {config['name']} failed to start")
                if stderr:
                    print(f"   Error: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error starting {config['name']}: {e}")
            return False
    
    def stop_api(self, api_name: str):
        """Stop a specific API"""
        if api_name in self.processes:
            process = self.processes[api_name]
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                print(f"🛑 Stopped {self.api_configs[api_name]['name']}")
            del self.processes[api_name]
    
    def stop_all(self):
        """Stop all running APIs"""
        print("\n🛑 Stopping all APIs...")
        for api_name in list(self.processes.keys()):
            self.stop_api(api_name)
    
    def status(self):
        """Show status of all APIs"""
        print("\n📊 API Status:")
        print("-" * 50)
        
        for api_name, config in self.api_configs.items():
            if api_name in self.processes:
                process = self.processes[api_name]
                if process.poll() is None:
                    status = "🟢 Running"
                else:
                    status = "🔴 Stopped"
                    del self.processes[api_name]
            else:
                status = "⚪ Not started"
            
            print(f"{config['name']:15} | {status:12} | Port {config['port']} | {config['description']}")

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\n🛑 Received interrupt signal...")
    manager.stop_all()
    sys.exit(0)

def main():
    """Main function"""
    global manager
    manager = APIManager()
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    parser = argparse.ArgumentParser(description="WitnessOS API Manager")
    parser.add_argument("--api", choices=["simple", "production", "agent", "all"], 
                       default="all", help="Which API(s) to start")
    parser.add_argument("--status", action="store_true", help="Show API status")
    parser.add_argument("--stop", action="store_true", help="Stop all APIs")
    
    args = parser.parse_args()
    
    if args.status:
        manager.status()
        return
    
    if args.stop:
        manager.stop_all()
        return
    
    print("🌟 WitnessOS API Manager")
    print("=" * 40)
    
    # Check environment
    if not manager.check_environment():
        print("\n❌ Environment check failed")
        print("   Run: python setup_environment.py")
        sys.exit(1)
    
    # Start requested APIs
    if args.api == "all":
        apis_to_start = ["simple", "production", "agent"]
    else:
        apis_to_start = [args.api]
    
    success_count = 0
    for api_name in apis_to_start:
        if manager.start_api(api_name):
            success_count += 1
    
    if success_count > 0:
        print(f"\n✅ Started {success_count}/{len(apis_to_start)} APIs successfully")
        manager.status()
        
        print("\n🎯 Quick Links:")
        for api_name in apis_to_start:
            if api_name in manager.processes:
                config = manager.api_configs[api_name]
                print(f"   {config['name']}: http://localhost:{config['port']}")
        
        print("\n⌨️  Press Ctrl+C to stop all APIs")
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
                # Check if any process has died
                for api_name in list(manager.processes.keys()):
                    if manager.processes[api_name].poll() is not None:
                        print(f"⚠️  {manager.api_configs[api_name]['name']} has stopped")
                        del manager.processes[api_name]
        except KeyboardInterrupt:
            pass
    else:
        print("\n❌ No APIs started successfully")
        sys.exit(1)

if __name__ == "__main__":
    main()
