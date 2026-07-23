# Vehicle tracking prototype

This directory contains the competition-era YOLOv5 + Deep SORT pipeline used to turn road video into tracked vehicle counts.

For the complete project narrative, data, model comparison, and limitations, see the [repository README](../README.md).

## Run

The original environment used Python 3.7.12 and PyTorch 1.8. Install dependencies in an isolated environment:

```bash
pip install -r requirements.txt

cd application/main
python app_track.py \
  --config ../../settings/config.yml \
  --source /path/to/input-video.mp4 \
  --device cpu
```

Available overrides are `--source`, `--output`, and `--device`.

## Database output

Database upload is disabled by default. To enable it:

1. Copy `settings/db_config.example.yml` to the ignored local file `settings/db_config.yml`, or set `TRAFFIC_DATABASE_URL`.
2. Set `upload_db: true` in `settings/config.yml`.
3. Run the tracker or FastAPI prototype from `application/main`.

Never commit the real database configuration.

## Third-party code

- `application/main/infrastructure/yolov5/`: GPL-3.0
- `application/main/infrastructure/deep_sort_pytorch/`: MIT

See [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) for the repository-level attribution and weight provenance note.
