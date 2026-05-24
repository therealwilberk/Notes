# 00 — Architecture

## Current State

```
src/wpick/
  db.py           # SQLite ops — raw connection helpers, scattered queries
  extractor.py    # auto-palette subprocess, writes features.jsonl
  clusterer.py    # HDBSCAN, reads features.jsonl, writes clusters.json
  assigner.py     # nearest-centroid, reads clusters.json
  picker.py       # rofi UI, thumbnails
  orchestrator.py # watcher, swww, matugen calls
  oklab.py        # color space math
  config.py       # config.toml loading
  cli.py          # Typer entry points
```

**Known problems:**
- `features.jsonl` and `clusters.json` are canonical state alongside SQLite — two sources of truth
- No module contracts: orchestrator and picker do direct DB calls, bypassing `db.py`
- No typed exceptions — external failures (subprocess, filesystem, DB) raise raw exceptions or fail silently
- Logging is ad-hoc `logger.debug(...)` with no consistent structure
- Type annotations incomplete — basedpyright will flag missing return types, `Any` leaks, optional handling

---

## Target Architecture

**Single source of truth: SQLite.** `features.jsonl` and `clusters.json` are ephemeral — written during a pipeline run, never read back as canonical state.

**Layer rule:** only `db.py` executes SQL. Every other module calls `db.py` functions. No exceptions.

**Module contracts** — each module exposes typed inputs/outputs:

| Module | Receives | Returns |
|---|---|---|
| `extractor.py` | `list[Path]` | `list[FeatureRow]` |
| `clusterer.py` | `list[FeatureRow]` | `list[ClusterRow]` |
| `assigner.py` | `FeatureRow`, `list[ClusterRow]` | `ClusterID` |
| `picker.py` | `list[ClusterRow]` | `Path` (selected wallpaper) |
| `orchestrator.py` | config + db | side effects only |

Define these as `TypedDict` or `dataclass` in a `models.py` file. No naked `dict` or `sqlite3.Row` passed between modules.

---

## Tasks

### Task 1 — Create `models.py`
Define all shared data types. Every inter-module boundary uses these. No raw dicts crossing module lines.

```python
# Example shapes — implement fully
@dataclass
class FeatureRow:
    image_id: str
    path: str
    oklab_vector: list[float]

@dataclass  
class ClusterRow:
    cluster_id: int
    centroid: list[float]
    label: str
```

### Task 2 — Harden `db.py`
- Implement `WallpaperDB` class (single connection, context manager)
- `_transaction()` context manager: commit on success, rollback + log on failure
- Raise `DatabaseError(Exception)` — never let `sqlite3.Error` escape the module
- All queries in `db.py` only — audit and remove any SQL in other files
- Row factory: `sqlite3.Row` configured once on connect

### Task 3 — Typed exceptions per module
Each module defines its own exception:

```
ExtractorError(WpickError)
ClusterError(WpickError)
AssignerError(WpickError)
OrchestratorError(WpickError)
```

All subclass a base `WpickError(Exception)`. Wrap all subprocess calls, filesystem ops, and external binary invocations in these.

### Task 4 — Structured logging
- One `logging.getLogger(__name__)` per module — no passing loggers around
- All log calls include context: `logger.error("extractor failed", extra={"path": str(path), "error": str(e)})`
- Log levels: `DEBUG` for pipeline progress, `WARNING` for recoverable issues (missing file, skip), `ERROR` for failures that abort an operation
- No `print()` anywhere

### Task 5 — Eliminate dual state
- Remove any code path that reads `features.jsonl` or `clusters.json` as input
- These files may still be written as debug artifacts but must not be read back
- All pipeline stages read from and write to SQLite exclusively

### Task 6 — Type annotation pass
Run `basedpyright` in strict mode. Fix in this order:
1. Missing return types on all public functions
2. `Optional[X]` / `X | None` — no unguarded `.` access on optionals
3. Remove all `Any` — replace with concrete types or `Unknown` with a comment
4. `sqlite3.Row` should not cross module boundaries (covered by Task 1)

Target: zero basedpyright errors, warnings treated as errors in CI.

### Task 7 — `config.py` startup validation
On load, validate:
- `wallpaper_dir` exists and is a directory
- `db_path` parent directory is writable
- `cluster_count` >= 2
- `thumbnail_size` is a positive int
- All enum-like values (`transition_type`, extensions list) are valid

Raise `ConfigError(WpickError)` with a human-readable message. This runs before any pipeline stage starts.

---

## Constraints
- Python 3.12+
- basedpyright strict mode — zero errors is the target
- No new dependencies without justification
- `schema.sql` is the schema source of truth — `db.py` does not define schema inline
