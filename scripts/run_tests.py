#!/usr/bin/env python3
"""
WitnessOS Test Runner
Comprehensive testing script for all WitnessOS components
"""

import argparse
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n🧪 {description}")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} - PASSED")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="WitnessOS Test Runner")
    parser.add_argument(
        '--type',
        choices=['unit', 'integration', 'api', 'all'],
        default='all',
        help='Type of tests to run'
    )
    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Run with coverage reporting'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Base pytest command
    pytest_cmd = ['python', '-m', 'pytest']
    
    if args.verbose:
        pytest_cmd.append('-v')
    
    if args.coverage:
        pytest_cmd.extend(['--cov=src', '--cov-report=html', '--cov-report=term'])
    
    success = True
    
    if args.type == 'unit' or args.type == 'all':
        cmd = pytest_cmd + ['tests/unit/', '-m', 'unit']
        success &= run_command(cmd, "Unit Tests")
    
    if args.type == 'integration' or args.type == 'all':
        cmd = pytest_cmd + ['tests/integration/', '-m', 'integration']
        success &= run_command(cmd, "Integration Tests")
    
    if args.type == 'api' or args.type == 'all':
        cmd = pytest_cmd + ['tests/api/', '-m', 'api']
        success &= run_command(cmd, "API Tests")
    
    # Run linting
    print("\n🔍 Running Code Quality Checks")
    
    # Flake8
    flake8_cmd = ['python', '-m', 'flake8', 'src/', '--max-line-length=100']
    run_command(flake8_cmd, "Flake8 Linting")
    
    # Summary
    print("\n" + "="*50)
    if success:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    import os
    main()