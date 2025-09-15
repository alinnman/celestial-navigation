"""
Visibility-Aware Random Sight Validation
========================================

Generates randomized test cases with proper star visibility checking.
Only selects stars that are actually visible (altitude > 10°) at the 
specified time and location.

© August Linnman, 2025, email: august@linnman.net
MIT License
"""

from pathlib import Path
import random
from datetime import datetime, timedelta
import json
import sys
from argparse import ArgumentParser
import numpy as np
from novas_validation import ValidationTestCase, NOVASValidator
from novas_star_altitude import get_star_altitude, get_navigation_stars

sys.path.append(str(Path(__file__).parent.parent))
#pylint: disable=C0413
from starfix import Testing

class VisibilityAwareGenerator:
    """Generates random test cases with proper star visibility checking"""

    def __init__(self, seed=42):
        """Initialize with optional random seed for reproducibility"""
        random.seed(seed)
        np.random.seed(seed)

        # Get all available navigation stars
        self.all_stars = list(get_navigation_stars().keys())

        # Minimum altitude for practical navigation (degrees)
        self.min_altitude = 10.0  # Stars below 10° are hard to observe
        self.max_altitude = 85.0  # Stars above 85° are hard to observe (near zenith)

        # Minimum angular separation between stars (degrees)
        self.min_separation = 15.0  # Avoid stars too close together

        print(f"Initialized with {len(self.all_stars)} navigation stars")

    def check_star_visibility(self, star_name, lat, lon, datetime_utc):
        """Check if a star is visible and suitable for navigation"""
        try:
            result = get_star_altitude(star_name, lat, lon, datetime_utc)
            altitude = result['altitude']

            # Check altitude limits
            if altitude < self.min_altitude or altitude > self.max_altitude:
                return False, altitude

            return True, altitude

#pylint: disable=W0718
        except Exception as _:
#pylint: enable=W0718
            # Star calculation failed (maybe below horizon or other issue)
            return False, -999

    def get_visible_stars(self, lat, lon, datetime_utc, max_stars=20):
        """Get all visible stars at given location and time"""
        visible_stars = []

        print(f"  Checking star visibility at {lat:.2f}°N, {lon:.2f}°E on {datetime_utc}...")

        for star_name in self.all_stars:
            is_visible, altitude = self.check_star_visibility(star_name, lat, lon, datetime_utc)

            if is_visible:
                try:
                    # Get azimuth too for separation checking
                    result = get_star_altitude(star_name, lat, lon, datetime_utc)
                    visible_stars.append({
                        'name': star_name,
                        'altitude': altitude,
                        'azimuth': result['azimuth']
                    })
#pylint: disable=W0702
                except:
#pylint: enable=W0702
                    continue  # Skip this star if calculation fails

        # Sort by altitude (higher stars first - generally better for navigation)
        visible_stars.sort(key=lambda x: x['altitude'], reverse=True)

        print(f"    Found {len(visible_stars)} visible stars (Alt > {self.min_altitude}°)")

        # Limit to reasonable number to avoid excessive computation
        return visible_stars[:max_stars]

    def calculate_angular_separation(self, alt1, az1, alt2, az2):
        """Calculate angular separation between two stars (spherical trigonometry)"""
        # Convert to radians
        alt1_r = np.radians(alt1)
        az1_r = np.radians(az1)
        alt2_r = np.radians(alt2)
        az2_r = np.radians(az2)

        # Spherical law of cosines
        cos_sep = (np.sin(alt1_r) * np.sin(alt2_r) +
                   np.cos(alt1_r) * np.cos(alt2_r) * np.cos(az2_r - az1_r))

        # Clamp to avoid numerical errors
        cos_sep = np.clip(cos_sep, -1.0, 1.0)

        separation = np.degrees(np.arccos(cos_sep))
        return separation

    def select_optimal_stars(self, visible_stars, target_count=3):
        """Select optimal star combination for sight reduction"""
        if len(visible_stars) < target_count:
            return [star['name'] for star in visible_stars]

        # Try to find a good combination with adequate separation
        best_combination = None
        best_score = 0

        # Try multiple random combinations
        for _ in range(50):  # Limit attempts to avoid infinite loops
            if len(visible_stars) < target_count:
                break

            # Randomly select stars
            selected = random.sample(visible_stars, target_count)

            # Calculate minimum separation
            min_separation = float('inf')
            total_altitude = 0

