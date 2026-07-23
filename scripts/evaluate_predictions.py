#!/usr/bin/env python3
"""Evaluate the stored congestion-index prediction files."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np
import pandas as pd


ACTUAL_COLUMN = "阻塞系数实际值"
PREDICTED_COLUMN = "阻塞系数预测值"
MODEL_FILES = {
    "Gradient Boosting": "full_tpi_prediction_results_window_final_gb_梯度.xlsx",
    "Random Forest": "full_tpi_prediction_results_window_final_rf.xlsx",
    "XGBoost": "full_tpi_prediction_results_window_final_xgb.xlsx",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute MAE, RMSE, and R² from stored predictions."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data/model-outputs"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/model-comparison.csv"),
    )
    return parser.parse_args()


def evaluate(path: Path) -> dict[str, float | int]:
    data = pd.read_excel(path)
    pairs = data[[ACTUAL_COLUMN, PREDICTED_COLUMN]].dropna()
    actual = pairs[ACTUAL_COLUMN].to_numpy(dtype=float)
    predicted = pairs[PREDICTED_COLUMN].to_numpy(dtype=float)
    residual = actual - predicted

    mae = float(np.mean(np.abs(residual)))
    rmse = float(np.sqrt(np.mean(np.square(residual))))
    denominator = float(np.sum(np.square(actual - actual.mean())))
    r_squared = 1.0 - float(np.sum(np.square(residual))) / denominator

    return {
        "stored_rows": len(data),
        "evaluation_rows": len(pairs),
        "missing_prediction_rows": len(data) - len(pairs),
        "mae": mae,
        "rmse": rmse,
        "r_squared": r_squared,
    }


def main() -> None:
    args = parse_args()
    rows = []
    for model, filename in MODEL_FILES.items():
        metrics = evaluate(args.data_dir / filename)
        rows.append({"model": model, **metrics})

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    for row in sorted(rows, key=lambda item: item["rmse"]):
        print(
            f"{row['model']}: RMSE={row['rmse']:.6f}, "
            f"MAE={row['mae']:.6f}, R²={row['r_squared']:.6f}, "
            f"n={row['evaluation_rows']}"
        )


if __name__ == "__main__":
    main()
