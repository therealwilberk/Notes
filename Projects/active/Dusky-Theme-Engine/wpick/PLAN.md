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

### Sequential (order matters) — ALL DONE

| # | Task | Agent | Status |
|---|---|---|---|
| 1 | Project scaffold | OpenCode | ✅ HER-13 |
| 2 | Config module | OpenCode | ✅ HER-14 |
| 3 | OKLab module | Hermes | ✅ HER-15 |
| 4 | Database module | OpenCode | ✅ HER-16 |
| 5 | Extraction module | OpenCode | ✅ HER-17 → HER-32 (auto-palette) |
| 6 | Clustering module | OpenCode | ✅ HER-18 → HER-33 (HDBSCAN) |
| 7 | Assignment module | OpenCode | ✅ HER-19 |
| 8 | Orchestrator module | OpenCode | ✅ HER-20 → HER-35 (API fix) |
| 9 | Picker module | OpenCode | ✅ HER-21 → HER-36 (API fix) |
| 10 | CLI module | OpenCode | ✅ HER-22 → HER-34 + HER-37 (Typer + API fix) |
| 11 | Tests | Hermes | ✅ HER-23 |

### Phase 2 Upgrades — ALL DONE

| # | Upgrade | Task | Status |
|---|---|---|---|
| 1 | Schema → SHA256[:16] | HER-31 | ✅ |
| 2 | Extractor → auto-palette | HER-32 | ✅ |
| 3 | Clusterer → HDBSCAN | HER-33 | ✅ |
| 4 | Cluster naming | HER-33 | ✅ (built-in) |
| 5 | Picker → card grid | HER-36 | ✅ |
| 6 | CLI → Typer | HER-34 + HER-37 | ✅ |
| 7 | Watcher | HER-35 | ✅ |
| 8 | Cycling | HER-35 | ✅ (built-in) |

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

- [x] All functions have type hints
- [x] Pydantic models for all data structures
- [x] Pure functions separated from impure
- [x] Logging structured (no print)
- [x] Tests pass: `uv run pytest` — 153 passed
- [x] Lint clean: `uv run ruff check src/`
- [x] Type check: `uv run mypy src/wpick/` — 22 minor (3rd-party stubs, numpy returns)