#pylint: disable=C0200
            for i in range(len(selected)):
                total_altitude += selected[i]['altitude']
                for j in range(i + 1, len(selected)):
                    sep = self.calculate_angular_separation(
                        selected[i]['altitude'], selected[i]['azimuth'],
                        selected[j]['altitude'], selected[j]['azimuth']
                    )
                    min_separation = min(min_separation, sep)
#pylint: enable=C0200

            # Score: prefer good separation and reasonable total altitude
            if min_separation >= self.min_separation:
                score = min_separation + total_altitude / len(selected)

                if score > best_score:
                    best_score = score
                    best_combination = selected

        # If no good combination found, just take the brightest stars
        if best_combination is None:
            print("    Warning: No optimal combination found, using brightest stars")
            best_combination = visible_stars[:target_count]
        else:
            min_sep = float('inf')
#pylint: disable=C0200
            for i in range(len(best_combination)):
                for j in range(i + 1, len(best_combination)):
                    sep = self.calculate_angular_separation(
                        best_combination[i]['altitude'], best_combination[i]['azimuth'],
                        best_combination[j]['altitude'], best_combination[j]['azimuth']
                    )
                    min_sep = min(min_sep, sep)
#pylint: enable=C0200
            print(f"    Selected {len(best_combination)}"
                  f" stars with {min_sep:.1f}° minimum separation")

        return [star['name'] for star in best_combination]

    def generate_random_location(self, region=None):
        """Generate random geographic location"""
        regions = {
            'arctic': (70, 85),
            'north_temperate': (35, 70),
            'tropical': (-23, 23),
            'south_temperate': (-70, -35),
            'antarctic': (-85, -70)
        }

        if region and region in regions:
            lat_min, lat_max = regions[region]
            lat = random.uniform(lat_min, lat_max)
        else:
            # Global random location (avoid extreme poles)
            lat = random.uniform(-75, 75)

        lon = random.uniform(-180, 180)
        return (lat, lon)

    def generate_random_datetime(self, year=2025):
        """Generate random datetime within a year"""
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)

        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randrange(days_between)

        # Bias toward night hours for better star visibility
        if random.random() < 0.7:  # 70% chance of night hours
            hour_choices = list(range(20, 24)) + list(range(0, 6))  # 8PM to 6AM
        else:
            hour_choices = list(range(6, 20))  # 6AM to 8PM (for polar regions, etc.)

        random_hour = random.choice(hour_choices)
        random_minutes = random.randint(0, 59)
        random_seconds = random.randint(0, 59)

        return start_date + timedelta(days=random_days,
                                    hours=random_hour,
                                    minutes=random_minutes,
                                    seconds=random_seconds)

    def generate_smart_test_case(self, test_id, max_attempts=10):
        """Generate a single random test case with visible stars"""

        for attempt in range(max_attempts):
            print(f"\nGenerating test case {test_id:03d} (attempt {attempt + 1})...")

            # Generate random location and time
            location = self.generate_random_location()
            datetime_utc = self.generate_random_datetime()

            # Find visible stars
            visible_stars = self.get_visible_stars(location[0], location[1], datetime_utc)

            if len(visible_stars) < 2:
                print(f"    Only {len(visible_stars)} visible stars, retrying...")
                continue

            # Select optimal star combination
            target_count = min(random.choice([2, 3, 3, 3, 4]), len(visible_stars))
            # Review
            # target_count = min(random.choice([100]), len(visible_stars))
            selected_stars = self.select_optimal_stars(visible_stars, target_count)

            if len(selected_stars) >= 2:
                # Determine region for description
                lat = location[0]
                if lat > 60:
                    region_desc = "Arctic"
                elif lat > 30:
                    region_desc = "Northern"
                elif lat > -30:
                    region_desc = "Tropical"
                elif lat > -60:
                    region_desc = "Southern"
                else:
                    region_desc = "Antarctic"

                # Create description with star info
                star_alts = []
                for star_name in selected_stars:
                    for vs in visible_stars:
                        if vs['name'] == star_name:
                            star_alts.append(f"{star_name.title()}({vs['altitude']:.0f}°)")
                            break

                description = f"Random {region_desc} navigation: {', '.join(star_alts)}"

                return ValidationTestCase(
                    name=f"Smart_{test_id:03d}_{region_desc}",
                    location=location,
                    datetime_utc=datetime_utc,
                    stars=selected_stars,
                    description=description
                )

        # If all attempts failed
        print(f"    Failed to generate valid test case after {max_attempts} attempts")
        return None

    def generate_smart_test_suite(self, count=50):
        """Generate a suite of smart random test cases"""
        test_cases = []

        print(f"Generating {count} smart random test cases with visible stars...")
        print("=" * 60)

        successful = 0
        for _ in range(count * 2):  # Try up to 2x target count
            if successful >= count:
                break

            test_case = self.generate_smart_test_case(successful + 1)

            if test_case is not None:
                test_cases.append(test_case)
                successful += 1

                if successful % 10 == 0:
                    print(f"\nProgress: {successful}/{count} test cases generated")

        print(f"\n{'='*60}")
        print(f"Successfully generated {len(test_cases)} test cases")
        return test_cases

