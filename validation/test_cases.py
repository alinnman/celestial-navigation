"""
Extended Test Cases for NOVAS Validation
========================================

Additional comprehensive test scenarios for validating celestial navigation
algorithms across diverse global conditions and star combinations.

© August Linnman, 2025, email: august@linnman.net
MIT License
"""

from datetime import datetime
from novas_validation import ValidationTestCase

def create_extended_test_cases():
    """Create comprehensive validation test cases covering global scenarios"""
    test_cases = []
    
    # Original high-accuracy test case - Baltic Sea
    test_cases.append(ValidationTestCase(
        name="Baltic Sea Precision",
        location=(59.444, 19.502),
        datetime_utc=datetime(2025, 4, 19, 1, 44, 43),
        stars=['vega', 'arcturus', 'capella'],
        description="High-precision reference case with known accurate results"
    ))
    
    # Arctic navigation - High latitude challenges
    test_cases.append(ValidationTestCase(
        name="Arctic Navigation",
        location=(75.0, 0.0),
        datetime_utc=datetime(2025, 7, 1, 12, 0, 0),
        stars=['vega', 'arcturus', 'capella'],
        description="High latitude Arctic navigation with challenging star geometry"
    ))
    
    # Equatorial crossing - Different star visibility
    test_cases.append(ValidationTestCase(
        name="Equatorial Crossing",
        location=(0.0, -25.0),
        datetime_utc=datetime(2025, 6, 15, 2, 30, 0),
        stars=['vega', 'arcturus', 'capella'],
        description="Equatorial navigation with optimal star visibility"
    ))
    
    # Southern hemisphere - Different star patterns
    test_cases.append(ValidationTestCase(
        name="Southern Ocean",
        location=(-40.0, 50.0),
        datetime_utc=datetime(2025, 8, 20, 22, 15, 0),
        stars=['vega', 'arcturus', 'capella'],
        description="Southern hemisphere navigation"
    ))
    
    # Pacific crossing - Classic blue water scenario
    test_cases.append(ValidationTestCase(
        name="Pacific Crossing",
        location=(20.0, -155.0),
        datetime_utc=datetime(2025, 9, 10, 4, 0, 0),
        stars=['vega', 'arcturus', 'capella'],
        description="Pacific Ocean crossing - classic blue water navigation"
    ))
    
    # Mediterranean - Coastal navigation
    test_cases.append(ValidationTestCase(
        name="Mediterranean Coastal",
        location=(35.0, 18.0),
        datetime_utc=datetime(2025, 5, 10, 21, 30, 0),
        stars=['vega', 'arcturus'],
        description="Two-star fix for coastal navigation"
    ))
    
    # North Atlantic - Transatlantic crossing
    test_cases.append(ValidationTestCase(
        name="North Atlantic Crossing",
        location=(40.0, -30.0),
        datetime_utc=datetime(2025, 3, 21, 20, 15, 30),
        stars=['vega', 'arcturus', 'capella'],
        description="Mid-latitude Atlantic crossing scenario"
    ))
    
    # Caribbean - Tropical navigation
    test_cases.append(ValidationTestCase(
        name="Caribbean Navigation",
        location=(18.0, -66.0),
        datetime_utc=datetime(2025, 12, 1, 23, 45, 0),
        stars=['vega', 'arcturus', 'capella'],
        description="Tropical Caribbean navigation"
    ))
    
    # Indian Ocean - Monsoon season navigation
    test_cases.append(ValidationTestCase(
        name="Indian Ocean Route",
        location=(-10.0, 73.0),
        datetime_utc=datetime(2025, 11, 15, 1, 20, 0),
        stars=['vega', 'arcturus', 'capella'],
        description="Indian Ocean navigation during monsoon season"
    ))
    
    # North Pacific - Great circle route
    test_cases.append(ValidationTestCase(
        name="North Pacific Route",
        location=(50.0, 180.0),
        datetime_utc=datetime(2025, 4, 5, 14, 30, 0),
        stars=['vega', 'arcturus', 'capella'],
        description="North Pacific great circle navigation"
    ))
    
    return test_cases

