"""
Individual engine implementations for WitnessOS Divination Engines

Each engine provides specialized divination calculations while inheriting
from the common BaseEngine interface.
"""

# Import available engines
try:
    from .numerology import NumerologyEngine
except ImportError:
    pass

try:
    from .biorhythm import BiorhythmEngine
except ImportError:
    pass

try:
    from .human_design import HumanDesignScanner
except ImportError:
    pass

try:
    from .vimshottari import VimshottariTimelineMapper
except ImportError:
    pass

# Future engines to be implemented:
# from .tarot import TarotEngine
# from .iching import IChingEngine
# from .gene_keys import GeneKeysEngine
# from .enneagram import EnneagramEngine
# from .sacred_geometry import SacredGeometryEngine
# from .sigil_forge import SigilForgeEngine

__all__ = [
    "NumerologyEngine",
    "BiorhythmEngine",
    "HumanDesignScanner",
    "VimshottariTimelineMapper",
    # Will be populated as more engines are implemented
]
