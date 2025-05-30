"""
Astronomical calculations using Swiss Ephemeris for WitnessOS Divination Engines

Provides core astronomical calculation functions for Human Design, Vedic Astrology,
and other systems requiring precise planetary positions.
"""

import swisseph as swe
from datetime import datetime, date, time, timedelta
from typing import Dict, List, Tuple, Optional, Any
import pytz
from base.data_models import ValidationError


# Swiss Ephemeris planet constants
PLANETS = {
    'sun': swe.SUN,
    'moon': swe.MOON,
    'mercury': swe.MERCURY,
    'venus': swe.VENUS,
    'mars': swe.MARS,
    'jupiter': swe.JUPITER,
    'saturn': swe.SATURN,
    'uranus': swe.URANUS,
    'neptune': swe.NEPTUNE,
    'pluto': swe.PLUTO,
    'north_node': swe.MEAN_NODE,
    'south_node': swe.MEAN_NODE,  # Will calculate opposite
}

# Optional planets that require additional ephemeris files
OPTIONAL_PLANETS = {
    'chiron': swe.CHIRON
}

# Vedic Nakshatras (27 lunar mansions)
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
    "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
    "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

# Human Design Gates (I-Ching hexagrams)
HUMAN_DESIGN_GATES = {
    i: f"Gate {i}" for i in range(1, 65)
}


