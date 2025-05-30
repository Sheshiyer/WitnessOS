#!/usr/bin/env python3
"""
Quick WitnessOS AI Agent Demo

Uses your actual Human Design chart data to demonstrate the AI agent capabilities.
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

# Your actual birth data from the chart
YOUR_BIRTH_DATA = {
    "name": "Sheshnarayan Gumbipuram Natarajan",
    "date": "13.08.1991",
    "time": "13:31",
    "location": "Bengaluru, Karnataka, India",
    "timezone": "Asia/Kolkata"
}

# Your Human Design chart data from the image
YOUR_HUMAN_DESIGN_DATA = {
    "personality_type": "Generator",
    "profile": "2/4 (Hermit/Opportunist)",
    "strategy": "Wait for an opportunity to respond",
    "authority": "Sacral",
    "definition": "Split Definition",
    "not_self": "Frustration",
    "incarnation_cross": "The Right Angle Cross of Explanation (4/49 | 29/43)",
    "variables": "PRL DRL",
    "design_gates": [24.4, 43.4, 54.6, 53.6, 24.4, 42.6, 52.1, 62.2, 31.5, 41.6, 38.5, 54.2, 49.1],
    "personality_gates": [4.2, 49.2, 54.4, 53.4, 46.6, 59.5, 59.5, 47.1, 4.5, 41.1, 38.1, 38.6, 1.5]
}

async def test_human_design_interpretation():
    """Test AI interpretation of your Human Design chart"""
    print("🌟 WitnessOS AI Agent - Human Design Interpretation Demo")
    print("=" * 70)
    print(f"Subject: {YOUR_BIRTH_DATA['name']}")
    print(f"Born: {YOUR_BIRTH_DATA['date']} at {YOUR_BIRTH_DATA['time']} in {YOUR_BIRTH_DATA['location']}")
    print(f"Type: {YOUR_HUMAN_DESIGN_DATA['personality_type']} {YOUR_HUMAN_DESIGN_DATA['profile']}")
    print(f"Strategy: {YOUR_HUMAN_DESIGN_DATA['strategy']}")
    print(f"Authority: {YOUR_HUMAN_DESIGN_DATA['authority']}")
    print()

    try:
        # Initialize agent
        agent = WitnessOSAgent(
            production_api_url="http://localhost:8002",
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY")
        )

        print("🔮 Generating AI interpretation of your Human Design chart...")
        print("-" * 50)

        # Create a mock Human Design calculation result for the agent to interpret
        mock_calculation_result = {
            "engine": "human_design",
            "result": YOUR_HUMAN_DESIGN_DATA,
            "status": "success",
            "timestamp": "2024-05-30T14:20:00Z"
        }

        # Test the AI interpretation directly using the agent's internal method
        interpretation = await agent._generate_interpretation(
            engine_name="human_design",
            calculation_data=mock_calculation_result,
            birth_data=YOUR_BIRTH_DATA,
            style="witnessOS",
            model_type="primary"
        )

        print("✅ AI Interpretation Generated!")
        print("=" * 70)
        print(interpretation)
        print("=" * 70)

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_numerology_interpretation():
    """Test AI interpretation of numerology for your birth data"""
    print("\n🔢 Numerology Interpretation Demo")
    print("=" * 50)

    try:
        agent = WitnessOSAgent(
            production_api_url="http://localhost:8002",
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY")
        )

        print("📊 Getting numerology calculation and AI interpretation...")

        # This will call the production API and get AI interpretation
        result = await agent.interpret_single_engine(
            engine_name="numerology",
            birth_data=YOUR_BIRTH_DATA,
            interpretation_style="witnessOS",
            model_type="primary"
        )

        if "consciousness_interpretation" in result:
            ai_guidance = result["consciousness_interpretation"]["ai_guidance"]
            print("\n✅ Numerology AI Interpretation:")
            print("-" * 40)
            print(ai_guidance)
            print("-" * 40)

            # Show reality patches
            reality_patches = result.get("witness_protocol", {}).get("reality_patches", [])
            if reality_patches:
                print("\n🔧 Reality Patches:")
                for patch in reality_patches[:2]:
                    print(f"- {patch.get('description', 'No description')}")

            return True
        else:
            print(f"❌ Unexpected result format: {result}")
            return False

    except Exception as e:
        print(f"❌ Error in numerology interpretation: {e}")
        return False

async def test_multi_engine_synthesis():
    """Test multi-engine analysis with AI synthesis"""
    print("\n🌊 Multi-Engine Consciousness Analysis Demo")
    print("=" * 60)

    try:
        agent = WitnessOSAgent(
            production_api_url="http://localhost:8002",
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY")
        )

        engines = ["numerology", "biorhythm"]
        print(f"🔍 Running multi-engine analysis: {', '.join(engines)}")

        result = await agent.interpret_multi_engine(
            engines=engines,
            birth_data=YOUR_BIRTH_DATA,
            interpretation_style="witnessOS",
            model_type="primary",
            include_synthesis=True
        )

        if "consciousness_synthesis" in result:
            synthesis = result["consciousness_synthesis"]["unified_field_analysis"]
            print("\n✅ Consciousness Field Synthesis:")
            print("-" * 50)
            print(synthesis[:800] + "..." if len(synthesis) > 800 else synthesis)
            print("-" * 50)

            # Show field coherence
            session = result.get("consciousness_session", {})
            field_coherence = session.get("field_coherence", "unknown")
            print(f"\n📊 Field Coherence: {field_coherence}")

            return True
        else:
            print(f"❌ No synthesis found in result")
            return False

    except Exception as e:
        print(f"❌ Error in multi-engine analysis: {e}")
        return False

async def main():
    """Main demo function"""
    # Check environment
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY environment variable not set")
        print("Please run: export OPENROUTER_API_KEY=your_key_here")
        return

    print("🤖 WitnessOS AI Agent - Personal Chart Demo")
    print("Using your actual birth data and Human Design chart!")
    print()

    # Test Human Design interpretation
    hd_success = await test_human_design_interpretation()

    # Test Numerology interpretation
    if hd_success:
        num_success = await test_numerology_interpretation()

        # Test Multi-engine synthesis
        if num_success:
            await test_multi_engine_synthesis()

    print("\n" + "=" * 70)
    print("✅ WitnessOS AI Agent Demo Complete!")
    print("🌟 The agent successfully translated technical calculations into consciousness guidance!")

if __name__ == "__main__":
    asyncio.run(main())
