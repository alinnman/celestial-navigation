"""
NOVAS Validation Framework for Celestial Navigation Toolkit
===========================================================

This module validates the accuracy of the celestial navigation toolkit
against NOVAS (Naval Observatory Vector Astrometry Software), which
represents the gold standard for astronomical calculations.

© August Linnman, 2025, email: august@linnman.net
MIT License
"""

from pathlib import Path
import sys
import json
from datetime import datetime
sys.path.append(str(Path(__file__).parent.parent))
#pylint: disable=C0413
from novas_star_altitude import get_star_altitude
from starfix import Sight, SightCollection, LatLonGeodetic, get_representation,\
     spherical_distance, km_to_nm
#pylint: enable=C0413

# Add the main toolkit to path


class ValidationTestCase:
    """Represents a single validation test case"""

    def __init__(self, name, location, datetime_utc, stars, description="", expected_position=None):
        self.name = name
        self.location = location  # (lat, lon)
        self.datetime_utc = datetime_utc
        self.stars = stars  # List of star names
        self.description = description
        self.expected_position = expected_position  # Known answer if available
        self.time = datetime_utc

class NOVASValidator:
    """Main validation class comparing toolkit results with NOVAS"""

    def __init__(self, output_dir="results"):
        self.test_cases = []
        self.results = []
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def add_test_case(self, test_case):
        ''' Adding a test case '''
        self.test_cases.append(test_case)

    def run_validation(self, test_case):
        """Run a single validation test"""
        print(f"\n{'='*60}")
        print(f"VALIDATION TEST: {test_case.name}")
        print(f"{'='*60}")
        print(f"Description: {test_case.description}")
        print(f"Location: {test_case.location[0]:.3f}°N, {test_case.location[1]:.3f}°E")
        print(f"Time: {test_case.datetime_utc} UTC")
        print(f"Stars: {', '.join([s.title() for s in test_case.stars])}")

        try:
            # 1. Calculate NOVAS reference altitudes
            print("\nNOVAS REFERENCE ALTITUDES:")
            novas_altitudes = {}
            for star in test_case.stars:
                result = get_star_altitude(star, test_case.location[0],\
                                           test_case.location[1], test_case.time)
                novas_altitudes[star] = result
                print(f"  {star.title():12}: {result['altitude']:7.4f}° "
                      f"({result['altitude']*60:7.1f}') Az: {result['azimuth']:6.1f}°")

            # 2. Create Sight objects using NOVAS altitudes
            # sights = []
            estimated_pos = LatLonGeodetic(test_case.location[0], test_case.location[1])

            #for star in test_case.stars:
            #    alt_deg = novas_altitudes[star]['altitude']
            #    alt_dms = self.decimal_to_dms(alt_deg)

            #    sight = Sight(
            #        object_name=star,
            #        set_time=test_case.datetime_utc.strftime("%Y-%m-%d %H:%M:%S+00:00"),
            #        measured_alt=alt_dms,
            #        estimated_position=estimated_pos,
            #        ho_obs=True  # Skip refraction since NOVAS already applied it
            #    sights.append(sight)

            # 3. Perform sight reduction
            #collection = SightCollection(sights)
            #intersections, fitness, diag, calculated_diff = collection.get_intersections(
            #    return_geodetic=True,
            #    estimated_position=estimated_pos,
            #    diagnostics=False
            #)

            def get_starfixes (estimated_position) -> SightCollection:
                sights = []
                for star in test_case.stars:
                    alt_deg = novas_altitudes[star]['altitude']
                    alt_dms = self.decimal_to_dms(alt_deg)

                    sight = Sight(
                        object_name=star,
                        set_time=test_case.datetime_utc.strftime("%Y-%m-%d %H:%M:%S+00:00"),
                        measured_alt=alt_dms,
                        estimated_position=estimated_position
                        #ho_obs=True  # Skip refraction since NOVAS already applied it
                    )
                    sights.append(sight)
                return SightCollection (sights)

            # intersections, fitness, diag, collection, calculated_diff


            intersections, fitness, _, _, calculated_diff = SightCollection.get_intersections_conv(
                return_geodetic=True,
                estimated_position=estimated_pos,
                get_starfixes = get_starfixes,
                diagnostics=False
            )

            # 4. Calculate accuracy
            if test_case.expected_position:
                true_pos = LatLonGeodetic(test_case.expected_position[0],\
                                          test_case.expected_position[1])
            else:
                # Use input location as "true" position
                true_pos = LatLonGeodetic(test_case.location[0], test_case.location[1])

            error_distance = self.calculate_distance_error(intersections, true_pos)

            # 5. Report results
            print("\nSIGHT REDUCTION RESULTS:")
            print(f"  Calculated Position: {get_representation(intersections, 4)}")
            print(f"  True Position:       {get_representation(true_pos, 4)}")
            print(f"  Position Error:      {error_distance:.3f} nautical miles")
            print(f"  Fitness Score:       {fitness:.3f}")
            print(f"  Calculated Sigma:    ±{calculated_diff/1.852:.3f} nm")

            # Accuracy rating
            if fitness < 0.5:
                rating = "BAD STAR CHOICE"
            elif error_distance < 0.1:
                rating = "EXCELLENT"
            elif error_distance < 0.5:
                rating = "VERY GOOD"
            elif error_distance < 1.0:
                rating = "GOOD"
            elif error_distance < 2.0:
                rating = "ACCEPTABLE"
            else:
                rating = "BAD"

            print(f"  Accuracy Rating:     {rating}")

            return {
                'test_name': test_case.name,
                'description': test_case.description,
                'location': test_case.location,
                'datetime_utc': test_case.datetime_utc.isoformat(),
                'stars': test_case.stars,
                'calculated_position': [intersections.get_lat(), intersections.get_lon()],
                'true_position': [true_pos.get_lat(), true_pos.get_lon()],
                'error_nm': error_distance,
                'fitness': fitness,
                'sigma_nm': calculated_diff/1.852,
                'rating': rating,
                'novas_altitudes': {star: alt['altitude'] for star, alt in novas_altitudes.items()},
                'success': True
            }
