# Development guide

## Requirements

- Python 3.11 or newer
- `pip`

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

## Run locally

```bash
fastapi dev main.py
```

The server is available at `http://127.0.0.1:8000` and its interactive API documentation is at `/docs`.

## Formatting

Format Python files with Black:

```bash
uv tool run black main.py
```
