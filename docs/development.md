# Development guide

## Requirements

- Python 3.11 or newer
- `uv`

## Setup

```bash
uv sync
```

## Run locally

```bash
uv run run.py 
```

The server is available at `http://127.0.0.1:8000` and its interactive API documentation is at `/docs`.

## Docker

```bash
docker build -t seriousdb .
docker run -p 8000:8000 seriousdb
```

## Formatting

Format Python files with `ruff`:

```bash
uv tool run ruff .
```

## Linting

Lint python files with `ruff`:

```bash
uv tool run ruff check .
```

To fix linter errors and warning if possible run following command:

```bash
uv tool run ruff check --fix .
```
