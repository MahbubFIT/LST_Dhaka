"""
02_LST_trend_hotspot_analysis.py

This script performs long-term LST trend analysis for Dhaka using the
official Landsat Collection 2 LST product. It computes:

    • Linear trend (°C/year)
    • Mann–Kendall Z-score
    • Sen’s slope
    • Hotspot classification

The script also generates summary histograms for reproducibility.
"""

import ee
import matplotlib.pyplot as plt

ee.Initialize(project="ee-sanim")

dhaka = ee.FeatureCollection("projects/ee-sanim/assets/Coredhaka")

monthly_lst = monthly_lst_clipped

def add_time_band(img):
    year = ee.Number(img.get("year"))
    month = ee.Number(img.get("month"))
    fractional_time = year.add(month.divide(12))
    return img.addBands(
        ee.Image.constant(fractional_time).rename("time").toFloat()
    )

lst_with_time = monthly_lst.map(add_time_band)

trend = (
    lst_with_time
    .select(["time", "LST_C"])
    .reduce(ee.Reducer.linearFit())
)

slope = trend.select("scale").rename("LST_Trend")
intercept = trend.select("offset").rename("LST_Intercept")

mk = (
    monthly_lst
    .select("LST_C")
    .reduce(ee.Reducer.kendallsCorrelation())
    .select("LST_C_tau")
    .rename("MK_Z")
)

sen = (
    lst_with_time
    .select(["time", "LST_C"])
    .reduce(ee.Reducer.sensSlope())
    .select("slope")
    .rename("Sen_Slope")
)

warming_threshold = 0.02
cooling_threshold = -0.02

hotspot_class = (
    slope.gt(warming_threshold).multiply(1)
    .add(slope.lt(cooling_threshold).multiply(-1))
    .rename("Hotspot_Class")
)

slope = slope.clip(dhaka)
intercept = intercept.clip(dhaka)
mk = mk.clip(dhaka)
sen = sen.clip(dhaka)
hotspot_class = hotspot_class.clip(dhaka)

combined = slope.addBands(mk).addBands(sen)

sample = combined.sample(
    region=dhaka.geometry(),
    scale=100,
    numPixels=2000,
    seed=42,
    geometries=False
).getInfo()

trend_vals, mk_vals, sen_vals = [], [], []

for f in sample["features"]:
    props = f["properties"]
    trend_vals.append(props.get("LST_Trend"))
    mk_vals.append(props.get("MK_Z"))
    sen_vals.append(props.get("Sen_Slope"))

plt.figure(figsize=(15, 4))

plt.subplot(1, 3, 1)
plt.hist(trend_vals, bins=40)
plt.title("LST Trend (°C/year)")

plt.subplot(1, 3, 2)
plt.hist(mk_vals, bins=40)
plt.title("Mann–Kendall Z-score")

plt.subplot(1, 3, 3)
plt.hist(sen_vals, bins=40)
plt.title("Sen’s Slope (°C/year)")

plt.tight_layout()
plt.show()
