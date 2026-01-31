import ee, geemap
ee.Authenticate()
ee.Initialize(project='ee-sanim')
"""
01_LST_processing_timeseries.py
---------------------------------------------------------
Purpose:
    Generate a monthly Land Surface Temperature (LST) time series
    for Dhaka using Landsat 8 and Landsat 9 Collection 2 Level-2
    thermal data (ST_B10). This script prepares a clean, clipped,
    cloud-masked ImageCollection for downstream trend analysis,
    zonal statistics, and vulnerability mapping.

Workflow:
    - Load Landsat 8 & 9
    - Cloud mask using QA_PIXEL
    - Convert ST_B10 to LST (Kelvin → Celsius)
    - Clip to Dhaka AOI
    - Create monthly median composites (2014–2024)

Author: Mahbubul Alam
Date: 2026
"""

import ee

# ---------------------------------------------------------
# 1. Initialize Earth Engine
# ---------------------------------------------------------
ee.Initialize(project='ee-sanim')

print("\n===============================================")
print("   LST PROCESSING: Dhaka Heat–Poverty Project")
print("===============================================\n")

# ---------------------------------------------------------
# 2. Load Dhaka boundary
# ---------------------------------------------------------
dhaka = ee.FeatureCollection("projects/ee-sanim/assets/Coredhaka")

# ---------------------------------------------------------
# 3. Cloud masking function (QA_PIXEL)
# ---------------------------------------------------------
def mask_landsat_clouds(image):
    """Mask clouds and cirrus using QA_PIXEL bit flags."""
    qa = image.select("QA_PIXEL")
    cloud_mask = qa.bitwiseAnd(1 << 3).eq(0)   # Cloud
    cirrus_mask = qa.bitwiseAnd(1 << 2).eq(0)  # Cirrus
    return image.updateMask(cloud_mask).updateMask(cirrus_mask)

# ---------------------------------------------------------
# 4. Convert ST_B10 to LST (Kelvin → Celsius)
# ---------------------------------------------------------
def compute_lst(image):
    """Convert Landsat Collection 2 ST_B10 to LST in Celsius."""
    lst_kelvin = image.select("ST_B10").multiply(0.00341802).add(149.0)
    lst_celsius = lst_kelvin.subtract(273.15).rename("LST_C")
    return image.addBands(lst_celsius)

# ---------------------------------------------------------
# 5. Load and filter Landsat 8 & 9
# ---------------------------------------------------------
def load_landsat(collection_id, start, end):
    """Load, filter, cloud-mask, and compute LST for a Landsat collection."""
    return (
        ee.ImageCollection(collection_id)
        .filterBounds(dhaka)
        .filterDate(start, end)
        .filter(ee.Filter.lt("CLOUD_COVER", 60))
        .map(mask_landsat_clouds)
        .map(compute_lst)
        .select("LST_C")
    )

ls8 = load_landsat("LANDSAT/LC08/C02/T1_L2", "2014-01-01", "2024-12-31")
ls9 = load_landsat("LANDSAT/LC09/C02/T1_L2", "2022-01-01", "2024-12-31")

landsat = ls8.merge(ls9)

print("Filtered Landsat image count:", landsat.size().getInfo())

# ---------------------------------------------------------
# 6. Create monthly median LST composites
# ---------------------------------------------------------
def monthly_composites(collection, start_year, end_year):
    """Generate monthly median LST composites for each year."""
    months = ee.List.sequence(1, 12)
    years = ee.List.sequence(start_year, end_year)

    def per_month(year, month):
        start = ee.Date.fromYMD(year, month, 1)
        end = start.advance(1, "month")
        composite = (
            collection.filterDate(start, end)
            .median()
            .set("year", year)
            .set("month", month)
            .set("system:time_start", start.millis())
        )
        return composite

    def per_year(year):
        return months.map(lambda m: per_month(year, m))

    return ee.ImageCollection(years.map(per_year).flatten())

monthly_lst = monthly_composites(landsat, 2014, 2024)

print("Monthly composites created:", monthly_lst.size().getInfo())

# ---------------------------------------------------------
# 7. Clip all composites to Dhaka
# ---------------------------------------------------------
monthly_lst_clipped = monthly_lst.map(lambda img: img.clip(dhaka))

print("\n===============================================")
print("   LST PROCESSING COMPLETE")
print("===============================================\n")
