# limit the number of cpus used by high performance libraries

import argparse
import os
from pathlib import Path
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import sys
lib_path = os.path.abspath(os.path.join('infrastructure', 'yolov5'))
sys.path.append(lib_path)

import torch
import torch.backends.cudnn as cudnn

import pandas as pd

from infrastructure.handlers.track import Tracker


def parse_args():
    project_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(
        description="Run YOLOv5 + Deep SORT vehicle tracking."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=project_root / "settings" / "config.yml",
        help="Path to the tracking YAML configuration.",
    )
    parser.add_argument(
        "--source",
        help="Optional video, image directory, stream URL, or camera index override.",
    )
    parser.add_argument(
        "--output",
        help="Optional output directory override.",
    )
    parser.add_argument(
        "--device",
        help="Optional inference device override, for example 'cpu' or '0'.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    os.chdir(Path(__file__).resolve().parent)
    tracker = Tracker(config_path=str(args.config))
    if args.source:
        tracker.opt.source = args.source
    if args.output:
        tracker.opt.output = args.output
    if args.device:
        tracker.opt.device = args.device
    with torch.no_grad():
        tracker.detect()
    
