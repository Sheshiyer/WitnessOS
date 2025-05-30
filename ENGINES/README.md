# WitnessOS Divination Engines

A modular collection of consciousness exploration and divination engines for the WitnessOS reality debugging framework.

## 🏗️ Project Structure

```
ENGINES/
├── README.md                    # This file
├── engines_todo.md             # Implementation roadmap and progress tracker
├── requirements.txt            # Python dependencies
├── __init__.py                 # Main package initialization and engine registry
│
├── base/                       # Foundation architecture
│   ├── engine_interface.py     # Abstract base class for all engines
│   ├── data_models.py          # Pydantic models for standardized I/O
│   └── utils.py                # Shared utilities and helper functions
│
├── calculations/               # Shared calculation modules
│   ├── astrology.py            # Swiss Ephemeris astronomical calculations
│   ├── biorhythm.py            # Sine wave mathematics for biorhythms
│   ├── divination.py           # Randomization and symbolic mapping
│   └── numerology.py           # Pythagorean & Chaldean number systems
│
├── engines/                    # Individual engine implementations
│   ├── numerology.py           # Numerology Field Extractor
│   ├── biorhythm.py            # Biorhythm Synchronizer
│   ├── human_design.py         # Human Design Scanner
│   ├── vimshottari.py          # Vimshottari Timeline Mapper
│   ├── tarot.py                # Tarot Sequence Decoder
│   ├── iching.py               # I-Ching Mutation Oracle
│   ├── gene_keys.py            # Gene Keys Compass
│   ├── enneagram.py            # Enneagram Resonator
│   └── *_models.py             # Data models for each engine
│
├── data/                       # Static data files
│   ├── astrology/              # Astronomical reference data
│   ├── tarot/                  # Tarot card definitions
│   ├── iching/                 # I-Ching hexagram data
│   ├── gene_keys/              # Gene Keys archetypal mappings
│   ├── enneagram/              # Enneagram type definitions
│   ├── human_design/           # Human Design system data
│   └── sacred_geometry/        # Sacred geometry patterns
│
├── tests/                      # Unit and integration tests
│   ├── test_foundation.py      # Foundation architecture tests
│   ├── test_numerology.py      # Numerology engine tests
│   ├── test_biorhythm.py       # Biorhythm engine tests
│   ├── test_human_design.py    # Human Design engine tests
│   ├── test_vimshottari.py     # Vimshottari engine tests
│   ├── test_tarot.py           # Tarot engine tests
│   ├── test_iching.py          # I-Ching engine tests
│   ├── test_gene_keys.py       # Gene Keys engine tests
│   └── test_enneagram.py       # Enneagram engine tests
│
├── demos/                      # Demonstration scripts
│   ├── demo_foundation.py      # Foundation architecture demo
│   ├── demo_numerology.py      # Numerology engine demo
│   ├── demo_biorhythm.py       # Biorhythm engine demo
│   ├── demo_human_design.py    # Human Design engine demo
│   ├── demo_vimshottari.py     # Vimshottari engine demo
│   ├── demo_phase4.py          # Symbolic engines demo (Tarot, I-Ching, Gene Keys)
│   └── demo_phase5.py          # Psychological engines demo (Enneagram)
│
├── validation/                 # Validation and testing framework
│   ├── test_validation_data.py # Real Human Design data for validation
│   └── run_validation_tests.py # Comprehensive validation test runner
│
└── docs/                       # Documentation
    ├── IMPLEMENTATION_ROADMAP.md
    ├── TECHNICAL_SPECS.md
    ├── PHASE1_COMPLETE.md
    ├── PHASE2_1_COMPLETE.md
    └── PHASE2_2_COMPLETE.md
```

## 🎯 Current Status

### ✅ Completed Phases
- **Phase 1**: Foundation Architecture (Base classes, data models, utilities)
- **Phase 2**: Simple Engines (Numerology, Biorhythm)
- **Phase 3**: Astronomical Engines (Human Design, Vimshottari Dasha)
- **Phase 4**: Symbolic Engines (Tarot, I-Ching, Gene Keys)
- **Phase 5**: Psychological Engines (Enneagram)

### 🔄 Current Phase
- **Phase 6**: Creative/Generative Engines (Sacred Geometry, Sigil Forge)

### 📋 Next Phases
- **Phase 7**: Integration & Testing (Multi-engine workflows, API endpoints)

## 🚀 Quick Start

```python
from ENGINES import get_engine

# Get a specific engine
numerology = get_engine("numerology_field_extractor")

# Run calculation with your data
result = numerology.calculate({
    "full_name": "Your Name",
    "birth_date": "1991-08-13",
    "system": "pythagorean"
})

print(result.formatted_output)
```

## 🧪 Testing

Run all tests:
```bash
cd ENGINES
python -m pytest tests/
```

Run validation tests with real data:
```bash
cd ENGINES/validation
python run_validation_tests.py
```

## 🎮 Demos

Run individual engine demos:
```bash
cd ENGINES/demos
python demo_numerology.py
python demo_human_design.py
python demo_phase4.py  # Multi-engine symbolic reading
```

## 🔮 Validation Data

All engines are tested with real Human Design data:
- **Subject**: Cumbipuram Nateshan Sheshnarayan
- **Birth**: August 13, 1991, 13:31, Bengaluru, India
- **Known Chart**: 2/4 Hermit/Opportunist Generator, Sacral Authority

This enables immediate accuracy verification against known chart information.

## 📚 Documentation

See `docs/` directory for detailed implementation documentation and technical specifications.

## 🌟 Philosophy

These engines are designed as consciousness exploration tools, not prediction systems. They provide pattern recognition and archetypal guidance for conscious navigation of reality fields.

---

*Part of the WitnessOS reality debugging framework*
*Maintained by: The Witness Alchemist & Runtime Architect*
