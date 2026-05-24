# 06 — Orchestrator

## Current State
- `orchestrator.py` handles `set_wallpaper`, `start_watcher`, swww and matugen subprocess calls
- `WallpaperError` exists and is used in `cli.py`
- `start_watcher` returns a watchdog `Observer` directly — lifecycle not managed
- No debounce on filesystem events — rapid file additions trigger repeated scans
- No PID file — multiple daemon instances can run silently
- matugen is called unconditionally — no check if enabled in config

---

## Target
- All external calls (swww, matugen, watchdog) wrapped with typed errors and timeouts
- Watcher has debounce, PID guard, and clean shutdown
- matugen is skipped if `config.matugen.enabled = false`
- `set_wallpaper` is atomic from the caller's perspective — either fully succeeds or raises

---

## Tasks

### Task 1 — Harden `set_wallpaper`

Current signature is likely `set_wallpaper(path: Path, log: bool) -> None`. Keep signature, harden internals:

```python
def set_wallpaper(path: Path, db: WallpaperDB, config: WpickConfig, *, log: bool = True) -> None:
    """
    Set wallpaper via swww, optionally run matugen, optionally log to history.
    Raises WallpaperError on any subprocess failure.
    """
```

Logic:
1. Verify `path.exists()` — raise `WallpaperError(f"path not found: {path}")` if not
2. Run swww subprocess with transition params from config
3. If `config.matugen.enabled`: run matugen subprocess
4. If `log=True`: call `db.log_history(image_id)`

Each subprocess call uses this pattern:

```python
def _run_subprocess(cmd: list[str], *, timeout: int = 10, label: str) -> None:
    """Run external command. Raises WallpaperError on failure or timeout."""
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if result.returncode != 0:
        raise WallpaperError(f"{label} failed: {result.stderr.strip()}")
```

swww timeout: 10s. matugen timeout: 30s (color scheme generation is slower).

### Task 2 — Binary availability checks

Add at module level:

```python
def check_swww_available() -> None: ...
def check_matugen_available() -> None: ...
```

Both use `shutil.which`. `check_swww_available` always raises if missing. `check_matugen_available` only raises if `config.matugen.enabled = true`. Call both from `cli.py`'s app callback (see 08-CLI), not inside every `set_wallpaper` call.

### Task 3 — Watcher debounce

The filesystem watcher fires on every file creation event. A batch copy of 50 wallpapers should trigger one scan, not 50.

Implement a debounce handler:

```python
class _DebouncedHandler(FileSystemEventHandler):
    def __init__(self, callback: Callable[[], None], delay: float = 2.0) -> None:
        self._callback = callback
        self._delay = delay
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()

    def on_created(self, event: FileCreatedEvent) -> None:
        if event.is_directory:
            return
        ext = Path(event.src_path).suffix.lower()
        if ext not in WATCHED_EXTENSIONS:
            return
        with self._lock:
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(self._delay, self._callback)
            self._timer.start()
```

`WATCHED_EXTENSIONS` comes from `config.extraction.extensions`. Delay is 2.0s — configurable via `config.watch.debounce_seconds`.

### Task 4 — PID file guard

```python
PID_FILE = Path("~/.local/share/wpick/daemon.pid").expanduser()

def _write_pid() -> None:
    """Write current PID. Raises WallpaperError if another instance is running."""
    if PID_FILE.exists():
        existing = int(PID_FILE.read_text().strip())
        try:
            os.kill(existing, 0)   # signal 0 = check existence only
            raise WallpaperError(f"wpick daemon already running (PID {existing})")
        except ProcessLookupError:
            pass   # stale PID file — overwrite
    PID_FILE.write_text(str(os.getpid()))

def _clear_pid() -> None:
    PID_FILE.unlink(missing_ok=True)
```

### Task 5 — Rewrite `start_watcher`

Signature:

```python
def start_watcher(config: WpickConfig, db: WallpaperDB) -> None:
    """
    Start filesystem watcher. Blocks until SIGINT/SIGTERM.
    Cleans up PID file on exit.
    """
```

Do not return the `Observer` — the caller (CLI) should not manage observer lifecycle. `start_watcher` owns the full lifecycle: write PID, start observer, block on `observer.join()`, catch `KeyboardInterrupt`, stop observer, clear PID.

Register a `signal.signal(SIGTERM, ...)` handler so systemd stop works cleanly.

### Task 6 — `add_schema` entry for config.watch

Add to `config.default.toml`:

```toml
[watch]
debounce_seconds = 2.0
```

Add `watch_debounce_seconds: float` to `WpickConfig` dataclass. Validate `> 0.0` in config validation.

---

## Constraints
- `WallpaperError(WpickError)` is the only exception that escapes `orchestrator.py`
- `orchestrator.py` must not import `sqlite3` directly
- All subprocess calls have explicit `timeout` — no hanging on frozen swww
- PID file path is always under `~/.local/share/wpick/` — not configurable
- basedpyright zero errors after changes
