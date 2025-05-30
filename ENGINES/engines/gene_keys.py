"""
Gene Keys Compass Engine for WitnessOS

Provides Gene Keys archetypal analysis based on birth data.
Calculates Activation, Venus, and Pearl sequences with pathworking guidance.
"""

from datetime import datetime, date
from typing import Dict, List, Any, Type, Optional

from base.engine_interface import BaseEngine
from base.data_models import BaseEngineInput, BaseEngineOutput
from base.utils import load_json_data
from calculations.divination import DivinationCalculator
from .gene_keys_models import (
    GeneKeysInput, GeneKeysOutput, GeneKey, SequenceGate, GeneKeysSequence,
    GeneKeysProfile, GeneKeysData
)


class GeneKeysCompass(BaseEngine):
    """
    Gene Keys Compass Engine
    
    Provides Gene Keys archetypal analysis based on birth data,
    calculating the Activation, Venus, and Pearl sequences.
    """
    
    def __init__(self):
        super().__init__()
        self.gene_keys_data: Optional[GeneKeysData] = None
        self.divination_calc = DivinationCalculator()
        self._load_gene_keys_data()
    
    @property
    def engine_name(self) -> str:
        return "Gene Keys Compass"
    
    @property
    def description(self) -> str:
        return "Provides Gene Keys archetypal analysis based on birth data with Activation, Venus, and Pearl sequences"
    
    @property
    def input_model(self) -> Type[BaseEngineInput]:
        return GeneKeysInput
    
    @property
    def output_model(self) -> Type[BaseEngineOutput]:
        return GeneKeysOutput
    
    def _load_gene_keys_data(self) -> None:
        """Load Gene Keys data from JSON files."""
        try:
            gene_keys_json = load_json_data("gene_keys", "archetypes.json")
            self.gene_keys_data = GeneKeysData(**gene_keys_json)
            self.logger.info("Loaded Gene Keys archetypal data")
        except Exception as e:
            self.logger.error(f"Failed to load Gene Keys data: {e}")
            raise
    
    def _get_gene_key_by_number(self, number: int) -> GeneKey:
        """Get Gene Key by its number."""
        # Ensure number is within valid range
        if number < 1 or number > 64:
            number = ((number - 1) % 64) + 1
        
        # If Gene Key doesn't exist in data, use a fallback
        if str(number) not in self.gene_keys_data.gene_keys:
            # Use Gene Key 1 as fallback
            number = 1
        
        key_data = self.gene_keys_data.gene_keys[str(number)]
        return GeneKey(**key_data)
    
    def _calculate_gene_key_from_date(self, birth_date: date, offset_days: int = 0) -> int:
        """
        Calculate Gene Key number from birth date.
        
        This is a simplified calculation. In a full implementation,
        this would use actual astronomical calculations.
        """
        # Add offset for design calculations (88 days before birth)
        calculation_date = birth_date
        if offset_days != 0:
            from datetime import timedelta
            calculation_date = birth_date - timedelta(days=offset_days)
        
        # Simple calculation based on day of year
        day_of_year = calculation_date.timetuple().tm_yday
        
        # Map to Gene Key number (1-64)
        gene_key_number = ((day_of_year - 1) % 64) + 1
        
        return gene_key_number
    
    def _create_activation_sequence(self, birth_date: date) -> GeneKeysSequence:
        """Create the Activation Sequence."""
        
        # Calculate the four gates
        lifes_work_num = self._calculate_gene_key_from_date(birth_date)
        evolution_num = self._calculate_gene_key_from_date(birth_date, 1)  # Slight offset
        radiance_num = self._calculate_gene_key_from_date(birth_date, 88)  # Design Sun
        purpose_num = self._calculate_gene_key_from_date(birth_date, 89)   # Design Earth
        
        gates = [
            SequenceGate(
                name="Life's Work",
                description="Your core life purpose and creative expression",
                gene_key=self._get_gene_key_by_number(lifes_work_num),
                calculation_method="Sun position at birth"
            ),
            SequenceGate(
                name="Evolution",
                description="Your path of personal development and growth",
                gene_key=self._get_gene_key_by_number(evolution_num),
                calculation_method="Earth position at birth"
            ),
            SequenceGate(
                name="Radiance",
                description="Your gift to humanity and how you shine",
                gene_key=self._get_gene_key_by_number(radiance_num),
                calculation_method="Sun position 88 days before birth"
            ),
            SequenceGate(
                name="Purpose",
                description="Your deepest calling and spiritual mission",
                gene_key=self._get_gene_key_by_number(purpose_num),
                calculation_method="Earth position 88 days before birth"
            )
        ]
        
        return GeneKeysSequence(
            name="Activation Sequence",
            description="The four primary gates that form your core genetic blueprint",
            gates=gates
        )
    
    def _create_venus_sequence(self, birth_date: date) -> GeneKeysSequence:
        """Create the Venus Sequence."""
        
        # Calculate Venus gates (simplified)
        attraction_num = self._calculate_gene_key_from_date(birth_date, 30)  # Venus cycle approximation
        magnetism_num = self._calculate_gene_key_from_date(birth_date, 118) # Venus design
        
        gates = [
            SequenceGate(
                name="Attraction",
                description="What draws you to others and others to you",
                gene_key=self._get_gene_key_by_number(attraction_num),
                calculation_method="Venus position at birth"
            ),
            SequenceGate(
                name="Magnetism",
                description="Your natural charisma and appeal",
                gene_key=self._get_gene_key_by_number(magnetism_num),
                calculation_method="Venus position 88 days before birth"
            )
        ]
        
        return GeneKeysSequence(
            name="Venus Sequence",
            description="The pathway of love and relationships",
            gates=gates
        )
    
    def _create_pearl_sequence(self, birth_date: date) -> GeneKeysSequence:
        """Create the Pearl Sequence."""
        
        # Calculate Pearl gates (simplified)
        vocation_num = self._calculate_gene_key_from_date(birth_date, 365)  # Jupiter cycle approximation
        culture_num = self._calculate_gene_key_from_date(birth_date, 10950) # Saturn cycle approximation
        brand_num = self._calculate_gene_key_from_date(birth_date, 30660)   # Uranus cycle approximation
        
        gates = [
            SequenceGate(
                name="Vocation",
                description="Your natural career path and work style",
                gene_key=self._get_gene_key_by_number(vocation_num),
                calculation_method="Jupiter position at birth"
            ),
            SequenceGate(
                name="Culture",
                description="Your contribution to collective evolution",
                gene_key=self._get_gene_key_by_number(culture_num),
                calculation_method="Saturn position at birth"
            ),
            SequenceGate(
                name="Brand",
                description="Your unique signature in the world",
                gene_key=self._get_gene_key_by_number(brand_num),
                calculation_method="Uranus position at birth"
            )
        ]
        
        return GeneKeysSequence(
            name="Pearl Sequence",
            description="The pathway of prosperity and material manifestation",
            gates=gates
        )
    
    def _generate_pathworking_guidance(self, profile: GeneKeysProfile, focus: Optional[str]) -> List[str]:
        """Generate pathworking guidance based on the profile."""
        
        guidance = []
        primary_key = profile.primary_gene_key
        
        # Core pathworking guidance
        guidance.append(f"Begin with contemplation of your Life's Work Gene Key {primary_key.number}: {primary_key.name}")
        guidance.append(f"Notice when you operate from the Shadow of {primary_key.shadow} and practice shifting to the Gift of {primary_key.gift}")
        guidance.append(f"Your programming partner is Gene Key {primary_key.programming_partner}, study both keys together for balance")
        
        # Sequence-specific guidance
        if focus == "activation" or focus == "all":
            guidance.append("Focus on your Activation Sequence to understand your core life purpose and creative expression")
        
        if focus == "venus" or focus == "all":
            guidance.append("Explore your Venus Sequence to understand your patterns in love and relationships")
        
        if focus == "pearl" or focus == "all":
            guidance.append("Work with your Pearl Sequence to align your vocation with your highest purpose")
        
        # Frequency shifting guidance
        guidance.append("Practice the art of frequency shifting: awareness of Shadow, embodiment of Gift, surrender to Siddhi")
        guidance.append("Remember that all three frequencies serve the evolution of consciousness")
        
        return guidance
    
    def _calculate(self, validated_input: GeneKeysInput) -> Dict[str, Any]:
        """Process the Gene Keys calculation."""
        
        birth_date = validated_input.birth_date
        
        # Create sequences
        activation_sequence = self._create_activation_sequence(birth_date)
        venus_sequence = self._create_venus_sequence(birth_date)
        pearl_sequence = self._create_pearl_sequence(birth_date)
        
        # Get primary Gene Key and programming partner
        primary_gene_key = activation_sequence.gates[0].gene_key  # Life's Work
        programming_partner = self._get_gene_key_by_number(primary_gene_key.programming_partner)
        
        # Create profile
        profile = GeneKeysProfile(
            activation_sequence=activation_sequence,
            venus_sequence=venus_sequence,
            pearl_sequence=pearl_sequence,
            birth_date=birth_date,
            primary_gene_key=primary_gene_key,
            programming_partner=programming_partner
        )
        
        # Generate pathworking guidance
        pathworking_guidance = self._generate_pathworking_guidance(
            profile, 
            validated_input.pathworking_focus or validated_input.focus_sequence
        )
        
        # Create key insights
        key_insights = [
            f"Your Life's Work is Gene Key {primary_gene_key.number}: {primary_gene_key.name}",
            f"Transform {primary_gene_key.shadow} (Shadow) into {primary_gene_key.gift} (Gift)",
            f"Your programming partner Gene Key {programming_partner.number} provides balance and perspective",
        ]
        
        if validated_input.focus_sequence == "venus" or validated_input.focus_sequence == "all":
            attraction_key = venus_sequence.gates[0].gene_key
            key_insights.append(f"In relationships, you attract through Gene Key {attraction_key.number}: {attraction_key.name}")
        
        if validated_input.focus_sequence == "pearl" or validated_input.focus_sequence == "all":
            vocation_key = pearl_sequence.gates[0].gene_key
            key_insights.append(f"Your vocation aligns with Gene Key {vocation_key.number}: {vocation_key.name}")
        
        # Calculate archetypal resonance
        gene_key_names = [gate.gene_key.name for gate in activation_sequence.gates]
        field_resonance = self.divination_calc.calculate_archetypal_resonance(
            gene_key_names,
            {"birth_date": str(birth_date)}
        )
        
        return {
            "profile": profile,
            "birth_date": birth_date,
            "calculation_timestamp": datetime.now(),
            "focus_sequence": validated_input.focus_sequence,
            "key_insights": key_insights,
            "pathworking_guidance": pathworking_guidance,
            "guidance_summary": f"Your Gene Keys reveal {primary_gene_key.name} as your Life's Work, guiding you to transform {primary_gene_key.shadow} into {primary_gene_key.gift}.",
            "primary_life_theme": primary_gene_key.life_theme,
            "programming_partnership": f"Gene Key {primary_gene_key.number} and {programming_partner.number} work together",
            "field_resonance": field_resonance,
            "field_signature": "gene_keys_archetypal_compass"
        }
    
    def _interpret(self, calculation_results: Dict[str, Any], input_data: GeneKeysInput) -> str:
        """Interpret calculation results into human-readable format."""
        
        profile = calculation_results["profile"]
        
        interpretation = f"🧬 Gene Keys Compass Reading\n\n"
        interpretation += f"👤 Birth Date: {calculation_results['birth_date']}\n"
        interpretation += f"🎯 Focus: {calculation_results['focus_sequence'].title()} Sequence\n"
        interpretation += f"🕐 Reading Time: {calculation_results['calculation_timestamp'].strftime('%Y-%m-%d %H:%M')}\n\n"
        
        # Primary Gene Key
        primary = profile.primary_gene_key
        interpretation += f"🌟 Life's Work: Gene Key {primary.number} - {primary.name}\n"
        interpretation += f"🌑 Shadow: {primary.shadow}\n"
        interpretation += f"🎁 Gift: {primary.gift}\n"
        interpretation += f"✨ Siddhi: {primary.siddhi}\n"
        interpretation += f"🧬 Codon: {primary.codon} ({primary.amino_acid})\n"
        interpretation += f"🎭 Life Theme: {primary.life_theme}\n\n"
        
        # Programming Partner
        partner = profile.programming_partner
        interpretation += f"🤝 Programming Partner: Gene Key {partner.number} - {partner.name}\n"
        interpretation += f"   Shadow: {partner.shadow} | Gift: {partner.gift} | Siddhi: {partner.siddhi}\n\n"
        
        # Sequences based on focus
        if input_data.focus_sequence in ["activation", "all"]:
            interpretation += "🔥 Activation Sequence:\n"
            for gate in profile.activation_sequence.gates:
                interpretation += f"   {gate.name}: Gene Key {gate.gene_key.number} - {gate.gene_key.name}\n"
            interpretation += "\n"
        
        if input_data.focus_sequence in ["venus", "all"]:
            interpretation += "💕 Venus Sequence:\n"
            for gate in profile.venus_sequence.gates:
                interpretation += f"   {gate.name}: Gene Key {gate.gene_key.number} - {gate.gene_key.name}\n"
            interpretation += "\n"
        
        if input_data.focus_sequence in ["pearl", "all"]:
            interpretation += "💎 Pearl Sequence:\n"
            for gate in profile.pearl_sequence.gates:
                interpretation += f"   {gate.name}: Gene Key {gate.gene_key.number} - {gate.gene_key.name}\n"
            interpretation += "\n"
        
        interpretation += f"🎯 Core Guidance: {calculation_results['guidance_summary']}\n\n"
        
        interpretation += "🛤️ Pathworking Steps:\n"
        for i, guidance in enumerate(calculation_results['pathworking_guidance'][:5], 1):
            interpretation += f"   {i}. {guidance}\n"
        
        return interpretation


# Export the engine class
__all__ = ["GeneKeysCompass"]
