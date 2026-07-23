#!/usr/bin/env python3
"""Add regular timestamps to frame/count records exported by the tracker."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Add timestamps to two-line frame/count records."
    )
    parser.add_argument("input", type=Path, help="Tracker text output.")
    parser.add_argument("output", type=Path, help="Timestamped text output.")
    parser.add_argument(
        "--start",
        required=True,
        help="Start time in ISO format, for example 2024-05-01T11:41:03.",
    )
    parser.add_argument(
        "--step-seconds",
        type=float,
        default=10.0,
        help="Time increment between records (default: 10).",
    )
    return parser.parse_args()


def load_records(path: Path) -> list[list[str]]:
    records: list[list[str]] = []
    current: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            current.append(line)
        elif current:
            records.append(current)
            current = []
    if current:
        records.append(current)
    return records


def main() -> None:
    args = parse_args()
    start = datetime.fromisoformat(args.start)
    step = timedelta(seconds=args.step_seconds)
    records = load_records(args.input)

    output_lines: list[str] = []
    for index, record in enumerate(records):
        timestamp = start + index * step
        output_lines.append(f"Timestamp: {timestamp:%Y-%m-%d %H:%M:%S}")
        output_lines.extend(record)
        output_lines.append("")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(output_lines), encoding="utf-8")
    print(f"Wrote {len(records)} timestamped records to {args.output}")


if __name__ == "__main__":
    main()
