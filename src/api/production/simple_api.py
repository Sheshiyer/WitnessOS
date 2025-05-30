#!/usr/bin/env python3
"""
Simple WitnessOS API for testing the AI agent

A minimal FastAPI server that provides basic calculation endpoints
without complex engine dependencies.
"""

import os
import sys
import json
from datetime import datetime, date
from typing import Dict, Any, Optional
from pathlib import Path

# Add ENGINES directory to path
engines_dir = Path(__file__).parent.parent
sys.path.insert(0, str(engines_dir))

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    import uvicorn
except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
    print("📦 Please install: pip install fastapi uvicorn[standard]")
    sys.exit(1)

app = FastAPI(
    title="WitnessOS Divination Engines API",
    description="Consciousness calculation and interpretation API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input models
class BirthData(BaseModel):
    name: str
    date: str  # YYYY-MM-DD format
    time: Optional[str] = None  # HH:MM format
    location: Optional[str] = None
    timezone: Optional[str] = None

class NumerologyRequest(BaseModel):
    birth_data: BirthData
    system: str = "pythagorean"
    current_year: Optional[int] = None

class BiorhythmRequest(BaseModel):
    birth_data: BirthData
    target_date: Optional[str] = None

class HumanDesignRequest(BaseModel):
    birth_data: BirthData
    include_design_calculation: bool = True
    detailed_gates: bool = True

class TarotRequest(BaseModel):
    question: str
    spread_type: str = "three_card"  # single_card, three_card, celtic_cross
    deck_type: str = "rider_waite"
    focus_area: Optional[str] = None

class IChingRequest(BaseModel):
    question: str
    method: str = "coins"  # coins, yarrow, random
    focus_area: Optional[str] = None

# Simple calculation functions
def calculate_life_path(birth_date: str) -> int:
    """Simple life path calculation"""
    # Parse date and sum digits
    date_parts = birth_date.replace("-", "")
    total = sum(int(digit) for digit in date_parts)
    
    # Reduce to single digit (except master numbers)
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(digit) for digit in str(total))
    
    return total

def calculate_expression_number(name: str) -> int:
    """Simple expression number calculation"""
    # Pythagorean values
    values = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
        'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
        'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
    }
    
    total = sum(values.get(char.upper(), 0) for char in name if char.isalpha())
    
    # Reduce to single digit (except master numbers)
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(digit) for digit in str(total))
    
    return total

def calculate_biorhythm_cycles(birth_date: str, target_date: str = None) -> Dict[str, float]:
    """Simple biorhythm calculation"""
    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")
    
    # Parse dates
    birth = datetime.strptime(birth_date, "%Y-%m-%d")
    target = datetime.strptime(target_date, "%Y-%m-%d")
    
    # Calculate days since birth
    days = (target - birth).days
    
    # Calculate cycles (simplified)
    import math
    physical = math.sin(2 * math.pi * days / 23)
    emotional = math.sin(2 * math.pi * days / 28)
    intellectual = math.sin(2 * math.pi * days / 33)
    
    return {
        "physical": round(physical * 100, 2),
        "emotional": round(emotional * 100, 2),
        "intellectual": round(intellectual * 100, 2),
        "days_since_birth": days
    }

def calculate_human_design_mock(birth_data: BirthData) -> Dict[str, Any]:
    """Mock Human Design calculation"""
    import random
    random.seed(hash(birth_data.name + birth_data.date))

    types = ["Generator", "Manifesting Generator", "Projector", "Manifestor", "Reflector"]
    authorities = ["Sacral", "Emotional", "Splenic", "Ego", "Self-Projected", "Mental", "Lunar"]
    profiles = ["1/3", "1/4", "2/4", "2/5", "3/5", "3/6", "4/6", "4/1", "5/1", "5/2", "6/2", "6/3"]

    hd_type = random.choice(types)
    authority = random.choice(authorities)
    profile = random.choice(profiles)

    return {
        "type": hd_type,
        "strategy": "To Respond" if "Generator" in hd_type else "To Wait for Invitation",
        "authority": authority,
        "profile": profile,
        "definition": random.choice(["Single", "Split", "Triple Split", "Quadruple Split"]),
        "incarnation_cross": f"Right Angle Cross of {random.choice(['Explanation', 'Service', 'Consciousness', 'Planning'])}"
    }

