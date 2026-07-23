#!/usr/bin/env python3
"""Extract frames from a video at a configurable sampling interval."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract sampled video frames.")
    parser.add_argument("video", type=Path, help="Input video.")
    parser.add_argument("output_dir", type=Path, help="Destination directory.")
    parser.add_argument(
        "--every",
        type=int,
        default=1,
        help="Save every Nth frame (default: 1).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.every < 1:
        raise SystemExit("--every must be at least 1")

    capture = cv2.VideoCapture(str(args.video))
    if not capture.isOpened():
        raise SystemExit(f"Could not open video: {args.video}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    frame_index = 0
    saved = 0
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        if frame_index % args.every == 0:
            output = args.output_dir / f"frame_{frame_index:08d}.png"
            if not cv2.imwrite(str(output), frame):
                raise RuntimeError(f"Failed to write frame: {output}")
            saved += 1
        frame_index += 1

    capture.release()
    print(f"Read {frame_index} frames and saved {saved} to {args.output_dir}")


if __name__ == "__main__":
    main()
