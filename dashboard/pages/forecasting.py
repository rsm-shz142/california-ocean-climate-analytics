import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from components import section_intro


def render_forecasting(data):

    metrics = data["metrics"]
    predictions = data["predictions"]

    st.title("🤖 SST Forecasting")

    section_intro(
        "Short-Term Sea Surface Temperature Forecast",
        "Machine learning models were trained to predict California coast regional mean SST seven days ahead using historical SST, rolling statistics, seasonality, and climate indices.",
    )

    st.subheader("Forecast Model Performance")

    st.dataframe(
        metrics,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    best_model = metrics.sort_values("rmse").iloc[0]

    with col1:
        st.metric("Best Model", best_model["model"])

    with col2:
        st.metric("RMSE", f"{best_model['rmse']:.3f} °C")

    with col3:
        st.metric("MAE", f"{best_model['mae']:.3f} °C")

    st.divider()

    model_dict = {
        "Persistence Baseline": "persistence_pred",
        "Linear Regression": "linear_regression_pred",
        "Random Forest": "random_forest_pred",
    }

    if "xgboost_pred" in predictions.columns:
        model_dict["XGBoost"] = "xgboost_pred"

    selected_model = st.selectbox(
        "Forecast Model",
        list(model_dict.keys()),
        index=list(model_dict.keys()).index("Random Forest"),
    )

    pred_column = model_dict[selected_model]

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date", value=predictions["date"].min())

    with col2:
        end_date = st.date_input("End Date", value=predictions["date"].max())

    plot_df = predictions[
        (predictions["date"] >= pd.to_datetime(start_date))
        & (predictions["date"] <= pd.to_datetime(end_date))
    ].copy()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=plot_df["date"],
            y=plot_df["actual_7d_ahead_sst"],
            mode="lines",
            name="Actual SST",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=plot_df["date"],
            y=plot_df[pred_column],
            mode="lines",
            name=selected_model,
        )
    )

    fig.update_layout(
        title=f"{selected_model}: 7-Day Ahead SST Forecast",
        xaxis_title="Date",
        yaxis_title="Sea Surface Temperature (°C)",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Model Comparison")

    fig = px.bar(
        metrics.sort_values("rmse"),
        x="model",
        y="rmse",
        color="rmse",
        title="Forecast RMSE Comparison",
        labels={"model": "Model", "rmse": "RMSE (°C)"},
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "Forecast models use lagged SST observations, rolling statistics, seasonal features, and climate indicators. "
        "Models are evaluated using chronological train/test split together with time-series cross-validation."
    )
