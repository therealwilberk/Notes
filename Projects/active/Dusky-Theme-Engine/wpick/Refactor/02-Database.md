# 02 — Database

## Current State
- `schema.sql` exists — source of truth for table definitions
- `db.py` has a `connection()` context manager and scattered query functions
- Raw SQL is executed directly in `cli.py` (`_cycle_wallpaper`, `restore`, `stats`) — this is wrong
- No migration strategy, no schema versioning
- `sqlite3.Row` objects passed to callers and used directly outside `db.py`

---

## Target
- `WallpaperDB` class owns all SQL
- One connection per operation, properly closed
- All callers receive typed dataclasses (from `models.py`), never raw `sqlite3.Row`
- Schema changes are versioned and applied automatically

---

## Tasks

### Task 1 — Implement `WallpaperDB` in `db.py`

Replace any existing connection helper with this structure:

```python
class WallpaperDB:
    def __init__(self, db_path: Path) -> None: ...
    def connect(self) -> None: ...
    def close(self) -> None: ...
    def __enter__(self) -> "WallpaperDB": ...
    def __exit__(self, ...) -> None: ...

    @contextmanager
    def _transaction(self) -> Generator[sqlite3.Cursor, None, None]:
        # commit on success, rollback + raise DatabaseError on sqlite3.Error
        ...
```

Rules:
- `row_factory = sqlite3.Row` set once on connect
- `PRAGMA journal_mode=WAL` and `PRAGMA foreign_keys=ON` set on every new connection
- `DatabaseError(WpickError)` is the only exception that escapes this module
- Never expose `sqlite3.Cursor` or `sqlite3.Row` outside this file

### Task 2 — Schema versioning

Add to `schema.sql`:

```sql
CREATE TABLE IF NOT EXISTS schema_migrations (
    version     INTEGER PRIMARY KEY,
    applied_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
```

In `db.py`, add:

```python
SCHEMA_VERSION = 1  # increment on every schema change

def init_schema(db_path: Path) -> None:
    """Apply schema.sql and run pending migrations."""
    ...

def _current_version(conn: sqlite3.Connection) -> int:
    """Return applied schema version, 0 if fresh."""
    ...
```

`init_schema` reads `schema.sql` from the package data directory, executes it, then checks `schema_migrations` and applies any pending migrations in order. This replaces any existing `init_schema` implementation.

### Task 3 — Typed query methods

Implement these methods on `WallpaperDB`. Return types must use models from `models.py` — no raw rows:

```python
# Images
def upsert_image(self, path: Path) -> ImageRow: ...
def get_image(self, image_id: str) -> ImageRow | None: ...
def get_all_images(self) -> list[ImageRow]: ...
def get_unextracted_images(self) -> list[ImageRow]: ...

# Features
def upsert_features(self, features: FeatureRow) -> None: ...
def get_features(self, image_id: str) -> FeatureRow | None: ...
def get_all_features(self) -> list[FeatureRow]: ...

# Clusters
def upsert_cluster(self, cluster: ClusterRow) -> None: ...
def get_clusters(self) -> list[ClusterRow]: ...
def assign_image_cluster(self, image_id: str, cluster_id: int) -> None: ...

# History
def log_history(self, image_id: str) -> None: ...
def get_latest_history(self, limit: int = 1) -> list[HistoryRow]: ...

# Stats (used by cli stats command)
def get_stats(self) -> StatsResult: ...
```

`StatsResult` is a dataclass with `total_images`, `extracted_images`, `clusters: list[ClusterRow]`.

### Task 4 — Remove SQL from `cli.py`

`_cycle_wallpaper`, `restore`, and `stats` in `cli.py` contain direct SQL. Replace each with calls to the appropriate `WallpaperDB` method from Task 3. `cli.py` must not import `sqlite3` at all.

Verify: `grep -r "conn.execute\|sqlite3" src/wpick/cli.py` returns nothing.

### Task 5 — `db.py` is the only SQL file

Run:
```bash
grep -r "\.execute\(" src/wpick/ --include="*.py" -l
```

Any file other than `db.py` in that list is a violation. Fix each one.

---

## Constraints
- `schema.sql` is never modified at runtime — it is read-only package data
- `PRAGMA foreign_keys=ON` must be set — the schema uses FK constraints
- basedpyright must pass with no errors on `db.py` after changes
- All `WallpaperDB` methods must have explicit return type annotations
