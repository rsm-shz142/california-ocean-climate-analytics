
# California Ocean Climate Analytics Platform

An end-to-end business analytics portfolio project using official NOAA ocean data to analyze California coast sea surface temperature trends, detect marine heatwave events, investigate ENSO impacts, and build short-term SST forecasting models.

## Project Highlights

- Processed NOAA OISST daily sea surface temperature data from 1982 to 2024.
- Built a reproducible Python data pipeline for California coast SST extraction.
- Detected marine heatwave events using daily climatology and a 90th percentile threshold.
- Analyzed the relationship between NOAA ONI and California SST anomalies.
- Built 7-day ahead SST forecasting models using baseline, Linear Regression, and Random Forest.
- Designed an interactive Streamlit + Plotly dashboard for project demonstration.

## Data Sources

- NOAA OISST v2.1 Daily Sea Surface Temperature
- NOAA CPC Oceanic Niño Index (ONI)

Raw NOAA NetCDF files are not stored in this repository. The project provides scripts to download and process the data.

## Project Structure

```text
.
├── dashboard/
│   ├── app.py
│   ├── components.py
│   ├── data.py
│   └── pages/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── scripts/
│   └── download_data.py
├── src/
│   ├── config.py
│   ├── download.py
│   ├── preprocess.py
│   ├── marine_heatwaves.py
│   ├── features.py
│   ├── modeling.py
│   └── evaluation.py
├── README.md
└── requirements.txt
```
