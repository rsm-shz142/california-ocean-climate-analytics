import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit

try:
    from xgboost import XGBRegressor

    XGBOOST_AVAILABLE = True
    XGBOOST_IMPORT_ERROR = None
except Exception as error:
    XGBRegressor = None
    XGBOOST_AVAILABLE = False
    XGBOOST_IMPORT_ERROR = error


def temporal_train_test_split(df: pd.DataFrame, test_start_date: str):
    train = df[df["date"] < test_start_date].copy()
    test = df[df["date"] >= test_start_date].copy()
    return train, test


def persistence_forecast(test_df: pd.DataFrame) -> np.ndarray:
    return test_df["sst_lag_7"].values


def train_linear_regression(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def train_random_forest(X_train, y_train):
    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=12,
        min_samples_leaf=3,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)
    return model


def train_xgboost(X_train, y_train):
    if not XGBOOST_AVAILABLE:
        raise ImportError(
            f"XGBoost is not available in this environment: {XGBOOST_IMPORT_ERROR}"
        )

    model = XGBRegressor(
        n_estimators=400,
        max_depth=4,
        learning_rate=0.03,
        subsample=0.9,
        colsample_bytree=0.9,
        objective="reg:squarederror",
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)
    return model


def time_series_cv_scores(model_factory, X, y, n_splits: int = 5):
    tscv = TimeSeriesSplit(n_splits=n_splits)
    scores = []

    for fold, (train_idx, val_idx) in enumerate(tscv.split(X), start=1):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

        model = model_factory()
        model.fit(X_train, y_train)
        pred = model.predict(X_val)

        rmse = np.sqrt(((y_val - pred) ** 2).mean())
        mae = np.abs(y_val - pred).mean()

        scores.append(
            {
                "fold": fold,
                "rmse": rmse,
                "mae": mae,
            }
        )

    return pd.DataFrame(scores)
