---
tags:
  - project
  - wpick
  - picker
  - rofi
  - ui
parent: "[[wpick]]"
created: 2026-05-23
---

# wpick — Picker

## Approach

rofi card grid — Hyde-style. Large preview thumbnails, grouped by cluster.

## Hyde Reference

From Hyde-project/hyde:
- `listview { columns: 4; }` (dynamic based on monitor width)
- `element { orientation: vertical; }` (icon on top, text below)
- `element-icon { size: 20em; }` (large preview cards)
- Cluster headers with member count
- Click to apply wallpaper + matugen theme

## Thumbnail Generation

```python
def _generate_thumbnail(image_path: Path, image_id: str) -> Path:
    thumb = _thumbnail_path(image_id)
    if thumb.exists():
        return thumb
    try:
        cfg = config.get()
        size = cfg["thumbnails"]["size"]
        quality = cfg["thumbnails"]["quality"]
        img = Image.open(image_path).convert("RGB")
        img.thumbnail((size, size), Image.LANCZOS)
        img.save(thumb, "JPEG", quality=quality)
    except Exception as e:
        logger.warning(f"Thumbnail failed for {image_path}: {e}")
    return thumb
```

## Rofi Entry Format

```
CLUSTER / filename\x00icon\x1f/path/to/thumbnail.jpg
```

Cluster headers:
```
── cluster_0 (42 images) ──\x00nonselectable\x1ftrue
```

## rofi Theme (Card Grid)

```rasi
/* wpick.rasi — wallpaper picker theme (Hyde-style card grid) */

* {
    bg-col:         #0d1117;
    bg-col-light:   #161b22;
    border-col:     #30363d;
    selected-col:   #1f6feb;
    fg-col:         #c9d1d9;
    fg-col2:        #8b949e;
    accent:         #58a6ff;

    font:           "JetBrains Mono 11";
    background-color: transparent;
    text-color:     @fg-col;
}

window {
    width:          90%;
    transparency:   "real";
    background-color: @bg-col;
    border:         2px solid;
    border-color:   @border-col;
    border-radius:  12px;
    padding:        0;
}

mainbox {
    background-color: transparent;
    children:       [inputbar, listview];
    spacing:        0;
    padding:        12px;
}

inputbar {
    background-color: @bg-col-light;
    border-radius:  8px;
    padding:        10px 14px;
    margin:         0 0 10px 0;
    children:       [prompt, textbox-prompt-colon, entry];
}

prompt {
    background-color: transparent;
    text-color:     @accent;
}

textbox-prompt-colon {
    expand:         false;
    str:            " ❯ ";
    text-color:     @fg-col2;
}

entry {
    background-color: transparent;
    text-color:     @fg-col;
    cursor:         text;
}

listview {
    background-color: transparent;
    columns:        4;
    lines:          3;
    scrollbar:      false;
    spacing:        10px;
    fixed-height:   false;
    dynamic:        true;
}

element {
    background-color: transparent;
    border-radius:  8px;
    padding:        8px;
    orientation:    vertical;
    spacing:        6px;
}

element selected.normal {
    background-color: @selected-col;
    text-color:     #ffffff;
}

element-icon {
    size:           20em;
    border-radius:  6px;
}

element-text {
    vertical-align: 0.5;
    horizontal-align: 0.5;
    text-color:     inherit;
}
```

## Dynamic Column Count

```python
def _get_column_count() -> int:
    """Calculate column count based on monitor width."""
    try:
        result = subprocess.run(
            ["hyprctl", "monitors", "-j"],
            capture_output=True, text=True
        )
        monitors = json.loads(result.stdout)
        focused = next((m for m in monitors if m.get("focused")), monitors[0])
        width = focused.get("width", 1920)
        scale = focused.get("scale", 1.0)
        effective_width = int(width / scale)

        # 20em @ 11px font ≈ 220px per card + 10px spacing
        card_width = 230
        cols = max(2, min(6, effective_width // card_width))
        return cols
    except Exception:
        return 4  # fallback
```

## picker.py

