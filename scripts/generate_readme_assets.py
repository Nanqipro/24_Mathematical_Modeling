#!/usr/bin/env python3
"""Regenerate the data-backed SVG charts used by the project README."""

from __future__ import annotations

import argparse
import csv
from html import escape
from pathlib import Path

import pandas as pd


COLORS = {
    "ink": "#0F172A",
    "muted": "#64748B",
    "cyan": "#06B6D4",
    "blue": "#2563EB",
    "amber": "#F59E0B",
    "grid": "#CBD5E1",
    "panel": "#F8FAFC",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate README SVG charts.")
    parser.add_argument(
        "--metrics",
        type=Path,
        default=Path("results/model-comparison.csv"),
    )
    parser.add_argument(
        "--counts-dir",
        type=Path,
        default=Path("data/vehicle-counts"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/readme-assets"),
    )
    return parser.parse_args()


def svg_document(width: int, height: int, body: str, title: str) -> str:
    display_width = width // 2
    display_height = height // 2
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{display_width}" height="{display_height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">Data-backed chart generated from repository files.</desc>
  <rect width="{width}" height="{height}" rx="24" fill="#FFFFFF"/>
  {body}
</svg>
"""


def text(
    x: float,
    y: float,
    value: str,
    *,
    size: int = 16,
    color: str = COLORS["ink"],
    weight: int = 400,
    anchor: str = "start",
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter,Arial,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{color}" '
        f'text-anchor="{anchor}">{escape(value)}</text>'
    )


def plot_model_metrics(metrics_path: Path, output_path: Path) -> None:
    with metrics_path.open(encoding="utf-8", newline="") as handle:
        rows = sorted(
            list(csv.DictReader(handle)),
            key=lambda row: float(row["rmse"]),
        )

    width, height = 1040, 500
    left, right, top = 250, 70, 128
    plot_width = width - left - right
    max_error = max(float(row["rmse"]) for row in rows) * 1.18
    body = [
        text(54, 58, "Congestion-index prediction comparison", size=26, weight=700),
        text(
            54,
            88,
            "Recomputed on 4,351 non-missing stored prediction pairs per model",
            size=14,
            color=COLORS["muted"],
        ),
    ]

    for tick in range(5):
        value = max_error * tick / 4
        x = left + plot_width * tick / 4
        body.append(
            f'<line x1="{x:.1f}" y1="{top - 18}" x2="{x:.1f}" y2="{height - 70}" '
            f'stroke="{COLORS["grid"]}" stroke-width="1"/>'
        )
        body.append(
            text(
                x,
                height - 44,
                f"{value:.3f}",
                size=12,
                color=COLORS["muted"],
                anchor="middle",
            )
        )

    for index, row in enumerate(rows):
        y = top + index * 104
        model = row["model"]
        mae = float(row["mae"])
        rmse = float(row["rmse"])
        r_squared = float(row["r_squared"])
        body.append(text(left - 18, y + 28, model, size=15, weight=600, anchor="end"))
        body.append(
            f'<rect x="{left}" y="{y}" width="{plot_width * mae / max_error:.1f}" '
            f'height="24" rx="6" fill="{COLORS["cyan"]}"/>'
        )
        body.append(
            f'<rect x="{left}" y="{y + 34}" width="{plot_width * rmse / max_error:.1f}" '
            f'height="24" rx="6" fill="{COLORS["blue"]}"/>'
        )
        body.append(
            text(
                left + plot_width * rmse / max_error + 10,
                y + 52,
                f"R² {r_squared:.4f}",
                size=12,
                color=COLORS["muted"],
            )
        )

    body.extend(
        [
            f'<rect x="54" y="432" width="14" height="14" rx="3" fill="{COLORS["cyan"]}"/>',
            text(76, 444, "MAE", size=12, color=COLORS["muted"]),
            f'<rect x="130" y="432" width="14" height="14" rx="3" fill="{COLORS["blue"]}"/>',
            text(152, 444, "RMSE", size=12, color=COLORS["muted"]),
            text(
                width - 54,
                444,
                "Error (lower is better)",
                size=12,
                color=COLORS["muted"],
                anchor="end",
            ),
        ]
    )
    output_path.write_text(
        svg_document(width, height, "\n  ".join(body), "Model comparison"),
        encoding="utf-8",
    )


def load_point_summary(counts_dir: Path) -> list[dict[str, float | int | str]]:
    point_map = {
        "107": "Point 1 · 107",
        "105": "Point 2 · 105",
        "108": "Point 3 · 108",
        "103": "Point 4 · 103",
    }
    rows = []
    for suffix, label in point_map.items():
        files = sorted(counts_dir.glob(f"{suffix}traffic_data*.csv"))
        combined = pd.concat(
            [pd.read_csv(path)[["vehicle_count"]] for path in files],
            ignore_index=True,
        )
        rows.append(
            {
                "point": label,
                "mean": float(combined["vehicle_count"].mean()),
                "peak": int(combined["vehicle_count"].max()),
                "samples": len(combined),
            }
        )
    return rows


def plot_traffic_counts(counts_dir: Path, output_path: Path) -> None:
    rows = load_point_summary(counts_dir)
    width, height = 1040, 500
    left, right, top, bottom = 100, 54, 126, 112
    plot_width = width - left - right
    plot_height = height - top - bottom
    max_count = max(int(row["peak"]) for row in rows)
    body = [
        text(54, 58, "Observed vehicle counts by monitoring point", size=26, weight=700),
        text(
            54,
            88,
            "Mean and peak counts across the repository's 10-second records",
            size=14,
            color=COLORS["muted"],
        ),
    ]

    for tick in range(5):
        value = max_count * tick / 4
        y = top + plot_height - plot_height * tick / 4
        body.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{width - right}" y2="{y:.1f}" '
            f'stroke="{COLORS["grid"]}" stroke-width="1"/>'
        )
        body.append(
            text(
                left - 14,
                y + 5,
                f"{value:.0f}",
                size=12,
                color=COLORS["muted"],
                anchor="end",
            )
        )

    group_width = plot_width / len(rows)
    bar_width = 52
    for index, row in enumerate(rows):
        center = left + group_width * (index + 0.5)
        mean_height = plot_height * float(row["mean"]) / max_count
        peak_height = plot_height * int(row["peak"]) / max_count
        mean_x = center - bar_width - 7
        peak_x = center + 7
        body.append(
            f'<rect x="{mean_x:.1f}" y="{top + plot_height - mean_height:.1f}" '
            f'width="{bar_width}" height="{mean_height:.1f}" rx="7" fill="{COLORS["cyan"]}"/>'
        )
        body.append(
            f'<rect x="{peak_x:.1f}" y="{top + plot_height - peak_height:.1f}" '
            f'width="{bar_width}" height="{peak_height:.1f}" rx="7" fill="{COLORS["amber"]}"/>'
        )
        body.append(
            text(
                center,
                top + plot_height + 30,
                str(row["point"]),
                size=13,
                weight=600,
                anchor="middle",
            )
        )
        body.append(
            text(
                center,
                top + plot_height + 53,
                f"n={int(row['samples']):,}",
                size=11,
                color=COLORS["muted"],
                anchor="middle",
            )
        )

    body.extend(
        [
            f'<rect x="54" y="452" width="14" height="14" rx="3" fill="{COLORS["cyan"]}"/>',
            text(76, 464, "Mean", size=12, color=COLORS["muted"]),
            f'<rect x="136" y="452" width="14" height="14" rx="3" fill="{COLORS["amber"]}"/>',
            text(158, 464, "Peak", size=12, color=COLORS["muted"]),
        ]
    )
    output_path.write_text(
        svg_document(width, height, "\n  ".join(body), "Traffic count summary"),
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    plot_model_metrics(args.metrics, args.output_dir / "model-performance.svg")
    plot_traffic_counts(args.counts_dir, args.output_dir / "traffic-counts.svg")
    print(f"Wrote README charts to {args.output_dir}")


if __name__ == "__main__":
    main()
