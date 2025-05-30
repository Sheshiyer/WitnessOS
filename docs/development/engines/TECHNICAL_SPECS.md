# TECHNICAL SPECIFICATIONS - WitnessOS Divination Engines

## 🎯 **Overview**
Comprehensive technical documentation for the mathematical, algorithmic, and data foundations of all 10 WitnessOS divination engines. Each engine specification includes input parameters, calculation methods, required libraries, data structures, and expected outputs.

---

## 🧮 **1. NUMEROLOGY FIELD EXTRACTOR**

### **Input Parameters**
```python
class NumerologyInput:
    full_name: str          # Complete birth name
    birth_date: date        # Date of birth
    current_date: date      # For personal year calculation
```

### **Core Calculations**

#### **1.1 Life Path Number**
```python
# Reduce birth date to single digit (except master numbers 11, 22, 33)
def calculate_life_path(birth_date):
    total = sum(int(digit) for digit in birth_date.strftime("%m%d%Y"))
    return reduce_to_single_digit(total, keep_master=True)
```

#### **1.2 Expression Number (Destiny Number)**
```python
# Pythagorean system: A=1, B=2, C=3... Z=26, then reduce
PYTHAGOREAN = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
}

def calculate_expression(full_name):
    total = sum(PYTHAGOREAN.get(char.upper(), 0) for char in full_name if char.isalpha())
    return reduce_to_single_digit(total, keep_master=True)
```

#### **1.3 Soul Urge Number (Heart's Desire)**
```python
# Only vowels from full name
VOWELS = 'AEIOU'
def calculate_soul_urge(full_name):
    vowel_total = sum(PYTHAGOREAN[char] for char in full_name.upper() if char in VOWELS)
    return reduce_to_single_digit(vowel_total, keep_master=True)
```

#### **1.4 Personality Number**
```python
# Only consonants from full name
def calculate_personality(full_name):
    consonant_total = sum(PYTHAGOREAN[char] for char in full_name.upper()
                         if char.isalpha() and char not in VOWELS)
    return reduce_to_single_digit(consonant_total, keep_master=True)
```

#### **1.5 Personal Year**
```python
def calculate_personal_year(birth_date, current_date):
    birth_month_day = birth_date.strftime("%m%d")
    current_year = current_date.year
    total = sum(int(digit) for digit in f"{birth_month_day}{current_year}")
    return reduce_to_single_digit(total)
```

### **Libraries Required**
- `datetime` (built-in)
- `typing` (built-in)

### **Output Structure**
```python
class NumerologyOutput:
    life_path: int
    expression: int
    soul_urge: int
    personality: int
    personal_year: int
    master_numbers: List[int]  # Any 11, 22, 33 found
    interpretation: Dict[str, str]
```

---

## 📈 **2. BIORHYTHM SYNCHRONIZER**

### **Input Parameters**
```python
class BiorhythmInput:
    birth_date: date
    target_date: date = None  # Defaults to today
```

### **Core Calculations**

#### **2.1 Cycle Calculations**
```python
import math

def calculate_biorhythm_cycles(birth_date, target_date):
    days_alive = (target_date - birth_date).days

    # Standard biorhythm cycles
    physical = math.sin(2 * math.pi * days_alive / 23) * 100      # 23-day cycle
    emotional = math.sin(2 * math.pi * days_alive / 28) * 100     # 28-day cycle
    intellectual = math.sin(2 * math.pi * days_alive / 33) * 100  # 33-day cycle

    return {
        'physical': round(physical, 2),
        'emotional': round(emotional, 2),
        'intellectual': round(intellectual, 2)
    }
```

#### **2.2 Critical Days Detection**
```python
def find_critical_days(birth_date, start_date, days_ahead=30):
    critical_days = []
    for i in range(days_ahead):
        check_date = start_date + timedelta(days=i)
        cycles = calculate_biorhythm_cycles(birth_date, check_date)

        # Critical day if any cycle crosses zero (within ±5%)
        if any(abs(cycle) <= 5 for cycle in cycles.values()):
            critical_days.append(check_date)

    return critical_days
```

### **Libraries Required**
- `math` (built-in)
- `datetime` (built-in)
- `numpy` (for advanced curve analysis)

### **Output Structure**
```python
class BiorhythmOutput:
    physical_percentage: float
    emotional_percentage: float
    intellectual_percentage: float
    cycle_trends: Dict[str, str]  # 'rising', 'falling', 'peak', 'valley'
    critical_days: List[date]
    energy_forecast: str
```

