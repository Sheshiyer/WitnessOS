#!/usr/bin/env python3
"""
Test OpenRouter API Connection

Tests the OpenRouter client with the provided API key and lists available models.
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

async def test_openrouter_connection():
    """Test basic OpenRouter API connection"""
    print("🔗 Testing OpenRouter API Connection")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment")
        return False
    
    print(f"✅ API Key found: {api_key[:20]}...")
    
    try:
        # Initialize client
        client = OpenRouterClient(api_key)
        print("✅ OpenRouter client initialized")
        
        # List available models
        models = client.list_available_models()
        print(f"\n📋 Available Models ({len(models)}):")
        print("-" * 30)
        
        for model_type, config in models.items():
            print(f"🤖 {model_type.upper()}")
            print(f"   Name: {config.name}")
            print(f"   Description: {config.description}")
            print(f"   Cost: ${config.cost_per_1k_tokens}/1k tokens")
            print(f"   Context: {config.context_window:,} tokens")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing OpenRouter client: {e}")
        return False

async def test_simple_request():
    """Test a simple API request"""
    print("🧪 Testing Simple API Request")
    print("=" * 50)
    
    try:
        client = OpenRouterClient()
        
        # Test with free model
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": "Say hello and introduce yourself briefly."}
        ]
        
        print("📤 Sending test request to primary model (Microsoft Phi-4)...")

        response = await client.generate_response(
            messages=messages,
            model_type="primary"
        )
        
        if "choices" in response and response["choices"]:
            content = response["choices"][0]["message"]["content"]
            model_used = response.get("_model_used", "unknown")
            model_name = response.get("_model_name", "unknown")
            attempt = response.get("_attempt", 1)

            print("✅ Response received:")
            print(f"Model used: {model_used} ({model_name}) - Attempt {attempt}")
            print("-" * 20)
            print(content)
            print("-" * 20)
            return True
        else:
            print("❌ Unexpected response format:")
            print(json.dumps(response, indent=2))
            return False
            
    except Exception as e:
        print(f"❌ Error in API request: {e}")
        return False

async def test_consciousness_interpretation():
    """Test a consciousness-themed interpretation"""
    print("🌟 Testing Consciousness Interpretation")
    print("=" * 50)
    
    try:
        client = OpenRouterClient()
        
        # Test consciousness interpretation prompt
        messages = [
            {
                "role": "system", 
                "content": """You are the WitnessOS Consciousness Agent, an AI interpreter specializing in translating symbolic computation into meaningful guidance for consciousness exploration. You operate within the mystical-technical framework of WitnessOS."""
            },
            {
                "role": "user", 
                "content": """Interpret this numerology calculation:

Birth Name: Mage Narayan
Birth Date: 13.08.1991
Life Path Number: 5
Expression Number: 7
Soul Urge Number: 3

Provide a brief consciousness-aware interpretation that maintains the mystical-technical balance."""
            }
        ]
        
        print("📤 Sending consciousness interpretation request...")
        
        response = await client.generate_response(
            messages=messages,
            model_type="primary",
            temperature=0.8
        )
        
        if "choices" in response and response["choices"]:
            content = response["choices"][0]["message"]["content"]
            model_used = response.get("_model_used", "unknown")
            model_name = response.get("_model_name", "unknown")
            attempt = response.get("_attempt", 1)

            print("✅ Consciousness interpretation received:")
            print(f"Model used: {model_used} ({model_name}) - Attempt {attempt}")
            print("-" * 40)
            print(content)
            print("-" * 40)
            return True
        else:
            print("❌ Unexpected response format")
            return False
            
    except Exception as e:
        print(f"❌ Error in consciousness interpretation: {e}")
        return False

async def test_model_selection():
    """Test different model types"""
    print("🎯 Testing Model Selection")
    print("=" * 50)
    
    client = OpenRouterClient()
    
    # Test model selection logic
    test_cases = [
        ("interpretation", "low"),
        ("synthesis", "high"),
        ("creative", "medium"),
        ("analysis", "medium")
    ]
    
    for task_type, complexity in test_cases:
        selected_model = client.select_optimal_model(task_type, complexity)
        model_config = client.get_model_info(selected_model)
        
        print(f"📋 Task: {task_type} ({complexity} complexity)")
        print(f"   Selected: {selected_model} -> {model_config.name}")
        print(f"   Cost: ${model_config.cost_per_1k_tokens}/1k tokens")
        print()

async def main():
    """Main test function"""
    print("🤖 WitnessOS OpenRouter API Test")
    print("=" * 60)
    
    # Test connection
    connection_ok = await test_openrouter_connection()
    if not connection_ok:
        print("\n❌ Connection test failed. Please check your API key.")
        return
    
    # Test simple request
    print("\n")
    simple_ok = await test_simple_request()
    if not simple_ok:
        print("\n❌ Simple request test failed.")
        return
    
    # Test consciousness interpretation
    print("\n")
    consciousness_ok = await test_consciousness_interpretation()
    if not consciousness_ok:
        print("\n❌ Consciousness interpretation test failed.")
        return
    
    # Test model selection
    print("\n")
    await test_model_selection()
    
    print("\n" + "=" * 60)
    print("✅ All OpenRouter tests passed!")
    print("🌟 The WitnessOS AI Agent is ready for consciousness interpretation!")
    print("\nNext steps:")
    print("1. Start the production API: python ENGINES/api/production_api.py")
    print("2. Start the agent API: python ENGINES/agent/start_agent.py")
    print("3. Test the full agent: python ENGINES/agent/demo_agent.py")

if __name__ == "__main__":
    asyncio.run(main())
