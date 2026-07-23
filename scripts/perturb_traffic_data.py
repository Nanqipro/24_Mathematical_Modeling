#!/usr/bin/env python3
"""Create a deterministic perturbed copy for sensitivity experiments.

This utility must not be used to replace source observations or to report
primary research results. It exists only to reproduce the repository's
historical perturbation experiment with an explicit random seed.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scale flow and density for a documented sensitivity run."
    )
    parser.add_argument("input", type=Path, help="Source .xlsx file.")
    parser.add_argument("output", type=Path, help="Destination .xlsx file.")
    parser.add_argument("--seed", type=int, default=2024)
    parser.add_argument("--low", type=float, default=0.9)
    parser.add_argument("--high", type=float, default=1.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not 0 < args.low <= args.high:
        raise SystemExit("Expected 0 < low <= high.")

    data = pd.read_excel(args.input)
    missing = {"flow", "density"} - set(data.columns)
    if missing:
        raise SystemExit(f"Missing required columns: {sorted(missing)}")

    rng = np.random.default_rng(args.seed)
    data["flow"] = (
        data["flow"] * rng.uniform(args.low, args.high, len(data))
    ).round().astype(int)
    data["density"] = (
        data["density"] * rng.uniform(args.low, args.high, len(data))
    ).round().astype(int)
    data["speed"] = (
        data["flow"].div(data["density"].replace(0, np.nan)).mul(10)
    ).replace([np.inf, -np.inf], np.nan).fillna(0.0)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    data.to_excel(args.output, index=False)
    print(f"Wrote {len(data)} rows to {args.output} using seed {args.seed}")


if __name__ == "__main__":
    main()
