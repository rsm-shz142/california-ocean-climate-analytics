from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"

ONI_RAW_DIR = RAW_DIR / "oni"
OISST_RAW_DIR = RAW_DIR / "oisst"

START_YEAR = 1982
END_YEAR = 2024

LAT_MIN = 30
LAT_MAX = 42
LON_MIN = 235
LON_MAX = 246

ONI_URL = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"

OISST_FILE_URL_TEMPLATE = (
    "https://downloads.psl.noaa.gov/Datasets/noaa.oisst.v2.highres/"
    "sst.day.mean.{year}.nc"
)