def calculate_tarot_mock(question: str, spread_type: str) -> Dict[str, Any]:
    """Mock Tarot reading"""
    import random
    random.seed(hash(question))

    major_arcana = [
        "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
        "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
        "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
        "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"
    ]

    if spread_type == "single_card":
        cards = [random.choice(major_arcana)]
        positions = ["Present Situation"]
    elif spread_type == "three_card":
        cards = random.sample(major_arcana, 3)
        positions = ["Past", "Present", "Future"]
    else:  # celtic_cross
        cards = random.sample(major_arcana, 10)
        positions = ["Present", "Challenge", "Past", "Future", "Crown", "Foundation",
                    "Recent Past", "Approach", "External", "Outcome"]

    reading = []
    for i, (card, position) in enumerate(zip(cards, positions)):
        reading.append({
            "position": position,
            "card": card,
            "reversed": random.choice([True, False]),
            "interpretation": f"The {card} in the {position} position suggests transformation and growth."
        })

    return {
        "spread_type": spread_type,
        "cards_drawn": len(cards),
        "reading": reading
    }

def calculate_iching_mock(question: str, method: str) -> Dict[str, Any]:
    """Mock I-Ching reading"""
    import random
    random.seed(hash(question))

    hexagram_names = [
        "The Creative", "The Receptive", "Difficulty at the Beginning", "Youthful Folly",
        "Waiting", "Conflict", "The Army", "Holding Together", "Small Taming",
        "Treading", "Peace", "Standstill", "Fellowship", "Great Possession",
        "Modesty", "Enthusiasm", "Following", "Work on the Decayed", "Approach",
        "Contemplation", "Biting Through", "Grace", "Splitting Apart", "Return"
    ]

    primary_hex = random.randint(1, 64)
    primary_name = random.choice(hexagram_names)

    # Generate changing lines
    changing_lines = []
    if random.choice([True, False]):  # 50% chance of changing lines
        changing_lines = random.sample(range(1, 7), random.randint(1, 3))

    result = {
        "method": method,
        "primary_hexagram": {
            "number": primary_hex,
            "name": primary_name,
            "judgment": f"The {primary_name} brings clarity to your question about change and transformation.",
            "image": f"The image of {primary_name} suggests patience and wisdom in your current situation."
        },
        "changing_lines": changing_lines
    }

    if changing_lines:
        mutation_hex = random.randint(1, 64)
        mutation_name = random.choice(hexagram_names)
        result["mutation_hexagram"] = {
            "number": mutation_hex,
            "name": mutation_name,
            "guidance": f"The transformation leads to {mutation_name}, indicating new possibilities."
        }

    return result

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "WitnessOS Divination Engines API",
        "version": "1.0.0",
        "status": "active",
        "available_engines": ["numerology", "biorhythm", "human_design", "tarot", "iching"],
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "engines_available": ["numerology", "biorhythm", "human_design", "tarot", "iching"]
    }

