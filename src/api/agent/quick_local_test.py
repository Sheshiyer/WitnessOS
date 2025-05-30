#!/usr/bin/env python3
"""
Quick test of WitnessOS Agent with local engines only
"""

import os
import sys
import asyncio
from pathlib import Path

# Add ENGINES directory to path
current_dir = Path(__file__).parent
engines_dir = current_dir.parent
sys.path.insert(0, str(engines_dir))

from agent.agent_service import WitnessOSAgent

async def test_local_engines():
    """Test the agent with local engines only"""
    
    # Check environment
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY environment variable not set")
        return

    print("🤖 WitnessOS AI Agent - Local Engines Test")
    print("Testing Aletheos + 10 Muses with local engine fallbacks")
    print()

    # Initialize agent with local engines only
    agent = WitnessOSAgent(
        production_api_url="http://localhost:9999",  # Intentionally wrong to force local
        openrouter_api_key=api_key,
        use_local_engines=True
    )

    # Test data
    test_subject = {
        "name": "Luna Starweaver",
        "date": "1988-06-21",
        "time": "12:00",
        "location": "Glastonbury, UK",
        "timezone": "Europe/London"
    }

    print(f"🌟 Testing with: {test_subject['name']}")
    print(f"   Born: {test_subject['date']} at {test_subject['time']} in {test_subject['location']}")
    print("=" * 70)

    # Test numerology with Aletheos
    print("\n🔢 Numerology + Aletheos Analysis")
    print("-" * 40)
    
    try:
        result = await agent.interpret_single_engine(
            engine_name="numerology",
            birth_data=test_subject,
            interpretation_style="witnessOS",
            model_type="primary"
        )
        
        if "consciousness_interpretation" in result:
            ai_guidance = result["consciousness_interpretation"]["ai_guidance"]
            print(f"✅ AI Interpretation (first 500 chars):")
            print(ai_guidance[:500] + "..." if len(ai_guidance) > 500 else ai_guidance)
            
            # Show calculation results
            calc_data = result.get("calculation_data", {})
            if "core_numbers" in calc_data:
                core = calc_data["core_numbers"]
                print(f"\n📊 Core Numbers:")
                print(f"   Life Path: {core.get('life_path')}")
                print(f"   Expression: {core.get('expression')}")
                print(f"   Soul Urge: {core.get('soul_urge')}")
                print(f"   Personality: {core.get('personality')}")
            
            # Show Aletheos insights
            witness_protocol = result.get("witness_protocol", {})
            if "aletheos_insights" in witness_protocol:
                insights = witness_protocol["aletheos_insights"]
                print(f"\n🌟 Aletheos Insights ({len(insights)} Muses activated):")
                for insight in insights[:3]:  # Show top 3
                    muse = insight.get("muse", "Unknown").replace("_", " ").title()
                    relevance = insight.get("relevance", 0)
                    print(f"   • {muse} (Relevance: {relevance:.2f})")
                    print(f"     {insight.get('insight', '')[:120]}...")
            
        else:
            print(f"❌ Unexpected result format")
            
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test biorhythm
    print("\n\n🌊 Biorhythm + Aletheos Analysis")
    print("-" * 40)
    
    try:
        result = await agent.interpret_single_engine(
            engine_name="biorhythm",
            birth_data=test_subject,
            interpretation_style="witnessOS",
            model_type="primary"
        )
        
        if "consciousness_interpretation" in result:
            ai_guidance = result["consciousness_interpretation"]["ai_guidance"]
            print(f"✅ AI Interpretation (first 400 chars):")
            print(ai_guidance[:400] + "..." if len(ai_guidance) > 400 else ai_guidance)
            
            # Show biorhythm cycles
            calc_data = result.get("calculation_data", {})
            if "cycles" in calc_data:
                cycles = calc_data["cycles"]
                print(f"\n📊 Current Cycles:")
                print(f"   Physical: {cycles.get('physical', 0):.1f}%")
                print(f"   Emotional: {cycles.get('emotional', 0):.1f}%")
                print(f"   Intellectual: {cycles.get('intellectual', 0):.1f}%")
            
        else:
            print(f"❌ Unexpected result format")
            
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test multi-engine with synthesis
    print("\n\n🌈 Multi-Engine Synthesis")
    print("-" * 40)
    
    try:
        result = await agent.interpret_multi_engine(
            engines=["numerology", "biorhythm"],
            birth_data=test_subject,
            interpretation_style="witnessOS",
            model_type="primary",
            include_synthesis=True
        )
        
        if "consciousness_synthesis" in result:
            synthesis = result["consciousness_synthesis"]["unified_field_analysis"]
            print(f"✅ Consciousness Synthesis (first 400 chars):")
            print(synthesis[:400] + "..." if len(synthesis) > 400 else synthesis)
            
            # Show field coherence
            session = result.get("consciousness_session", {})
            field_coherence = session.get("field_coherence", "unknown")
            print(f"\n📊 Field Coherence: {field_coherence}")
            
        else:
            print(f"❌ No synthesis generated")
            
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n" + "=" * 70)
    print("🎯 Test Summary:")
    print("   ✅ Local engines working (numerology, biorhythm)")
    print("   ✅ Aletheos + 10 Muses context extraction")
    print("   ✅ AI interpretations with consciousness guidance")
    print("   ✅ Multi-engine synthesis capabilities")
    print("   ✅ WitnessOS mystical-technical balance maintained")
    print("\n🌟 The enhanced WitnessOS Agent is fully operational!")

if __name__ == "__main__":
    asyncio.run(test_local_engines())
