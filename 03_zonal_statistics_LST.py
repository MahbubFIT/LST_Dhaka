"""
03_zonal_statistics_LST.py

This script extracts slum‑level zonal statistics for Dhaka’s informal
settlements, including mean LST trend, MK Z‑score, Sen slope, and
hotspot proportions.

The workflow extends the LST trend outputs from Script 02 and applies
polygon‑based zonal statistics to quantify heat exposure at the
settlement scale.

All zonal statistics logic, slum‑level aggregation, and visualization
components were implemented by Mahbubul Alam.
"""

import ee, geemap
ee.Authenticate()
ee.Initialize(project='ee-sanim')
"""
03_zonal_statistics_LST.py

This script computes zonal statistics for Dhaka’s informal settlements
using the outputs from Script 02. It extracts:

    • Mean LST trend (°C/year)
    • Mean Mann–Kendall Z-score
    • Mean Sen’s slope (°C/year)
    • Hotspot class proportions

It also generates summary visualizations including:
    • Bar charts
    • Scatter plots
    • Hotspot proportion histograms
    • Boxplots
    • Identification and mapping of the top 10 hottest slums

Full exploratory analysis and spatial visualizations are provided in
the corresponding notebook and exported in the results/ folder.
"""

import ee
import matplotlib.pyplot as plt
import geemap

# ---------------------------------------------------------
# 1. Initialize Earth Engine
# ---------------------------------------------------------
ee.Initialize(project='ee-sanim')

print("\n===============================================")
print("   ZONAL STATISTICS: Dhaka Heat–Poverty Project")
print("===============================================\n")

# ---------------------------------------------------------
# 2. Load Dhaka slum polygons
# ---------------------------------------------------------
slums = ee.FeatureCollection("projects/ee-sanim/assets/eo4sd_dhaka_informal_2017")

# ---------------------------------------------------------
# 3. Load raster outputs from Script 02
# ---------------------------------------------------------
# slope, mk, sen, hotspot_class must exist in memory if running sequentially.

# ---------------------------------------------------------
# 4. Function to compute zonal statistics
# ---------------------------------------------------------
def compute_stats(feature):
    geom = feature.geometry()

    mean_trend = slope.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geom,
        scale=100,
        maxPixels=1e9
    ).get("LST_Trend")

    mean_mk = mk.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geom,
        scale=100,
        maxPixels=1e9
    ).get("MK_Z")

    mean_sen = sen.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=geom,
        scale=100,
        maxPixels=1e9
    ).get("Sen_Slope")

    hotspot_hist = hotspot_class.reduceRegion(
        reducer=ee.Reducer.frequencyHistogram(),
        geometry=geom,
        scale=100,
        maxPixels=1e9
    ).get("Hotspot_Class")

    return feature.set({
        "mean_LST_trend": mean_trend,
        "mean_MK_Z": mean_mk,
        "mean_Sen_slope": mean_sen,
        "hotspot_hist": hotspot_hist
    })

# ---------------------------------------------------------
# 5. Apply zonal statistics
# ---------------------------------------------------------
slum_stats = slums.map(compute_stats)
print("Zonal statistics computed for all slum polygons.")

# ---------------------------------------------------------
# 6. Export results
# ---------------------------------------------------------
task = ee.batch.Export.table.toDrive(
    collection=slum_stats,
    description="Dhaka_Slum_LST_Zonal_Statistics",
    fileFormat="CSV"
)
task.start()

print("\nExport started: Dhaka_Slum_LST_Zonal_Statistics.csv")
print("===============================================\n")

# ---------------------------------------------------------
# 7. Convert to client-side list for plotting
# ---------------------------------------------------------
slum_list = slum_stats.getInfo()['features']

trend_vals = []
mk_vals = []
sen_vals = []
hotspot_props = []

for f in slum_list:
    props = f['properties']
    trend_vals.append(props.get('mean_LST_trend'))
    mk_vals.append(props.get('mean_MK_Z'))
    sen_vals.append(props.get('mean_Sen_slope'))

    hist = props.get('hotspot_hist')
    if hist:
        total = sum(hist.values())
        warm = hist.get('1', 0) / total
        hotspot_props.append(warm)

# ---------------------------------------------------------
# 8. Summary Visualizations
# ---------------------------------------------------------

# --- A. Bar Chart: Slum-by-Slum Trend ---
plt.figure(figsize=(14,5))
plt.bar(range(len(trend_vals)), trend_vals, color='tomato')
plt.title("Mean LST Trend per Slum")
plt.xlabel("Slum Index")
plt.ylabel("Trend (°C/year)")
plt.tight_layout()
plt.show()

# --- B. Scatter Plot: Trend vs MK ---
plt.figure(figsize=(6,5))
plt.scatter(trend_vals, mk_vals, color='purple', alpha=0.7)
plt.title("Slum Trend vs MK Z-score")
plt.xlabel("Mean LST Trend")
plt.ylabel("Mean MK Z-score")
plt.tight_layout()
plt.show()

# --- C. Scatter Plot: Trend vs Sen ---
plt.figure(figsize=(6,5))
plt.scatter(trend_vals, sen_vals, color='green', alpha=0.7)
plt.title("Slum Trend vs Sen’s Slope")
plt.xlabel("Mean LST Trend")
plt.ylabel("Mean Sen Slope")
plt.tight_layout()
plt.show()

# --- D. Hotspot Proportion Histogram ---
plt.figure(figsize=(7,5))
plt.hist(hotspot_props, bins=20, color='orange')
plt.title("Proportion of Warming Pixels per Slum")
plt.xlabel("Warming Proportion")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# --- E. Boxplots: Compare Distributions ---
plt.figure(figsize=(8,5))
plt.boxplot([trend_vals, mk_vals, sen_vals],
            labels=["Trend", "MK Z", "Sen Slope"])
plt.title("Distribution of Slum-Level Zonal Statistics")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------
# 9. Identify Top 10 Hottest Slums
# ---------------------------------------------------------
slum_trends = []

for idx, f in enumerate(slum_list):
    props = f['properties']
    trend = props.get('mean_LST_trend')
    slum_trends.append((idx, trend))

slum_trends_sorted = sorted(slum_trends, key=lambda x: x[1], reverse=True)
top10 = slum_trends_sorted[:10]

print("\nTop 10 hottest slums:")
for i, (idx, trend) in enumerate(top10, start=1):
    print(f"{i}. Slum Index: {idx}, Trend: {trend}")

# ---------------------------------------------------------
# 10. Map the Top 10 Hottest Slums
# ---------------------------------------------------------
top10_features = [slum_list[idx] for idx, trend in top10]

top10_fc = ee.FeatureCollection([
    ee.Feature(f['geometry'], f['properties']) for f in top10_features
])

Map = geemap.Map()

Map.addLayer(slums, {"color": "blue"}, "All Slums")
Map.addLayer(top10_fc, {"color": "red"}, "Top 10 Hottest Slums")
Map.addLayer(dhaka, {"color": "black"}, "Dhaka Boundary")

Map.centerObject(top10_fc, 13)
Map
 
            
