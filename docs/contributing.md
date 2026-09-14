# Contributing

Keep changes focused and update the relevant documentation when behavior changes.

Before opening a change, format the Python code:

'Classic'-Use:
```bash
uv tool run black .
```

When adding or changing an endpoint, update [the API reference](api.md) and verify the behavior through the FastAPI documentation at `/docs` or an HTTP client.

## Working on issues

Opening an issue starts a discussion; it does not by itself approve an
implementation or prescribe the suggested solution.

Before starting a feature, API, architecture, dependency, or tooling change:

1. Check for related open pull requests.
2. Comment on the issue with the approach you intend to take.
3. Wait for maintainer confirmation, assignment, or an `accepted` label before
   implementing it.

Small documentation fixes and clearly scoped bug fixes may proceed directly,
but should link the relevant issue when one exists. Maintainers may choose a
different design, defer the work, or close an issue without implementation.
