from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.config import (
    RAW_DIR,
    ONI_RAW_DIR,
    OISST_RAW_DIR,
    PROCESSED_DIR,
    START_YEAR,
    END_YEAR,
)
from src.utils import ensure_dir, print_section
from src.download import (
    download_oni_raw,
    download_oisst_file,
    open_local_oisst_file,
)
from src.preprocess import (
    process_oni,
    subset_california,
    regional_daily_mean_sst,
)


def main():
    for folder in [RAW_DIR, ONI_RAW_DIR, OISST_RAW_DIR, PROCESSED_DIR]:
        ensure_dir(folder)

    print_section("Downloading ONI")
    oni_raw = download_oni_raw()
    oni = process_oni(oni_raw)

    oni_raw_path = ONI_RAW_DIR / "oni_noaa_cpc_raw.csv"
    oni_processed_path = PROCESSED_DIR / "oni_monthly.csv"

    oni_raw.to_csv(oni_raw_path, index=False)
    oni.to_csv(oni_processed_path, index=False)

    print(f"Saved raw ONI: {oni_raw_path}")
    print(f"Saved processed ONI: {oni_processed_path}")

    print_section("Downloading and processing California OISST")

    all_years = []

    years = list(range(START_YEAR, END_YEAR + 1))

    for i, year in enumerate(years, start=1):
        print(f"\nProcessing {year} ({i}/{len(years)})...")

        try:
            file_path = download_oisst_file(year)
            ds = open_local_oisst_file(file_path)

            ds_ca = subset_california(ds)
            daily = regional_daily_mean_sst(ds_ca)

            all_years.append(daily)

            ds.close()

            print(f"Finished {year}: {len(daily)} rows")

        except Exception as error:
            print(f"Failed {year}: {error}")

    sst = pd.concat(all_years, ignore_index=True)

    sst_path = PROCESSED_DIR / f"california_daily_sst_{START_YEAR}_{END_YEAR}.csv"
    sst.to_csv(sst_path, index=False)

    print(f"\nSaved California SST: {sst_path}")
    print(sst.head())


if __name__ == "__main__":
    main()
