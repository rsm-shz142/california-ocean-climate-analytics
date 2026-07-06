import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate_regression(y_true, y_pred, model_name: str) -> dict:
    mse = mean_squared_error(y_true, y_pred)
    rmse = mse**0.5
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    return {
        "model": model_name,
        "rmse": rmse,
        "mae": mae,
        "r2": r2,
    }


def make_metrics_table(results: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(results).sort_values("rmse").reset_index(drop=True)