---

## ⚡ **3. HUMAN DESIGN SCANNER**

### **Input Parameters**
```python
class HumanDesignInput:
    birth_date: date
    birth_time: time
    birth_location: Tuple[float, float]  # (latitude, longitude)
    timezone: str
```

### **Core Calculations**

#### **3.1 Astronomical Calculations**
```python
import swisseph as swe

def calculate_planetary_positions(julian_day):
    planets = [
        swe.SUN, swe.EARTH, swe.MOON, swe.MERCURY, swe.VENUS,
        swe.MARS, swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO
    ]

    positions = {}
    for planet in planets:
        pos, _ = swe.calc_ut(julian_day, planet)
        positions[planet] = pos[0]  # Longitude in degrees

    return positions
```

#### **3.2 I-Ching Gate Mapping**
```python
def degrees_to_gate_line(degrees):
    # 360 degrees / 64 gates = 5.625 degrees per gate
    gate_size = 360 / 64
    line_size = gate_size / 6

    gate = int(degrees / gate_size) + 1
    line = int((degrees % gate_size) / line_size) + 1

    return gate, line
```

#### **3.3 Design vs Personality Calculation**
```python
def calculate_design_time(birth_datetime):
    # Design is calculated 88 degrees of Sun movement before birth
    # Approximately 88 days before birth
    return birth_datetime - timedelta(days=88)
```

#### **3.4 Type Determination**
```python
def determine_type(defined_centers):
    sacral_defined = 'sacral' in defined_centers
    throat_defined = 'throat' in defined_centers

    if not sacral_defined and not throat_defined:
        return 'Reflector'
    elif sacral_defined and throat_defined:
        return 'Manifesting Generator'
    elif sacral_defined:
        return 'Generator'
    elif throat_defined:
        return 'Manifestor'
    else:
        return 'Projector'
```

### **Libraries Required**
- `pyswisseph`
- `pytz`
- `datetime`

### **Data Required**
- I-Ching gate definitions (64 gates)
- Center definitions (9 centers)
- Channel definitions (36 channels)
- Gate-to-center mappings

### **Output Structure**
```python
class HumanDesignOutput:
    type: str
    strategy: str
    authority: str
    profile: Tuple[int, int]
    defined_centers: List[str]
    undefined_centers: List[str]
    gates: Dict[str, Tuple[int, int]]  # 'personality_sun': (gate, line)
    channels: List[int]
```

---

## 🌌 **4. VIMSHOTTARI DASHA TIMELINE MAPPER**

### **Input Parameters**
```python
class VimshottariInput:
    birth_date: date
    birth_time: time
    birth_location: Tuple[float, float]
    current_date: date = None
```

### **Core Calculations**

#### **4.1 Moon Nakshatra Calculation**
```python
def calculate_moon_nakshatra(julian_day):
    moon_pos, _ = swe.calc_ut(julian_day, swe.MOON)
    moon_longitude = moon_pos[0]

    # 27 nakshatras, each 13°20' (13.333...)
    nakshatra_size = 360 / 27
    nakshatra_number = int(moon_longitude / nakshatra_size) + 1

    # Position within nakshatra (0-1)
    nakshatra_position = (moon_longitude % nakshatra_size) / nakshatra_size

    return nakshatra_number, nakshatra_position
```

#### **4.2 Dasha Period Calculations**
```python
# Vimshottari Dasha periods in years
DASHA_PERIODS = {
    'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10, 'Mars': 7,
    'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17
}

NAKSHATRA_LORDS = [
    'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury'
] * 3  # Repeats 3 times for 27 nakshatras

def calculate_current_dasha(birth_nakshatra, nakshatra_position, birth_date, current_date):
    lord = NAKSHATRA_LORDS[birth_nakshatra - 1]
    period_years = DASHA_PERIODS[lord]

    # Calculate remaining period at birth
    remaining_at_birth = period_years * (1 - nakshatra_position)

    # Calculate elapsed time since birth
    elapsed_years = (current_date - birth_date).days / 365.25

    # Find current Mahadasha
    if elapsed_years <= remaining_at_birth:
        return lord, remaining_at_birth - elapsed_years

    # Continue through subsequent dashas...
    # (Complex calculation involving all 9 planetary periods)
```

### **Libraries Required**
- `pyswisseph`
- `datetime`
- `pytz`

### **Data Required**
- Nakshatra definitions and lords
- Dasha period lengths
- Antardasha subdivisions