@app.post("/calculate/numerology")
async def calculate_numerology(request: NumerologyRequest):
    """Calculate numerology profile"""
    try:
        birth_data = request.birth_data
        
        # Basic calculations
        life_path = calculate_life_path(birth_data.date)
        expression = calculate_expression_number(birth_data.name)
        
        # Mock additional numbers for completeness
        soul_urge = (expression + 2) % 9 + 1
        personality = (expression + 4) % 9 + 1
        
        current_year = request.current_year or datetime.now().year
        personal_year = (life_path + sum(int(d) for d in str(current_year))) % 9 + 1
        
        result = {
            "engine": "numerology",
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "input": {
                "name": birth_data.name,
                "birth_date": birth_data.date,
                "system": request.system
            },
            "core_numbers": {
                "life_path": life_path,
                "expression": expression,
                "soul_urge": soul_urge,
                "personality": personality
            },
            "personal_year": personal_year,
            "master_numbers": [n for n in [life_path, expression, soul_urge, personality] if n in [11, 22, 33]],
            "interpretation": f"Life Path {life_path} indicates a soul journey focused on mastering the archetypal frequency of {life_path}. Your expression number {expression} shows how your essence manifests in the world.",
            "recommendations": [
                f"Meditate on your Life Path number {life_path}",
                "Practice aligning your actions with your soul's purpose",
                f"This year (Personal Year {personal_year}) focus on growth and development"
            ]
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

@app.post("/calculate/biorhythm")
async def calculate_biorhythm(request: BiorhythmRequest):
    """Calculate biorhythm cycles"""
    try:
        birth_data = request.birth_data
        target_date = request.target_date or datetime.now().strftime("%Y-%m-%d")
        
        cycles = calculate_biorhythm_cycles(birth_data.date, target_date)
        
        result = {
            "engine": "biorhythm",
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "input": {
                "name": birth_data.name,
                "birth_date": birth_data.date,
                "target_date": target_date
            },
            "cycles": cycles,
            "interpretation": f"Your biorhythm cycles show: Physical at {cycles['physical']}%, Emotional at {cycles['emotional']}%, Intellectual at {cycles['intellectual']}%. These represent your natural energy fluctuations.",
            "recommendations": [
                "Align important activities with your high-energy cycles",
                "Use low-energy periods for rest and reflection",
                "Track patterns over time to optimize your schedule"
            ]
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

@app.post("/calculate/human_design")
async def calculate_human_design(request: HumanDesignRequest):
    """Calculate Human Design chart"""
    try:
        birth_data = request.birth_data

        # Validate required fields for Human Design
        if not birth_data.time:
            raise HTTPException(status_code=400, detail="Birth time is required for Human Design calculations")
        if not birth_data.location:
            raise HTTPException(status_code=400, detail="Birth location is required for Human Design calculations")

        hd_data = calculate_human_design_mock(birth_data)

        result = {
            "engine": "human_design",
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "input": {
                "name": birth_data.name,
                "birth_date": birth_data.date,
                "birth_time": birth_data.time,
                "birth_location": birth_data.location
            },
            "chart": hd_data,
            "interpretation": f"You are a {hd_data['type']} with {hd_data['authority']} authority. Your strategy is '{hd_data['strategy']}' and your profile is {hd_data['profile']}.",
            "recommendations": [
                f"Honor your {hd_data['type']} strategy: {hd_data['strategy']}",
                f"Trust your {hd_data['authority']} authority for decision-making",
                "Experiment with your design for 7 years to embody your true nature"
            ]
        }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

@app.post("/calculate/tarot")
async def calculate_tarot(request: TarotRequest):
    """Perform Tarot reading"""
    try:
        tarot_data = calculate_tarot_mock(request.question, request.spread_type)

        result = {
            "engine": "tarot",
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "input": {
                "question": request.question,
                "spread_type": request.spread_type,
                "deck_type": request.deck_type,
                "focus_area": request.focus_area
            },
            "reading": tarot_data,
            "interpretation": f"Your {request.spread_type} reading reveals important insights about your question. The cards suggest a journey of transformation and growth.",
            "recommendations": [
                "Reflect on the symbolism of each card in relation to your question",
                "Consider how the card positions relate to your current situation",
                "Trust your intuition when interpreting the messages"
            ]
        }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

@app.post("/calculate/iching")
async def calculate_iching(request: IChingRequest):
    """Perform I-Ching consultation"""
    try:
        iching_data = calculate_iching_mock(request.question, request.method)

        result = {
            "engine": "iching",
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "input": {
                "question": request.question,
                "method": request.method,
                "focus_area": request.focus_area
            },
            "consultation": iching_data,
            "interpretation": f"The I-Ching reveals {iching_data['primary_hexagram']['name']} as guidance for your question. This hexagram speaks to the nature of change and transformation in your situation.",
            "recommendations": [
                "Meditate on the hexagram's imagery and meaning",
                "Consider how the changing lines (if any) apply to your situation",
                "Embrace the wisdom of ancient Chinese philosophy in your decision-making"
            ]
        }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")

@app.get("/engines")
async def list_engines():
    """List available calculation engines"""
    return {
        "available_engines": [
            {
                "name": "numerology",
                "description": "Soul-number matrix extraction and vibrational signature analysis",
                "endpoint": "/calculate/numerology"
            },
            {
                "name": "biorhythm",
                "description": "Natural energy cycle analysis and optimization",
                "endpoint": "/calculate/biorhythm"
            },
            {
                "name": "human_design",
                "description": "Complete Human Design chart analysis with type, strategy, and authority",
                "endpoint": "/calculate/human_design"
            },
            {
                "name": "tarot",
                "description": "Archetypal guidance through traditional tarot card spreads",
                "endpoint": "/calculate/tarot"
            },
            {
                "name": "iching",
                "description": "Ancient Chinese wisdom through hexagram consultation",
                "endpoint": "/calculate/iching"
            }
        ]
    }

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple WitnessOS API Server")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8001, help="Port to run on")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    
    args = parser.parse_args()
    
    print(f"🌟 Starting WitnessOS Simple API")
    print(f"🌐 Server: http://{args.host}:{args.port}")
    print(f"📚 Documentation: http://{args.host}:{args.port}/docs")
    
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=args.reload
    )
