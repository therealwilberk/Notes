# 08 — CLI

## Current State (from `cli.py` audit)

Known violations:
- `_cycle_wallpaper`, `restore`, `stats` execute raw SQL directly — `db.connection()` called in cli
- `cli.py` imports `sqlite3` indirectly via `db.connection()` usage
- Duplicate `from pathlib import Path` inside `pick()` (already top-level)
- No app-level startup validation — bad config or missing binaries fail mid-command
- `set_wallpaper`, `launch_picker`, `start_watcher`, `scan_and_extract`, `run_clustering` all have new signatures from subdocs 03–07 — cli.py call sites are stale
- `start_watcher` no longer returns an `Observer` (06-Orchestrator Task 5) — `watch` command must be updated

---

## Tasks

### Task 1 — App callback for startup validation

Add a Typer app callback that runs before every command:

```python
@app.callback()
def _startup(ctx: typer.Context) -> None:
    """Validate config and check required binaries before any command runs."""
    if ctx.invoked_subcommand in ("init",):
        return   # init runs before full validation is possible

    from wpick.config import load_config
    from wpick.extractor import check_auto_palette_available
    from wpick.orchestrator import check_matugen_available, check_swww_available
    from wpick.picker import check_rofi_available

    try:
        cfg = load_config()   # raises ConfigError on bad config
    except ConfigError as e:
        typer.echo(f"Config error: {e}", err=True)
        raise typer.Exit(1)

    check_auto_palette_available()   # raises ExtractorError if missing
    check_swww_available()
    if cfg.matugen.enabled:
        check_matugen_available()
    if ctx.invoked_subcommand in ("pick",):
        check_rofi_available()
```

Catch each typed exception and exit with code 1 and a clear message. Do not let `WpickError` subclasses propagate past the CLI layer.

### Task 2 — `WallpaperDB` injection pattern

Every command that touches the DB follows this pattern:

```python
@app.command()
def some_command() -> None:
    from wpick.config import load_config
    from wpick.db import WallpaperDB

    cfg = load_config()
    with WallpaperDB(cfg.db_path) as db:
        # call module functions, passing db and cfg explicitly
        result = some_module_function(db=db, config=cfg)
```

No command constructs a raw connection or calls `db.connection()` directly. No command passes `db_path` as a `Path` to module functions — always pass the open `WallpaperDB` instance.

**Single instance rule:** each command opens exactly one `WallpaperDB` instance per invocation. If a helper function needs the DB, it receives it as a parameter — it does not construct a new one. `grep -n "WallpaperDB(" src/wpick/cli.py` should return exactly one match per command function.

### Task 3 — Fix `scan` command

Current: `scan_and_extract(root, force=force, db_path=cfg.db_path, on_progress=progress)`

Update to new signature (03-Extraction Task 5):

```python
with WallpaperDB(cfg.db_path) as db:
    result = scan_and_extract(root, db=db, config=cfg, force=force, on_progress=progress)
typer.echo(f"Scan complete: {result.extracted}/{result.total} extracted, {result.errors} errors")
```

`ScanResult` replaces the bare tuple return. Update output line accordingly.

### Task 4 — Fix `cluster` command

Current: `run_clustering()` — no args.

Update to new signature (04-Clustering Task 2):

```python
with WallpaperDB(cfg.db_path) as db:
    record = run_clustering(db=db, config=cfg)
typer.echo(
    f"✓ {record.cluster_count} clusters  |  "
    f"{record.noise_count} noise → misc  |  "
    f"run: {record.run_id}"
)
```

### Task 5 — Fix `assign` command

Update both call sites to pass `db`:

```python
with WallpaperDB(cfg.db_path) as db:
    if path:
        result = assign_image(image_id, db=db)   # resolve image_id from path first
        typer.echo(f"Assigned {path.name} → cluster {result.cluster_id}")
    else:
        batch = assign_all_unassigned(db=db)
        typer.echo(f"Assigned: {batch.assigned}, failed: {batch.failed}")
```

