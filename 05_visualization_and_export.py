"""
05_visualization_and_export.py

This script produces final visualizations for the thesis, including:
    • vulnerability histograms
    • heat–poverty scatter plots
    • slum‑level vulnerability maps

It consolidates outputs from Scripts 03 and 04 and prepares publication‑
ready figures for the Results chapter.

All visualization logic and map styling were implemented by Mahbubul Alam.
"""
import pandas as pd
import matplotlib.pyplot as plt
import ee
import geemap

ee.Initialize(project='ee-sanim')

# ---------------------------------------------------------
# Load CSV outputs
# ---------------------------------------------------------
slum_vuln = pd.read_csv("/content/drive/MyDrive/Dhaka_Slum_Heat_Poverty_Vulnerability.csv")
slum_stats = pd.read_csv("/content/drive/MyDrive/Dhaka_Slum_LST_Zonal_Statistics.csv")

print("Loaded slum vulnerability:", slum_vuln.shape)
print("Loaded slum stats:", slum_stats.shape)

# ---------------------------------------------------------
# Plot 1: Vulnerability distribution
# ---------------------------------------------------------
plt.figure(figsize=(8,5))
plt.hist(slum_vuln["vulnerability"], bins=20, color="steelblue")
plt.title("Slum‑Level Heat–Poverty Vulnerability")
plt.xlabel("Vulnerability Index")
plt.ylabel("Number of Slums")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------
# Plot 2: Heat vs Poverty scatter
# ---------------------------------------------------------
plt.figure(figsize=(7,5))
plt.scatter(
    slum_vuln["norm_poverty"],
    slum_vuln["norm_heat"],
    alpha=0.6,
    color="darkred"
)
plt.title("Heat vs Poverty (Slum Level)")
plt.xlabel("Normalized Poverty (Building Density)")
plt.ylabel("Normalized Heat (LST Trend)")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------
# Simple slum vulnerability map (geemap)
# ---------------------------------------------------------
# Load slum polygons from Earth Engine
slums = ee.FeatureCollection("projects/ee-sanim/assets/eo4sd_dhaka_informal_2017")

# Prepare vulnerability data as an ee.List for server-side access
py_vulnerability_values = slum_vuln["vulnerability"].tolist()
ee_vulnerability_list = ee.List(py_vulnerability_values)

# Helper function to attach vulnerability by index
def attach_by_index(i):
    f = ee.Feature(slums.toList(slums.size()).get(i))
    v = ee_vulnerability_list.get(i)
    return f.set("vulnerability", v)

# Map the vulnerability values onto the slum features
slums_vuln = ee.FeatureCollection(
    ee.List.sequence(0, slums.size().subtract(1)).map(attach_by_index)
)

# Convert FeatureCollection to an Image for visualization, selecting the 'vulnerability' property
vulnerability_image = slums_vuln.reduceToImage(properties=['vulnerability'], reducer=ee.Reducer.first())

# Visualization style
vuln_vis = {
    "min": 0,
    "max": 1,
    "palette": ["#f7fbff", "#c6dbef", "#6baed6", "#2171b5", "#08306b"]
}

# Create map
Map = geemap.Map()
Map.addLayer(vulnerability_image, vuln_vis, "Slum Vulnerability") # Use the new vulnerability_image
Map.centerObject(slums, 11)
Map.addLayer(dhaka, {"color": "black"}, "Dhaka Boundary")
Map
