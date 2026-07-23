from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]


class ReleaseToolTests(unittest.TestCase):
    def run_script(self, name: str, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / name), *args],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    def test_text_to_metrics_pipeline(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temp_dir = Path(directory)
            raw = temp_dir / "raw.txt"
            timestamped = temp_dir / "timestamped.txt"
            counts = temp_dir / "counts.csv"
            metrics = temp_dir / "metrics.csv"
            raw.write_text(
                "Frame 1 Results\nVehicle Count: 2\n\n"
                "Frame 2 Results\nVehicle Count: 4\n",
                encoding="utf-8",
            )

            self.run_script(
                "add_timestamps.py",
                str(raw),
                str(timestamped),
                "--start",
                "2024-05-01T12:00:00",
                "--step-seconds",
                "10",
            )
            self.run_script(
                "extract_vehicle_counts.py",
                str(timestamped),
                str(counts),
            )
            self.run_script(
                "calculate_traffic_metrics.py",
                str(counts),
                str(metrics),
                "--interval-seconds",
                "10",
                "--road-length-meters",
                "20",
            )

            output = pd.read_csv(metrics)
            self.assertEqual(output["vehicle_count"].tolist(), [2, 4])
            self.assertEqual(
                output["flow_veh_per_hour"].tolist(),
                [720.0, 1440.0],
            )
            self.assertEqual(
                output["density_veh_per_km"].tolist(),
                [100.0, 200.0],
            )
            self.assertEqual(
                output["speed_km_per_hour"].tolist(),
                [7.2, 7.2],
            )

    def test_prediction_metrics_are_reproducible(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "model-comparison.csv"
            self.run_script(
                "evaluate_predictions.py",
                "--output",
                str(output),
            )
            with output.open(encoding="utf-8", newline="") as handle:
                rows = {row["model"]: row for row in csv.DictReader(handle)}

            self.assertEqual(set(rows), {"Gradient Boosting", "Random Forest", "XGBoost"})
            self.assertEqual(int(rows["XGBoost"]["evaluation_rows"]), 4351)
            self.assertAlmostEqual(
                float(rows["XGBoost"]["rmse"]),
                0.00230002,
                places=7,
            )

    def test_readme_svgs_are_well_formed(self) -> None:
        assets = REPO_ROOT / "docs" / "readme-assets"
        for path in assets.glob("*.svg"):
            with self.subTest(path=path.name):
                root = ET.parse(path).getroot()
                self.assertTrue(root.tag.endswith("svg"))


if __name__ == "__main__":
    unittest.main()
