import streamlit as st

from components import section_intro


def render_about(data):

    daily = data["daily"]
    events = data["events"]

    st.title("ℹ Project Overview")

    st.markdown(
        """
# California Ocean Climate Analytics Platform

An end-to-end business analytics project built using official NOAA ocean observations
to investigate long-term sea surface temperature variability, detect marine heatwave
events, analyze ENSO impacts, and forecast regional SST along the California coast.
"""
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        section_intro(
            "Project Scope",
            """
• Study Region: California Coast

• Time Period: 1982–2024

• Spatial Resolution: NOAA OISST 0.25°

• Temporal Resolution: Daily
""",
        )

    with col2:
        section_intro(
            "Datasets",
            """
• NOAA OISST v2.1 Daily SST

• NOAA Oceanic Niño Index (ONI)

• 43 Years of Daily Observations
""",
        )

    st.divider()

    section_intro("Analytics Pipeline", "")

    st.code(
        """
NOAA OISST + NOAA ONI

        ↓

Data Acquisition

        ↓

Preprocessing

        ↓

Exploratory Data Analysis

        ↓

Marine Heatwave Detection

        ↓

ENSO Impact Analysis

        ↓

Machine Learning Forecasting

        ↓

Interactive Dashboard
"""
    )

    st.divider()

    section_intro("Methods", "")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
### Climate Analytics

- Daily SST climatology

- SST anomaly calculation

- Marine heatwave detection

- ENSO phase analysis

- Lag correlation
"""
        )

    with col2:
        st.markdown(
            """
### Machine Learning

- Feature Engineering

- Time Series Split

- Linear Regression

- Random Forest

- XGBoost-ready Pipeline
"""
        )

    st.divider()

    section_intro("Project Statistics", "")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Years", "43")

    col2.metric("Daily Records", f"{len(daily):,}")

    col3.metric("Marine Heatwave Events", f"{len(events)}")

    col4.metric("Dashboard Pages", "6")

    st.divider()

    section_intro("Future Improvements", "")

    st.markdown(
        """
- Full Hobday et al. (2016) marine heatwave implementation

- Spatial marine heatwave detection (grid-level)

- XGBoost model optimization

- LSTM / Temporal Fusion Transformer comparison

- Cloud deployment

- Automated NOAA daily updates
"""
    )

    st.divider()

    st.success(
        "Developed as an M.S. Business Analytics portfolio project "
        "using official NOAA datasets."
    )
