import pandas as pd
import numpy as np


def create_forecast_features(df: pd.DataFrame, horizon_days: int = 7) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    df["month"] = df["date"].dt.month
    df["day_of_year"] = df["date"].dt.dayofyear

    df["sin_day"] = np.sin(2 * np.pi * df["day_of_year"] / 365.25)
    df["cos_day"] = np.cos(2 * np.pi * df["day_of_year"] / 365.25)

    for lag in [1, 2, 3, 7, 14, 30]:
        df[f"sst_lag_{lag}"] = df["sst"].shift(lag)

    df["sst_roll_mean_7"] = df["sst"].shift(1).rolling(7).mean()
    df["sst_roll_mean_30"] = df["sst"].shift(1).rolling(30).mean()
    df["sst_roll_std_7"] = df["sst"].shift(1).rolling(7).std()

    if "oni" in df.columns:
        df["oni_lag_1"] = df["oni"].shift(1)
    else:
        df["oni_lag_1"] = np.nan

    if "sst_anomaly" in df.columns:
        df["sst_anomaly_lag_1"] = df["sst_anomaly"].shift(1)
    else:
        df["sst_anomaly_lag_1"] = np.nan

    df["target_sst_7d_ahead"] = df["sst"].shift(-horizon_days)

    df = df.dropna().reset_index(drop=True)

    return df


def get_feature_columns() -> list[str]:
    return [
        "month",
        "sin_day",
        "cos_day",
        "sst_lag_1",
        "sst_lag_2",
        "sst_lag_3",
        "sst_lag_7",
        "sst_lag_14",
        "sst_lag_30",
        "sst_roll_mean_7",
        "sst_roll_mean_30",
        "sst_roll_std_7",
        "oni_lag_1",
        "sst_anomaly_lag_1",
    ]
