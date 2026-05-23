# wpick — Implementation Plan

## Stack

- Python 3.12+ (uv)
- auto-palette (Rust binary)
- HDBSCAN + scikit-learn
- Pillow (thumbnails)
- Pydantic (models, validation)
- Typer (CLI)
- SQLite (storage)
- swww + matugen
- rofi-wayland

## Architecture Rules

1. **Pure functions** — no side effects, explicit inputs/outputs, testable in isolation
2. **Impure functions** — DB calls, subprocess, filesystem. Isolated in `infra/` layer
3. **Pydantic models** — all data structures validated at boundaries
4. **Type hints** — every function signature fully typed
5. **Logging** — structured, no print statements

## Module Dependency Graph

```
setup → config → oklab (parallel)
              → db → extraction → clustering  (parallel)
                                → assignment → orchestrator → picker → cli
```

## Tasks

### Sequential (order matters)

| # | Task | Agent | Why |
|---|---|---|---|
| 1 | Project scaffold | OpenCode | pyproject.toml, dirs, __init__.py, pydantic models |
| 2 | Config module | OpenCode | pydantic Settings, TOML loader, validation |
| 3 | OKLab module | Hermes | Standalone, 30 lines, pure math |
| 4 | Database module | OpenCode | Schema, connection pool, pure/impure split |
| 5 | Extraction module | OpenCode | auto-palette integration, stats, pydantic models |
| 6 | Clustering module | OpenCode | HDBSCAN, cluster naming, pydantic models |
| 7 | Assignment module | OpenCode | Cosine similarity, incremental logic |
| 8 | Orchestrator module | OpenCode | Watcher, swww, matugen, cycling |
| 9 | Picker module | OpenCode | rofi card grid, dynamic columns |
| 10 | CLI module | OpenCode | Typer commands, all entry points |
| 11 | Tests | Hermes | Unit + integration, fixtures |

### Parallel (no dependencies between them)

- **Batch A** (after setup): Config + OKLab
- **Batch B** (after config): Database + (wait for extraction)
- **Batch C** (after extraction): Clustering + Assignment
- **Batch D** (after all): CLI + Tests

## File Structure

```
~/.config/wpick/
├── pyproject.toml
├── config.default.toml
├── schema.sql
├── rofi/
│   ├── wpick.rasi
│   └── wpick-picker.sh
├── systemd/
│   └── wpick-watch.service
├── src/
│   └── wpick/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── db.py
│       ├── extractor.py
│       ├── clusterer.py
│       ├── assigner.py
│       ├── orchestrator.py
│       ├── picker.py
│       ├── oklab.py
│       ├── models.py          ← pydantic models (shared)
│       ├── infra.py           ← impure functions (DB, subprocess, FS)
│       └── pure.py            ← pure functions (math, logic)
└── tests/
    ├── conftest.py
    ├── fixtures/
    ├── test_oklab.py
    ├── test_extractor.py
    ├── test_clusterer.py
    ├── test_assigner.py
    └── test_db.py
```

## Quality Gates

- [ ] All functions have type hints
- [ ] Pydantic models for all data structures
- [ ] Pure functions separated from impure
- [ ] Logging structured (no print)
- [ ] Tests pass: `uv run pytest`
- [ ] Lint clean: `uv run ruff check src/`
- [ ] Type check: `uv run mypy src/wpick/`
