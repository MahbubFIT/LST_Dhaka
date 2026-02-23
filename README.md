# Mapping the Heat Divide: Spatio‑Temporal Analysis of Thermal Hotspots and Socio‑Economic Inequality in Dhaka (2014–2024)

**Scientific Research Project – Final Code Repository**  
**Author:** Mahbubul Alam  
**Programme:** Master’s in Forest Information Technology (FIT)  
**Institution:** HNEE, Eberswalde  
**Supervisor:** Prof. Dr. Jan‑Peter Mund  

---

## Overview

This repository contains the complete and reproducible analytical workflow developed for the scientific research project  
**“Mapping the Heat Divide: Spatio‑Temporal Analysis of Thermal Hotspots and Socio‑Economic Inequality in Dhaka (2014–2024)”**.

It includes all final notebooks, scripts, figures, and environment specifications required to reproduce the results presented in the scientific report.  
All workflows have been cleaned, harmonised, and validated for full reproducibility.

## Methodological Workflow
The analysis follows a multi‑stage workflow consistent with the scientific report:

### 1. LST Retrieval and Pre‑Processing
- Cloud and shadow masking  
- Conversion to LST  
- Annual and seasonal composites  

### 2. Trend Analysis
- Mann‑Kendall significance test  
- Theil‑Sen slope estimation  
- MODIS‑based long‑term validation  

### 3. Hotspot Detection
- Getis‑Ord Gi* statistic  
- Hotspot and cold‑spot mapping  
- 10‑year hotspot persistence  

### 4. Socio‑Economic Integration
- Zonal statistics for building density  
- Poverty–heat correlation analysis  
- Ward‑level vulnerability assessment  

### 5. HPVI Construction
- Normalisation of indicators  
- Weighted index formulation  
- Classification into vulnerability levels  

### 6. Final Visualisation
- High‑resolution maps  
- Statistical plots  
- Multi‑panel comparison figures
- 
## Purpose of This Repository

This repository provides the **final reproducible workflow** for analysing long‑term thermal hotspot dynamics and socio‑economic inequality in Dhaka. It includes:

- complete Jupyter notebooks for each analytical stage  
- modular Python scripts for LST processing, hotspot detection, zonal statistics, and vulnerability mapping  
- all final figures used in the scientific report  
- a reproducible environment file  
- documentation of the full analytical pipeline  

The structure ensures transparency, clarity, and scientific reproducibility.

## Important Figures

### 1. Study Area Map
![Study Area](Figures/Study_Area.png)

### 2. LST Trend (2014–2024) 
![LST Trend 2014–2024](Figures/lst_trend_2014_2024.png.png)
Displays long‑term warming patterns across Dhaka.

### 3. Hotspot Persistence (10-Year)
![Hotspot Persistence](Figures/hotspot_persistence.png.png)

### 5. Heat–Poverty Vulnerability Index (HPVI)
![HPVI Map](Figures/hpvi_map.png.png)
Ward‑level vulnerability classification combining heat exposure and socio‑economic indicators.

### 6. Heat–Poverty Overlay
![Inequality Overlay](Figures/inequality_overlay.png.png)
Visualises the spatial relationship between thermal hotspots and poverty.

### **7. NDVI–LST Relationship (Supplementary)**
![NDVI vs LST](Figures/NDVI_LST.png)

Shows the cooling effect of vegetation.

### **8. LST Distribution **
![Picture14](Figures/Picture14.png)

### **9. Workflow Diagram**
![Workflow Diagram](Figures/Workflow.png) 
Illustrates the full analytical pipeline from preprocessing to final mapping.

## Purpose of This Repository

This repository provides the **final reproducible workflow** for analysing thermal hotspots and socio‑economic inequality in Dhaka. It includes:

- complete Jupyter notebooks  
- modular Python scripts  
- final figures used in the scientific report  
- a reproducible environment file  
- documentation of the full analytical pipeline  

---
## Final Submission Includes

- cleaned and documented notebooks  
- harmonised Python scripts  
- important  figures  
- reproducible environment (`requirements.txt`)  
- complete workflow documentation  

## Data Availability

- **Satellite datasets** (Landsat 8/9, MODIS) accessed through **Google Earth Engine**  
- **Socio‑economic datasets** (EDSO 2017, NB_BUDENS) not included due to licensing restrictions  
** Socio‑economic datasets (EDSO 2017, NB_BUDENS) are publicly accessible but cannot be redistributed in this repository due to licensing terms.
**Users may obtain the datasets directly from the original providers.
---

## Contact

**Mahbubul Alam**  
Master’s in Forest Information Technology (FIT)  
HNEE, Eberswalde
