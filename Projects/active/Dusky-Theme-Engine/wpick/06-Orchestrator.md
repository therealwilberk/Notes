---
tags:
  - project
  - wpick
  - orchestrator
  - swww
  - matugen
parent: "[[wpick]]"
created: 2026-05-23
---

# wpick — Orchestrator

## Responsibilities

- Watch wallpaper directory for new images
- Trigger extract → assign on new files
- Set wallpaper via swww
- Trigger matugen after set
- Log history

**No analysis logic here.**

## swww Integration

```python
def set_wallpaper(path: Path, log: bool = True) -> None:
    """Set wallpaper via swww, then call matugen."""
    _require_swww()
    _ensure_swww_daemon()

    cfg = config.get()
    sw = cfg["swww"]

    cmd = [
        "swww", "img", str(path.resolve()),
        "--transition-type", sw["transition_type"],
        "--transition-pos", sw["transition_pos"],
        "--transition-fps", str(sw["transition_fps"]),
        "--transition-duration", str(sw["transition_duration"]),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise WallpaperError(f"swww failed: {result.stderr.strip()}")

    if log:
        img_id = db.image_id(path)
        db.log_history(img_id)

    _call_matugen(path)
```

## matugen Integration

```python
def _call_matugen(path: Path) -> None:
    cfg = config.get()
    if not cfg["matugen"]["enabled"]:
        return

    if not shutil.which("matugen"):
        logger.warning("matugen not found in PATH, skipping theme generation")
        return

    extra = cfg["matugen"].get("extra_flags", [])
    cmd = ["matugen", "image", str(path.resolve())] + extra

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        logger.warning(f"matugen exited {result.returncode}: {result.stderr.strip()}")
```

## Filesystem Watcher

```python
class _WallpaperHandler(FileSystemEventHandler):
    def __init__(self, wallpapers_root: Path, debounce: float):
        self._root = wallpapers_root
        self._debounce = debounce
        self._pending: dict[str, Timer] = {}
        cfg = config.get()
        self._extensions = set(cfg["extraction"]["extensions"])

    def on_created(self, event: FileCreatedEvent) -> None:
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix.lstrip(".").lower() not in self._extensions:
            return

        key = str(path)
        if key in self._pending:
            self._pending[key].cancel()

        def process():
            self._pending.pop(key, None)
            logger.info(f"New wallpaper detected: {path.name}")
            assign_image(path, self._root)

        timer = Timer(self._debounce, process)
        self._pending[key] = timer
        timer.start()
```

## Wallpaper Cycling

```python
def cycle_wallpaper(direction: str = "next") -> None:
    """Cycle to next/prev wallpaper in current cluster."""
    with db.connection() as conn:
        # Get current wallpaper's cluster
        row = conn.execute("""
            SELECT i.cluster_id FROM history h
            JOIN images i ON h.image_id = i.id
            ORDER BY h.set_at DESC LIMIT 1
        """).fetchone()

    if not row or not row["cluster_id"]:
        logger.warning("No current cluster found")
        return

    cluster_id = row["cluster_id"]
    images = db.get_images_by_cluster(cluster_id)

    if not images:
        return

    # Get current position in cluster
    current_id = db.image_id(Path(row["path"])) if row else None
    paths = [Path(img["path"]) for img in images]

    if current_id:
        current_idx = next(
            (i for i, img in enumerate(images) if img["id"] == current_id), 0
        )
    else:
        current_idx = 0

    if direction == "next":
        next_idx = (current_idx + 1) % len(paths)
    else:
        next_idx = (current_idx - 1) % len(paths)

    set_wallpaper(paths[next_idx])
```

## See Also

- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/05-Assignment]] — What watcher triggers
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/07-Picker]] — How wallpaper is selected
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/08-CLI]] — `wpick watch` command