### **Output Structure**
```python
class VimshottariOutput:
    current_mahadasha: str
    mahadasha_remaining: float  # years
    current_antardasha: str
    antardasha_remaining: float  # months
    birth_nakshatra: str
    dasha_timeline: List[Dict]  # Future periods
```

---

## 🎴 **5. TAROT SEQUENCE DECODER**

### **Input Parameters**
```python
class TarotInput:
    question: str = None
    spread_type: str = 'single'  # 'single', 'three_card', 'celtic_cross'
    deck_type: str = 'rider_waite'
    seed: int = None  # For reproducible readings
```

### **Core Calculations**

#### **5.1 Card Selection Algorithm**
```python
import random

def shuffle_and_draw(deck, num_cards, seed=None):
    if seed:
        random.seed(seed)

    shuffled_deck = deck.copy()
    random.shuffle(shuffled_deck)

    drawn_cards = []
    for i in range(num_cards):
        card = shuffled_deck.pop()
        # Determine if reversed (50% chance)
        reversed = random.choice([True, False])
        drawn_cards.append({'card': card, 'reversed': reversed})

    return drawn_cards
```

#### **5.2 Spread Layouts**
```python
SPREAD_LAYOUTS = {
    'single': {
        'positions': ['Present Situation'],
        'card_count': 1
    },
    'three_card': {
        'positions': ['Past', 'Present', 'Future'],
        'card_count': 3
    },
    'celtic_cross': {
        'positions': [
            'Present Situation', 'Challenge', 'Distant Past', 'Recent Past',
            'Possible Outcome', 'Near Future', 'Your Approach', 'External Influences',
            'Hopes and Fears', 'Final Outcome'
        ],
        'card_count': 10
    }
}
```

### **Libraries Required**
- `random` (built-in)
- `json` (for card data)

### **Data Required**
- Complete tarot deck definitions (78 cards)
- Card meanings (upright and reversed)
- Spread position interpretations

### **Output Structure**
```python
class TarotOutput:
    spread_type: str
    cards: List[Dict]  # [{'position': str, 'card': str, 'reversed': bool, 'meaning': str}]
    overall_theme: str
    guidance: str
```

---

## ☯️ **6. I-CHING MUTATION ORACLE**

### **Input Parameters**
```python
class IChingInput:
    question: str = None
    method: str = 'coins'  # 'coins', 'yarrow', 'random'
    seed: int = None
```

### **Core Calculations**

#### **6.1 Hexagram Generation**
```python
def generate_hexagram_coins():
    lines = []
    for _ in range(6):  # 6 lines, bottom to top
        # Throw 3 coins, heads=3, tails=2
        throw = sum(random.choice([2, 3]) for _ in range(3))

        if throw == 6:    # Old Yin (changing)
            lines.append({'value': 0, 'changing': True})
        elif throw == 7:  # Young Yang
            lines.append({'value': 1, 'changing': False})
        elif throw == 8:  # Young Yin
            lines.append({'value': 0, 'changing': False})
        elif throw == 9:  # Old Yang (changing)
            lines.append({'value': 1, 'changing': True})

    return lines

def lines_to_hexagram_number(lines):
    # Convert 6 lines to hexagram number (1-64)
    binary = ''.join(str(line['value']) for line in reversed(lines))
    return int(binary, 2) + 1
```

#### **6.2 Mutation Calculation**
```python
def calculate_mutation(original_lines):
    if not any(line['changing'] for line in original_lines):
        return None  # No changing lines

    mutated_lines = []
    for line in original_lines:
        if line['changing']:
            # Flip the line
            mutated_lines.append({'value': 1 - line['value'], 'changing': False})
        else:
            mutated_lines.append(line)

    return lines_to_hexagram_number(mutated_lines)
```

### **Libraries Required**
- `random` (built-in)
- `json` (for hexagram data)

### **Data Required**
- 64 hexagram definitions with names and meanings
- Line interpretations for each hexagram
- Trigram combinations

### **Output Structure**
```python
class IChingOutput:
    primary_hexagram: int
    hexagram_name: str
    changing_lines: List[int]
    mutation_hexagram: int = None
    interpretation: str
    line_meanings: List[str]
```

---

## 🧬 **7. GENE KEYS COMPASS**

### **Input Parameters**
```python
class GeneKeysInput:
    birth_date: date
    birth_time: time
    birth_location: Tuple[float, float]
```

### **Core Calculations**

