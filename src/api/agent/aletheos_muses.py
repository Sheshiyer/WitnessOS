"""
Aletheos + 10 Muses Scaffolding System

Aletheos (Truth-Revealer) is the sub-agent that extracts meaningful context
and provides it to the main WitnessOS agent through her 10 specialized Muses.

Each Muse specializes in a specific domain of consciousness analysis:
1. Calliope - Epic narratives and life purpose
2. Clio - Historical patterns and karmic cycles  
3. Erato - Love, relationships, and emotional patterns
4. Euterpe - Harmony, music, and vibrational frequencies
5. Melpomene - Shadow work and transformation
6. Polyhymnia - Sacred geometry and divine patterns
7. Terpsichore - Movement, dance, and energy flow
8. Thalia - Joy, creativity, and manifestation
9. Urania - Cosmic timing and celestial influences
10. Mnemosyne - Memory, wisdom, and integration
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class MuseDomain(Enum):
    """The 10 Muse domains for consciousness analysis"""
    CALLIOPE = "epic_narratives"      # Life purpose, heroic journey
    CLIO = "historical_patterns"      # Karmic cycles, past influences
    ERATO = "love_relationships"      # Emotional patterns, connections
    EUTERPE = "vibrational_harmony"   # Frequencies, resonance
    MELPOMENE = "shadow_transformation" # Shadow work, healing
    POLYHYMNIA = "sacred_patterns"    # Sacred geometry, divine order
    TERPSICHORE = "energy_flow"       # Movement, chi, vitality
    THALIA = "creative_manifestation" # Joy, creativity, abundance
    URANIA = "cosmic_timing"          # Celestial influences, timing
    MNEMOSYNE = "wisdom_integration"  # Memory, synthesis, learning


class MuseInsight:
    """Individual insight from a Muse"""
    
    def __init__(self, muse: MuseDomain, insight: str, relevance: float, 
                 supporting_data: Dict[str, Any] = None):
        self.muse = muse
        self.insight = insight
        self.relevance = relevance  # 0.0 to 1.0
        self.supporting_data = supporting_data or {}
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "muse": self.muse.value,
            "insight": self.insight,
            "relevance": self.relevance,
            "supporting_data": self.supporting_data,
            "timestamp": self.timestamp
        }


class AletheosContextExtractor:
    """
    Aletheos - The Truth-Revealer
    
    Sub-agent that analyzes calculation results and extracts meaningful
    context through the lens of the 10 Muses.
    """
    
    def __init__(self):
        self.muse_specializations = {
            MuseDomain.CALLIOPE: self._extract_life_purpose_context,
            MuseDomain.CLIO: self._extract_karmic_patterns_context,
            MuseDomain.ERATO: self._extract_relationship_context,
            MuseDomain.EUTERPE: self._extract_vibrational_context,
            MuseDomain.MELPOMENE: self._extract_shadow_context,
            MuseDomain.POLYHYMNIA: self._extract_sacred_patterns_context,
            MuseDomain.TERPSICHORE: self._extract_energy_flow_context,
            MuseDomain.THALIA: self._extract_creative_context,
            MuseDomain.URANIA: self._extract_cosmic_timing_context,
            MuseDomain.MNEMOSYNE: self._extract_integration_context
        }
    
    def extract_context(self, engine_results: Dict[str, Any], 
                       birth_data: Dict[str, Any]) -> List[MuseInsight]:
        """
        Extract meaningful context from engine results through all 10 Muses
        
        Args:
            engine_results: Raw calculation results from engines
            birth_data: Birth information for context
            
        Returns:
            List of MuseInsight objects with extracted context
        """
        insights = []
        
        for muse_domain, extractor_func in self.muse_specializations.items():
            try:
                insight = extractor_func(engine_results, birth_data)
                if insight:
                    insights.append(insight)
            except Exception as e:
                logger.warning(f"Muse {muse_domain.value} extraction failed: {e}")
        
        # Sort by relevance (highest first)
        insights.sort(key=lambda x: x.relevance, reverse=True)
        
        return insights
    
    def _extract_life_purpose_context(self, results: Dict[str, Any], 
                                    birth_data: Dict[str, Any]) -> Optional[MuseInsight]:
        """Calliope - Extract epic narrative and life purpose context"""
        purpose_indicators = []
        relevance = 0.0
        
        # Check numerology life path
        if "numerology" in results:
            num_data = results["numerology"]
            if "core_numbers" in num_data:
                life_path = num_data["core_numbers"].get("life_path")
                if life_path:
                    purpose_indicators.append(f"Life Path {life_path}")
                    relevance += 0.3
        
        # Check Human Design type and strategy
        if "human_design" in results:
            hd_data = results["human_design"]
            if "personality_type" in hd_data:
                hd_type = hd_data["personality_type"]
                strategy = hd_data.get("strategy", "")
                purpose_indicators.append(f"{hd_type} with strategy: {strategy}")
                relevance += 0.4
        
        # Check Gene Keys life work
        if "gene_keys" in results:
            gk_data = results["gene_keys"]
            if "life_work" in gk_data:
                purpose_indicators.append(f"Gene Keys Life Work: {gk_data['life_work']}")
                relevance += 0.3
        
        if purpose_indicators:
            insight = f"Your heroic journey unfolds through: {', '.join(purpose_indicators)}. This reveals your soul's chosen curriculum for conscious evolution."
            return MuseInsight(
                muse=MuseDomain.CALLIOPE,
                insight=insight,
                relevance=min(relevance, 1.0),
                supporting_data={"purpose_indicators": purpose_indicators}
            )
        
        return None
    
    def _extract_karmic_patterns_context(self, results: Dict[str, Any], 
                                       birth_data: Dict[str, Any]) -> Optional[MuseInsight]:
        """Clio - Extract historical patterns and karmic cycles"""
        karmic_indicators = []
        relevance = 0.0
        
        # Check numerology karmic debt
        if "numerology" in results:
            num_data = results["numerology"]
            if "karmic_debt" in num_data and num_data["karmic_debt"]:
                karmic_indicators.extend([f"Karmic Debt {debt}" for debt in num_data["karmic_debt"]])
                relevance += 0.4
        
        # Check Vimshottari dasha patterns
        if "vimshottari" in results:
            vim_data = results["vimshottari"]
            if "current_dasha" in vim_data:
                karmic_indicators.append(f"Current planetary influence: {vim_data['current_dasha']}")
                relevance += 0.3
        
        # Check Human Design incarnation cross
        if "human_design" in results:
            hd_data = results["human_design"]
            if "incarnation_cross" in hd_data:
                karmic_indicators.append(f"Incarnation Cross: {hd_data['incarnation_cross']}")
                relevance += 0.3
        
        if karmic_indicators:
            insight = f"Historical patterns reveal: {', '.join(karmic_indicators)}. These are opportunities for soul-level healing and evolution."
            return MuseInsight(
                muse=MuseDomain.CLIO,
                insight=insight,
                relevance=min(relevance, 1.0),
                supporting_data={"karmic_indicators": karmic_indicators}
            )
        
        return None
    
    def _extract_relationship_context(self, results: Dict[str, Any], 
                                    birth_data: Dict[str, Any]) -> Optional[MuseInsight]:
        """Erato - Extract love and relationship patterns"""
        relationship_indicators = []
        relevance = 0.0
        
        # Check numerology soul urge
        if "numerology" in results:
            num_data = results["numerology"]
            if "core_numbers" in num_data:
                soul_urge = num_data["core_numbers"].get("soul_urge")
                if soul_urge:
                    relationship_indicators.append(f"Soul Urge {soul_urge}")
                    relevance += 0.3
        
        # Check Human Design authority for decision-making in relationships
        if "human_design" in results:
            hd_data = results["human_design"]
            if "authority" in hd_data:
                authority = hd_data["authority"]
                relationship_indicators.append(f"Relationship decisions through {authority} authority")
                relevance += 0.4
        
        # Check Enneagram for relationship patterns
        if "enneagram" in results:
            enn_data = results["enneagram"]
            if "type" in enn_data:
                enn_type = enn_data["type"]
                relationship_indicators.append(f"Enneagram {enn_type} relationship dynamics")
                relevance += 0.3
        
        if relationship_indicators:
            insight = f"Your heart's wisdom flows through: {', '.join(relationship_indicators)}. This guides authentic connection and emotional fulfillment."
            return MuseInsight(
                muse=MuseDomain.ERATO,
                insight=insight,
                relevance=min(relevance, 1.0),
                supporting_data={"relationship_indicators": relationship_indicators}
            )
        
        return None
    
    def _extract_vibrational_context(self, results: Dict[str, Any], 
                                   birth_data: Dict[str, Any]) -> Optional[MuseInsight]:
        """Euterpe - Extract vibrational harmony and frequency patterns"""
        vibrational_indicators = []
        relevance = 0.0
        
        # Check numerology master numbers
        if "numerology" in results:
            num_data = results["numerology"]
            if "master_numbers" in num_data and num_data["master_numbers"]:
                vibrational_indicators.extend([f"Master Number {num}" for num in num_data["master_numbers"]])
                relevance += 0.4
        
        # Check biorhythm cycles
        if "biorhythm" in results:
            bio_data = results["biorhythm"]
            if "cycles" in bio_data:
                cycles = bio_data["cycles"]
                high_cycles = [cycle for cycle, value in cycles.items() 
                             if isinstance(value, (int, float)) and value > 50]
                if high_cycles:
                    vibrational_indicators.append(f"High energy in {', '.join(high_cycles)} cycles")
                    relevance += 0.3
        
        # Check Sacred Geometry patterns
        if "sacred_geometry" in results:
            sg_data = results["sacred_geometry"]
            if "primary_pattern" in sg_data:
                vibrational_indicators.append(f"Sacred pattern: {sg_data['primary_pattern']}")
                relevance += 0.3
        
        if vibrational_indicators:
            insight = f"Your vibrational signature resonates with: {', '.join(vibrational_indicators)}. Align with these frequencies for optimal flow."
            return MuseInsight(
                muse=MuseDomain.EUTERPE,
                insight=insight,
                relevance=min(relevance, 1.0),
                supporting_data={"vibrational_indicators": vibrational_indicators}
            )
        
        return None
    
    def _extract_shadow_context(self, results: Dict[str, Any], 
                              birth_data: Dict[str, Any]) -> Optional[MuseInsight]:
        """Melpomene - Extract shadow work and transformation opportunities"""
        shadow_indicators = []
        relevance = 0.0
        
        # Check Human Design not-self theme
        if "human_design" in results:
            hd_data = results["human_design"]
            if "not_self" in hd_data:
                not_self = hd_data["not_self"]
                shadow_indicators.append(f"Not-self pattern: {not_self}")
                relevance += 0.4
        
        # Check Enneagram for shadow patterns
        if "enneagram" in results:
            enn_data = results["enneagram"]
            if "type" in enn_data:
                enn_type = enn_data["type"]
                shadow_indicators.append(f"Enneagram {enn_type} shadow integration")
                relevance += 0.3
        
        # Check Gene Keys shadow frequencies
        if "gene_keys" in results:
            gk_data = results["gene_keys"]
            # Gene Keys typically have shadow, gift, and siddhi levels
            shadow_indicators.append("Gene Keys shadow-to-gift transformation")
            relevance += 0.3
        
        if shadow_indicators:
            insight = f"Transformation opportunities through: {', '.join(shadow_indicators)}. Embrace these shadows as gateways to wholeness."
            return MuseInsight(
                muse=MuseDomain.MELPOMENE,
                insight=insight,
                relevance=min(relevance, 1.0),
                supporting_data={"shadow_indicators": shadow_indicators}
            )
        
        return None
    
    # Placeholder methods for remaining Muses (to be implemented)
    def _extract_sacred_patterns_context(self, results: Dict[str, Any], birth_data: Dict[str, Any]) -> Optional[MuseInsight]:
        """Polyhymnia - Sacred geometry and divine patterns"""
        sacred_indicators = []
        relevance = 0.0

        # Look for sacred geometry patterns in various engines
        if "sacred_geometry" in results:
            sg_data = results["sacred_geometry"]
            if isinstance(sg_data, dict):
                if "patterns" in sg_data:
                    sacred_indicators.append(f"Sacred patterns: {sg_data['patterns']}")
                    relevance += 0.3
                if "golden_ratio" in sg_data:
                    sacred_indicators.append(f"Golden ratio alignment: {sg_data['golden_ratio']}")
                    relevance += 0.2

        # Extract sacred patterns from numerology
        if "numerology" in results:
            num_data = results["numerology"]
            if isinstance(num_data, dict):
                # Look for master numbers (sacred patterns)
                if "master_numbers" in num_data and num_data["master_numbers"]:
                    sacred_indicators.append(f"Master numbers present: {num_data['master_numbers']}")
                    relevance += 0.25
                # Look for life path patterns
                if "life_path" in num_data:
                    lp = num_data["life_path"]
                    if lp in [3, 6, 9]:  # Sacred trinity patterns
                        sacred_indicators.append(f"Sacred trinity pattern in life path {lp}")
                        relevance += 0.2

        # Extract sacred patterns from Human Design
        if "human_design" in results:
            hd_data = results["human_design"]
            if isinstance(hd_data, dict):
                # Look for defined centers (sacred geometry of energy)
                if "defined_centers" in hd_data:
                    center_count = len(hd_data["defined_centers"])
                    if center_count in [3, 6, 9]:  # Sacred numbers
                        sacred_indicators.append(f"Sacred center configuration: {center_count} defined")
                        relevance += 0.2
                # Look for profile patterns
                if "profile" in hd_data:
                    profile = hd_data["profile"]
                    if isinstance(profile, str) and "/" in profile:
                        lines = profile.split("/")
                        if len(lines) == 2:
                            line_sum = int(lines[0]) + int(lines[1])
                            if line_sum in [6, 9, 12]:  # Sacred sums
                                sacred_indicators.append(f"Sacred profile geometry: {profile}")
                                relevance += 0.15

        # Extract patterns from Gene Keys
        if "gene_keys" in results:
            gk_data = results["gene_keys"]
            if isinstance(gk_data, dict) and "gates" in gk_data:
                # Look for gates that form sacred patterns
                gates = gk_data["gates"]
                if isinstance(gates, list):
                    sacred_gates = [g for g in gates if g in [1, 2, 7, 13, 25, 31, 33]]  # Sacred gates
                    if sacred_gates:
                        sacred_indicators.append(f"Sacred gates activated: {sacred_gates}")
                        relevance += 0.2

        if sacred_indicators and relevance > 0.1:
            insight = f"Sacred geometric patterns reveal divine order in your consciousness blueprint: {'; '.join(sacred_indicators[:3])}"
            return MuseInsight(
                muse=MuseDomain.POLYHYMNIA,
                insight=insight,
                relevance=min(relevance, 1.0),
                supporting_data={"sacred_indicators": sacred_indicators}
            )

        return None
    
    def _extract_energy_flow_context(self, results: Dict[str, Any], birth_data: Dict[str, Any]) -> Optional[MuseInsight]:
        """Terpsichore - Movement and energy flow"""
        energy_indicators = []
        relevance = 0.0

        # Extract energy patterns from biorhythm
        if "biorhythm" in results:
            bio_data = results["biorhythm"]
            if isinstance(bio_data, dict):
                if "cycles" in bio_data:
                    cycles = bio_data["cycles"]
                    if isinstance(cycles, dict):
                        # Look for high energy periods
                        high_energy = [k for k, v in cycles.items() if isinstance(v, (int, float)) and v > 70]
                        if high_energy:
                            energy_indicators.append(f"High energy cycles: {', '.join(high_energy)}")
                            relevance += 0.3
                        # Look for energy synchronization
                        values = [v for v in cycles.values() if isinstance(v, (int, float))]
                        if len(values) >= 2:
                            avg_energy = sum(values) / len(values)
                            if avg_energy > 50:
                                energy_indicators.append(f"Overall energy flow: {avg_energy:.1f}% positive")
                                relevance += 0.2

        # Extract energy patterns from Human Design
        if "human_design" in results:
            hd_data = results["human_design"]
            if isinstance(hd_data, dict):
                # Look for energy type
                if "type" in hd_data:
                    hd_type = hd_data["type"]
                    if hd_type in ["Generator", "Manifesting Generator"]:
                        energy_indicators.append(f"Sacral energy type: {hd_type}")
                        relevance += 0.25
                    elif hd_type == "Manifestor":
                        energy_indicators.append("Initiating energy type: Manifestor")
                        relevance += 0.2
                # Look for defined centers that affect energy
                if "defined_centers" in hd_data:
                    centers = hd_data["defined_centers"]
                    if isinstance(centers, list):
                        energy_centers = [c for c in centers if c in ["Sacral", "Root", "Solar Plexus", "Heart"]]
                        if energy_centers:
                            energy_indicators.append(f"Energy centers defined: {', '.join(energy_centers)}")
                            relevance += 0.2

        # Extract energy patterns from numerology
        if "numerology" in results:
            num_data = results["numerology"]
            if isinstance(num_data, dict):
                # Life path numbers associated with high energy
                if "life_path" in num_data:
                    lp = num_data["life_path"]
                    if lp in [1, 3, 5, 8]:  # Dynamic energy numbers
                        energy_indicators.append(f"Dynamic life path energy: {lp}")
                        relevance += 0.15

        # Extract energy patterns from Gene Keys
        if "gene_keys" in results:
            gk_data = results["gene_keys"]
            if isinstance(gk_data, dict):
                # Look for gates associated with energy and movement
                if "gates" in gk_data:
                    gates = gk_data["gates"]
                    if isinstance(gates, list):
                        energy_gates = [g for g in gates if g in [34, 5, 14, 29, 59]]  # Power/energy gates
                        if energy_gates:
                            energy_indicators.append(f"Energy gates activated: {energy_gates}")
                            relevance += 0.2

        if energy_indicators and relevance > 0.1:
            insight = f"Your energy flow patterns reveal dynamic movement potential: {'; '.join(energy_indicators[:3])}"
            return MuseInsight(
                muse=MuseDomain.TERPSICHORE,
                insight=insight,
                relevance=min(relevance, 1.0),
                supporting_data={"energy_indicators": energy_indicators}
            )

        return None
    
    def _extract_creative_context(self, results: Dict[str, Any], birth_data: Dict[str, Any]) -> Optional[MuseInsight]:
        """Thalia - Joy, creativity, and manifestation"""
        creative_indicators = []
        relevance = 0.0

        # Extract creativity patterns from numerology
        if "numerology" in results:
            num_data = results["numerology"]
            if isinstance(num_data, dict):
                # Creative life path numbers
                if "life_path" in num_data:
                    lp = num_data["life_path"]
                    if lp in [3, 6, 9]:  # Creative expression numbers
                        creative_indicators.append(f"Creative life path: {lp}")
                        relevance += 0.25
                # Creative expression numbers
                if "expression" in num_data:
                    expr = num_data["expression"]
                    if expr in [3, 5, 7, 11]:  # Artistic expression
                        creative_indicators.append(f"Artistic expression number: {expr}")
                        relevance += 0.2

        # Extract creativity from Human Design
        if "human_design" in results:
            hd_data = results["human_design"]
            if isinstance(hd_data, dict):
                # Look for creative gates
                if "gates" in hd_data:
                    gates = hd_data["gates"]
                    if isinstance(gates, dict):
                        creative_gates = []
                        for gate_pos, gate_info in gates.items():
                            if isinstance(gate_info, dict) and "number" in gate_info:
                                gate_num = gate_info["number"]
                                if gate_num in [1, 3, 7, 13, 43]:  # Creative/inspiration gates
                                    creative_gates.append(gate_num)
                        if creative_gates:
                            creative_indicators.append(f"Creative gates: {creative_gates}")
                            relevance += 0.3
                # Look for creative centers
                if "defined_centers" in hd_data:
                    centers = hd_data["defined_centers"]
                    if isinstance(centers, list):
                        if "Throat" in centers:  # Manifestation center
                            creative_indicators.append("Throat center defined: natural manifestor")
                            relevance += 0.2

        # Extract creativity from Gene Keys
        if "gene_keys" in results:
            gk_data = results["gene_keys"]
            if isinstance(gk_data, dict):
                if "gates" in gk_data:
                    gates = gk_data["gates"]
                    if isinstance(gates, list):
                        creative_gk_gates = [g for g in gates if g in [1, 3, 7, 13, 22, 43]]  # Creative gates
                        if creative_gk_gates:
                            creative_indicators.append(f"Creative Gene Keys: {creative_gk_gates}")
                            relevance += 0.25

        # Extract creativity from Tarot
        if "tarot" in results:
            tarot_data = results["tarot"]
            if isinstance(tarot_data, dict):
                if "cards" in tarot_data:
                    cards = tarot_data["cards"]
                    if isinstance(cards, list):
                        creative_cards = [c for c in cards if isinstance(c, str) and
                                        any(word in c.lower() for word in ["magician", "empress", "star", "sun"])]
                        if creative_cards:
                            creative_indicators.append(f"Creative tarot energies: {creative_cards}")
                            relevance += 0.2

        # Extract creativity from Enneagram
        if "enneagram" in results:
            enn_data = results["enneagram"]
            if isinstance(enn_data, dict):
                if "type" in enn_data:
                    enn_type = enn_data["type"]
                    if enn_type in [4, 7]:  # Creative types
                        creative_indicators.append(f"Creative Enneagram type: {enn_type}")
                        relevance += 0.2

        if creative_indicators and relevance > 0.1:
            insight = f"Your creative potential shines through multiple channels: {'; '.join(creative_indicators[:3])}"
            return MuseInsight(
                muse=MuseDomain.THALIA,
                insight=insight,
                relevance=min(relevance, 1.0),
                supporting_data={"creative_indicators": creative_indicators}
            )

        return None
    
    def _extract_cosmic_timing_context(self, results: Dict[str, Any], birth_data: Dict[str, Any]) -> Optional[MuseInsight]:
        """Urania - Cosmic timing and celestial influences"""
        timing_indicators = []
        relevance = 0.0

        # Extract timing from Vimshottari dasha
        if "vimshottari" in results:
            vim_data = results["vimshottari"]
            if isinstance(vim_data, dict):
                if "current_mahadasha" in vim_data:
                    mahadasha = vim_data["current_mahadasha"]
                    timing_indicators.append(f"Current planetary period: {mahadasha}")
                    relevance += 0.3
                if "current_antardasha" in vim_data:
                    antardasha = vim_data["current_antardasha"]
                    timing_indicators.append(f"Current sub-period: {antardasha}")
                    relevance += 0.2
                if "mahadasha_remaining" in vim_data:
                    remaining = vim_data["mahadasha_remaining"]
                    if isinstance(remaining, (int, float)) and remaining < 2:
                        timing_indicators.append(f"Major transition approaching: {remaining:.1f} years")
                        relevance += 0.25

        # Extract timing from biorhythm
        if "biorhythm" in results:
            bio_data = results["biorhythm"]
            if isinstance(bio_data, dict):
                if "cycles" in bio_data:
                    cycles = bio_data["cycles"]
                    if isinstance(cycles, dict):
                        # Look for cycle peaks and valleys
                        peak_cycles = [k for k, v in cycles.items() if isinstance(v, (int, float)) and v > 80]
                        valley_cycles = [k for k, v in cycles.items() if isinstance(v, (int, float)) and v < -80]
                        if peak_cycles:
                            timing_indicators.append(f"Peak energy timing: {', '.join(peak_cycles)}")
                            relevance += 0.2
                        if valley_cycles:
                            timing_indicators.append(f"Rest period timing: {', '.join(valley_cycles)}")
                            relevance += 0.15

        # Extract timing from numerology personal year
        if "numerology" in results:
            num_data = results["numerology"]
            if isinstance(num_data, dict):
                if "personal_year" in num_data:
                    py = num_data["personal_year"]
                    if py in [1, 9]:  # Major cycle transitions
                        timing_indicators.append(f"Major life cycle: Personal Year {py}")
                        relevance += 0.25
                    elif py in [5, 8]:  # Dynamic years
                        timing_indicators.append(f"Dynamic timing: Personal Year {py}")
                        relevance += 0.2

        # Extract timing from I-Ching
        if "iching" in results:
            iching_data = results["iching"]
            if isinstance(iching_data, dict):
                if "primary_hexagram" in iching_data:
                    hex_data = iching_data["primary_hexagram"]
                    if isinstance(hex_data, dict) and "name" in hex_data:
                        hex_name = hex_data["name"]
                        # Timing-related hexagrams
                        timing_hexagrams = ["Waiting", "Duration", "Gradual Progress", "Development"]
                        if any(timing in hex_name for timing in timing_hexagrams):
                            timing_indicators.append(f"Cosmic timing guidance: {hex_name}")
                            relevance += 0.2
                if "changing_lines" in iching_data:
                    changing = iching_data["changing_lines"]
                    if isinstance(changing, list) and changing:
                        timing_indicators.append(f"Transformation timing: {len(changing)} changing lines")
                        relevance += 0.15

        # Extract timing from birth data
        if birth_data and "date" in birth_data:
            birth_date = birth_data["date"]
            if isinstance(birth_date, str):
                try:
                    # Parse birth date to extract timing patterns
                    from datetime import datetime
                    if "." in birth_date:  # DD.MM.YYYY format
                        day, month, year = birth_date.split(".")
                    elif "-" in birth_date:  # YYYY-MM-DD format
                        year, month, day = birth_date.split("-")
                    else:
                        day, month, year = None, None, None

                    if day and month:
                        # Check for powerful timing dates
                        if day in ["1", "8", "9"] or month in ["1", "8", "12"]:
                            timing_indicators.append(f"Powerful birth timing: {day}/{month}")
                            relevance += 0.1
                except:
                    pass

        if timing_indicators and relevance > 0.1:
            insight = f"Cosmic timing reveals significant patterns in your life cycles: {'; '.join(timing_indicators[:3])}"
            return MuseInsight(
                muse=MuseDomain.URANIA,
                insight=insight,
                relevance=min(relevance, 1.0),
                supporting_data={"timing_indicators": timing_indicators}
            )

        return None
    
    def _extract_integration_context(self, results: Dict[str, Any], birth_data: Dict[str, Any]) -> Optional[MuseInsight]:
        """Mnemosyne - Wisdom integration and synthesis"""
        integration_indicators = []
        relevance = 0.0

        # Count how many engines provided data (integration complexity)
        engine_count = len([k for k in results.keys() if k in [
            "numerology", "biorhythm", "human_design", "vimshottari",
            "gene_keys", "tarot", "iching", "enneagram", "sacred_geometry", "sigil_forge"
        ]])

        if engine_count >= 3:
            integration_indicators.append(f"Multi-system synthesis: {engine_count} engines activated")
            relevance += 0.3

        # Look for cross-system patterns and correlations
        patterns_found = []

        # Check for leadership/authority patterns across systems
        leadership_indicators = 0
        if "numerology" in results:
            num_data = results["numerology"]
            if isinstance(num_data, dict) and "life_path" in num_data:
                if num_data["life_path"] in [1, 8]:
                    leadership_indicators += 1

        if "human_design" in results:
            hd_data = results["human_design"]
            if isinstance(hd_data, dict) and "type" in hd_data:
                if hd_data["type"] == "Manifestor":
                    leadership_indicators += 1

        if "enneagram" in results:
            enn_data = results["enneagram"]
            if isinstance(enn_data, dict) and "type" in enn_data:
                if enn_data["type"] in [3, 8]:
                    leadership_indicators += 1

        if leadership_indicators >= 2:
            patterns_found.append("Leadership archetype")
            relevance += 0.25

        # Check for creative/artistic patterns
        creative_indicators = 0
        if "numerology" in results:
            num_data = results["numerology"]
            if isinstance(num_data, dict):
                if num_data.get("life_path") in [3, 6, 9] or num_data.get("expression") in [3, 5, 7]:
                    creative_indicators += 1

        if "human_design" in results:
            hd_data = results["human_design"]
            if isinstance(hd_data, dict) and "defined_centers" in hd_data:
                if "Throat" in hd_data["defined_centers"]:
                    creative_indicators += 1

        if "enneagram" in results:
            enn_data = results["enneagram"]
            if isinstance(enn_data, dict) and "type" in enn_data:
                if enn_data["type"] in [4, 7]:
                    creative_indicators += 1

        if creative_indicators >= 2:
            patterns_found.append("Creative expression archetype")
            relevance += 0.25

        # Check for spiritual/wisdom patterns
        spiritual_indicators = 0
        if "numerology" in results:
            num_data = results["numerology"]
            if isinstance(num_data, dict):
                if num_data.get("life_path") in [7, 9, 11] or num_data.get("master_numbers"):
                    spiritual_indicators += 1

        if "gene_keys" in results:
            spiritual_indicators += 1  # Gene Keys is inherently spiritual

        if "iching" in results or "tarot" in results:
            spiritual_indicators += 1  # Divination systems

        if spiritual_indicators >= 2:
            patterns_found.append("Spiritual wisdom archetype")
            relevance += 0.25

        # Check for transformation/healing patterns
        transformation_indicators = 0
        if "human_design" in results:
            hd_data = results["human_design"]
            if isinstance(hd_data, dict) and "profile" in hd_data:
                profile = hd_data["profile"]
                if isinstance(profile, str) and any(line in profile for line in ["3/", "6/"]):
                    transformation_indicators += 1

        if "enneagram" in results:
            enn_data = results["enneagram"]
            if isinstance(enn_data, dict) and "type" in enn_data:
                if enn_data["type"] in [4, 5, 9]:  # Transformation types
                    transformation_indicators += 1

        if transformation_indicators >= 1:
            patterns_found.append("Transformation catalyst archetype")
            relevance += 0.2

        # Add integration insights
        if patterns_found:
            integration_indicators.append(f"Archetypal patterns: {', '.join(patterns_found)}")
            relevance += 0.2

        # Check for timing synchronicities
        if "vimshottari" in results and "biorhythm" in results:
            integration_indicators.append("Vedic and Western timing systems aligned")
            relevance += 0.15

        # Check for consciousness evolution indicators
        evolution_indicators = []
        if "gene_keys" in results:
            evolution_indicators.append("Genetic evolution pathway")
        if "human_design" in results:
            evolution_indicators.append("Consciousness blueprint")
        if "numerology" in results:
            evolution_indicators.append("Mathematical life pattern")

        if len(evolution_indicators) >= 2:
            integration_indicators.append(f"Evolution pathways: {', '.join(evolution_indicators[:2])}")
            relevance += 0.2

        if integration_indicators and relevance > 0.2:
            insight = f"Deep integration reveals your consciousness architecture: {'; '.join(integration_indicators[:3])}"
            return MuseInsight(
                muse=MuseDomain.MNEMOSYNE,
                insight=insight,
                relevance=min(relevance, 1.0),
                supporting_data={
                    "integration_indicators": integration_indicators,
                    "patterns_found": patterns_found,
                    "engine_count": engine_count
                }
            )

        return None
    
    def format_context_for_agent(self, insights: List[MuseInsight]) -> str:
        """
        Format extracted context for the main WitnessOS agent
        
        Args:
            insights: List of MuseInsight objects
            
        Returns:
            Formatted context string for agent consumption
        """
        if not insights:
            return "No significant patterns detected by the Muses."
        
        context_parts = [
            "🌟 ALETHEOS CONTEXT EXTRACTION 🌟",
            "",
            "The 10 Muses have revealed the following consciousness patterns:",
            ""
        ]
        
        for insight in insights[:5]:  # Top 5 most relevant insights
            muse_name = insight.muse.value.replace("_", " ").title()
            context_parts.append(f"• {muse_name}: {insight.insight}")
        
        context_parts.extend([
            "",
            "Use this context to provide deeper, more meaningful interpretations that",
            "connect the technical calculations to the user's consciousness journey.",
            ""
        ])
        
        return "\n".join(context_parts)


# Export the main class
__all__ = ["AletheosContextExtractor", "MuseInsight", "MuseDomain"]
