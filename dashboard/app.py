import streamlit as st

from data import load_dashboard_data
from pages.overview import render_overview
from pages.trends import render_trends
from pages.marine_heatwaves import render_marine_heatwaves
from pages.enso import render_enso
from pages.forecasting import render_forecasting
from pages.about import render_about


st.set_page_config(
    page_title="California Ocean Climate Analytics",
    page_icon="🌊",
    layout="wide",
)


data = load_dashboard_data()

st.sidebar.title("🌊 Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Overview",
        "🌡 SST Trends",
        "🔥 Marine Heatwaves",
        "🌎 ENSO Analysis",
        "🤖 Forecasting",
        "ℹ About",
    ],
)


if page == "🏠 Overview":
    render_overview(data)
elif page == "🌡 SST Trends":
    render_trends(data)
elif page == "🔥 Marine Heatwaves":
    render_marine_heatwaves(data)
elif page == "🌎 ENSO Analysis":
    render_enso(data)
elif page == "🤖 Forecasting":
    render_forecasting(data)
elif page == "ℹ About":
    render_about(data)
