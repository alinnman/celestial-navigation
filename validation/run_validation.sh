#!/bin/bash
# Celestial Navigation Validation Runner
# © August Linnman, 2025

echo "==============================================="
echo "Celestial Navigation Toolkit - NOVAS Validation"
echo "==============================================="

# Check if we're in the right directory
if [ ! -f "novas_validation.py" ]; then
    echo "Error: Must run from validation/ directory"
    echo "Usage: cd validation && ./run_validation.sh"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Ensure results directory exists
mkdir -p results

# Run validation
echo "Running NOVAS (smart random) validation..."
# python novas_validation.py
python smart_random_validation.py $1 $2 $3 $4 $5 $6

# Check if validation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "==============================================="
    echo "Validation completed successfully!"
    echo "==============================================="
    echo "Results saved to:"
    echo "  - results/validation_results.json"
    echo "  - results/validation_report.txt"
    echo ""
    echo "Quick summary:"
    if [ -f "results/validation_report.txt" ]; then
        grep -A 10 "SUMMARY STATISTICS" results/validation_report.txt
    fi
else
    echo ""
    echo "==============================================="
    echo "Validation failed - check error messages above"
    echo "==============================================="
    exit 1
fi

# Deactivate virtual environment
# conda deactivate

echo ""
echo "Validation complete. Check results/ directory for detailed output."
