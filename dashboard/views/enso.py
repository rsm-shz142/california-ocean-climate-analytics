import plotly.express as px
import streamlit as st

from components import section_intro


def render_enso(data):

    enso = data["enso"]

    st.title("🌎 ENSO Analysis")

    section_intro(
        "El Niño, La Niña, and California SST Anomalies",
        "This page examines how NOAA Oceanic Niño Index (ONI) relates to California coast SST anomalies and marine heatwave activity.",
    )

    corr = enso[["oni", "sst_anomaly"]].corr().loc["oni", "sst_anomaly"]
    corr_mhw = enso[["oni", "mhw_days"]].corr().loc["oni", "mhw_days"]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("ONI vs SST Anomaly Correlation", f"{corr:.3f}")

    with col2:
        st.metric("ONI vs Monthly MHW Days Correlation", f"{corr_mhw:.3f}")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        fig = px.scatter(
            enso,
            x="oni",
            y="sst_anomaly",
            color="enso_phase",
            trendline="ols",
            title="ONI vs SST Anomaly",
            labels={
                "oni": "ONI",
                "sst_anomaly": "SST Anomaly (°C)",
                "enso_phase": "ENSO Phase",
            },
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.box(
            enso,
            x="enso_phase",
            y="sst_anomaly",
            title="SST Anomaly by ENSO Phase",
            labels={"enso_phase": "ENSO Phase", "sst_anomaly": "SST Anomaly (°C)"},
        )

        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        fig = px.scatter(
            enso,
            x="oni",
            y="mhw_days",
            color="enso_phase",
            title="ONI vs Monthly Marine Heatwave Days",
            labels={"oni": "ONI", "mhw_days": "MHW Days", "enso_phase": "ENSO Phase"},
        )

        st.plotly_chart(fig, use_container_width=True)

    with col4:
        fig = px.box(
            enso,
            x="enso_phase",
            y="mhw_days",
            title="Monthly Marine Heatwave Days by ENSO Phase",
            labels={"enso_phase": "ENSO Phase", "mhw_days": "Monthly MHW Days"},
        )

        st.plotly_chart(fig, use_container_width=True)

    st.info(
        "ENSO is associated with California coast SST anomalies, but it is not the only driver. "
        "Regional SST is also affected by coastal upwelling, basin-scale variability, and local ocean-atmosphere conditions."
    )
