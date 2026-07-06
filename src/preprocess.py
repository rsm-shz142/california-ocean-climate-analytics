import numpy as np
import pandas as pd
import xarray as xr

from src.config import LAT_MIN, LAT_MAX, LON_MIN, LON_MAX


def process_oni(oni_raw: pd.DataFrame) -> pd.DataFrame:
    season_to_month = {
        "DJF": 1,
        "JFM": 2,
        "FMA": 3,
        "MAM": 4,
        "AMJ": 5,
        "MJJ": 6,
        "JJA": 7,
        "JAS": 8,
        "ASO": 9,
        "SON": 10,
        "OND": 11,
        "NDJ": 12,
    }

    oni = oni_raw.copy()
    oni["month"] = oni["SEAS"].map(season_to_month)

    oni["date"] = pd.to_datetime(dict(year=oni["YR"], month=oni["month"], day=1))

    oni = oni.rename(
        columns={
            "SEAS": "season",
            "YR": "year",
            "TOTAL": "nino34_sst",
            "ANOM": "oni",
        }
    )

    oni["enso_phase"] = np.select(
        [oni["oni"] >= 0.5, oni["oni"] <= -0.5],
        ["El Niño", "La Niña"],
        default="Neutral",
    )

    oni = oni[["date", "year", "month", "season", "nino34_sst", "oni", "enso_phase"]]

    return oni.sort_values("date").reset_index(drop=True)


def subset_california(ds: xr.Dataset) -> xr.Dataset:
    return ds.sel(
        lat=slice(LAT_MIN, LAT_MAX),
        lon=slice(LON_MIN, LON_MAX),
    )


def regional_daily_mean_sst(ds_ca: xr.Dataset) -> pd.DataFrame:
    daily = (
        ds_ca["sst"]
        .mean(dim=["lat", "lon"], skipna=True)
        .to_dataframe()
        .reset_index()
        .rename(columns={"time": "date"})
    )

    daily["date"] = pd.to_datetime(daily["date"])
    daily["year"] = daily["date"].dt.year

    return daily[["date", "year", "sst"]]
