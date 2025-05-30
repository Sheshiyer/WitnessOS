#!/usr/bin/env python3
"""
Simple OpenRouter Test

Quick test to verify which models are working.
"""

import os
import sys
import asyncio
import json
from pathlib import Path

# Add ENGINES directory to path
current_dir = Path(__file__).parent
engines_dir = current_dir.parent
sys.path.insert(0, str(engines_dir))

# Load environment variables from .env.local
from dotenv import load_dotenv
load_dotenv(engines_dir / ".env.local")

from agent.openrouter_client import OpenRouterClient

async def test_single_model(client, model_type, model_name):
    """Test a single model"""
    print(f"\n🧪 Testing {model_type}: {model_name}")
    print("-" * 50)
    
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Say hello in one sentence."}
    ]
    
    try:
        # Use a shorter timeout for testing
        response = await client.generate_response(
            messages=messages,
            model_type=model_type,
            timeout=10  # 10 second timeout
        )
        
        if "choices" in response and response["choices"]:
            content = response["choices"][0]["message"]["content"]
            model_used = response.get("_model_used", "unknown")
            model_name_used = response.get("_model_name", "unknown")
            attempt = response.get("_attempt", 1)
            
            print(f"✅ SUCCESS")
            print(f"   Model used: {model_used} ({model_name_used})")
            print(f"   Attempt: {attempt}")
            print(f"   Response: {content[:100]}...")
            return True
        else:
            print(f"❌ FAILED - Unexpected response format")
            return False
            
    except Exception as e:
        print(f"❌ FAILED - {str(e)[:100]}...")
        return False

async def test_all_models():
    """Test all available models"""
    print("🤖 Simple OpenRouter Model Test")
    print("=" * 60)
    
    # Check API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found")
        return
    
    print(f"✅ API Key: {api_key[:20]}...")
    
    try:
        client = OpenRouterClient(api_key)
        models = client.list_available_models()
        
        print(f"\n📋 Testing {len(models)} models:")
        
        results = {}
        for model_type, config in models.items():
            success = await test_single_model(client, model_type, config.name)
            results[model_type] = success
        
        print("\n" + "=" * 60)
        print("📊 RESULTS SUMMARY:")
        print("-" * 30)
        
        working_models = []
        failed_models = []
        
        for model_type, success in results.items():
            if success:
                working_models.append(model_type)
                print(f"✅ {model_type}: WORKING")
            else:
                failed_models.append(model_type)
                print(f"❌ {model_type}: FAILED")
        
        print(f"\n🎯 Working models: {len(working_models)}/{len(models)}")
        if working_models:
            print(f"   Best to use: {working_models[0]}")
        else:
            print("   ⚠️  No models are working!")
        
        return working_models
        
    except Exception as e:
        print(f"❌ Error initializing client: {e}")
        return []

async def test_fallback_mechanism():
    """Test the automatic fallback mechanism"""
    print("\n🔄 Testing Fallback Mechanism")
    print("=" * 60)
    
    try:
        client = OpenRouterClient()
        
        # This should try primary first, then fallback automatically
        messages = [
            {"role": "system", "content": "You are a consciousness guide."},
            {"role": "user", "content": "Explain consciousness in one sentence."}
        ]
        
        print("📤 Sending request with automatic fallback...")
        
        response = await client.generate_response(
            messages=messages,
            model_type="primary"  # Start with primary, will fallback if needed
        )
        
        if "choices" in response and response["choices"]:
            content = response["choices"][0]["message"]["content"]
            model_used = response.get("_model_used", "unknown")
            model_name_used = response.get("_model_name", "unknown")
            attempt = response.get("_attempt", 1)
            
            print("✅ Fallback mechanism working!")
            print(f"   Final model used: {model_used} ({model_name_used})")
            print(f"   Attempts made: {attempt}")
            print(f"   Response: {content}")
            return True
        else:
            print("❌ Fallback mechanism failed")
            return False
            
    except Exception as e:
        print(f"❌ Fallback test failed: {e}")
        return False

async def main():
    """Main test function"""
    # Test individual models
    working_models = await test_all_models()
    
    # Test fallback mechanism
    if working_models:
        await test_fallback_mechanism()
    else:
        print("\n⚠️  Skipping fallback test - no working models found")
    
    print("\n" + "=" * 60)
    if working_models:
        print("✅ OpenRouter integration is working!")
        print("🚀 Ready to start the WitnessOS AI Agent!")
    else:
        print("❌ OpenRouter integration needs debugging")
        print("🔧 Check your API key and network connection")

if __name__ == "__main__":
    asyncio.run(main())