```python
"""Picker: rofi-based wallpaper browser, grouped by cluster."""
from __future__ import annotations

import json
import logging
import subprocess
from pathlib import Path

from PIL import Image

from wpick import config, db
from wpick.orchestrator import set_wallpaper, WallpaperError

logger = logging.getLogger(__name__)


def _thumbnail_path(image_id: str) -> Path:
    cfg = config.get()
    cache = Path(cfg["paths"]["cache"]) / "thumbnails"
    cache.mkdir(parents=True, exist_ok=True)
    return cache / f"{image_id}.jpg"


def _generate_thumbnail(image_path: Path, image_id: str) -> Path:
    thumb = _thumbnail_path(image_id)
    if thumb.exists():
        return thumb
    try:
        cfg = config.get()
        size = cfg["thumbnails"]["size"]
        quality = cfg["thumbnails"]["quality"]
        img = Image.open(image_path).convert("RGB")
        img.thumbnail((size, size), Image.LANCZOS)
        img.save(thumb, "JPEG", quality=quality)
    except Exception as e:
        logger.warning(f"Thumbnail failed for {image_path}: {e}")
    return thumb


def _get_clusters_with_images() -> list[dict]:
    """Return clusters sorted by member count, each with their images."""
    with db.connection() as conn:
        clusters = conn.execute(
            "SELECT id, member_count, name FROM clusters ORDER BY member_count DESC"
        ).fetchall()

    result = []
    for cluster in clusters:
        images = db.get_images_by_cluster(cluster["id"])
        if images:
            result.append({
                "cluster_id": cluster["id"],
                "cluster_name": cluster["name"] or cluster["id"],
                "member_count": cluster["member_count"],
                "images": [dict(img) for img in images],
            })
    return result


def _build_rofi_input(clusters: list[dict]) -> tuple[str, dict[str, str]]:
    """Build rofi dmenu input string and a map of entry_key → image_path."""
    lines = []
    path_map = {}

    for cluster in clusters:
        cluster_id = cluster["cluster_id"]
        cluster_name = cluster["cluster_name"]
        count = cluster["member_count"]
        lines.append(f"── {cluster_name} ({count}) ──\x00nonselectable\x1ftrue")

        for img in cluster["images"]:
            img_id = img["id"]
            name = img["filename"]
            img_path = Path(img["path"])

            thumb = _generate_thumbnail(img_path, img_id)
            entry_key = f"{cluster_id}/{name}"

            if thumb.exists():
                line = f"{entry_key}\x00icon\x1f{thumb}"
            else:
                line = entry_key

            lines.append(line)
            path_map[entry_key] = img["path"]

    return "\n".join(lines), path_map


def launch_picker() -> None:
    """Launch rofi picker. On selection, sets wallpaper and calls matugen."""
    cfg = config.get()
    rasi = Path(__file__).parent.parent.parent / "rofi" / "wpick.rasi"

    clusters = _get_clusters_with_images()
    if not clusters:
        logger.error("No clusters found. Run `wpick scan && wpick cluster` first.")
        return

    rofi_input, path_map = _build_rofi_input(clusters)

    # Dynamic column count
    try:
        result = subprocess.run(
            ["hyprctl", "monitors", "-j"],
            capture_output=True, text=True
        )
        monitors = json.loads(result.stdout)
        focused = next((m for m in monitors if m.get("focused")), monitors[0])
        width = focused.get("width", 1920)
        scale = focused.get("scale", 1.0)
        effective_width = int(width / scale)
        cols = max(2, min(6, effective_width // 230))
    except Exception:
        cols = 4

    r_override = f"listview{{columns:{cols};}}"

    rofi_cmd = [
        "rofi", "-dmenu",
        "-i",
        "-p", "wallpaper",
        "-show-icons",
        "-format", "s",
        "-theme-str", r_override,
    ]
    if rasi.exists():
        rofi_cmd += ["-theme", str(rasi)]

    try:
        result = subprocess.run(
            rofi_cmd,
            input=rofi_input,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        logger.error("rofi not found. Install: pacman -S rofi-wayland")
        return

    if result.returncode != 0:
        return

    selected = result.stdout.strip()
    if not selected or selected not in path_map:
        return

    img_path = Path(path_map[selected])
    try:
        set_wallpaper(img_path)
    except WallpaperError as e:
        logger.error(f"Failed to set wallpaper: {e}")
```

## See Also

- [[06-Orchestrator]] — What happens after selection
- [[08-CLI]] — `wpick pick` command
- [[10-Deployment]] — Keybind setup
