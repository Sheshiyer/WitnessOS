#!/usr/bin/env python3
"""
WitnessOS API Testing Script

Test script for validating the WitnessOS Divination Engines API endpoints.
Tests all major functionality including individual engines, multi-engine runs,
workflows, and field analysis.

Usage:
    python test_api.py                    # Test against localhost:8000
    python test_api.py --host localhost   # Custom host
    python test_api.py --port 8080        # Custom port
    python test_api.py --verbose          # Detailed output
"""

import argparse
import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any

# Test data using your personal birth information
TEST_BIRTH_DATA = {
    "name": "Cumbipuram Nateshan Sheshnarayan",
    "date": "13.08.1991",
    "time": "13:31",
    "location": "Bengaluru",
    "timezone": "Asia/Kolkata"
}

class WitnessOSAPITester:
    """Test suite for WitnessOS API endpoints"""
    
    def __init__(self, base_url: str, verbose: bool = False):
        self.base_url = base_url.rstrip('/')
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'WitnessOS-API-Tester/1.0'
        })
        
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def verbose_log(self, message: str):
        """Log verbose message"""
        if self.verbose:
            self.log(message, "DEBUG")
    
    def test_health_check(self) -> bool:
        """Test the health check endpoint"""
        self.log("Testing health check endpoint...")
        
        try:
            response = self.session.get(f"{self.base_url}/health")
            
            if response.status_code == 200:
                data = response.json()
                self.log("✅ Health check passed")
                self.verbose_log(f"Response: {json.dumps(data, indent=2)}")
                return True
            else:
                self.log(f"❌ Health check failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log(f"❌ Health check error: {e}")
            return False
    
    def test_list_engines(self) -> bool:
        """Test listing available engines"""
        self.log("Testing engine listing...")
        
        try:
            response = self.session.get(f"{self.base_url}/engines")
            
            if response.status_code == 200:
                data = response.json()
                engines = data.get('available_engines', [])
                self.log(f"✅ Found {len(engines)} engines: {', '.join(engines)}")
                self.verbose_log(f"Response: {json.dumps(data, indent=2)}")
                return True
            else:
                self.log(f"❌ Engine listing failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log(f"❌ Engine listing error: {e}")
            return False
    
    def test_single_engine(self, engine_name: str) -> bool:
        """Test running a single engine"""
        self.log(f"Testing {engine_name} engine...")
        
        try:
            # Prepare request data
            request_data = {
                "engine_name": engine_name,
                "input_data": TEST_BIRTH_DATA,
                "format": "witnessOS"
            }
            
            response = self.session.post(
                f"{self.base_url}/engines/run",
                json=request_data
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"✅ {engine_name} engine completed successfully")
                self.verbose_log(f"Response: {json.dumps(data, indent=2)}")
                return True
            else:
                self.log(f"❌ {engine_name} engine failed: {response.status_code}")
                if self.verbose:
                    self.log(f"Error: {response.text}")
                return False
                
        except Exception as e:
            self.log(f"❌ {engine_name} engine error: {e}")
            return False
    
    def test_multi_engine(self) -> bool:
        """Test running multiple engines"""
        self.log("Testing multi-engine execution...")
        
        try:
            # Test with engines that should work
            request_data = {
                "engines": ["numerology", "biorhythm"],
                "birth_data": TEST_BIRTH_DATA,
                "parallel": True,
                "synthesize": True,
                "format": "witnessOS"
            }
            
            response = self.session.post(
                f"{self.base_url}/engines/multi",
                json=request_data
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log("✅ Multi-engine execution completed successfully")
                self.verbose_log(f"Response: {json.dumps(data, indent=2)}")
                return True
            else:
                self.log(f"❌ Multi-engine execution failed: {response.status_code}")
                if self.verbose:
                    self.log(f"Error: {response.text}")
                return False
                
        except Exception as e:
            self.log(f"❌ Multi-engine execution error: {e}")
            return False
    
    def test_workflows(self) -> bool:
        """Test workflow listing and execution"""
        self.log("Testing workflow functionality...")
        
        try:
            # First, list available workflows
            response = self.session.get(f"{self.base_url}/workflows")
            
            if response.status_code != 200:
                self.log(f"❌ Workflow listing failed: {response.status_code}")
                return False
            
            workflows_data = response.json()
            workflows = workflows_data.get('available_workflows', [])
            self.log(f"Found {len(workflows)} workflows")
            
            if not workflows:
                self.log("⚠️  No workflows available to test")
                return True
            
            # Test running a workflow
            test_workflow = workflows[0]  # Use first available workflow
            request_data = {
                "workflow_name": test_workflow,
                "birth_data": TEST_BIRTH_DATA,
                "format": "witnessOS"
            }
            
            response = self.session.post(
                f"{self.base_url}/workflows/run",
                json=request_data
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"✅ Workflow '{test_workflow}' completed successfully")
                self.verbose_log(f"Response: {json.dumps(data, indent=2)}")
                return True
            else:
                self.log(f"❌ Workflow execution failed: {response.status_code}")
                if self.verbose:
                    self.log(f"Error: {response.text}")
                return False
                
        except Exception as e:
            self.log(f"❌ Workflow testing error: {e}")
            return False
    
    def test_field_analysis(self) -> bool:
        """Test consciousness field analysis"""
        self.log("Testing field analysis...")
        
        try:
            request_data = {
                "birth_data": TEST_BIRTH_DATA,
                "engines": ["numerology", "biorhythm"],
                "analysis_depth": "standard"
            }
            
            response = self.session.post(
                f"{self.base_url}/field-analysis",
                json=request_data
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log("✅ Field analysis completed successfully")
                self.verbose_log(f"Response: {json.dumps(data, indent=2)}")
                return True
            else:
                self.log(f"❌ Field analysis failed: {response.status_code}")
                if self.verbose:
                    self.log(f"Error: {response.text}")
                return False
                
        except Exception as e:
            self.log(f"❌ Field analysis error: {e}")
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all API tests"""
        self.log("🌟 Starting WitnessOS API Test Suite")
        self.log(f"🌐 Testing against: {self.base_url}")
        
        results = {}
        
        # Basic connectivity tests
        results['health_check'] = self.test_health_check()
        results['list_engines'] = self.test_list_engines()
        
        # Engine tests
        test_engines = ['numerology', 'biorhythm']
        for engine in test_engines:
            results[f'engine_{engine}'] = self.test_single_engine(engine)
        
        # Integration tests
        results['multi_engine'] = self.test_multi_engine()
        results['workflows'] = self.test_workflows()
        results['field_analysis'] = self.test_field_analysis()
        
        # Summary
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        self.log(f"\n📊 Test Results: {passed}/{total} tests passed")
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            self.log(f"   {test_name}: {status}")
        
        if passed == total:
            self.log("🎉 All tests passed! WitnessOS API is working correctly.")
        else:
            self.log("⚠️  Some tests failed. Check the logs above for details.")
        
        return results

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Test WitnessOS Divination Engines API",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--host",
        default="localhost",
        help="API host (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="API port (default: 8000)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--ssl",
        action="store_true",
        help="Use HTTPS instead of HTTP"
    )
    
    args = parser.parse_args()
    
    # Build base URL
    protocol = "https" if args.ssl else "http"
    base_url = f"{protocol}://{args.host}:{args.port}"
    
    # Run tests
    tester = WitnessOSAPITester(base_url, args.verbose)
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    all_passed = all(results.values())
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