class AstrologyCalculator:
    """Core astronomical calculation engine using Swiss Ephemeris."""

    def __init__(self):
        """Initialize the calculator with Swiss Ephemeris."""
        # Set ephemeris path (uses built-in data)
        swe.set_ephe_path('')

    def _datetime_to_julian(self, dt: datetime, timezone_str: Optional[str] = None) -> float:
        """
        Convert datetime to Julian Day Number for Swiss Ephemeris.

        Args:
            dt: Datetime object
            timezone_str: Timezone string (e.g., 'America/New_York')

        Returns:
            Julian Day Number
        """
        if timezone_str:
            tz = pytz.timezone(timezone_str)
            if dt.tzinfo is None:
                dt = tz.localize(dt)
            else:
                dt = dt.astimezone(tz)

        # Convert to UTC for Swiss Ephemeris
        if dt.tzinfo is not None:
            dt = dt.astimezone(pytz.UTC)

        # Swiss Ephemeris expects Gregorian calendar
        julian_day = swe.julday(dt.year, dt.month, dt.day,
                               dt.hour + dt.minute/60.0 + dt.second/3600.0)

        return julian_day

    def get_planetary_positions(self, birth_datetime: datetime,
                              latitude: float, longitude: float,
                              timezone_str: Optional[str] = None) -> Dict[str, Dict[str, float]]:
        """
        Calculate planetary positions for given time and location.

        Args:
            birth_datetime: Birth date and time
            latitude: Birth latitude
            longitude: Birth longitude
            timezone_str: Timezone string

        Returns:
            Dictionary with planetary positions (longitude, latitude, distance)
        """
        julian_day = self._datetime_to_julian(birth_datetime, timezone_str)

        positions = {}

        # Calculate core planets
        for planet_name, planet_id in PLANETS.items():
            try:
                # Calculate geocentric position
                pos, ret_flag = swe.calc_ut(julian_day, planet_id)

                # Handle South Node (opposite of North Node)
                if planet_name == 'south_node':
                    pos = list(pos)  # Convert tuple to list for modification
                    pos[0] = (pos[0] + 180) % 360

                positions[planet_name] = {
                    'longitude': pos[0],
                    'latitude': pos[1],
                    'distance': pos[2],
                    'longitude_speed': pos[3] if len(pos) > 3 else 0,
                    'latitude_speed': pos[4] if len(pos) > 4 else 0
                }

            except Exception as e:
                raise ValidationError(f"Failed to calculate {planet_name} position: {str(e)}")

        # Try to calculate optional planets (skip if ephemeris files missing)
        for planet_name, planet_id in OPTIONAL_PLANETS.items():
            try:
                pos, ret_flag = swe.calc_ut(julian_day, planet_id)
                positions[planet_name] = {
                    'longitude': pos[0],
                    'latitude': pos[1],
                    'distance': pos[2],
                    'longitude_speed': pos[3] if len(pos) > 3 else 0,
                    'latitude_speed': pos[4] if len(pos) > 4 else 0
                }
            except Exception:
                # Skip optional planets if ephemeris data not available
                pass

        return positions

    def longitude_to_human_design_gate(self, longitude: float) -> int:
        """
        Convert astronomical longitude to Human Design gate number.

        Args:
            longitude: Longitude in degrees (0-360)

        Returns:
            Gate number (1-64)
        """
        # Human Design uses 64 gates mapped to 360 degrees
        # Each gate covers 360/64 = 5.625 degrees
        gate_size = 360.0 / 64.0
        gate_number = int((longitude / gate_size) % 64) + 1

        return gate_number

    def longitude_to_nakshatra(self, longitude: float) -> Tuple[str, int, float]:
        """
        Convert Moon longitude to Vedic nakshatra.

        Args:
            longitude: Moon longitude in degrees

        Returns:
            Tuple of (nakshatra_name, pada_number, degrees_in_nakshatra)
        """
        # Each nakshatra covers 360/27 = 13.333... degrees
        nakshatra_size = 360.0 / 27.0

        # Calculate nakshatra index
        nakshatra_index = int(longitude / nakshatra_size)
        nakshatra_name = NAKSHATRAS[nakshatra_index]

        # Calculate position within nakshatra
        degrees_in_nakshatra = longitude % nakshatra_size

        # Calculate pada (quarter) - each nakshatra has 4 padas
        pada_number = int(degrees_in_nakshatra / (nakshatra_size / 4)) + 1

        return nakshatra_name, pada_number, degrees_in_nakshatra

    def calculate_human_design_data(self, birth_datetime: datetime,
                                  latitude: float, longitude: float,
                                  timezone_str: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculate Human Design specific astronomical data.

        Args:
            birth_datetime: Birth date and time
            latitude: Birth latitude
            longitude: Birth longitude
            timezone_str: Timezone string

        Returns:
            Dictionary with Human Design calculation data
        """
        # Get planetary positions for birth time (Personality)
        personality_positions = self.get_planetary_positions(
            birth_datetime, latitude, longitude, timezone_str
        )

        # Calculate Design time (88 days before birth)
        design_datetime = birth_datetime - timedelta(days=88)

        # Get planetary positions for design time
        design_positions = self.get_planetary_positions(
            design_datetime, latitude, longitude, timezone_str
        )

        # Convert to Human Design gates
        personality_gates = {}
        design_gates = {}

        for planet in ['sun', 'moon', 'mercury', 'venus', 'mars',
                      'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']:
            if planet in personality_positions:
                personality_gates[planet] = self.longitude_to_human_design_gate(
                    personality_positions[planet]['longitude']
                )
                design_gates[planet] = self.longitude_to_human_design_gate(
                    design_positions[planet]['longitude']
                )

        return {
            'personality_gates': personality_gates,
            'design_gates': design_gates,
            'personality_positions': personality_positions,
            'design_positions': design_positions,
            'design_datetime': design_datetime
        }

    def calculate_vedic_data(self, birth_datetime: datetime,
                           latitude: float, longitude: float,
                           timezone_str: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculate Vedic astrology specific data.

        Args:
            birth_datetime: Birth date and time
            latitude: Birth latitude
            longitude: Birth longitude
            timezone_str: Timezone string

        Returns:
            Dictionary with Vedic astrology data
        """
        positions = self.get_planetary_positions(
            birth_datetime, latitude, longitude, timezone_str
        )

        # Calculate Moon nakshatra
        moon_longitude = positions['moon']['longitude']
        nakshatra_name, pada, degrees_in_nakshatra = self.longitude_to_nakshatra(moon_longitude)

        return {
            'planetary_positions': positions,
            'moon_nakshatra': {
                'name': nakshatra_name,
                'pada': pada,
                'degrees_in_nakshatra': degrees_in_nakshatra,
                'longitude': moon_longitude
            }
        }


# Utility functions
def validate_coordinates(latitude: float, longitude: float) -> bool:
    """Validate geographic coordinates."""
    if not (-90 <= latitude <= 90):
        raise ValidationError(f"Latitude {latitude} must be between -90 and 90")
    if not (-180 <= longitude <= 180):
        raise ValidationError(f"Longitude {longitude} must be between -180 and 180")
    return True


def validate_datetime(dt: datetime) -> bool:
    """Validate datetime for astronomical calculations."""
    # Swiss Ephemeris works from 13000 BCE to 17000 CE
    if dt.year < -13000 or dt.year > 17000:
        raise ValidationError(f"Year {dt.year} is outside Swiss Ephemeris range (-13000 to 17000)")
    return True
