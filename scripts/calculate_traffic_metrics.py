#!/usr/bin/env python3
"""Derive flow, density, and speed from interval vehicle counts."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate traffic-flow metrics from vehicle counts."
    )
    parser.add_argument("input", type=Path, help="CSV with vehicle_count.")
    parser.add_argument("output", type=Path, help="Destination CSV.")
    parser.add_argument(
        "--interval-seconds",
        type=float,
        default=10.0,
        help="Observation interval in seconds (default: 10).",
    )
    parser.add_argument(
        "--road-length-meters",
        type=float,
        default=20.0,
        help="Observed road length in meters (default: 20).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.interval_seconds <= 0 or args.road_length_meters <= 0:
        raise SystemExit("Interval and road length must be positive.")

    data = pd.read_csv(args.input)
    if "vehicle_count" not in data.columns:
        raise SystemExit("Input CSV must contain a vehicle_count column.")

    data["flow_veh_per_hour"] = (
        data["vehicle_count"] / args.interval_seconds * 3600.0
    )
    data["density_veh_per_km"] = (
        data["vehicle_count"] / args.road_length_meters * 1000.0
    )
    data["speed_km_per_hour"] = (
        data["flow_veh_per_hour"] / data["density_veh_per_km"]
    ).fillna(0.0)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(args.output, index=False)
    print(f"Wrote {len(data)} rows to {args.output}")


if __name__ == "__main__":
    main()
