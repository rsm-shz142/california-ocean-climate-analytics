import io
from pathlib import Path

import pandas as pd
import requests
import urllib3
import xarray as xr

from src.config import ONI_URL, OISST_FILE_URL_TEMPLATE, OISST_RAW_DIR

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def download_oni_raw() -> pd.DataFrame:
    response = requests.get(ONI_URL, verify=False, timeout=30)
    response.raise_for_status()

    return pd.read_csv(io.StringIO(response.text), sep=r"\s+")


def download_oisst_file(year: int) -> Path:
    OISST_RAW_DIR.mkdir(parents=True, exist_ok=True)

    url = OISST_FILE_URL_TEMPLATE.format(year=year)
    output_path = OISST_RAW_DIR / f"sst.day.mean.{year}.nc"

    if output_path.exists():
        try:
            with xr.open_dataset(output_path) as ds:
                _ = ds["sst"].shape
            print(f"Using existing valid file: {output_path.name}")
            return output_path
        except Exception:
            print(f"Existing file is corrupted. Re-downloading: {output_path.name}")
            output_path.unlink()

    print(f"Downloading OISST file for {year}...")

    with requests.get(url, stream=True, verify=False, timeout=300) as response:
        response.raise_for_status()

        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    return output_path


def open_local_oisst_file(path: Path) -> xr.Dataset:
    return xr.open_dataset(path)
