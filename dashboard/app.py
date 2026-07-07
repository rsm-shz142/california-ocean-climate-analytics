import streamlit as st

from data import load_dashboard_data
from components import sidebar_brand
from views.overview import render_overview
from views.trends import render_trends
from views.marine_heatwaves import render_marine_heatwaves
from views.enso import render_enso
from views.forecasting import render_forecasting
from views.about import render_about


st.set_page_config(
    page_title="California Ocean Climate Analytics",
    page_icon="🌊",
    layout="wide",
)

data = load_dashboard_data()

sidebar_brand()

page = st.sidebar.radio(
    "Explore",
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