Note: `assign_image` now takes `image_id: str`, not `path: Path`. Resolve the ID via `db.get_image_by_path(path)` before calling. Add `get_image_by_path(path: Path) -> ImageRow | None` to `WallpaperDB` if not present.

### Task 6 — Fix `pick` command

Remove duplicate `from pathlib import Path` import. Update call site:

```python
with WallpaperDB(cfg.db_path) as db:
    path = launch_picker(db=db, config=cfg, force_thumbnails=force_thumbnails)
    if not path:
        typer.echo("No wallpaper selected")
        raise typer.Exit(1)
    if no_set:
        typer.echo(f"Picked: {path}")
        return
    set_wallpaper(path, db=db, config=cfg, log=True)
```

### Task 7 — Fix `_cycle_wallpaper`

Remove all raw SQL. Replace with `WallpaperDB` calls:

```python
def _cycle_wallpaper(direction: str) -> None:
    from wpick.config import load_config
    from wpick.db import WallpaperDB
    from wpick.orchestrator import set_wallpaper

    cfg = load_config()
    with WallpaperDB(cfg.db_path) as db:
        history = db.get_latest_history(limit=1)
        if not history:
            typer.echo("No wallpaper history found.")
            raise typer.Exit(1)

        all_images = db.get_all_images()
        if len(all_images) < 2:
            typer.echo("Only one wallpaper available.")
            raise typer.Exit(1)

        current_id = history[0].image_id
        ids = [img.image_id for img in all_images]
        idx = next((i for i, x in enumerate(ids) if x == current_id), 0)
        target = all_images[(idx + 1) % len(ids)] if direction == "next" \
                 else all_images[(idx - 1) % len(ids)]

        set_wallpaper(Path(target.path), db=db, config=cfg, log=True)
        typer.echo(f"Wallpaper: {Path(target.path).name}")
```

### Task 8 — Fix `watch` command

`start_watcher` now blocks (06-Orchestrator Task 5). Remove `observer.join()`:

```python
@app.command()
def watch() -> None:
    from wpick.config import load_config
    from wpick.db import WallpaperDB
    from wpick.orchestrator import WallpaperError, start_watcher

    cfg = load_config()
    try:
        with WallpaperDB(cfg.db_path) as db:
            start_watcher(config=cfg, db=db)   # blocks until SIGINT/SIGTERM
    except WallpaperError as e:
        typer.echo(f"Watcher error: {e}", err=True)
        raise typer.Exit(1)
```

### Task 9 — Fix `restore` and `stats`

**restore** — replace raw SQL:
```python
with WallpaperDB(cfg.db_path) as db:
    history = db.get_latest_history(limit=1)
    if not history:
        typer.echo("No wallpaper history found.")
        return
    set_wallpaper(Path(history[0].image_id_to_path), db=db, config=cfg, log=False)
```
Note: `HistoryRow` needs a resolved `path` field or `db.get_image(history[0].image_id)` to get the path.

**stats** — replace three raw queries with one `db.get_stats()` call:
```python
with WallpaperDB(cfg.db_path) as db:
    s = db.get_stats()
typer.echo(f"Images: {s.total_images} total, {s.extracted_images} extracted")
for c in s.clusters:
    bar = "█" * min(40, c.member_count // 2)
    typer.echo(f"  {c.label:20s}  {c.member_count:4d}  {bar}")
```

### Task 10 — Verify no sqlite3 in cli.py

After all changes:
```bash
grep -n "sqlite3\|conn\.execute\|db\.connection" src/wpick/cli.py
```

Must return nothing.

---

## Constraints
- `cli.py` catches all `WpickError` subclasses and exits with code 1 — never lets them propagate
- Every command that uses DB opens `WallpaperDB` as a context manager
- `cli.py` must not import `sqlite3`
- basedpyright zero errors after changes
