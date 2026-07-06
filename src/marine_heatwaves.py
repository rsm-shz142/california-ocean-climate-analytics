import numpy as np
import pandas as pd


EVENT_COLUMNS = [
    "event_id",
    "start_date",
    "end_date",
    "duration_days",
    "max_intensity",
    "mean_intensity",
    "cumulative_intensity",
    "year",
]


def add_day_of_year(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["day_of_year"] = df["date"].dt.dayofyear

    # 为了避免 leap day 影响 365-day climatology，先移除 Feb 29
    df = df[~((df["date"].dt.month == 2) & (df["date"].dt.day == 29))].copy()

    # 移除 Feb 29 后重新计算 day_of_year，让每年都是 365 天
    df["day_of_year"] = df["date"].dt.strftime("%j").astype(int)
    df.loc[df["date"].dt.is_leap_year & (df["day_of_year"] > 60), "day_of_year"] -= 1

    return df


def calculate_climatology(
    df: pd.DataFrame,
    baseline_start: int = 1982,
    baseline_end: int = 2011,
    percentile: float = 0.9,
) -> pd.DataFrame:
    df = add_day_of_year(df)

    baseline = df[(df["year"] >= baseline_start) & (df["year"] <= baseline_end)].copy()

    climatology = (
        baseline.groupby("day_of_year")["sst"]
        .agg(
            climatological_mean="mean",
            threshold=lambda x: x.quantile(percentile),
        )
        .reset_index()
    )

    return climatology


def add_anomalies_and_thresholds(
    df: pd.DataFrame, climatology: pd.DataFrame
) -> pd.DataFrame:
    df = add_day_of_year(df)

    merged = df.merge(climatology, on="day_of_year", how="left")

    merged["sst_anomaly"] = merged["sst"] - merged["climatological_mean"]
    merged["threshold_anomaly"] = merged["threshold"] - merged["climatological_mean"]
    merged["above_threshold"] = merged["sst"] > merged["threshold"]

    return merged


def detect_marine_heatwaves(
    df: pd.DataFrame, min_duration: int = 5
) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = df.copy().sort_values("date").reset_index(drop=True)
    df["mhw_event_id"] = np.nan

    event_id = 0
    current_event_days = []

    for idx, row in df.iterrows():
        if row["above_threshold"]:
            current_event_days.append(idx)
        else:
            if len(current_event_days) >= min_duration:
                event_id += 1
                df.loc[current_event_days, "mhw_event_id"] = event_id
            current_event_days = []

    if len(current_event_days) >= min_duration:
        event_id += 1
        df.loc[current_event_days, "mhw_event_id"] = event_id

    events = []

    for eid, group in df.dropna(subset=["mhw_event_id"]).groupby("mhw_event_id"):
        events.append(
            {
                "event_id": int(eid),
                "start_date": group["date"].min(),
                "end_date": group["date"].max(),
                "duration_days": len(group),
                "max_intensity": group["sst_anomaly"].max(),
                "mean_intensity": group["sst_anomaly"].mean(),
                "cumulative_intensity": group["sst_anomaly"].sum(),
                "year": group["date"].dt.year.mode().iloc[0],
            }
        )

    events_df = pd.DataFrame(events, columns=EVENT_COLUMNS)

    return df, events_df


def summarize_events_by_year(events_df: pd.DataFrame) -> pd.DataFrame:
    if events_df.empty:
        return pd.DataFrame(
            columns=[
                "year",
                "event_count",
                "total_mhw_days",
                "max_duration",
                "max_intensity",
                "cumulative_intensity",
            ]
        )

    return (
        events_df.groupby("year")
        .agg(
            event_count=("event_id", "count"),
            total_mhw_days=("duration_days", "sum"),
            max_duration=("duration_days", "max"),
            max_intensity=("max_intensity", "max"),
            cumulative_intensity=("cumulative_intensity", "sum"),
        )
        .reset_index()
        .sort_values("year")
    )