#pylint: disable=W0718
        except Exception as e:
#pylint: enable=W0718
            print(f"VALIDATION FAILED: {e}")

            return {
                'test_name': test_case.name,
                'description': test_case.description,
                'error_message': str(e),
                'success': False
            }

    def decimal_to_dms(self, decimal_degrees):
        """Convert decimal degrees to DD:MM:SS format"""
        d = int(decimal_degrees)
        m = int((decimal_degrees - d) * 60)
        s = ((decimal_degrees - d) * 60 - m) * 60
        return f"{d}:{m:02d}:{s:05.2f}"

    def calculate_distance_error(self, pos1, pos2):
        """Calculate distance error in nautical miles"""
        distance_km = spherical_distance(pos1, pos2)
        return km_to_nm(distance_km)

    def run_all_validations(self):
        """Run all validation tests and generate summary"""
        print("CELESTIAL NAVIGATION TOOLKIT - NOVAS VALIDATION")
        print("=" * 80)
        print("Validating sight reduction algorithms against U.S. Naval Observatory standards")
        print("=" * 80)

        self.results = []
        for test_case in self.test_cases:

            result = self.run_validation(test_case)
            try:
                if result['rating'] == "BAD STAR CHOICE":
                    continue
            except KeyError as _:
                pass
            self.results.append(result)

        self.generate_summary()
        self.save_results()

    def generate_summary(self):
        """Generate validation summary report"""
        print(f"\n{'='*80}")
        print("VALIDATION SUMMARY")
        print(f"{'='*80}")

        successful_tests = [r for r in self.results if r['success']]
        failed_tests = [r for r in self.results if not r['success']]

        if successful_tests:
            errors = [r['error_nm'] for r in successful_tests]
            avg_error = sum(errors) / len(errors)
            max_error = max(errors)
            min_error = min(errors)

            print(f"Total Test Cases:     {len(self.results)}")
            print(f"Successful Tests:     {len(successful_tests)}/{len(self.results)}"
                  f" ({100*len(successful_tests)/len(self.results):.0f}%)")
            print(f"Average Error:        {avg_error:.3f} nautical miles")
            print(f"Maximum Error:        {max_error:.3f} nautical miles")
            print(f"Minimum Error:        {min_error:.3f} nautical miles")

            # Overall accuracy classification
            if max_error < 0.1:
                overall_rating = "EXCELLENT (< 0.1 nm)"
            elif max_error < 0.5:
                overall_rating = "VERY GOOD (< 0.5 nm)"
            elif max_error < 1.0:
                overall_rating = "GOOD (< 1.0 nm)"
            else:
                overall_rating = "ACCEPTABLE"

            print(f"\nOVERALL ACCURACY RATING: {overall_rating}")

            # Detailed results table
            print("\nDETAILED RESULTS:")
            print(f"{'Test Case':<25} {'Location':<20} {'Stars':<15} {'Error (nm)':<12}"
                  f" {'Rating':<12}")
            print("-" * 90)
            for result in successful_tests:
                location_str = f"{result['location'][0]:.1f}°N,{result['location'][1]:.1f}°E"
                stars_str = f"{len(result['stars'])} stars"
                print(f"{result['test_name']:<25} {location_str:<20} {stars_str:<15} "
                      f"{result['error_nm']:<12.3f} {result['rating']:<12}")

        if failed_tests:
            print(f"\nFAILED TESTS: {len(failed_tests)}")
            for test in failed_tests:
                print(f"  - {test['test_name']}: {test['error_message']}")

        print(f"\n{'='*80}")
        print("Validation complete. Results saved to validation/results/")
        print(f"{'='*80}")

    def save_results(self):
        """Save results to files"""
        # Save JSON results
        json_file = self.output_dir / "validation_results.json"
        with open(json_file, 'w', encoding="UTF-8") as f:
            json.dump({
                'validation_date': datetime.now().isoformat(),
                'total_tests': len(self.results),
                'successful_tests': len([r for r in self.results if r['success']]),
                'results': self.results
            }, f, indent=2)

        # Save text report
        report_file = self.output_dir / "validation_report.txt"
        with open(report_file, 'w', encoding="UTF-8") as f:
            f.write("CELESTIAL NAVIGATION TOOLKIT - NOVAS VALIDATION REPORT\n")
            f.write("=" * 60 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")

            successful_tests = [r for r in self.results if r['success']]
            if successful_tests:
                errors = [r['error_nm'] for r in successful_tests]
                avg_error = sum(errors) / len(errors)
                max_error = max(errors)
                min_error = min(errors)

                f.write("SUMMARY STATISTICS\n")
                f.write("-" * 30 + "\n")
                f.write(f"Total Test Cases: {len(self.results)}\n")
                f.write(f"Successful Tests: {len(successful_tests)}/{len(self.results)}\n")
                f.write(f"Average Error: {avg_error:.3f} nautical miles\n")
                f.write(f"Maximum Error: {max_error:.3f} nautical miles\n")
                f.write(f"Minimum Error: {min_error:.3f} nautical miles\n\n")

                f.write("DETAILED RESULTS\n")
                f.write("-" * 30 + "\n")
                for result in successful_tests:
                    f.write(f"\nTest: {result['test_name']}\n")
                    f.write(f"Description: {result['description']}\n")
                    f.write(f"Location: {result['location'][0]:.3f}°N,"
                            f" {result['location'][1]:.3f}°E\n")
                    f.write(f"Stars: {', '.join(result['stars'])}\n")
                    f.write(f"Error: {result['error_nm']:.3f} nm\n")
                    f.write(f"Rating: {result['rating']}\n")

        print("Results saved to:")
        print(f"  - {json_file}")
        print(f"  - {report_file}")

def create_test_cases():
    """Create comprehensive validation test cases"""
    test_cases = []

    # Test Case 1: Baltic Sea - Your original data
    test_cases.append(ValidationTestCase(
        name="Baltic Sea Fix",
        location=(59.444, 19.502),
        datetime_utc=datetime(2025, 4, 19, 1, 44, 43),
        stars=['vega', 'arcturus', 'capella'],
        description="High latitude location with bright navigation stars"
    ))

    # Test Case 2: Mid-latitude location
    test_cases.append(ValidationTestCase(
        name="North Atlantic Fix",
        location=(40.0, -30.0),
        datetime_utc=datetime(2025, 3, 21, 23, 15, 30),
        stars=['pollux', 'arcturus', 'capella'],
        description="Mid-latitude Atlantic crossing scenario",
    ))

    # Test Case 3: Two star fix - minimum case
    test_cases.append(ValidationTestCase(
        name="Two Star Fix",
        location=(35.0, 18.0),
        datetime_utc=datetime(2025, 5, 10, 21, 30, 0),
        stars=['vega', 'arcturus'],
        description="Minimum two-star fix validation"
    ))

    # Test Case 4: Equatorial location
    test_cases.append(ValidationTestCase(
        name="Equatorial Fix",
        location=(0.0, 73.0),
        datetime_utc=datetime(2025, 6, 15, 2, 30, 0),
        stars=['enif', 'deneb', 'altair'],
        description="Equatorial location test"
    ))

    return test_cases

def main():
    """Main validation runner"""
    validator = NOVASValidator()
    # Add test cases
    for test_case in create_test_cases():
        validator.add_test_case(test_case)

    # Run validation
    validator.run_all_validations()

if __name__ == "__main__":
    main()
