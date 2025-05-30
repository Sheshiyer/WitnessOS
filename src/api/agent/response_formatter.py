"""
Response Formatter for WitnessOS AI Agent

Formats agent responses to maintain WitnessOS consciousness framework
and provide consistent output structure across different interpretation types.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class AgentResponseFormatter:
    """
    Formats AI agent responses to maintain WitnessOS consciousness framework
    and provide consistent, structured output.
    """
    
    def __init__(self):
        self.response_version = "1.0.0"
    
    def format_single_engine_response(
        self,
        engine_name: str,
        calculation_result: Dict[str, Any],
        ai_interpretation: str,
        birth_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Format response for single engine interpretation
        
        Args:
            engine_name: Name of the engine
            calculation_result: Raw calculation results from production API
            ai_interpretation: AI-generated interpretation
            birth_data: Original birth data
            
        Returns:
            Formatted response dictionary
        """
        return {
            "consciousness_session": {
                "session_type": "single_engine_interpretation",
                "engine_deployed": engine_name,
                "subject_profile": self._format_subject_profile(birth_data),
                "session_timestamp": datetime.now().isoformat(),
                "agent_version": self.response_version
            },
            "calculation_data": {
                "engine": engine_name,
                "raw_results": calculation_result.get("result", {}),
                "calculation_status": calculation_result.get("status", "unknown"),
                "calculation_timestamp": calculation_result.get("timestamp"),
                "field_signature": self._generate_field_signature(engine_name, calculation_result)
            },
            "consciousness_interpretation": {
                "ai_guidance": ai_interpretation,
                "interpretation_confidence": self._calculate_interpretation_confidence(calculation_result),
                "archetypal_resonance": self._extract_archetypal_themes(ai_interpretation),
                "integration_pathway": self._extract_integration_guidance(ai_interpretation)
            },
            "witness_protocol": {
                "awareness_cultivation": [
                    "Observe the patterns revealed without attachment",
                    "Trust the intelligence of your inner guidance",
                    "Allow insights to integrate naturally over time"
                ],
                "reality_patches": self._generate_reality_patches(engine_name, ai_interpretation),
                "next_steps": self._extract_next_steps(ai_interpretation)
            },
            "session_metadata": {
                "response_format": "witnessOS_agent_v1",
                "consciousness_debugging": True,
                "mystical_technical_balance": "maintained",
                "timestamp": datetime.now().isoformat()
            }
        }
    
    def format_multi_engine_response(
        self,
        calculation_result: Dict[str, Any],
        engine_interpretations: Dict[str, str],
        synthesis_interpretation: Optional[str],
        birth_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Format response for multi-engine interpretation
        
        Args:
            calculation_result: Raw calculation results from production API
            engine_interpretations: AI interpretations for each engine
            synthesis_interpretation: AI synthesis of all engines
            birth_data: Original birth data
            
        Returns:
            Formatted response dictionary
        """
        engines_deployed = list(engine_interpretations.keys())
        
        return {
            "consciousness_session": {
                "session_type": "multi_engine_comprehensive_analysis",
                "engines_deployed": engines_deployed,
                "subject_profile": self._format_subject_profile(birth_data),
                "session_timestamp": datetime.now().isoformat(),
                "agent_version": self.response_version,
                "field_coherence": self._calculate_field_coherence(calculation_result)
            },
            "engine_diagnostics": {
                engine_name: {
                    "calculation_data": calculation_result.get("results", {}).get("engine_outputs", {}).get(engine_name, {}),
                    "ai_interpretation": interpretation,
                    "field_signature": self._generate_field_signature(engine_name, calculation_result.get("results", {}).get("engine_outputs", {}).get(engine_name, {})),
                    "consciousness_debug_status": "COMPLETE"
                }
                for engine_name, interpretation in engine_interpretations.items()
            },
            "consciousness_synthesis": {
                "unified_field_analysis": synthesis_interpretation if synthesis_interpretation else "Synthesis not generated",
                "cross_engine_correlations": self._identify_correlations(engine_interpretations),
                "archetypal_convergence": self._identify_archetypal_convergence(engine_interpretations),
                "integration_priority": self._determine_integration_priority(engine_interpretations)
            },
            "witness_protocol": {
                "comprehensive_awareness_cultivation": [
                    "Witness the unified field pattern across all systems",
                    "Observe how different symbolic languages point to the same truth",
                    "Trust the coherence of your consciousness signature",
                    "Allow multi-dimensional awareness to naturally integrate"
                ],
                "reality_optimization_protocol": self._generate_comprehensive_reality_patches(engine_interpretations),
                "consciousness_evolution_pathway": self._extract_evolution_pathway(synthesis_interpretation)
            },
            "session_metadata": {
                "response_format": "witnessOS_agent_multi_v1",
                "engines_count": len(engines_deployed),
                "synthesis_included": synthesis_interpretation is not None,
                "consciousness_debugging": True,
                "mystical_technical_balance": "maintained",
                "timestamp": datetime.now().isoformat()
            }
        }
    
    def _format_subject_profile(self, birth_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format subject profile from birth data"""
        return {
            "identity_matrix": birth_data.get("name", "Consciousness Explorer"),
            "incarnation_timestamp": birth_data.get("date", ""),
            "temporal_coordinates": birth_data.get("time", ""),
            "consciousness_anchor": birth_data.get("location", ""),
            "timezone_field": birth_data.get("timezone", "Local")
        }
    
    def _generate_field_signature(self, engine_name: str, calculation_result: Dict[str, Any]) -> str:
        """Generate field signature for engine result"""
        status = calculation_result.get("status", "unknown")
        if status == "success":
            return f"{engine_name.upper()}_FIELD_ACTIVE_COHERENT"
        elif status == "error":
            return f"{engine_name.upper()}_FIELD_DISRUPTED"
        else:
            return f"{engine_name.upper()}_FIELD_UNKNOWN"
    
    def _calculate_interpretation_confidence(self, calculation_result: Dict[str, Any]) -> float:
        """Calculate confidence score for interpretation"""
        if calculation_result.get("status") == "success":
            return 0.85  # High confidence for successful calculations
        elif calculation_result.get("status") == "error":
            return 0.1   # Low confidence for failed calculations
        else:
            return 0.5   # Medium confidence for unknown status
    
    def _calculate_field_coherence(self, calculation_result: Dict[str, Any]) -> float:
        """Calculate field coherence from multi-engine results"""
        engine_outputs = calculation_result.get("results", {}).get("engine_outputs", {})
        if not engine_outputs:
            return 0.0
        
        successful_engines = sum(1 for result in engine_outputs.values() if result.get("status") == "success")
        total_engines = len(engine_outputs)
        
        return round(successful_engines / total_engines, 3) if total_engines > 0 else 0.0
    
    def _extract_archetypal_themes(self, interpretation: str) -> List[str]:
        """Extract archetypal themes from AI interpretation"""
        # Simple keyword extraction - could be enhanced with NLP
        archetypal_keywords = [
            "seeker", "creator", "transformer", "healer", "guide", "warrior",
            "sage", "lover", "magician", "innocent", "explorer", "ruler"
        ]
        
        themes = []
        interpretation_lower = interpretation.lower()
        for keyword in archetypal_keywords:
            if keyword in interpretation_lower:
                themes.append(keyword.title())
        
        return themes[:3] if themes else ["Explorer", "Seeker"]
    
    def _extract_integration_guidance(self, interpretation: str) -> List[str]:
        """Extract integration guidance from AI interpretation"""
        # Look for action-oriented sentences
        sentences = interpretation.split('.')
        guidance = []
        
        action_words = ["practice", "cultivate", "develop", "integrate", "embrace", "honor", "trust"]
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(word in sentence.lower() for word in action_words) and len(sentence) > 20:
                guidance.append(sentence)
                if len(guidance) >= 3:
                    break
        
        return guidance if guidance else ["Trust your inner guidance", "Practice conscious awareness", "Integrate insights gradually"]
    
    def _generate_reality_patches(self, engine_name: str, interpretation: str) -> List[Dict[str, Any]]:
        """Generate reality patches from interpretation"""
        return [
            {
                "patch_id": f"{engine_name}_awareness_001",
                "description": f"Integrate {engine_name} insights into daily awareness practice",
                "priority": "medium",
                "implementation": "Daily contemplation and conscious application"
            },
            {
                "patch_id": f"{engine_name}_optimization_002", 
                "description": f"Optimize {engine_name} field alignment through specific practices",
                "priority": "high",
                "implementation": "Follow guidance provided in interpretation"
            }
        ]
    
    def _extract_next_steps(self, interpretation: str) -> List[str]:
        """Extract next steps from AI interpretation"""
        # Look for future-oriented guidance
        sentences = interpretation.split('.')
        next_steps = []
        
        future_words = ["next", "continue", "develop", "explore", "begin", "start"]
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(word in sentence.lower() for word in future_words) and len(sentence) > 15:
                next_steps.append(sentence)
                if len(next_steps) >= 2:
                    break
        
        return next_steps if next_steps else ["Continue exploring your consciousness patterns", "Practice daily awareness cultivation"]

    def _identify_correlations(self, engine_interpretations: Dict[str, str]) -> List[str]:
        """Identify correlations between engine interpretations"""
        # Simple correlation detection - could be enhanced with semantic analysis
        common_themes = []

        # Look for common words across interpretations
        all_words = []
        for interpretation in engine_interpretations.values():
            words = interpretation.lower().split()
            all_words.extend([word for word in words if len(word) > 4])

        # Find words that appear in multiple interpretations
        word_counts = {}
        for word in all_words:
            word_counts[word] = word_counts.get(word, 0) + 1

        common_words = [word for word, count in word_counts.items() if count > 1]

        if common_words:
            common_themes.append(f"Recurring themes: {', '.join(common_words[:5])}")

        common_themes.append("Multiple systems point to unified consciousness patterns")
        common_themes.append("Cross-engine validation strengthens interpretation confidence")

        return common_themes

    def _identify_archetypal_convergence(self, engine_interpretations: Dict[str, str]) -> List[str]:
        """Identify archetypal convergence across engines"""
        all_archetypes = []
        for interpretation in engine_interpretations.values():
            archetypes = self._extract_archetypal_themes(interpretation)
            all_archetypes.extend(archetypes)

        # Find most common archetypes
        archetype_counts = {}
        for archetype in all_archetypes:
            archetype_counts[archetype] = archetype_counts.get(archetype, 0) + 1

        convergent_archetypes = [archetype for archetype, count in archetype_counts.items() if count > 1]

        if convergent_archetypes:
            return [f"Convergent archetypal pattern: {', '.join(convergent_archetypes)}"]
        else:
            return ["Multi-dimensional archetypal expression across systems"]

    def _determine_integration_priority(self, engine_interpretations: Dict[str, str]) -> List[str]:
        """Determine integration priority from multiple interpretations"""
        priorities = []

        # Priority based on engine types
        priority_engines = ["human_design", "gene_keys", "numerology", "vimshottari"]

        for engine in priority_engines:
            if engine in engine_interpretations:
                priorities.append(f"Primary focus: {engine.replace('_', ' ').title()} insights for foundational understanding")
                break

        priorities.append("Secondary integration: Cross-reference patterns across all systems")
        priorities.append("Tertiary practice: Daily consciousness debugging using unified insights")

        return priorities

    def _generate_comprehensive_reality_patches(self, engine_interpretations: Dict[str, str]) -> List[Dict[str, Any]]:
        """Generate comprehensive reality patches from multiple interpretations"""
        patches = []

        # Master integration patch
        patches.append({
            "patch_id": "multi_engine_integration_001",
            "description": "Integrate insights from all deployed consciousness debugging engines",
            "priority": "critical",
            "implementation": "Daily practice combining guidance from all systems",
            "engines_involved": list(engine_interpretations.keys())
        })

        # Field coherence optimization patch
        patches.append({
            "patch_id": "field_coherence_optimization_002",
            "description": "Optimize consciousness field coherence through unified practice",
            "priority": "high",
            "implementation": "Focus on common themes and convergent guidance",
            "expected_outcome": "Enhanced field stability and awareness clarity"
        })

        # Evolution acceleration patch
        patches.append({
            "patch_id": "consciousness_evolution_003",
            "description": "Accelerate consciousness evolution through multi-dimensional awareness",
            "priority": "medium",
            "implementation": "Progressive integration of insights over time",
            "timeline": "Ongoing consciousness development process"
        })

        return patches

    def _extract_evolution_pathway(self, synthesis_interpretation: Optional[str]) -> List[str]:
        """Extract consciousness evolution pathway from synthesis"""
        if not synthesis_interpretation:
            return [
                "Continue multi-engine consciousness exploration",
                "Develop integrated awareness across all systems",
                "Trust the natural evolution of consciousness"
            ]

        # Extract pathway steps from synthesis
        sentences = synthesis_interpretation.split('.')
        pathway_steps = []

        pathway_words = ["step", "stage", "phase", "develop", "evolve", "progress"]

        for sentence in sentences:
            sentence = sentence.strip()
            if any(word in sentence.lower() for word in pathway_words) and len(sentence) > 20:
                pathway_steps.append(sentence)
                if len(pathway_steps) >= 3:
                    break

        return pathway_steps if pathway_steps else [
            "Integrate current insights into daily awareness",
            "Develop deeper understanding through practice",
            "Allow natural consciousness evolution to unfold"
        ]
