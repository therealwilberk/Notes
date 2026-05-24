---
tags:
  - project
  - wpick
  - extraction
  - auto-palette
parent: "[[wpick]]"
created: 2026-05-23
---

# wpick — Extraction

## Approach

Use **auto-palette** (Rust binary) for dominant color extraction. Don't reinvent what works.

### Pipeline per image

1. Open + validate image
2. Call `auto-palette <path> --format json`
3. Parse output: dominant colors + OKLAB values + weights
4. Compute global stats (brightness, contrast, warmth, entropy)
5. Build flat feature vector: `[L,a,b,weight]*n_colors + [stats]`

## auto-palette Integration

### Install

```bash
# From source
cargo install auto-palette-cli

# Or download binary from releases
# https://github.com/utsumi-h/auto-palette/releases
```

### CLI interface

```bash
auto-palette image.jpg --format json
```

Output:
```json
{
  "palette": [
    {"color": {"r": 220, "g": 50, "b": 50}, "population": 0.35},
    {"color": {"r": 40, "g": 40, "b": 220}, "population": 0.25},
    ...
  ]
}
```

### extractor.py

```python
"""
Feature extraction: image → auto-palette → OKLab vector + global stats.

Pipeline per image:
  1. Call auto-palette binary
  2. Parse JSON output
  3. Compute stats (brightness, contrast, warmth, entropy)
  4. Build flat feature vector
"""
from __future__ import annotations

import json
import logging
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, UnidentifiedImageError

from wpick import config, db
from wpick.oklab import srgb_to_oklab

logger = logging.getLogger(__name__)

# Feature vector layout:
#   [L0, a0, b0, w0, L1, a1, b1, w1, ..., Lk, ak, bk, wk,  <- palette: k*4
#    mean_L, std_L, mean_a, mean_b, warmth, entropy]         <- stats: 6
# Total dims = n_colors * 4 + 6


class ExtractionError(Exception):
    pass


def _call_auto_palette(path: Path) -> list[dict]:
    """Call auto-palette binary, return palette entries."""
    try:
        result = subprocess.run(
            ["auto-palette", str(path), "--format", "json"],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except FileNotFoundError:
        raise ExtractionError("auto-palette not found in PATH")
    except subprocess.TimeoutExpired:
        raise ExtractionError(f"auto-palette timed out on {path.name}")

    if result.returncode != 0:
        raise ExtractionError(f"auto-palette failed: {result.stderr.strip()}")

    try:
        data = json.loads(result.stdout)
        return data.get("palette", [])
    except json.JSONDecodeError as e:
        raise ExtractionError(f"Invalid auto-palette output: {e}")


def _compute_stats(path: Path) -> dict:
    """Compute global image statistics."""
    try:
        img = Image.open(path)
        img.verify()
        img = Image.open(path)
    except (UnidentifiedImageError, Exception) as e:
        raise ExtractionError(f"Cannot open image: {e}")

    if img.mode != "RGB":
        img = img.convert("RGB")

    # Resize for stats computation
    cfg = config.get()
    sample_size = cfg["extraction"]["sample_size"]
    w, h = img.size
    scale = sample_size / max(w, h)
    new_w, new_h = max(1, int(w * scale)), max(1, int(h * scale))
    img = img.resize((new_w, new_h), Image.LANCZOS)

    pixels = np.array(img, dtype=np.float32) / 255.0
    flat = pixels.reshape(-1, 3)
    r, g, b = flat[:, 0], flat[:, 1], flat[:, 2]

    # Perceived brightness (ITU-R BT.709)
    brightness = float((0.2126 * r + 0.7152 * g + 0.0722 * b).mean())

    # Contrast: std of brightness
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    contrast = float(lum.std())

    # Warmth: ratio of (R+G) vs B
    warmth = float((r.mean() + g.mean() * 0.5) - b.mean())

    # Entropy on quantized brightness (8 bins)
    hist, _ = np.histogram(lum, bins=8, range=(0, 1))
    hist = hist / hist.sum()
    hist = hist[hist > 0]
    entropy = float(-np.sum(hist * np.log2(hist)))

    return {
        "brightness": brightness,
        "contrast": contrast,
        "warmth": warmth,
        "entropy": entropy,
    }


def extract_features(path: Path) -> dict:
    """
    Full extraction pipeline for one image.

    Returns dict with keys: image_id, path, vector (np.ndarray), palette, stats
    Raises ExtractionError on failure.
    """
    cfg = config.get()
    n_colors = cfg["extraction"]["n_colors"]

    # Call auto-palette
    palette_raw = _call_auto_palette(path)

    # Convert to OKLab and build palette
    palette = []
    for entry in palette_raw[:n_colors]:
        c = entry["color"]
        rgb = np.array([c["r"] / 255.0, c["g"] / 255.0, c["b"] / 255.0], dtype=np.float32)
        oklab = srgb_to_oklab(rgb)
        palette.append({
            "hex": "#{:02x}{:02x}{:02x}".format(c["r"], c["g"], c["b"]),
            "rgb": rgb.tolist(),
            "oklab": oklab.tolist(),
            "weight": entry["population"],
        })

    # Pad if fewer colors than expected
    while len(palette) < n_colors:
        palette.append({
            "hex": "#000000",
            "rgb": [0.0, 0.0, 0.0],
            "oklab": [0.0, 0.0, 0.0],
            "weight": 0.0,
        })

    # Compute stats
    stats = _compute_stats(path)

    # Build flat feature vector
    oklab_colors = np.array([p["oklab"] for p in palette], dtype=np.float32)
    weights = np.array([p["weight"] for p in palette], dtype=np.float32)
    palette_part = np.column_stack([oklab_colors, weights]).flatten()

    stats_part = np.array([
        oklab_colors[:, 0].mean(),   # mean_L
        oklab_colors[:, 0].std(),    # std_L
        oklab_colors[:, 1].mean(),   # mean_a
        oklab_colors[:, 2].mean(),   # mean_b
        stats["warmth"],
        stats["entropy"],
    ], dtype=np.float32)

    vector = np.concatenate([palette_part, stats_part])

    return {
        "image_id": db.image_id(path),
        "path": str(path),
        "vector": vector,
        "palette": palette,
        "stats": stats,
    }


def scan_and_extract(
    wallpapers_root: Path,
    force: bool = False,
    on_progress: callable | None = None,
) -> tuple[int, int, int]:
    """Scan wallpapers_root, extract features for all images."""
    cfg = config.get()
    extensions = set(cfg["extraction"]["extensions"])

    paths = [
        p for ext in extensions
        for p in wallpapers_root.rglob(f"*.{ext}")
    ]
    paths += [
        p for ext in extensions
        for p in wallpapers_root.rglob(f"*.{ext.upper()}")
    ]
    paths = sorted(set(paths))

    for p in paths:
        db.upsert_image(p, wallpapers_root)

    if not force:
        unextracted = {r["path"] for r in db.get_unextracted_images()}
        paths = [p for p in paths if str(p.resolve()) in unextracted]

    total = len(paths)
    extracted = 0
    errors = 0

    for i, path in enumerate(paths):
        if on_progress:
            on_progress(i + 1, total, path)
        try:
            result = extract_features(path)
            db.store_features(
                result["image_id"],
                result["vector"],
                result["palette"],
                result["stats"],
            )
            _append_jsonl(result)
            extracted += 1
        except ExtractionError as e:
            logger.warning(f"Skipping {path}: {e}")
            errors += 1
        except Exception as e:
            logger.error(f"Unexpected error on {path}: {e}")
            errors += 1

    return total, extracted, errors


def _append_jsonl(result: dict) -> None:
    cfg = config.get()
    out = Path(cfg["paths"]["storage"]) / "features.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    line = {
        "image_id": result["image_id"],
        "path": result["path"],
        "palette": result["palette"],
        "stats": result["stats"],
    }
    with open(out, "a") as f:
        f.write(json.dumps(line) + "\n")
```

## See Also

- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/00-Architecture]] — Pipeline overview
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/04-Clustering]] — What happens after extraction
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/07-Picker]] — How palette is displayed
