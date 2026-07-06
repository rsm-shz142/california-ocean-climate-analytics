from pathlib import Path
import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


@st.cache_data
def load_dashboard_data():
    daily = pd.read_csv(PROCESSED_DIR / "mhw_daily_labeled_1982_2024.csv")
    events = pd.read_csv(PROCESSED_DIR / "mhw_events_1982_2024.csv")
    annual_mhw = pd.read_csv(PROCESSED_DIR / "mhw_annual_summary_1982_2024.csv")
    enso = pd.read_csv(PROCESSED_DIR / "monthly_sst_anomaly_oni_1982_2024.csv")
    metrics = pd.read_csv(PROCESSED_DIR / "forecast_model_metrics_1982_2024.csv")
    predictions = pd.read_csv(PROCESSED_DIR / "forecast_predictions_1982_2024.csv")

    daily["date"] = pd.to_datetime(daily["date"])
    events["start_date"] = pd.to_datetime(events["start_date"])
    events["end_date"] = pd.to_datetime(events["end_date"])
    enso["date"] = pd.to_datetime(enso["date"])
    predictions["date"] = pd.to_datetime(predictions["date"])

    return {
        "daily": daily,
        "events": events,
        "annual_mhw": annual_mhw,
        "enso": enso,
        "metrics": metrics,
        "predictions": predictions,
    }
