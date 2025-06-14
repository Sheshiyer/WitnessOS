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
                              timezone_str: Optional[str] = None,
                              sidereal: bool = False) -> Dict[str, Dict[str, float]]:
        """
        Calculate planetary positions for given time and location.

        Args:
            birth_datetime: Birth date and time
            latitude: Birth latitude
            longitude: Birth longitude
            timezone_str: Timezone string
            sidereal: If True, use sidereal zodiac (Vedic), else tropical (Western)

        Returns:
            Dictionary with planetary positions (longitude, latitude, distance)
        """
        julian_day = self._datetime_to_julian(birth_datetime, timezone_str)

        # Set ayanamsa for sidereal calculations (Vedic astrology)
        if sidereal:
            # Use Lahiri ayanamsa (most common in Vedic astrology)
            swe.set_sid_mode(swe.SIDM_LAHIRI)

        positions = {}

        # Calculate core planets
        for planet_name, planet_id in PLANETS.items():
            try:
                # Calculate geocentric position
                if sidereal:
                    pos, ret_flag = swe.calc_ut(julian_day, planet_id, swe.FLG_SIDEREAL)
                else:
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
                if sidereal:
                    pos, ret_flag = swe.calc_ut(julian_day, planet_id, swe.FLG_SIDEREAL)
                else:
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
        Convert astronomical longitude to Human Design gate number using the official sequence.

        Args:
            longitude: Longitude in degrees (0-360)

        Returns:
            Gate number (1-64)
        """
        # Apply the 46-degree offset used in the official Human Design system
        # This aligns our astronomical coordinates with the Human Design wheel
        adjusted_longitude = (longitude + 46.0) % 360

        # Each gate covers 360/64 = 5.625 degrees
        gate_size = 360.0 / 64.0

        # Calculate position in the official Human Design gate sequence
        position = int(adjusted_longitude / gate_size)
        position = min(position, 63)  # Ensure we don't exceed bounds

        # Official Human Design gate sequence (based on Godhead structure)
        gate_sequence = self._get_official_gate_sequence()

        return gate_sequence[position]

    def _get_official_gate_sequence(self) -> list:
        """
        Get the official Human Design gate sequence based on the Godhead structure.

        Returns:
            List of 64 gates in the correct Human Design sequence
        """
        # Quarter of Initiation - Purpose fulfilled through Mind
        quarter_initiation = [
            [13, 49, 30, 55],  # Kali - The Destroyer of False Devotion
            [37, 63, 22, 36],  # Mitra - The Evolution of Consciousness
            [25, 17, 21, 51],  # Michael - The Angelical Mind
            [42, 3, 27, 24]    # Janus - The Fertility of Mind
        ]

        # Quarter of Civilization - Purpose fulfilled through Form
        quarter_civilization = [
            [2, 23, 8, 20],    # Maia - The Mother Goddess
            [16, 35, 45, 12],  # Lakshmi - Goddess of Beauty and Good Fortune
            [15, 52, 39, 53],  # Parvati - Goddess of Domestic Bliss
            [62, 56, 31, 33]   # Ma'at - Goddess of Truth, Justice and Cosmic Harmony
        ]

        # Quarter of Duality - Purpose fulfilled through Bonding
        quarter_duality = [
            [7, 4, 29, 59],    # Thoth - God of Wisdom, Writing and Time
            [40, 64, 47, 6],   # Harmonia - Goddess of the Family Bond
            [46, 18, 48, 57],  # Christ Consciousness Field - "Love Thy Neighbor"
            [44, 28, 50, 32]   # Minerva - Virgin Goddess of Warfare, Arts and Crafts
        ]

        # Quarter of Mutation - Purpose fulfilled through Transformation
        quarter_mutation = [
            [1, 43, 14, 34],   # Hades - God of the Underworld
            [9, 5, 26, 11],    # Prometheus - Thief of Fire and Benefactor of Humanity
            [10, 58, 38, 54],  # Vishnu - God of Monotheism
            [60, 61, 41, 19]   # The Keepers of the Wheel - Guardians of the Wheel
        ]

        # Combine all quarters in the correct sequence
        all_quarters = [
            quarter_initiation,
            quarter_civilization,
            quarter_duality,
            quarter_mutation
        ]

        # Create flat sequence of gates
        gate_sequence = []
        for quarter in all_quarters:
            for godhead in quarter:
                gate_sequence.extend(godhead)

        return gate_sequence

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

    def _calculate_design_time_solar_arc(self, birth_datetime: datetime,
                                       timezone_str: Optional[str] = None) -> datetime:
        """
        Calculate the design time using 88 degrees of solar arc (official Human Design method).

        This method finds the exact time when the Sun was 88 degrees earlier in its orbit,
        which is the official Human Design calculation method as established by Ra Uru Hu.

        Args:
            birth_datetime: Birth date and time
            timezone_str: Timezone string

        Returns:
            Design datetime (88 degrees of solar arc before birth)
        """
        # Convert birth time to Julian Day for Swiss Ephemeris
        birth_jd = self._datetime_to_julian(birth_datetime, timezone_str)

        # Get Sun position at birth
        birth_sun_pos, _ = swe.calc_ut(birth_jd, swe.SUN)
        birth_sun_longitude = birth_sun_pos[0]

        # Calculate target Sun longitude (88 degrees earlier)
        target_sun_longitude = (birth_sun_longitude - 88.0) % 360

        # Find the time when Sun was at target longitude
        # Start search approximately 88 days before birth
        search_start_jd = birth_jd - 100  # Start 100 days before to be safe
        search_end_jd = birth_jd - 80     # End 80 days before to be safe

        design_jd = self._find_sun_longitude_time(target_sun_longitude, search_start_jd, search_end_jd)

        if design_jd is None:
            # Fallback to 88 days if solar arc calculation fails
            from datetime import timedelta
            return birth_datetime - timedelta(days=88)

        # Convert Julian Day back to datetime
        year, month, day, hour = swe.revjul(design_jd)
        hour_int = int(hour)
        minute = int((hour - hour_int) * 60)
        second = int(((hour - hour_int) * 60 - minute) * 60)

        design_datetime = datetime(year, month, day, hour_int, minute, second)

        # Apply timezone if specified
        if timezone_str:
            utc_dt = pytz.UTC.localize(design_datetime)
            tz = pytz.timezone(timezone_str)
            design_datetime = utc_dt.astimezone(tz).replace(tzinfo=None)

        return design_datetime

    def _find_sun_longitude_time(self, target_longitude: float, start_jd: float, end_jd: float) -> Optional[float]:
        """
        Find the Julian Day when the Sun was at a specific longitude using binary search.

        Args:
            target_longitude: Target Sun longitude in degrees (0-360)
            start_jd: Start of search range (Julian Day)
            end_jd: End of search range (Julian Day)

        Returns:
            Julian Day when Sun was at target longitude, or None if not found
        """
        tolerance = 0.001  # Tolerance in degrees (about 1.4 minutes of time)
        max_iterations = 50

        for _ in range(max_iterations):
            mid_jd = (start_jd + end_jd) / 2

            # Get Sun position at midpoint
            sun_pos, _ = swe.calc_ut(mid_jd, swe.SUN)
            current_longitude = sun_pos[0]

            # Calculate difference, handling 360-degree wrap
            diff = (target_longitude - current_longitude + 180) % 360 - 180

            if abs(diff) < tolerance:
                return mid_jd

            # Adjust search range
            if diff > 0:
                start_jd = mid_jd
            else:
                end_jd = mid_jd

            # Prevent infinite loop
            if abs(end_jd - start_jd) < 0.0001:  # Less than ~8 seconds
                break

        return None

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

        # Calculate Design time using 88 degrees of solar arc (official Human Design method)
        design_datetime = self._calculate_design_time_solar_arc(birth_datetime, timezone_str)

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

        # Calculate Earth gates (opposite of Sun)
        if 'sun' in personality_positions:
            earth_longitude_personality = (personality_positions['sun']['longitude'] + 180) % 360
            earth_longitude_design = (design_positions['sun']['longitude'] + 180) % 360

            personality_gates['earth'] = self.longitude_to_human_design_gate(earth_longitude_personality)
            design_gates['earth'] = self.longitude_to_human_design_gate(earth_longitude_design)

        # Calculate solar arc details for verification
        solar_arc_details = None
        if 'sun' in personality_positions and 'sun' in design_positions:
            personality_sun_lon = personality_positions['sun']['longitude']
            design_sun_lon = design_positions['sun']['longitude']
            solar_arc_difference = (personality_sun_lon - design_sun_lon + 360) % 360

            solar_arc_details = {
                'personality_sun_longitude': f"{personality_sun_lon:.3f}°",
                'design_sun_longitude': f"{design_sun_lon:.3f}°",
                'solar_arc_difference': f"{solar_arc_difference:.1f}°",
                'design_date': design_datetime.strftime('%Y-%m-%d %H:%M UTC') if design_datetime else None
            }

        return {
            'personality_gates': personality_gates,
            'design_gates': design_gates,
            'personality_positions': personality_positions,
            'design_positions': design_positions,
            'design_datetime': design_datetime,
            'solar_arc_details': solar_arc_details
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
            birth_datetime, latitude, longitude, timezone_str, sidereal=True
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
