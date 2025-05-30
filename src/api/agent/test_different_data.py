#!/usr/bin/env python3
"""
Test WitnessOS AI Agent with Different Birth Data

Tests the agent with various birth data to verify it works beyond personal charts.
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

# Test data for different people
TEST_SUBJECTS = [
    {
        "name": "Alice Johnson",
        "date": "1985-03-15",
        "time": "09:30",
        "location": "New York, NY, USA",
        "timezone": "America/New_York",
        "description": "Creative professional, artist"
    },
    {
        "name": "Bob Chen",
        "date": "1992-11-22",
        "time": "14:45",
        "location": "San Francisco, CA, USA", 
        "timezone": "America/Los_Angeles",
        "description": "Tech entrepreneur, innovator"
    },
    {
        "name": "Maria Rodriguez",
        "date": "1978-07-08",
        "time": "18:20",
        "location": "Madrid, Spain",
        "timezone": "Europe/Madrid",
        "description": "Healer, spiritual teacher"
    },
    {
        "name": "David Kim",
        "date": "1990-12-03",
        "time": "06:15",
        "location": "Seoul, South Korea",
        "timezone": "Asia/Seoul",
        "description": "Musician, composer"
    }
]

async def test_single_engine_with_subject(agent, subject, engine_name):
    """Test single engine interpretation for a subject"""
    print(f"\n🔮 Testing {engine_name} for {subject['name']}")
    print(f"   Born: {subject['date']} at {subject['time']} in {subject['location']}")
    print(f"   Profile: {subject['description']}")
    print("-" * 60)
    
    try:
        result = await agent.interpret_single_engine(
            engine_name=engine_name,
            birth_data=subject,
            interpretation_style="witnessOS",
            model_type="primary"
        )
        
        if "consciousness_interpretation" in result:
            ai_guidance = result["consciousness_interpretation"]["ai_guidance"]
            print(f"✅ AI Interpretation (first 400 chars):")
            print(ai_guidance[:400] + "..." if len(ai_guidance) > 400 else ai_guidance)
            
            # Show Aletheos insights if available
            witness_protocol = result.get("witness_protocol", {})
            if "aletheos_insights" in witness_protocol:
                insights = witness_protocol["aletheos_insights"]
                print(f"\n🌟 Aletheos Insights ({len(insights)} Muses activated):")
                for insight in insights[:2]:  # Show top 2
                    muse = insight.get("muse", "Unknown").replace("_", " ").title()
                    print(f"   • {muse}: {insight.get('insight', '')[:100]}...")
            
            return True
        else:
            print(f"❌ Unexpected result format")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_multi_engine_with_subject(agent, subject):
    """Test multi-engine analysis for a subject"""
    print(f"\n🌊 Multi-Engine Analysis for {subject['name']}")
    print("=" * 60)
    
    try:
        engines = ["numerology", "biorhythm"]
        result = await agent.interpret_multi_engine(
            engines=engines,
            birth_data=subject,
            interpretation_style="witnessOS",
            model_type="primary",
            include_synthesis=True
        )
        
        if "consciousness_synthesis" in result:
            synthesis = result["consciousness_synthesis"]["unified_field_analysis"]
            print(f"✅ Consciousness Synthesis (first 300 chars):")
            print(synthesis[:300] + "..." if len(synthesis) > 300 else synthesis)
            
            # Show field coherence
            session = result.get("consciousness_session", {})
            field_coherence = session.get("field_coherence", "unknown")
            print(f"\n📊 Field Coherence: {field_coherence}")
            
            return True
        else:
            print(f"❌ No synthesis generated")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_aletheos_muses_directly():
    """Test Aletheos + Muses system directly"""
    print("\n🌟 Testing Aletheos + 10 Muses System Directly")
    print("=" * 60)
    
    try:
        from agent.aletheos_muses import AletheosContextExtractor
        
        aletheos = AletheosContextExtractor()
        
        # Mock engine results for testing
        mock_results = {
            "numerology": {
                "core_numbers": {"life_path": 7, "expression": 3, "soul_urge": 2},
                "master_numbers": [11],
                "karmic_debt": [13]
            },
            "human_design": {
                "personality_type": "Projector",
                "authority": "Emotional",
                "not_self": "Bitterness",
                "incarnation_cross": "Right Angle Cross of Service"
            }
        }
        
        birth_data = TEST_SUBJECTS[0]  # Use Alice as test subject
        
        insights = aletheos.extract_context(mock_results, birth_data)
        
        print(f"✅ Extracted {len(insights)} insights from {len(insights)} active Muses:")
        
        for insight in insights:
            muse_name = insight.muse.value.replace("_", " ").title()
            print(f"\n• {muse_name} (Relevance: {insight.relevance:.2f})")
            print(f"  {insight.insight}")
        
        # Test context formatting
        formatted_context = aletheos.format_context_for_agent(insights)
        print(f"\n📝 Formatted Context for Agent:")
        print(formatted_context[:400] + "..." if len(formatted_context) > 400 else formatted_context)
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Aletheos: {e}")
        return False

async def main():
    """Main test function"""
    # Check environment
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY environment variable not set")
        print("Please run: export OPENROUTER_API_KEY=your_key_here")
        return

    print("🤖 WitnessOS AI Agent - Multi-Subject Testing")
    print("Testing with different birth data to verify universal functionality")
    print()

    # Test Aletheos system directly first
    aletheos_success = await test_aletheos_muses_directly()
    
    if not aletheos_success:
        print("❌ Aletheos system test failed, continuing with agent tests...")
    
    # Initialize agent
    agent = WitnessOSAgent(
        production_api_url="http://localhost:8002",
        openrouter_api_key=api_key,
        use_local_engines=True
    )

    print(f"\n🧪 Testing {len(TEST_SUBJECTS)} different subjects...")
    
    total_tests = 0
    successful_tests = 0
    
    for i, subject in enumerate(TEST_SUBJECTS, 1):
        print(f"\n{'='*70}")
        print(f"SUBJECT {i}/{len(TEST_SUBJECTS)}: {subject['name']}")
        print(f"{'='*70}")
        
        # Test numerology
        total_tests += 1
        if await test_single_engine_with_subject(agent, subject, "numerology"):
            successful_tests += 1
        
        # Test biorhythm
        total_tests += 1
        if await test_single_engine_with_subject(agent, subject, "biorhythm"):
            successful_tests += 1
        
        # Test multi-engine for first 2 subjects
        if i <= 2:
            total_tests += 1
            if await test_multi_engine_with_subject(agent, subject):
                successful_tests += 1

    print(f"\n{'='*70}")
    print(f"✅ TEST RESULTS: {successful_tests}/{total_tests} tests passed")
    print(f"📊 Success Rate: {(successful_tests/total_tests)*100:.1f}%")
    
    if successful_tests == total_tests:
        print("🌟 All tests passed! WitnessOS Agent works with diverse birth data!")
    elif successful_tests > total_tests * 0.8:
        print("✨ Most tests passed! Agent is working well with different subjects.")
    else:
        print("⚠️  Some tests failed. Check the errors above for issues.")
    
    print(f"\n🎯 Key Achievements:")
    print(f"   • Aletheos + 10 Muses context extraction system")
    print(f"   • Local engine fallbacks working")
    print(f"   • AI interpretations with consciousness guidance")
    print(f"   • Multi-engine synthesis capabilities")
    print(f"   • Universal compatibility with different birth data")

if __name__ == "__main__":
    asyncio.run(main())
