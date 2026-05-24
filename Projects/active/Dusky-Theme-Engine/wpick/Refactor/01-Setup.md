# 01 — Setup

## Current State
- `pyproject.toml` exists, uv-managed
- `config.default.toml` exists
- `schema.sql` exists
- Python version target: confirm it's pinned to `3.12` in `pyproject.toml`

---

## Tasks

### Task 1 — Audit `pyproject.toml`

Verify these sections are correct and complete:

```toml
[project]
name = "wpick"
version = "0.1.0"
requires-python = ">=3.12"

[project.scripts]
wpick = "wpick.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Runtime dependencies should include at minimum:
`typer`, `pillow`, `hdbscan`, `scikit-learn`, `tomllib` (stdlib 3.11+, no install needed), `watchdog`

Dev dependencies:
```toml
[dependency-groups]
dev = [
  "pytest",
  "pytest-cov",
  "basedpyright",
  "ruff",
]
```

Flag anything missing or pinned too loosely (e.g. `pillow>=10.0` not `pillow>=9`).

### Task 2 — basedpyright config

Add to `pyproject.toml`:

```toml
[tool.basedpyright]
include = ["src"]
pythonVersion = "3.12"
typeCheckingMode = "standard"
reportMissingImports = true
reportMissingTypeStubs = false
reportUnknownVariableType = true
reportUnknownMemberType = true
reportUnknownParameterType = true
reportUnknownArgumentType = true
venvPath = "."
venv = ".venv"
```

Start with `"standard"` not `"strict"` — move to strict once the codebase passes standard cleanly. Document this in a comment.

### Task 3 — ruff config

Add to `pyproject.toml`:

```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]
ignore = []
```

Run `ruff check src/` — fix all existing violations before any other work begins. This is baseline hygiene.

### Task 4 — pytest config

Add to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--tb=short -q"

[tool.coverage.run]
source = ["src/wpick"]
omit = ["tests/*"]

[tool.coverage.report]
fail_under = 70
```

Run `pytest --co -q` (collect-only) to verify all test files are discoverable without errors. Fix any import failures before proceeding.

### Task 5 — `config.py` wiring

`config.default.toml` is the fallback. User config at `~/.config/wpick/config.toml` merges on top.

Loading order:
1. Read `config.default.toml` (shipped with package, always present)
2. If user config exists, deep-merge over defaults
3. Expand all `~` paths with `Path.expanduser()`
4. Validate (see 00-Architecture Task 7)
5. Return a typed config object — not a raw dict

```python
@dataclass
class WpickConfig:
    wallpaper_dir: Path
    db_path: Path
    cache_dir: Path
    max_colors: int
    cluster_count: int
    # ... all fields explicit, no **kwargs
```

`tomllib` is stdlib in 3.11+ — no external dep needed.

### Task 6 — Makefile targets

Verify or add these targets:

```makefile
lint:
    ruff check src/ tests/
    basedpyright

test:
    pytest

cov:
    pytest --cov=wpick --cov-report=term-missing

check: lint test   # run both — use this in CI
```

`make check` should be the single command that confirms the codebase is clean.

---

## Constraints
- Do not change `uv.lock` manually — run `uv sync` after any `pyproject.toml` dependency change
- `config.default.toml` is read-only at runtime — never write to it
- All path resolution happens in `config.py` — no `Path.expanduser()` scattered elsewhere