#### **7.1 Based on Human Design Foundation**
```python
def calculate_gene_keys_profile(human_design_gates):
    # Gene Keys uses same I-Ching gates as Human Design
    activation_sequence = {
        'life_work': human_design_gates['personality_sun'][0],
        'evolution': human_design_gates['personality_earth'][0],
        'radiance': human_design_gates['design_sun'][0],
        'purpose': human_design_gates['design_earth'][0]
    }

    return activation_sequence
```

#### **7.2 Shadow-Gift-Siddhi Mapping**
```python
GENE_KEYS_ARCHETYPES = {
    1: {
        'shadow': 'Entropy',
        'gift': 'Freshness',
        'siddhi': 'Beauty'
    },
    # ... all 64 gates
}

def get_archetypal_pathway(gate_number):
    return GENE_KEYS_ARCHETYPES.get(gate_number, {})
```

### **Libraries Required**
- Same as Human Design (pyswisseph, etc.)

### **Data Required**
- 64 Gene Keys with Shadow→Gift→Siddhi mappings
- Sequence interpretations
- Codon wheel relationships

### **Output Structure**
```python
class GeneKeysOutput:
    activation_sequence: Dict[str, int]
    venus_sequence: Dict[str, int]
    pearl_sequence: Dict[str, int]
    pathways: Dict[str, Dict]  # Shadow/Gift/Siddhi for each gate
    current_focus: str
```

---

## 🧠 **8. ENNEAGRAM RESONATOR**

### **Input Parameters**
```python
class EnneagramInput:
    assessment_responses: List[int] = None  # Questionnaire scores
    intuitive_type: int = None  # Direct type selection
    stress_level: str = 'normal'  # 'low', 'normal', 'high'
```

### **Core Calculations**

#### **8.1 Type Determination**
```python
def calculate_enneagram_type(responses):
    # Score responses for each of 9 types
    type_scores = [0] * 9

    for i, response in enumerate(responses):
        question_type = QUESTION_MAPPINGS[i]  # Which type this question measures
        type_scores[question_type - 1] += response

    return type_scores.index(max(type_scores)) + 1
```

#### **8.2 Wing Calculation**
```python
def calculate_wings(primary_type, type_scores):
    # Adjacent types are potential wings
    left_wing = primary_type - 1 if primary_type > 1 else 9
    right_wing = primary_type + 1 if primary_type < 9 else 1

    left_score = type_scores[left_wing - 1]
    right_score = type_scores[right_wing - 1]

    if left_score > right_score:
        return f"{primary_type}w{left_wing}"
    else:
        return f"{primary_type}w{right_wing}"
```

#### **8.3 Arrow Movements**
```python
STRESS_ARROWS = {1: 4, 2: 8, 3: 9, 4: 2, 5: 7, 6: 3, 7: 1, 8: 5, 9: 6}
GROWTH_ARROWS = {1: 7, 2: 4, 3: 6, 4: 1, 5: 8, 6: 9, 7: 5, 8: 2, 9: 3}

def get_arrow_movements(enneagram_type):
    return {
        'stress_point': STRESS_ARROWS[enneagram_type],
        'growth_point': GROWTH_ARROWS[enneagram_type]
    }
```

### **Libraries Required**
- `statistics` (built-in)

### **Data Required**
- Enneagram type descriptions
- Assessment questionnaire
- Wing and arrow definitions
- Instinctual variant descriptions

### **Output Structure**
```python
class EnneagramOutput:
    primary_type: int
    wing: str
    stress_point: int
    growth_point: int
    instinctual_variant: str
    integration_level: int
    core_motivation: str
    basic_fear: str
```

---

## 🔺 **9. SACRED GEOMETRY MAPPER**

### **Input Parameters**
```python
class SacredGeometryInput:
    intention: str
    resonance_profile: Dict = None  # User preferences
    geometry_type: str = 'auto'  # 'mandala', 'flower_of_life', 'platonic'
    complexity: str = 'medium'  # 'simple', 'medium', 'complex'
```

### **Core Calculations**

#### **9.1 Golden Ratio Constructions**
```python
import math

PHI = (1 + math.sqrt(5)) / 2  # Golden ratio

def generate_golden_spiral(center, radius, turns=3):
    points = []
    angle_step = 0.1

    for i in range(int(turns * 2 * math.pi / angle_step)):
        angle = i * angle_step
        r = radius * math.exp(angle / (2 * math.pi) * math.log(PHI))

        x = center[0] + r * math.cos(angle)
        y = center[1] + r * math.sin(angle)
        points.append((x, y))

    return points
```

