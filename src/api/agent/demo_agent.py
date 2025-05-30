#!/usr/bin/env python3
"""
WitnessOS AI Agent Demo

Demonstrates the AI agent capabilities with sample birth data and interpretations.
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

from agent.agent_service import WitnessOSAgent

# Sample birth data (using user's data as default test data)
SAMPLE_BIRTH_DATA = {
    "name": "Mage Narayan",
    "date": "13.08.1991",
    "time": "13:31",
    "location": "Bengaluru",
    "timezone": "Asia/Kolkata"
}

async def demo_single_engine_interpretation():
    """Demo single engine interpretation"""
    print("\n🔮 Single Engine Interpretation Demo")
    print("=" * 50)
    
    # Initialize agent
    agent = WitnessOSAgent(
        production_api_url="http://localhost:8002",
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY")
    )
    
    # Test numerology interpretation
    print("Testing Numerology Engine with AI Interpretation...")
    
    try:
        result = await agent.interpret_single_engine(
            engine_name="numerology",
            birth_data=SAMPLE_BIRTH_DATA,
            interpretation_style="balanced",
            model_type="balanced"
        )
        
        print("\n✅ Numerology Interpretation Result:")
        print(f"Engine: {result.get('calculation_data', {}).get('engine', 'Unknown')}")
        print(f"Status: {result.get('calculation_data', {}).get('calculation_status', 'Unknown')}")
        print(f"Field Signature: {result.get('calculation_data', {}).get('field_signature', 'Unknown')}")
        
        # Display AI interpretation
        ai_guidance = result.get('consciousness_interpretation', {}).get('ai_guidance', '')
        if ai_guidance:
            print("\n🧠 AI Interpretation:")
            print("-" * 30)
            print(ai_guidance[:500] + "..." if len(ai_guidance) > 500 else ai_guidance)
        
        # Display reality patches
        reality_patches = result.get('witness_protocol', {}).get('reality_patches', [])
        if reality_patches:
            print("\n🔧 Reality Patches:")
            for patch in reality_patches[:2]:
                print(f"- {patch.get('description', 'No description')}")
        
    except Exception as e:
        print(f"❌ Error in single engine demo: {e}")

async def demo_multi_engine_interpretation():
    """Demo multi-engine interpretation with synthesis"""
    print("\n🌟 Multi-Engine Interpretation Demo")
    print("=" * 50)
    
    # Initialize agent
    agent = WitnessOSAgent(
        production_api_url="http://localhost:8002",
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY")
    )
    
    # Test multi-engine interpretation
    engines = ["numerology", "biorhythm", "human_design"]
    print(f"Testing Multi-Engine Analysis: {', '.join(engines)}")
    
    try:
        result = await agent.interpret_multi_engine(
            engines=engines,
            birth_data=SAMPLE_BIRTH_DATA,
            interpretation_style="witnessOS",
            model_type="reasoning",
            include_synthesis=True
        )
        
        print("\n✅ Multi-Engine Analysis Result:")
        session = result.get('consciousness_session', {})
        print(f"Session Type: {session.get('session_type', 'Unknown')}")
        print(f"Engines Deployed: {session.get('engines_deployed', [])}")
        print(f"Field Coherence: {session.get('field_coherence', 'Unknown')}")
        
        # Display engine diagnostics
        engine_diagnostics = result.get('engine_diagnostics', {})
        print(f"\n🔍 Engine Diagnostics ({len(engine_diagnostics)} engines):")
        for engine_name, diagnostic in engine_diagnostics.items():
            status = diagnostic.get('consciousness_debug_status', 'Unknown')
            print(f"- {engine_name.title()}: {status}")
        
        # Display synthesis
        synthesis = result.get('consciousness_synthesis', {}).get('unified_field_analysis', '')
        if synthesis:
            print("\n🧬 Consciousness Synthesis:")
            print("-" * 30)
            print(synthesis[:400] + "..." if len(synthesis) > 400 else synthesis)
        
        # Display reality optimization protocol
        reality_protocol = result.get('witness_protocol', {}).get('reality_optimization_protocol', [])
        if reality_protocol:
            print("\n⚡ Reality Optimization Protocol:")
            for patch in reality_protocol[:2]:
                print(f"- {patch.get('description', 'No description')}")
        
    except Exception as e:
        print(f"❌ Error in multi-engine demo: {e}")

async def demo_workflow_interpretation():
    """Demo workflow interpretation"""
    print("\n🌊 Workflow Interpretation Demo")
    print("=" * 50)
    
    # Initialize agent
    agent = WitnessOSAgent(
        production_api_url="http://localhost:8002",
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY")
    )
    
    # Test workflow interpretation
    workflow_name = "complete_natal"
    print(f"Testing Workflow: {workflow_name}")
    
    try:
        result = await agent.interpret_workflow(
            workflow_name=workflow_name,
            birth_data=SAMPLE_BIRTH_DATA,
            interpretation_style="witnessOS",
            model_type="creative"
        )
        
        print("\n✅ Workflow Interpretation Result:")
        session = result.get('consciousness_session', {})
        print(f"Session Type: {session.get('session_type', 'Unknown')}")
        print(f"Engines Deployed: {session.get('engines_deployed', [])}")
        
        # Display consciousness evolution pathway
        evolution_pathway = result.get('witness_protocol', {}).get('consciousness_evolution_pathway', [])
        if evolution_pathway:
            print("\n🌱 Consciousness Evolution Pathway:")
            for step in evolution_pathway[:3]:
                print(f"- {step}")
        
    except Exception as e:
        print(f"❌ Error in workflow demo: {e}")

async def demo_model_selection():
    """Demo different model types"""
    print("\n🧠 Model Selection Demo")
    print("=" * 50)
    
    # Initialize agent
    agent = WitnessOSAgent(
        production_api_url="http://localhost:8002",
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY")
    )
    
    # Test different models
    models = ["fast", "balanced", "creative"]
    
    for model_type in models:
        print(f"\nTesting {model_type.title()} Model:")
        try:
            result = await agent.interpret_single_engine(
                engine_name="numerology",
                birth_data=SAMPLE_BIRTH_DATA,
                interpretation_style="mystical",
                model_type=model_type
            )
            
            ai_guidance = result.get('consciousness_interpretation', {}).get('ai_guidance', '')
            print(f"✅ {model_type.title()} interpretation length: {len(ai_guidance)} characters")
            
        except Exception as e:
            print(f"❌ Error with {model_type} model: {e}")

async def main():
    """Main demo function"""
    print("🤖 WitnessOS AI Agent Demo")
    print("=" * 60)
    print(f"Using sample birth data: {SAMPLE_BIRTH_DATA['name']}")
    print(f"Born: {SAMPLE_BIRTH_DATA['date']} at {SAMPLE_BIRTH_DATA['time']} in {SAMPLE_BIRTH_DATA['location']}")
    
    # Check environment
    if not os.getenv("OPENROUTER_API_KEY"):
        print("\n❌ OPENROUTER_API_KEY environment variable not set")
        print("Please set your OpenRouter API key to run the demo.")
        return
    
    try:
        # Run demos
        await demo_single_engine_interpretation()
        await demo_multi_engine_interpretation()
        await demo_workflow_interpretation()
        await demo_model_selection()
        
        print("\n" + "=" * 60)
        print("✅ Demo completed successfully!")
        print("🌟 The WitnessOS AI Agent is ready for consciousness interpretation!")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("Make sure the production API is running on http://localhost:8002")

if __name__ == "__main__":
    asyncio.run(main())
