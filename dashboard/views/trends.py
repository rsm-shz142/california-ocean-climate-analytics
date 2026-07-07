import plotly.express as px
import streamlit as st

from components import section_intro


def render_trends(data):
    daily = data["daily"]

    st.title("🌡 SST Trends")

    section_intro(
        "Long-Term Sea Surface Temperature Patterns",
        "This page explores California coast regional mean sea surface temperature from 1982 to 2024, including daily variability, annual trends, and seasonal cycles.",
    )

    annual_sst = daily.groupby("year", as_index=False)["sst"].mean()

    fig = px.line(
        annual_sst,
        x="year",
        y="sst",
        markers=True,
        title="Annual Mean SST - California Coast",
        labels={"year": "Year", "sst": "SST (°C)"},
    )
    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(
        daily,
        x="date",
        y="sst",
        title="Daily Regional Mean SST, 1982–2024",
        labels={"date": "Date", "sst": "SST (°C)"},
    )
    st.plotly_chart(fig, use_container_width=True)

    daily_copy = daily.copy()
    daily_copy["month"] = daily_copy["date"].dt.month

    monthly_sst = daily_copy.groupby("month", as_index=False)["sst"].mean()

    fig = px.line(
        monthly_sst,
        x="month",
        y="sst",
        markers=True,
        title="Average Seasonal SST Cycle",
        labels={"month": "Month", "sst": "SST (°C)"},
    )
    st.plotly_chart(fig, use_container_width=True)