def create_stress_test_cases():
    """Create challenging test cases to stress-test the algorithms"""
    test_cases = []
    
    # Very high latitude - Near pole
    test_cases.append(ValidationTestCase(
        name="Near North Pole",
        location=(85.0, 0.0),
        datetime_utc=datetime(2025, 6, 21, 12, 0, 0),
        stars=['vega', 'arcturus', 'capella'],
        description="Extreme high latitude near North Pole"
    ))
    
    # Date line crossing
    test_cases.append(ValidationTestCase(
        name="Date Line Crossing",
        location=(30.0, 179.0),
        datetime_utc=datetime(2025, 7, 4, 11, 30, 0),
        stars=['vega', 'arcturus', 'capella'],
        description="Navigation across international date line"
    ))
    
    # Prime meridian crossing
    test_cases.append(ValidationTestCase(
        name="Prime Meridian Crossing",
        location=(51.5, 0.0),
        datetime_utc=datetime(2025, 8, 15, 19, 45, 0),
        stars=['vega', 'arcturus', 'capella'],
        description="Navigation across prime meridian (Greenwich)"
    ))
    
    # Southern high latitude
    test_cases.append(ValidationTestCase(
        name="Drake Passage",
        location=(-58.0, -65.0),
        datetime_utc=datetime(2025, 12, 15, 3, 45, 0),
        stars=['vega', 'arcturus', 'capella'],
        description="Southern high latitude - Drake Passage navigation"
    ))
    
    return test_cases

def create_seasonal_test_cases():
    """Create test cases covering seasonal variations"""
    test_cases = []
    
    # Same location, different seasons
    base_location = (45.0, -60.0)  # North Atlantic
    
    # Spring navigation
    test_cases.append(ValidationTestCase(
        name="Spring Navigation",
        location=base_location,
        datetime_utc=datetime(2025, 3, 21, 2, 0, 0),
        stars=['vega', 'arcturus', 'capella'],
        description="Spring equinox navigation - North Atlantic"
    ))
    
    # Summer navigation
    test_cases.append(ValidationTestCase(
        name="Summer Navigation",
        location=base_location,
        datetime_utc=datetime(2025, 6, 21, 2, 0, 0),
        stars=['vega', 'arcturus', 'capella'],
        description="Summer solstice navigation - North Atlantic"
    ))
    
    # Autumn navigation
    test_cases.append(ValidationTestCase(
        name="Autumn Navigation",
        location=base_location,
        datetime_utc=datetime(2025, 9, 23, 2, 0, 0),
        stars=['vega', 'arcturus', 'capella'],
        description="Autumn equinox navigation - North Atlantic"
    ))
    
    # Winter navigation
    test_cases.append(ValidationTestCase(
        name="Winter Navigation",
        location=base_location,
        datetime_utc=datetime(2025, 12, 21, 2, 0, 0),
        stars=['vega', 'arcturus', 'capella'],
        description="Winter solstice navigation - North Atlantic"
    ))
    
    return test_cases

def get_all_test_cases():
    """Get all available test cases"""
    all_cases = []
    all_cases.extend(create_extended_test_cases())
    all_cases.extend(create_stress_test_cases())
    all_cases.extend(create_seasonal_test_cases())
    return all_cases

if __name__ == "__main__":
    # Demo: Print all available test cases
    print("Available Validation Test Cases:")
    print("=" * 50)
    
    all_cases = get_all_test_cases()
    for i, case in enumerate(all_cases, 1):
        print(f"{i:2d}. {case.name}")
        print(f"    Location: {case.location[0]:.1f}°N, {case.location[1]:.1f}°E")
        print(f"    Time: {case.datetime_utc}")
        print(f"    Stars: {', '.join(case.stars)}")
        print(f"    Description: {case.description}")
        print()
    
    print(f"Total test cases available: {len(all_cases)}")