#### **9.2 Mandala Generation**
```python
def generate_mandala_pattern(center, radius, petals=8, layers=3):
    patterns = []

    for layer in range(layers):
        layer_radius = radius * (layer + 1) / layers
        angle_step = 2 * math.pi / petals

        for petal in range(petals):
            angle = petal * angle_step
            x = center[0] + layer_radius * math.cos(angle)
            y = center[1] + layer_radius * math.sin(angle)
            patterns.append({'center': (x, y), 'radius': layer_radius / 4})

    return patterns
```

#### **9.3 Platonic Solid Projections**
```python
def project_platonic_solid(solid_type, size=100):
    # 2D projections of 3D Platonic solids
    if solid_type == 'tetrahedron':
        return generate_tetrahedron_projection(size)
    elif solid_type == 'cube':
        return generate_cube_projection(size)
    # ... other solids
```

### **Libraries Required**
- `math` (built-in)
- `matplotlib` (for rendering)
- `PIL/Pillow` (for image generation)
- `cairo` (for vector graphics)

### **Output Structure**
```python
class SacredGeometryOutput:
    geometry_type: str
    svg_data: str
    png_data: bytes
    mathematical_properties: Dict
    symbolic_meaning: str
```

---

## 🖋️ **10. SIGIL FORGE SYNTHESIZER**

### **Input Parameters**
```python
class SigilInput:
    intention: str
    style: str = 'traditional'  # 'traditional', 'modern', 'geometric'
    complexity: str = 'medium'
    personal_symbols: List[str] = None
```

### **Core Calculations**

#### **10.1 Letter Elimination Method**
```python
def create_sigil_traditional(intention):
    # Remove vowels and duplicate letters
    consonants = []
    seen = set()

    for char in intention.upper():
        if char.isalpha() and char not in 'AEIOU' and char not in seen:
            consonants.append(char)
            seen.add(char)

    return consonants
```

#### **10.2 Symbol Combination**
```python
def combine_letters_to_sigil(letters):
    # Simplified approach: create geometric combinations
    base_shapes = {
        'B': 'vertical_line_with_bumps',
        'C': 'arc',
        'D': 'vertical_line_with_arc',
        # ... mapping for all letters
    }

    combined_elements = []
    for letter in letters:
        if letter in base_shapes:
            combined_elements.append(base_shapes[letter])

    return optimize_sigil_design(combined_elements)
```

#### **10.3 Aesthetic Optimization**
```python
def optimize_sigil_design(elements):
    # Balance, symmetry, and flow optimization
    optimized = {
        'elements': elements,
        'balance_point': calculate_visual_center(elements),
        'symmetry_score': calculate_symmetry(elements),
        'flow_paths': trace_visual_flow(elements)
    }

    return optimized
```

### **Libraries Required**
- `PIL/Pillow` (image generation)
- `cairo` (vector graphics)
- `svglib` (SVG manipulation)

### **Output Structure**
```python
class SigilOutput:
    svg_data: str
    png_data: bytes
    creation_method: str
    symbolic_elements: List[str]
    activation_guidance: str
```

---

## 🔧 **SHARED INFRASTRUCTURE REQUIREMENTS**

### **Common Data Models**
```python
from pydantic import BaseModel
from datetime import date, time
from typing import Optional, List, Dict, Tuple, Any

class BaseEngineInput(BaseModel):
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    timestamp: Optional[date] = None

class BaseEngineOutput(BaseModel):
    engine_name: str
    calculation_time: float
    confidence_score: float
    raw_data: Dict[str, Any]
    formatted_output: str
    recommendations: List[str]
```

### **Required Python Libraries**
```bash
# Core dependencies
pip install pydantic pytz

# Astronomical calculations
pip install pyswisseph

# Mathematical and visualization
pip install numpy matplotlib

# Image generation
pip install pillow cairo-python

# Optional for advanced features
pip install svglib reportlab
```

### **Data Storage Structure**
```
ENGINES/data/
├── tarot/
│   ├── rider_waite.json
│   ├── thoth.json
│   └── marseille.json
├── iching/
│   ├── hexagrams.json
│   └── trigrams.json
├── gene_keys/
│   ├── archetypes.json
│   └── sequences.json
├── human_design/
│   ├── gates.json
│   ├── centers.json
│   └── channels.json
├── astrology/
│   ├── nakshatras.json
│   └── dasha_periods.json
└── sacred_geometry/
    ├── templates.json
    └── symbols.json
```

---

*Technical Specifications Complete*
*Ready for Phase 1 Implementation*
