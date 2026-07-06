import plotly.express as px
import streamlit as st

from components import kpi_card, section_intro


def render_overview(data):
    daily = data["daily"]
    events = data["events"]
    metrics = data["metrics"]
    annual_mhw = data["annual_mhw"]

    avg_sst = daily["sst"].mean()
    total_days = len(daily)
    event_count = len(events)
    max_intensity = events["max_intensity"].max()
    best_model = metrics.sort_values("rmse").iloc[0]

    st.title("🌊 California Ocean Climate Analytics Platform")
    st.markdown(
        """
        Interactive decision-support platform for monitoring long-term ocean warming,
        marine heatwave events, ENSO variability, and short-term sea surface temperature
        forecasts along the California coast.
        """
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        kpi_card("🌡", f"{avg_sst:.2f} °C", "Average Regional SST")

    with col2:
        kpi_card("📅", f"{total_days:,}", "Daily NOAA Records")

    with col3:
        kpi_card("🔥", f"{event_count}", "Marine Heatwave Events")

    with col4:
        kpi_card("🤖", best_model["model"], "Best Forecast Model")

    st.divider()

    section_intro(
        "Executive Summary",
        "This project integrates NOAA ocean temperature observations, ENSO climate indices, "
        "marine heatwave detection, and machine learning forecasting into a single analytics workflow.",
    )

    col1, col2 = st.columns(2)

    annual_sst = daily.groupby("year", as_index=False)["sst"].mean()

    with col1:
        fig = px.line(
            annual_sst,
            x="year",
            y="sst",
            markers=True,
            title="Annual Mean SST Trend",
            labels={"year": "Year", "sst": "SST (°C)"},
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            metrics.sort_values("rmse"),
            x="model",
            y="rmse",
            title="Forecast Model RMSE",
            labels={"model": "Model", "rmse": "RMSE (°C)"},
        )
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        fig = px.bar(
            annual_mhw,
            x="year",
            y="total_mhw_days",
            title="Annual Marine Heatwave Days",
            labels={"year": "Year", "total_mhw_days": "MHW Days"},
        )
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        fig = px.scatter(
            data["enso"],
            x="oni",
            y="sst_anomaly",
            trendline="ols",
            title="ENSO and SST Anomaly Relationship",
            labels={"oni": "ONI", "sst_anomaly": "SST Anomaly (°C)"},
        )
        st.plotly_chart(fig, use_container_width=True)

    st.info(
        f"Key result: the strongest detected marine heatwave intensity reached "
        f"{max_intensity:.2f} °C above climatology, and the best current forecast model is "
        f"{best_model['model']} with RMSE {best_model['rmse']:.3f} °C."
    )
