import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components import section_intro


def render_marine_heatwaves(data):

    daily = data["daily"]
    events = data["events"]
    annual = data["annual_mhw"]

    st.title("🔥 Marine Heatwave Detection")

    section_intro(
        "Marine Heatwave Events",
        "Marine heatwaves are detected when daily SST exceeds the seasonally varying 90th percentile threshold for at least five consecutive days.",
    )

    years = sorted(daily["year"].unique())

    selected_year = st.selectbox("Select Year", years, index=years.index(2015))

    plot_data = daily[daily["year"] == selected_year].copy()
    mhw_days = plot_data[plot_data["mhw_event_id"].notna()]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=plot_data["date"], y=plot_data["sst"], mode="lines", name="Daily SST"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=plot_data["date"],
            y=plot_data["threshold"],
            mode="lines",
            name="90th Percentile Threshold",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=mhw_days["date"],
            y=mhw_days["sst"],
            mode="markers",
            name="Marine Heatwave Days",
        )
    )

    fig.update_layout(
        title=f"Marine Heatwave Detection ({selected_year})",
        xaxis_title="Date",
        yaxis_title="SST (°C)",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            annual,
            x="year",
            y="event_count",
            title="Annual Marine Heatwave Events",
            labels={"year": "Year", "event_count": "Events"},
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            annual,
            x="year",
            y="total_mhw_days",
            title="Annual Marine Heatwave Days",
            labels={"year": "Year", "total_mhw_days": "Days"},
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Top 10 Strongest Marine Heatwave Events")

    display_events = (
        events.sort_values(by=["max_intensity", "duration_days"], ascending=False)
        .head(10)
        .copy()
    )

    display_events = display_events[
        [
            "event_id",
            "start_date",
            "end_date",
            "duration_days",
            "max_intensity",
            "mean_intensity",
        ]
    ]

    display_events.columns = [
        "Event ID",
        "Start",
        "End",
        "Duration (Days)",
        "Max Intensity (°C)",
        "Mean Intensity (°C)",
    ]

    st.dataframe(display_events, use_container_width=True, hide_index=True)

    st.info(
        "Marine heatwaves are detected using NOAA OISST daily observations and a "
        "seasonally varying 90th percentile threshold calculated from the 1982–2011 baseline period."
    )
