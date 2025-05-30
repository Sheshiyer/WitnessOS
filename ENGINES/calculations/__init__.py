"""
Shared calculation modules for WitnessOS Divination Engines

Contains reusable calculation logic that multiple engines can leverage,
avoiding duplication and ensuring consistency.
"""

# Import available calculation modules
try:
    from .numerology import NumerologyCalculator
except ImportError:
    pass

try:
    from .biorhythm import BiorhythmCalculator
except ImportError:
    pass

# Examples of future modules:
# from .astrology import SwissEphemerisCalculator
# from .geometry import SacredGeometryCalculator
# from .divination import DivinationRandomizer

__all__ = [
    "NumerologyCalculator",
    "BiorhythmCalculator",
    # Will be populated as more modules are implemented
]
