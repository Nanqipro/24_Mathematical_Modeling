#!/usr/bin/env python3
"""Convert timestamped tracker text into a tidy vehicle-count CSV."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


TIMESTAMP_RE = re.compile(r"^Timestamp:\s*(.+?)\s*$")
COUNT_RE = re.compile(r"^Vehicle Count:\s*(\d+)\s*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract timestamp and vehicle count pairs from tracker text."
    )
    parser.add_argument("input", type=Path, help="Timestamped tracker text.")
    parser.add_argument("output", type=Path, help="Destination CSV.")
    return parser.parse_args()


def extract_rows(path: Path) -> list[tuple[str, int]]:
    rows: list[tuple[str, int]] = []
    timestamp: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        timestamp_match = TIMESTAMP_RE.match(line)
        if timestamp_match:
            timestamp = timestamp_match.group(1)
            continue

        count_match = COUNT_RE.match(line)
        if count_match and timestamp is not None:
            rows.append((timestamp, int(count_match.group(1))))
            timestamp = None

    return rows


def main() -> None:
    args = parse_args()
    rows = extract_rows(args.input)
    if not rows:
        raise SystemExit("No timestamp/count pairs were found.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["timestamps", "vehicle_count"])
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
