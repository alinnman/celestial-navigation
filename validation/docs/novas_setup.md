# NOVAS Installation and Setup Guide

This guide explains how to install and configure NOVAS (Naval Observatory Vector Astrometry Software) for validating the celestial navigation toolkit.

## What is NOVAS?

NOVAS is the official astronomical calculation software developed and maintained by the U.S. Naval Observatory. It provides:

- **Sub-arcsecond precision** star and planet positions
- **Professional-grade algorithms** used by astronomers and navigators worldwide
- **Comprehensive corrections** for precession, nutation, aberration, parallax, refraction
- **Authoritative reference standard** for astronomical calculations

## Installation Methods

### Method 1: pip install (Recommended)

```bash
pip install novas
```

This installs the Python wrapper for NOVAS, which provides easy access to NOVAS functions from Python.

### Method 2: Conda install

```bash
conda install -c conda-forge novas
```

### Method 3: From source (Advanced)

```bash
git clone https://github.com/brandon-rhodes/python-novas
cd python-novas
pip install .
```

## Verification

Test your NOVAS installation:

```python
import novas.compat as novas

# Test basic functionality
jd = novas.julian_date(2025, 4, 19, 12.0)
print(f"Julian Date: {jd}")

# Test star position calculation
location = novas.make_on_surface(59.444, 19.502, 0.0, 10.0, 1013.25)
print("NOVAS installation successful!")
```

Expected output:
```
Julian Date: 2460584.0
NOVAS installation successful!
```

## Common Installation Issues

### Issue 1: ImportError for novas.compat

**Problem:**
```
ImportError: No module named 'novas.compat'
```

**Solution:**
```bash
pip uninstall novas
pip install novas
```

### Issue 2: Missing numpy dependency

**Problem:**
```
ImportError: numpy is required
```

**Solution:**
```bash
pip install numpy
pip install novas
```

### Issue 3: Windows compilation errors

**Problem:**
```
Microsoft Visual C++ 14.0 is required
```

**Solution:**
1. Install Visual Studio Build Tools
2. Or use conda instead: `conda install -c conda-forge novas`

### Issue 4: macOS compilation errors

**Problem:**
```
clang: error: unsupported option '-fopenmp'
```

**Solution:**
```bash
brew install libomp
pip install novas
```

## NOVAS Configuration for Validation

The validation framework uses these NOVAS settings:

```python
# Atmospheric refraction: ENABLED
ref_option = 1  # Standard atmospheric refraction

# Time precision
delta_t = 69.2  # TT-UT1 difference for 2025 (seconds)

# Polar motion (standard values for most applications)
xp = 0.0  # Polar motion x-component (arcseconds)
yp = 0.0  # Polar motion y-component (arcseconds)

# Accuracy mode
accuracy = 0  # Full precision mode
```

## NOVAS Function Reference

### Key functions used in validation:

#### `julian_date(year, month, day, hour)`
Convert calendar date to Julian Date.

#### `make_on_surface(lat, lon, height, temp, pressure)`
Create observer location object.

#### `make_cat_entry(name, catalog, number, ra, dec, pm_ra, pm_dec, parallax, rv)`
Create star catalog entry.

#### `topo_star(jd_tt, delta_t, star, location)`
Calculate topocentric star position.

#### `equ2hor(jd_ut1, delta_t, xp, yp, location, ra, dec, ref_option, accuracy)`
Convert equatorial to horizontal coordinates.

## Validation Dependencies

For the complete validation framework:

```bash
# Core dependencies
pip install novas numpy

# Optional: For enhanced analysis
pip install matplotlib pandas

# Development
pip install pytest
```

## Troubleshooting

### Check NOVAS version
```python
import novas
print(novas.__version__)
```

### Test star calculation
```python
from validation.novas_star_altitude import get_star_altitude

result = get_star_altitude('vega', 59.444, 19.502)
print(f"Vega altitude: {result['altitude']:.4f}°")
```

### Verify star catalog
```python
from validation.novas_star_altitude import get_navigation_stars

catalog = get_navigation_stars()
print(f"Available stars: {list(catalog.keys())}")
```

## Performance Notes

- **NOVAS calculations are fast**: Typically < 1ms per star position
- **Memory usage is minimal**: No large data files required
- **Precision is excellent**: Sub-arcsecond accuracy for all calculations
- **Validation is comprehensive**: Tests multiple scenarios automatically

## Alternative References

If NOVAS installation fails, alternative astronomical libraries:

1. **Skyfield** (used in main toolkit):
   ```bash
   pip install skyfield
   ```

2. **PyEphem**:
   ```bash
   pip install pyephem
   ```

3. **Astropy**:
   ```bash
   pip install astropy
   ```

However, **NOVAS is preferred** for validation because:
- It's the official U.S. Naval Observatory standard
- It provides the most authoritative reference for celestial navigation
- Professional navigators worldwide use NOVAS-based calculations

## Getting Help

- **NOVAS Documentation**: [Naval Observatory NOVAS page](https://aa.usno.navy.mil/software/novas_info)
- **Python NOVAS**: [GitHub repository](https://github.com/brandon-rhodes/python-novas)
- **Issues**: Check the validation troubleshooting guide
- **Professional Support**: Contact U.S. Naval Observatory for authoritative guidance

---

**Setup Guide**: Part of Celestial Navigation Validation Framework  
**© August Linnman, 2025**  
**Reference**: U.S. Naval Observatory NOVAS Documentation
