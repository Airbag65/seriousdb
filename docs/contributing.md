# Contributing

Keep changes focused and update the relevant documentation when behavior changes.

Before opening a change, sync the development dependencies, then format and lint the Python code:

```bash
uv sync --group dev
uv run ruff format .
uv run ruff check .
```

When adding or changing an endpoint, update [the API reference](api.md) and verify the behavior through the FastAPI documentation at `/docs` or an HTTP client.
