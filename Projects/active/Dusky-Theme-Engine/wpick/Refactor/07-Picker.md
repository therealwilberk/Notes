# 07 — Picker

## Current State
- `picker.py` generates thumbnails, builds rofi entries grouped by cluster, launches rofi
- `launch_picker(force_thumbnails)` exists, return type likely `str | None`
- Thumbnail generation may not be idempotent (unclear if cache is checked before regenerating)
- rofi subprocess failure likely raises raw `subprocess.SubprocessError` or uncaught `FileNotFoundError`
- Entry format (what rofi displays per image) is unspecified in code

---

## Target
- Thumbnails are generated once and cached — only missing or stale thumbnails are regenerated
- rofi subprocess fully wrapped — failure raises `PickerError`, user cancellation returns `None`
- Entry format is structured and consistent
- `launch_picker` returns `Path | None`, not `str | None`

---

## Tasks

### Task 1 — Add picker types to `models.py`

```python
@dataclass
class ThumbnailResult:
    image_id: str
    thumb_path: Path
    was_generated: bool   # False if cache hit

@dataclass
class RofiEntry:
    display: str    # text shown in rofi
    image_id: str
    path: Path
    cluster_label: str
```

### Task 2 — Thumbnail generation

```python
def generate_thumbnail(
    source: Path,
    cache_dir: Path,
    size: int,
    quality: int,
) -> ThumbnailResult:
    """
    Generate thumbnail if not cached. Returns cache hit without regenerating.
    Raises PickerError on Pillow failure.
    """
```

Cache key: `{image_id[:16]}.jpg` under `cache_dir/thumbs/`. Check existence before opening source image.

```python
def generate_all_thumbnails(
    images: list[ImageRow],
    config: WpickConfig,
    *,
    force: bool = False,
    on_progress: Callable[[int, int], None] | None = None,
) -> list[ThumbnailResult]:
```

On `PickerError` per image: log `WARNING`, skip that image — do not abort. An image with no thumbnail is excluded from rofi entries.

Pillow operations that can fail: file not found, unsupported format, corrupt image. Wrap all three explicitly:

```python
try:
    with Image.open(source) as img:
        img.thumbnail((size, size))
        img.save(dest, "JPEG", quality=quality)
except (FileNotFoundError, UnidentifiedImageError, OSError) as e:
    raise PickerError(f"thumbnail failed for {source.name}: {e}") from e
```

### Task 3 — Build rofi entries

```python
def build_rofi_entries(
    clusters: list[ClusterRow],
    images: list[ImageRow],
    thumbnails: dict[str, Path],   # image_id -> thumb_path
) -> list[RofiEntry]:
    """
    Group images by cluster, sorted by cluster label then image filename.
    Images with no thumbnail are excluded.
    """
```

Display format per entry: `"{cluster_label}  {filename}"` — simple, no unicode decoration that rofi might not render. Cluster separator entries (rofi `-mesg` or a no-op entry) are allowed but optional.

### Task 4 — rofi subprocess

```python
def _launch_rofi(entries: list[RofiEntry], theme: Path | None) -> RofiEntry | None:
    """
    Launch rofi with entries as stdin. Return selected entry or None if cancelled.
    Raises PickerError if rofi binary is missing or exits with unexpected code.
    """
```

rofi exit codes:
- `0` — selection made (stdout contains selected line)
- `1` — cancelled (user pressed Escape) — return `None`, do not raise
- Any other code — raise `PickerError(f"rofi exited {returncode}")`

Pass entries as newline-joined stdin. Use `-dmenu` mode. Theme via `-theme {path}` if `config.rofi_theme` exists, skip flag entirely if it doesn't — do not pass a missing path.

```python
def check_rofi_available() -> None:
    """Raise PickerError if rofi is not on PATH."""
```

Call from `cli.py` app callback, not inside `launch_picker`.

### Task 5 — Rewrite `launch_picker`

Signature:

```python
def launch_picker(
    db: WallpaperDB,
    config: WpickConfig,
    *,
    force_thumbnails: bool = False,
) -> Path | None:
    """
    Full picker flow: load data, generate thumbnails, launch rofi.
    Returns selected wallpaper path or None if cancelled.
    Raises PickerError on unrecoverable failure.
    """
```

Logic:
1. `clusters = db.get_clusters()` — raise `PickerError("no clusters — run wpick cluster first")` if empty
2. `images = db.get_all_images()`
3. `thumbnails = generate_all_thumbnails(images, config, force=force_thumbnails)`
4. `entries = build_rofi_entries(clusters, images, {t.image_id: t.thumb_path for t in thumbnails})`
5. Raise `PickerError("no displayable images")` if `entries` is empty
6. `selected = _launch_rofi(entries, config.rofi_theme)` — return `None` if cancelled
7. Return `selected.path`

### Task 6 — Thumbnail cache invalidation

A thumbnail is stale if the source file's `mtime` is newer than the thumbnail's `mtime`. Check this in `generate_thumbnail`:

```python
def _is_cache_valid(source: Path, thumb: Path) -> bool:
    if not thumb.exists():
        return False
    return thumb.stat().st_mtime >= source.stat().st_mtime
```

`force=True` skips this check and always regenerates.

---

## Constraints
- `PickerError(WpickError)` is the only exception that escapes `picker.py`
- `picker.py` must not import `sqlite3` directly
- `launch_picker` returns `Path | None` — callers must not receive `str`
- Thumbnail cache directory is `config.cache_dir / "thumbs"` — created if missing, never hardcoded
- rofi cancellation (exit 1) is not an error — return `None` cleanly
- basedpyright zero errors after changes