def run_smart_random_validation(count: int=50, seed : int=42, gp_shift : float=0.0):
    """Run visibility-aware random validation"""
    print("=" * 80)
    print(f"SMART RANDOM VALIDATION - {count} TEST CASES")
    print("Only selecting visible stars suitable for navigation")
    print("=" * 80)

    if gp_shift != 0.0:
        Testing.GP_shift = gp_shift

    # Generate smart test cases
    generator = VisibilityAwareGenerator(seed=seed)
    test_cases = generator.generate_smart_test_suite(count)

    if len(test_cases) == 0:
        print("ERROR: No valid test cases generated!")
        return [], {}

    # Run validation
    print(f"\nRunning NOVAS validation on {len(test_cases)} smart test cases...")
    print("=" * 60)

    validator = NOVASValidator(output_dir="results")
    for test_case in test_cases:
        validator.add_test_case(test_case)

    validator.run_all_validations()

    # Save smart validation results
    smart_results = {
        'generated_cases': len(test_cases),
        'target_cases': count,
        'generation_success_rate': len(test_cases) / count * 100,
        'validation_results': validator.results,
        'parameters': {
            'min_altitude': generator.min_altitude,
            'max_altitude': generator.max_altitude,
            'min_separation': generator.min_separation,
            'seed': seed
        }
    }

    with open('results/smart_random_validation.json', 'w', encoding="UTF-8") as f:
        json.dump(smart_results, f, indent=2, default=str)

    print("\nSmart random validation results saved to: results/smart_random_validation.json")

    return validator.results, smart_results

def main ():
    ''' Main function for the random validator '''
    # Run smart random validation

    parser = ArgumentParser()
    parser.add_argument("-l", "--length", default="500")
    parser.add_argument("-s", "--seed", default="42")
    parser.add_argument("-g", "--gp-shift", default="0")

    args = parser.parse_args()

    print(args)

    print("Testing smart random validation with visible star selection...")
    results, _ = run_smart_random_validation \
    (count=int(args.length), seed=int(args.seed), gp_shift=float(args.gp_shift))
    # Start with smaller count for testing

    successful_results = [r for r in results if r['success']]
    if successful_results:
        errors = [r['error_nm'] for r in successful_results]
        print("\nSMART VALIDATION SUMMARY:")
        print(f"Successful tests: {len(successful_results)}/{len(results)}")
        print(f"Average error: {np.mean(errors):.3f} nm")
        print(f"Max error: {np.max(errors):.3f} nm")
    else:
        print("\nNo successful validations - check star visibility logic")

if __name__ == "__main__":
    main ()
