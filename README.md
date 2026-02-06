
Mapping the Heat Divide: Spatio‑Temporal Analysis of Thermal Hotspots and Socio‑Economic Inequality in Dhaka (2014–2024)
Scientific Research Project – Draft Code Repository  
Author: Mahbubul Alam
Programme: Master’s in Forest Information Technology (FIT)
Institution: HNEE, Eberswalde
Supervisor: Prof. Dr. Jan‑Peter Mund

Overview
This repository contains the base code and workflow structure used to develop the scientific report “Mapping the Heat Divide: Spatio‑Temporal Analysis of Thermal Hotspots and Socio‑Economic Inequality in Dhaka (2014–2024)”.
The current version documents the analytical pipeline and includes the main notebooks, scripts, and selected intermediate outputs.

The fully cleaned, final, and reproducible workflow — including all notebooks, scripts, and final outputs — will be submitted together with the final scientific report.

Repository Structure
Code
LST_Dhaka/
│
├── Notebooks/
│   ├── 01_LST_processing_timeseries.ipynb
│   └── 02_LST_trend_hotspot_analysis.ipynb
│
├── Scripts/
│   ├── 00_data_precheck.py
│   ├── 01_LST_processing_timeseries.py
│   ├── 02_LST_trend_hotspot_analysis.py
│   ├── 03_zonal_statistics_LST.py
│   ├── 04_heat_poverty_vulnerability_mapping.py
│   └── 05_visualization_and_export.py
│
├── CONTRIBUTING.md
├── LICENSE
└── README.md
Purpose of This Repository
This draft repository serves three goals:

Transparency – to show the structure of the analytical workflow used in the report.

Documentation – to outline how Landsat/MODIS LST, trend analysis, hotspot detection, and poverty‑heat linkage were implemented.

Reproducibility (Final Version) – the complete, cleaned workflow will be delivered with the final submission.

Current Status (Draft)
Base code and workflow logic are included.

Some intermediate outputs are provided for illustration.

Data cleaning and code organisation are in progress.

Final notebooks will include:

harmonised functions

consistent plotting styles

complete documentation

reproducible outputs for all figures in the report

Final Submission Will Include
Fully cleaned and documented Jupyter notebooks

All Python scripts with consistent structure

Exported figures used in the scientific report

A reproducible environment file (e.g., requirements.txt)

Final data‑processing workflow description

Data Availability
Satellite datasets (Landsat 8/9, MODIS) are accessed through Google Earth Engine.
Socio‑economic datasets (EDSO 2017, NB_BUDENS) are not included in this repository due to licensing and size constraints.

Contact
For questions or collaboration:
Mahbubul Alam  
Master’s in Forest Information Technology
HNEE, Eberswalde
