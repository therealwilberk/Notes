---
tags: [ml, python, dev-tools, ruff, mypy, pre-commit, pytest, loguru]
aliases: ["ML dev tools cheatsheet", "ml-dev-tools"]
parent: "[[MOCs/Python — Map of Content]]"
created: 2026-06-11
status: complete
---

## 80/20

```bash
# ruff -- Rust-based linter (replaces flake8 + isort + pyupgrade)
uv run ruff check              # lint all files
uv run ruff check --fix        # auto-fix what it can
uv run ruff format             # format code (like black)
uv run ruff check --watch .    # watch mode

# mypy -- gradual type checker
uv run mypy src/               # type-check all source
uv run mypy src/ --strict      # strict mode (no implicit Any)

# pre-commit -- git hooks
uv run pre-commit run --all-files   # run all hooks manually
uv run pre-commit autoupdate        # update hook versions

# nbstripout -- strip notebook output
uv run nbstripout notebooks/*.ipynb  # remove output cells

# pytest -- test runner
uv run pytest                        # run all tests
uv run pytest tests/ -v              # verbose
uv run pytest tests/ -k "feature"    # filter by name
uv run pytest --tb=short             # shorter tracebacks

# loguru -- zero-boilerplate logging
from loguru import logger
logger.info("Data ingested from {}", path)
logger.warning("Null rate on {} is {:.1%}", col, rate)
logger.error("Schema validation failed: {}", exc)
```

## Each tool in 30s

### ruff

Fastest Python linter (Rust). Combines Flake8, isort, pyupgrade. Configure in `pyproject.toml` under `[tool.ruff]`.

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "W"]  # pyupgrade is UP

[tool.ruff.format]
quote-style = "double"
```

### mypy

Gradual type checker. Catches interface mismatches at check time instead of runtime. Configure in `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.11"
strict = true
ignore_missing_imports = true
```

### pre-commit

Runs quality checks on every `git commit`. If any check fails, the commit is blocked. Configure in `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
```

Install: `uv run pre-commit install`

### nbstripout

Strips notebook output cells to prevent giant JSON diffs in version control. Run before committing notebooks, or set up as a pre-commit hook.

```bash
uv run nbstripout notebooks/*.ipynb
```

### pytest

Python test runner. Discovers tests by filename pattern (`test_*.py` or `*_test.py`). Configure in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

### loguru

Replaces stdlib `logging` module. Works immediately with no handler/formatter setup.

```python
from loguru import logger

# No __name__ logger, no handler config, no formatter
# Default: 2024-06-01 10:15:30.123 | INFO | module:12 - message
```

## Traps

- **ruff and mypy in pre-commit** -- if pre-commit is set up, `git commit` is blocked on lint/type errors. Run `pre-commit run --all-files` to check before committing.
- **mypy `--strict` with pandas/numpy** -- many stubs are incomplete. `ignore_missing_imports = true` is usually needed.
- **nbstripout mutates files** -- run it deliberately, or set up as a pre-commit hook to avoid accidental git add of JSON garbage.
- **pytest discovery** -- if you name files differently than `test_*.py`, pytest won't find them unless you configure `python_files`.
- **loguru in libraries** -- if loguru is in a library, consumers of that library inherit the loguru configuration (which may conflict with their own). In library code, consider the stdlib `logging` bridge.
