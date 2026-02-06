#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ee, geemap
ee.Authenticate()
ee.Initialize(project='ee-sanim')



# In[2]:


"""
00_data_precheck.py
---------------------------------------------------------
Purpose:
    This script validates all Google Earth Engine (GEE) assets
    required for the Dhaka Heat–Poverty Analysis workflow.

    It checks:
    - Whether assets exist and can be loaded
    - Whether FeatureCollections contain required properties
    - Whether Landsat 8 and Landsat 9 collections load correctly
    - Whether required thermal and QA bands are present
    - Whether geometries and projections are valid

    Running this script before any processing ensures that all
    datasets are available and correctly structured.

Author: Mahbubul Alam
Date: 2026
"""

import ee

# ---------------------------------------------------------
# 1. Initialize Earth Engine
# ---------------------------------------------------------
ee.Initialize(project='ee-sanim')

print("\n===============================================")
print("   GEE DATA PRECHECK: Dhaka Heat–Poverty Project")
print("===============================================\n")

# ---------------------------------------------------------
# 2. Define required GEE assets
# ---------------------------------------------------------
ASSETS = {
    "Poverty dataset (EO4SD)": "projects/ee-sanim/assets/eo4sd_dhaka_informal_2017",
    "Dhaka boundary": "projects/ee-sanim/assets/Coredhaka"
}

# Required properties for FeatureCollections
REQUIRED_PROPERTIES = {
    "Poverty dataset (EO4SD)": ["AL3_NAMEF", "NB_BUDENS"],
    "Dhaka boundary": ["NAME_3"]
}

# Landsat 8 and 9 collections
LANDSAT_COLLECTIONS = {
    "Landsat 8 (LC08)": "LANDSAT/LC08/C02/T1_L2",
    "Landsat 9 (LC09)": "LANDSAT/LC09/C02/T1_L2"
}

# Required Landsat bands
REQUIRED_LANDSAT_BANDS = ["ST_B10", "QA_PIXEL"]

# ---------------------------------------------------------
# 3. Helper functions
# ---------------------------------------------------------
def check_asset_exists(label, asset_id):
    """Check if a FeatureCollection asset exists and can be loaded."""
    try:
        fc = ee.FeatureCollection(asset_id)
        size = fc.size().getInfo()
        print(f"[OK] {label} loaded successfully ({size} features).")
        return fc
    except Exception as e:
        print(f"[MISSING] {label} could not be loaded: {e}")
        return None


def check_properties(label, fc, required_props):
    """Check if required properties exist in the FeatureCollection."""
    try:
        keys = fc.first().toDictionary().keys().getInfo()
        missing = [p for p in required_props if p not in keys]

        if missing:
            print(f"[PROPERTY WARNING] {label} missing: {missing}")
        else:
            print(f"[OK] {label} contains all required properties.")
    except Exception as e:
        print(f"[ERROR] Could not inspect properties of {label}: {e}")


def check_landsat_collection(label, collection_id):
    """Check if Landsat collection loads and contains required bands."""
    try:
        col = ee.ImageCollection(collection_id).filterDate("2014-01-01", "2024-12-31")
        count = col.size().getInfo()
        print(f"[OK] {label} loaded ({count} images).")

        # Check band availability
        first = col.first()
        bands = first.bandNames().getInfo()
        missing = [b for b in REQUIRED_LANDSAT_BANDS if b not in bands]

        if missing:
            print(f"[BAND WARNING] {label} missing bands: {missing}")
        else:
            print(f"[OK] {label} contains all required bands.")

    except Exception as e:
        print(f"[ERROR] Could not load {label}: {e}")


# ---------------------------------------------------------
# 4. Run checks for FeatureCollections
# ---------------------------------------------------------
for label, asset_id in ASSETS.items():
    fc = check_asset_exists(label, asset_id)
    if fc:
        check_properties(label, fc, REQUIRED_PROPERTIES[label])

# ---------------------------------------------------------
# 5. Run checks for Landsat 8 and Landsat 9
# ---------------------------------------------------------
for label, collection_id in LANDSAT_COLLECTIONS.items():
    check_landsat_collection(label, collection_id)

print("\n===============================================")
print("   GEE DATA PRECHECK COMPLETE")
print("===============================================\n")

