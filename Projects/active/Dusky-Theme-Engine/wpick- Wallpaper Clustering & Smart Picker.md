

## Complete Roadmap: Dev → Production

> **Stack**: Arch + Hyprland · swww · matugen · rofi · uv · Python 3.12+  
> **Working name**: `wpick` — rename freely before publishing  
> **Scope**: 1500+ images, nested dirs, incremental on new images, shareable later

---

## Table of Contents

1. [Mental Model](https://claude.ai/chat/390c1167-a5cb-43fa-a3ac-21d7127faa07#1-mental-model)
2. [Project Layout](https://claude.ai/chat/390c1167-a5cb-43fa-a3ac-21d7127faa07#2-project-layout)
3. [Environment Setup (uv)](https://claude.ai/chat/390c1167-a5cb-43fa-a3ac-21d7127faa07#3-environment-setup-uv)
4. [Configuration](https://claude.ai/chat/390c1167-a5cb-43fa-a3ac-21d7127faa07#4-configuration)
5. [Database Schema](https://claude.ai/chat/390c1167-a5cb-43fa-a3ac-21d7127faa07#5-database-schema)
6. [Module Design](https://claude.ai/chat/390c1167-a5cb-43fa-a3ac-21d7127faa07#6-module-design)
    - 6.1 [db.py — Storage Layer]
    - 6.2 [config.py — Config Loader]
    - 6.3 [extractor.py — Feature Extraction]
    - 6.4 [clusterer.py — HDBSCAN Clustering]
    - 6.5 [assigner.py — Incremental Assignment]
    - 6.6 [orchestrator.py — Watcher + Integration]
    - 6.7 [picker.py — rofi Interface
    - 6.8 [cli.py — Entry Points]
7. [OKLab Conversion]
8. [rofi Theme & Picker Script](https://claude.ai/chat/390c1167-a5cb-43fa-a3ac-21d7127faa07#8-rofi-theme--picker-script)
9. [swww + matugen Integration](https://claude.ai/chat/390c1167-a5cb-43fa-a3ac-21d7127faa07#9-swww--matugen-integration)
10. [Error Handling Strategy](https://claude.ai/chat/390c1167-a5cb-43fa-a3ac-21d7127faa07#10-error-handling-strategy)
11. [Tests](https://claude.ai/chat/390c1167-a5cb-43fa-a3ac-21d7127faa07#11-tests)
12. [systemd User Service](https://claude.ai/chat/390c1167-a5cb-43fa-a3ac-21d7127faa07#12-systemd-user-service)
13. [Production Checklist](https://claude.ai/chat/390c1167-a5cb-43fa-a3ac-21d7127faa07#13-production-checklist)
14. [Future: Rust Extractor](https://claude.ai/chat/390c1167-a5cb-43fa-a3ac-21d7127faa07#14-future-rust-extractor)
15. [Phase Summary](https://claude.ai/chat/390c1167-a5cb-43fa-a3ac-21d7127faa07#15-phase-summary)

---

## 1. Mental Model

Before touching code, internalize this:

```
wallpapers/           ← your nested image dirs, read-only from wpick's perspective
  ├── mushrooms/
  ├── scifi/
  └── landscapes/

       ↓  scan

extractor             ← Pillow + OKLab conversion, outputs feature vectors
       ↓
features.jsonl        ← one JSON object per line, source of truth for ML

       ↓  (first time or manual recluster)

clusterer             ← HDBSCAN, reads all features, outputs cluster map
       ↓
clusters.json         ← {cluster_id → [image_ids], centroid → [...]}

       ↓  (on new images)

assigner              ← cosine similarity against stored centroids
       ↓
updates DB only       ← no full recluster

       ↓  (user action)

picker                ← rofi dmenu, shows thumbnails grouped by cluster
       ↓
selected path
       ↓
swww img <path>       ← sets wallpaper
       ↓
matugen image <path>  ← generates color scheme (matugen handles the rest)
```

**Key separation**: matugen is downstream of everything. wpick's clustering job is purely navigation (grouping by aesthetic similarity). Theme accuracy is matugen's job.

**New image flow**: extractor → assigner (nearest centroid) → DB update. No recluster.

**When to recluster**: manually, after bulk additions, or on a schedule. Never automatically on new image — that causes cluster drift.

---

## 2. Project Layout

```
~/.config/wpick/
├── pyproject.toml
├── uv.lock
├── .venv/                         ← managed by uv, never touch manually
├── config.toml                    ← user config, not in version control
├── config.default.toml            ← shipped defaults, version controlled
│
├── src/
│   └── wpick/
│       ├── __init__.py
│       ├── cli.py                 ← typer entry points
│       ├── config.py              ← config loader (tomllib)
│       ├── db.py                  ← all SQLite operations
│       ├── extractor.py           ← image → feature vector
│       ├── clusterer.py           ← feature vectors → cluster map
│       ├── assigner.py            ← new image → nearest cluster
│       ├── orchestrator.py        ← watcher + swww + matugen calls
│       ├── picker.py              ← rofi interface + thumbnail gen
│       └── oklab.py               ← color space conversions
│
├── rofi/
│   ├── wpick.rasi                 ← rofi theme (HydeSee-style)
│   └── wpick-picker.sh            ← rofi launch wrapper
│
├── systemd/
│   └── wpick-watch.service        ← user service
│
├── storage/                       ← runtime data, gitignored
│   ├── wpick.db
│   └── features.jsonl
│
└── tests/
    ├── conftest.py
    ├── fixtures/
    │   ├── solid_red.png          ← 64x64 solid red
    │   ├── solid_blue.png         ← 64x64 solid blue
    │   ├── gradient.png           ← horizontal gradient
    │   └── corrupt.bin            ← not an image, for error tests
    ├── test_oklab.py
    ├── test_extractor.py
    ├── test_clusterer.py
    ├── test_assigner.py
    ├── test_db.py
    └── test_integration.py
```

---

## 3. Environment Setup (uv)

### 3.1 Install uv (if not present)

```bash
# Check
uv --version

# Install if missing
curl -LsSf https://astral.sh/uv/install.sh | sh
# or: pacman -S uv (if in AUR)
```

### 3.2 Initialize project

```bash
mkdir -p ~/.config/wpick
cd ~/.config/wpick

uv init --name wpick --python 3.12
```

### 3.3 Add dependencies

```bash
# Core
uv add pillow hdbscan numpy scikit-learn typer tomllib-backport

# Note: tomllib is stdlib in Python 3.11+, backport for older
# If using 3.12 (recommended), skip tomllib-backport

# Watching
uv add watchdog

# Dev/test
uv add --dev pytest pytest-cov pytest-mock ruff mypy
```

Full `pyproject.toml`:

```toml
[project]
name = "wpick"
version = "0.1.0"
description = "Wallpaper clustering and smart picker for Hyprland"
requires-python = ">=3.12"
dependencies = [
    "pillow>=10.0",
    "hdbscan>=0.8.33",
    "numpy>=1.26",
    "scikit-learn>=1.4",
    "typer>=0.12",
    "watchdog>=4.0",
]

[project.scripts]
wpick = "wpick.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/wpick"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src/wpick --cov-report=term-missing -v"

[tool.ruff]
line-length = 100
src = ["src"]

[tool.mypy]
strict = false
ignore_missing_imports = true

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "pytest-mock>=3.12",
    "ruff>=0.4",
    "mypy>=1.10",
]
```

### 3.4 Verify

```bash
uv run python --version   # should print 3.12.x
uv run pytest --collect-only  # should collect 0 tests (none written yet, no error)
```

### 3.5 Running commands

```bash
# During development (runs in venv automatically)
uv run wpick scan
uv run wpick cluster
uv run wpick pick

# Install as tool (for system-wide use, e.g. from rofi scripts)
uv tool install .
# Then: wpick scan works anywhere without uv run
```

---

## 4. Configuration

### `config.default.toml`

```toml
[paths]
# All paths support ~ expansion
wallpapers = "~/wallpapers"
cache      = "~/.cache/wpick"
storage    = "~/.local/share/wpick"

[extraction]
sample_size = 256        # resize longest edge to this before processing
n_colors    = 8          # dominant colors per image
extensions  = ["jpg", "jpeg", "png", "webp", "bmp"]

[clustering]
min_cluster_size = 8     # HDBSCAN: minimum images per cluster
min_samples      = 3     # HDBSCAN: core point threshold
# Images HDBSCAN labels as noise (-1) go to a "misc" catch-all cluster

[thumbnails]
size    = 256            # thumbnail longest edge in pixels
quality = 85             # JPEG quality

[swww]
transition_type   = "grow"
transition_pos    = "0.5,0.5"
transition_fps    = 60
transition_duration = 1.5

[matugen]
enabled = true
# Additional matugen flags, appended verbatim
extra_flags = []

[watcher]
enabled         = true
debounce_seconds = 5     # wait after last event before processing
```

### `src/wpick/config.py`

```python
"""Config loader. Merges defaults with user overrides."""
from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any


_DEFAULTS_PATH = Path(__file__).parent.parent.parent / "config.default.toml"
_USER_PATH = Path("~/.config/wpick/config.toml").expanduser()


def _expand_paths(d: dict[str, Any]) -> dict[str, Any]:
    """Recursively expand ~ in string values under 'paths' key."""
    result = {}
    for k, v in d.items():
        if isinstance(v, dict):
            result[k] = _expand_paths(v)
        elif isinstance(v, str) and v.startswith("~"):
            result[k] = str(Path(v).expanduser())
        else:
            result[k] = v
    return result


def load() -> dict[str, Any]:
    with open(_DEFAULTS_PATH, "rb") as f:
        cfg = tomllib.load(f)

    if _USER_PATH.exists():
        with open(_USER_PATH, "rb") as f:
            user = tomllib.load(f)
        # Shallow merge per section
        for section, values in user.items():
            if section in cfg and isinstance(cfg[section], dict):
                cfg[section].update(values)
            else:
                cfg[section] = values

    return _expand_paths(cfg)


# Module-level singleton
_cfg: dict[str, Any] | None = None


def get() -> dict[str, Any]:
    global _cfg
    if _cfg is None:
        _cfg = load()
    return _cfg
```

---

## 5. Database Schema

Single SQLite file at `~/.local/share/wpick/wpick.db`.

```sql
-- images: one row per discovered wallpaper
CREATE TABLE IF NOT EXISTS images (
    id           TEXT PRIMARY KEY,   -- sha256[:16] of absolute path
    path         TEXT UNIQUE NOT NULL,
    folder       TEXT NOT NULL,      -- relative folder name from wallpapers root
    filename     TEXT NOT NULL,
    width        INTEGER,
    height       INTEGER,
    file_size    INTEGER,
    extracted_at TEXT,               -- ISO8601 or NULL if not yet extracted
    cluster_id   TEXT,               -- FK → clusters.id, NULL until assigned
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

-- features: separate table, can be rebuilt from features.jsonl
CREATE TABLE IF NOT EXISTS features (
    image_id     TEXT PRIMARY KEY REFERENCES images(id),
    vector       BLOB NOT NULL,       -- numpy array, stored as float32 bytes
    palette_json TEXT NOT NULL,       -- full palette for display/debug
    stats_json   TEXT NOT NULL,       -- brightness/contrast/warmth/entropy
    version      INTEGER NOT NULL DEFAULT 1  -- bump when extraction logic changes
);

-- clusters: output of HDBSCAN run
CREATE TABLE IF NOT EXISTS clusters (
    id            TEXT PRIMARY KEY,   -- "cluster_0", "cluster_1", ..., "misc"
    label         INTEGER NOT NULL,   -- raw HDBSCAN label (-1 = noise → misc)
    centroid      BLOB NOT NULL,      -- numpy float32 bytes
    member_count  INTEGER NOT NULL DEFAULT 0,
    created_at    TEXT NOT NULL DEFAULT (datetime('now')),
    run_id        TEXT NOT NULL       -- which clustering run produced this
);

-- cluster_runs: audit log of recluster events
CREATE TABLE IF NOT EXISTS cluster_runs (
    id           TEXT PRIMARY KEY,
    image_count  INTEGER NOT NULL,
    cluster_count INTEGER NOT NULL,
    noise_count  INTEGER NOT NULL,
    params_json  TEXT NOT NULL,       -- HDBSCAN params used
    ran_at       TEXT NOT NULL DEFAULT (datetime('now'))
);

-- history: what was actually set as wallpaper
CREATE TABLE IF NOT EXISTS history (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    image_id   TEXT NOT NULL REFERENCES images(id),
    set_at     TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_images_cluster ON images(cluster_id);
CREATE INDEX IF NOT EXISTS idx_images_folder  ON images(folder);
CREATE INDEX IF NOT EXISTS idx_history_recent ON history(set_at DESC);
```

---

## 6. Module Design

### 6.1 `db.py` — Storage Layer

```python
"""All database operations. No business logic here."""
from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

import numpy as np

from wpick import config


def _db_path() -> Path:
    p = Path(config.get()["paths"]["storage"]) / "wpick.db"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


@contextmanager
def connection() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_schema() -> None:
    sql_path = Path(__file__).parent.parent.parent / "schema.sql"
    with connection() as conn:
        conn.executescript(sql_path.read_text())


def image_id(path: Path) -> str:
    return hashlib.sha256(str(path.resolve()).encode()).hexdigest()[:16]


def upsert_image(path: Path, wallpapers_root: Path) -> str:
    img_id = image_id(path)
    folder = path.relative_to(wallpapers_root).parent.as_posix()
    with connection() as conn:
        conn.execute(
            """
            INSERT INTO images (id, path, folder, filename)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                path = excluded.path,
                folder = excluded.folder
            """,
            (img_id, str(path.resolve()), folder, path.name),
        )
    return img_id


def store_features(image_id: str, vector: np.ndarray, palette: list, stats: dict) -> None:
    with connection() as conn:
        conn.execute(
            """
            INSERT INTO features (image_id, vector, palette_json, stats_json)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(image_id) DO UPDATE SET
                vector = excluded.vector,
                palette_json = excluded.palette_json,
                stats_json = excluded.stats_json,
                version = version + 1
            """,
            (
                image_id,
                vector.astype(np.float32).tobytes(),
                json.dumps(palette),
                json.dumps(stats),
            ),
        )
        conn.execute(
            "UPDATE images SET extracted_at = datetime('now') WHERE id = ?",
            (image_id,),
        )


def load_all_features() -> list[dict]:
    """Returns list of {image_id, vector (np.ndarray)}."""
    with connection() as conn:
        rows = conn.execute(
            "SELECT f.image_id, f.vector FROM features f JOIN images i ON f.image_id = i.id"
        ).fetchall()
    return [
        {
            "image_id": r["image_id"],
            "vector": np.frombuffer(r["vector"], dtype=np.float32),
        }
        for r in rows
    ]


def store_cluster_run(run_id: str, cluster_count: int, noise_count: int,
                      image_count: int, params: dict) -> None:
    with connection() as conn:
        conn.execute(
            """
            INSERT INTO cluster_runs (id, image_count, cluster_count, noise_count, params_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            (run_id, image_count, cluster_count, noise_count, json.dumps(params)),
        )


def store_cluster(cluster_id: str, label: int, centroid: np.ndarray,
                  member_count: int, run_id: str) -> None:
    with connection() as conn:
        conn.execute(
            """
            INSERT INTO clusters (id, label, centroid, member_count, run_id)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                centroid = excluded.centroid,
                member_count = excluded.member_count,
                run_id = excluded.run_id
            """,
            (cluster_id, label, centroid.astype(np.float32).tobytes(), member_count, run_id),
        )


def assign_image_to_cluster(image_id: str, cluster_id: str) -> None:
    with connection() as conn:
        conn.execute(
            "UPDATE images SET cluster_id = ? WHERE id = ?",
            (cluster_id, image_id),
        )


def load_all_centroids() -> list[dict]:
    with connection() as conn:
        rows = conn.execute("SELECT id, centroid FROM clusters").fetchall()
    return [
        {"cluster_id": r["id"], "centroid": np.frombuffer(r["centroid"], dtype=np.float32)}
        for r in rows
    ]


def get_images_by_cluster(cluster_id: str) -> list[sqlite3.Row]:
    with connection() as conn:
        return conn.execute(
            "SELECT id, path, filename FROM images WHERE cluster_id = ? ORDER BY filename",
            (cluster_id,),
        ).fetchall()


def log_history(image_id: str) -> None:
    with connection() as conn:
        conn.execute("INSERT INTO history (image_id) VALUES (?)", (image_id,))


def get_unextracted_images() -> list[sqlite3.Row]:
    with connection() as conn:
        return conn.execute(
            "SELECT id, path FROM images WHERE extracted_at IS NULL"
        ).fetchall()


def get_unassigned_images() -> list[sqlite3.Row]:
    with connection() as conn:
        return conn.execute(
            "SELECT id, path FROM images WHERE extracted_at IS NOT NULL AND cluster_id IS NULL"
        ).fetchall()
```

---

### 6.2 `config.py` — Config Loader

_(Already shown in Section 4 above.)_

---

### 6.3 `extractor.py` — Feature Extraction

This is the most critical module. Every downstream step depends on vector quality.

```python
"""
Feature extraction: image → OKLab color vector + global stats.

Pipeline per image:
  1. Open + validate
  2. Resize to sample_size (longest edge)
  3. Convert to RGB (handles RGBA, P, LA modes)
  4. K-means (k=n_colors) → dominant colors + weights
  5. Convert each color to OKLab
  6. Compute global stats (brightness, contrast, warmth, entropy)
  7. Build flat feature vector: [L,a,b,weight]*n_colors + [stats]
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

import numpy as np
from PIL import Image, UnidentifiedImageError
from sklearn.cluster import MiniBatchKMeans

from wpick import config, db
from wpick.oklab import srgb_to_oklab

logger = logging.getLogger(__name__)

# Feature vector layout:
#   [L0, a0, b0, w0, L1, a1, b1, w1, ..., Lk, ak, bk, wk,  <- palette: k*4
#    mean_L, std_L, mean_a, mean_b, warmth, entropy]         <- stats: 6
# Total dims = n_colors * 4 + 6


class ExtractionError(Exception):
    pass


def _load_image(path: Path, sample_size: int) -> np.ndarray:
    """Load, resize, and return as float32 RGB array (H, W, 3) in [0,1]."""
    try:
        img = Image.open(path)
        img.verify()  # catches truncated files
        img = Image.open(path)  # reopen after verify (verify closes)
    except (UnidentifiedImageError, Exception) as e:
        raise ExtractionError(f"Cannot open image: {e}") from e

    # Normalize mode
    if img.mode == "RGBA":
        bg = Image.new("RGB", img.size, (0, 0, 0))
        bg.paste(img, mask=img.split()[3])
        img = bg
    elif img.mode != "RGB":
        img = img.convert("RGB")

    # Resize: longest edge → sample_size
    w, h = img.size
    scale = sample_size / max(w, h)
    new_w, new_h = max(1, int(w * scale)), max(1, int(h * scale))
    img = img.resize((new_w, new_h), Image.LANCZOS)

    arr = np.array(img, dtype=np.float32) / 255.0
    return arr


def _dominant_colors(
    pixels: np.ndarray, n_colors: int
) -> tuple[np.ndarray, np.ndarray]:
    """
    pixels: (N, 3) float32 in [0,1]
    Returns: colors (n_colors, 3), weights (n_colors,) summing to 1
    """
    flat = pixels.reshape(-1, 3)

    if len(flat) < n_colors:
        # Pad with black if image is tiny
        pad = np.zeros((n_colors - len(flat), 3), dtype=np.float32)
        flat = np.vstack([flat, pad])

    kmeans = MiniBatchKMeans(
        n_clusters=n_colors,
        random_state=42,
        n_init=3,
        batch_size=min(1000, len(flat)),
    )
    labels = kmeans.fit_predict(flat)
    centers = kmeans.cluster_centers_.astype(np.float32)

    counts = np.bincount(labels, minlength=n_colors).astype(np.float32)
    weights = counts / counts.sum()

    # Sort by weight descending (most dominant first)
    order = np.argsort(-weights)
    return centers[order], weights[order]


def _image_stats(pixels: np.ndarray) -> dict:
    """Global image statistics. pixels: (H, W, 3) float32 [0,1]."""
    flat = pixels.reshape(-1, 3)
    r, g, b = flat[:, 0], flat[:, 1], flat[:, 2]

    # Perceived brightness (ITU-R BT.709)
    brightness = (0.2126 * r + 0.7152 * g + 0.0722 * b).mean()

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
        "brightness": float(brightness),
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
    sample_size = cfg["extraction"]["sample_size"]
    n_colors = cfg["extraction"]["n_colors"]

    pixels = _load_image(path, sample_size)
    colors, weights = _dominant_colors(pixels, n_colors)
    stats = _image_stats(pixels)

    # Convert palette to OKLab
    oklab_colors = np.array([srgb_to_oklab(c) for c in colors], dtype=np.float32)

    # Palette for storage/display (original RGB + oklab + weight)
    palette = [
        {
            "hex": "#{:02x}{:02x}{:02x}".format(
                int(c[0] * 255), int(c[1] * 255), int(c[2] * 255)
            ),
            "rgb": c.tolist(),
            "oklab": oklab_colors[i].tolist(),
            "weight": float(weights[i]),
        }
        for i, c in enumerate(colors)
    ]

    # Build flat feature vector
    palette_part = np.column_stack([oklab_colors, weights]).flatten()  # n_colors * 4

    oklab_all = oklab_colors
    stats_part = np.array([
        oklab_all[:, 0].mean(),   # mean_L
        oklab_all[:, 0].std(),    # std_L
        oklab_all[:, 1].mean(),   # mean_a
        oklab_all[:, 2].mean(),   # mean_b
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
    """
    Scan wallpapers_root recursively, extract features for all images.

    Args:
        force: re-extract even if already extracted
        on_progress: callback(current, total, path)

    Returns: (total, extracted, skipped, errors)
    """
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

    # Register all paths in DB first
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
            # Also append to features.jsonl for debuggability
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
        # vector not in jsonl — too verbose, use DB for that
    }
    with open(out, "a") as f:
        f.write(json.dumps(line) + "\n")
```

---

### 6.4 `clusterer.py` — HDBSCAN Clustering

```python
"""
Clustering: all feature vectors → cluster map.

This is a FULL recluster. Run manually or after bulk additions.
Never triggered automatically on new images.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime

import numpy as np
from sklearn.preprocessing import StandardScaler

from wpick import config, db

logger = logging.getLogger(__name__)


class ClusteringError(Exception):
    pass


def _normalize(matrix: np.ndarray) -> np.ndarray:
    """StandardScaler normalization. Required before HDBSCAN."""
    scaler = StandardScaler()
    return scaler.fit_transform(matrix).astype(np.float32)


def run_clustering() -> dict:
    """
    Load all features, run HDBSCAN, store results.

    Returns summary dict.
    Raises ClusteringError if fewer than min_cluster_size*2 images.
    """
    # Import here: hdbscan has heavy import cost
    import hdbscan

    cfg = config.get()["clustering"]
    min_cluster_size = cfg["min_cluster_size"]
    min_samples = cfg["min_samples"]

    rows = db.load_all_features()
    if not rows:
        raise ClusteringError("No extracted features found. Run `wpick scan` first.")

    if len(rows) < min_cluster_size * 2:
        raise ClusteringError(
            f"Need at least {min_cluster_size * 2} images to cluster, "
            f"have {len(rows)}. Lower min_cluster_size or add more images."
        )

    image_ids = [r["image_id"] for r in rows]
    matrix = np.stack([r["vector"] for r in rows])

    logger.info(f"Clustering {len(rows)} images (vector dim={matrix.shape[1]})")

    normed = _normalize(matrix)

    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric="euclidean",
        cluster_selection_method="eom",
        prediction_data=True,
    )
    labels = clusterer.fit_predict(normed)

    unique_labels = set(labels)
    cluster_labels = sorted(l for l in unique_labels if l >= 0)
    noise_count = int(np.sum(labels == -1))
    cluster_count = len(cluster_labels)

    run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"

    # Store clusters
    for label in cluster_labels:
        mask = labels == label
        cluster_id = f"cluster_{label}"
        members = matrix[mask]
        centroid = members.mean(axis=0)
        db.store_cluster(cluster_id, label, centroid, int(mask.sum()), run_id)
        for img_id in np.array(image_ids)[mask]:
            db.assign_image_to_cluster(img_id, cluster_id)

    # Noise images → "misc" cluster
    if noise_count > 0:
        misc_mask = labels == -1
        misc_members = matrix[misc_mask]
        misc_centroid = misc_members.mean(axis=0)
        db.store_cluster("misc", -1, misc_centroid, noise_count, run_id)
        for img_id in np.array(image_ids)[misc_mask]:
            db.assign_image_to_cluster(img_id, "misc")

    db.store_cluster_run(
        run_id=run_id,
        cluster_count=cluster_count + (1 if noise_count else 0),
        noise_count=noise_count,
        image_count=len(rows),
        params={"min_cluster_size": min_cluster_size, "min_samples": min_samples},
    )

    summary = {
        "run_id": run_id,
        "total_images": len(rows),
        "clusters": cluster_count,
        "noise_images": noise_count,
        "labels": cluster_labels,
    }
    logger.info(f"Clustering complete: {cluster_count} clusters, {noise_count} noise")
    return summary
```

---

### 6.5 `assigner.py` — Incremental Assignment

```python
"""
Incremental assignment: new image → nearest existing cluster via cosine similarity.

Never triggers a recluster. If no clusters exist, images are quarantined
(cluster_id = NULL) until a recluster is run.
"""
from __future__ import annotations

import logging

import numpy as np

from wpick import db
from wpick.extractor import extract_features, ExtractionError
from pathlib import Path

logger = logging.getLogger(__name__)

_SIMILARITY_THRESHOLD = 0.65  # below this → goes to "misc"


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def assign_image(path: Path, wallpapers_root: Path) -> str | None:
    """
    Extract features for path, find nearest cluster centroid.

    Returns assigned cluster_id, or None if no clusters exist.
    """
    centroids = db.load_all_centroids()
    if not centroids:
        logger.warning("No clusters found. Image will be unassigned until recluster.")
        db.upsert_image(path, wallpapers_root)
        return None

    try:
        result = extract_features(path)
    except ExtractionError as e:
        logger.error(f"Cannot assign {path}: {e}")
        return None

    img_id = db.upsert_image(path, wallpapers_root)
    db.store_features(result["image_id"], result["vector"], result["palette"], result["stats"])

    vector = result["vector"]
    best_cluster = None
    best_sim = -1.0

    for c in centroids:
        sim = _cosine_similarity(vector, c["centroid"])
        if sim > best_sim:
            best_sim = sim
            best_cluster = c["cluster_id"]

    if best_sim < _SIMILARITY_THRESHOLD:
        logger.info(
            f"Low similarity ({best_sim:.3f}) for {path.name} → assigning to misc"
        )
        best_cluster = "misc"

    db.assign_image_to_cluster(result["image_id"], best_cluster)
    logger.info(f"Assigned {path.name} → {best_cluster} (similarity: {best_sim:.3f})")
    return best_cluster


def assign_all_unassigned(wallpapers_root: Path) -> tuple[int, int]:
    """Assign all images that have features but no cluster. Returns (assigned, failed)."""
    unassigned = db.get_unassigned_images()
    assigned = 0
    failed = 0
    for row in unassigned:
        result = assign_image(Path(row["path"]), wallpapers_root)
        if result:
            assigned += 1
        else:
            failed += 1
    return assigned, failed
```

---

### 6.6 `orchestrator.py` — Watcher + Integration

```python
"""
Orchestrator: filesystem watcher + swww + matugen integration.

Responsibilities:
- Watch wallpaper directory for new images
- Trigger extract → assign on new files
- Set wallpaper via swww
- Trigger matugen after set
- Log history

This module contains NO analysis logic.
"""
from __future__ import annotations

import logging
import shutil
import subprocess
import time
from pathlib import Path
from threading import Timer

from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from watchdog.observers import Observer

from wpick import config, db
from wpick.assigner import assign_image

logger = logging.getLogger(__name__)


class WallpaperError(Exception):
    pass


# ── swww integration ─────────────────────────────────────────────────────────

def _require_swww() -> None:
    if not shutil.which("swww"):
        raise WallpaperError("swww not found in PATH. Install: pacman -S swww")


def _ensure_swww_daemon() -> None:
    """Start swww-daemon if not running."""
    result = subprocess.run(["swww", "query"], capture_output=True)
    if result.returncode != 0:
        logger.info("swww daemon not running, starting...")
        subprocess.Popen(
            ["swww-daemon"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(0.5)  # give it a moment


def set_wallpaper(path: Path, log: bool = True) -> None:
    """
    Set wallpaper via swww, then call matugen.
    Raises WallpaperError on failure.
    """
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

    logger.info(f"Wallpaper set: {path.name}")

    if log:
        img_id = db.image_id(path)
        db.log_history(img_id)

    _call_matugen(path)


# ── matugen integration ───────────────────────────────────────────────────────

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
    else:
        logger.info("matugen theme generated")


# ── filesystem watcher ────────────────────────────────────────────────────────

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

        # Debounce: wait for file to finish writing
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


def start_watcher() -> None:
    """Blocking watcher. Run as a systemd service or background process."""
    cfg = config.get()
    root = Path(cfg["paths"]["wallpapers"])
    debounce = cfg["watcher"]["debounce_seconds"]

    if not root.exists():
        raise WallpaperError(f"Wallpapers directory not found: {root}")

    handler = _WallpaperHandler(root, debounce)
    observer = Observer()
    observer.schedule(handler, str(root), recursive=True)
    observer.start()

    logger.info(f"Watching {root} for new wallpapers...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()
```

---

### 6.7 `picker.py` — rofi Interface

```python
"""
Picker: rofi-based wallpaper browser, grouped by cluster.

Thumbnail generation:
  ~/.cache/wpick/thumbnails/<image_id>.jpg

rofi entry format (dmenu with icons):
  "filename\x00icon\x1f/path/to/thumbnail.jpg"
"""
from __future__ import annotations

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
        # Return a path that doesn't exist — rofi will show without icon
    return thumb


def _get_clusters_with_images() -> list[dict]:
    """Return clusters sorted by member count, each with their images."""
    with db.connection() as conn:
        clusters = conn.execute(
            "SELECT id, member_count FROM clusters ORDER BY member_count DESC"
        ).fetchall()

    result = []
    for cluster in clusters:
        images = db.get_images_by_cluster(cluster["id"])
        if images:
            result.append({
                "cluster_id": cluster["id"],
                "member_count": cluster["member_count"],
                "images": [dict(img) for img in images],
            })
    return result


def _build_rofi_input(clusters: list[dict]) -> tuple[str, dict[str, str]]:
    """
    Build rofi dmenu input string and a map of entry_key → image_path.

    Entry format: "CLUSTER / filename\x00icon\x1f/thumb/path"
    Cluster headers: "── cluster_0 (42) ──\x00nonselectable\x1ftrue"
    """
    lines = []
    path_map = {}

    for cluster in clusters:
        cluster_id = cluster["cluster_id"]
        count = cluster["member_count"]
        # Non-selectable header (rofi syntax)
        lines.append(f"── {cluster_id}  ({count} images) ──\x00nonselectable\x1ftrue")

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

    rofi_cmd = [
        "rofi", "-dmenu",
        "-i",                        # case insensitive
        "-p", "wallpaper",
        "-show-icons",
        "-format", "s",
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
        # User cancelled (ESC) or error
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

---

### 6.8 `cli.py` — Entry Points

```python
"""CLI entry points via Typer."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

app = typer.Typer(name="wpick", help="Wallpaper clustering and smart picker.")


@app.command()
def init():
    """Initialize database schema and cache directories."""
    from wpick import db, config
    db.init_schema()
    cfg = config.get()
    for key in ("cache", "storage"):
        Path(cfg["paths"][key]).mkdir(parents=True, exist_ok=True)
    typer.echo("✓ wpick initialized")


@app.command()
def scan(
    force: bool = typer.Option(False, "--force", help="Re-extract already-extracted images"),
    quiet: bool = typer.Option(False, "--quiet", "-q"),
):
    """Scan wallpaper directory and extract features from all images."""
    from wpick import config
    from wpick.extractor import scan_and_extract

    cfg = config.get()
    root = Path(cfg["paths"]["wallpapers"])

    if not root.exists():
        typer.echo(f"Error: wallpapers directory not found: {root}", err=True)
        raise typer.Exit(1)

    def progress(current, total, path):
        if not quiet:
            typer.echo(f"\r[{current}/{total}] {path.name}", nl=False)

    total, extracted, errors = scan_and_extract(root, force=force, on_progress=progress)
    if not quiet:
        typer.echo()  # newline after progress
    typer.echo(f"Scan complete: {extracted}/{total} extracted, {errors} errors")


@app.command()
def cluster():
    """Run HDBSCAN clustering on extracted features."""
    from wpick.clusterer import run_clustering, ClusteringError

    try:
        summary = run_clustering()
    except ClusteringError as e:
        typer.echo(f"Clustering failed: {e}", err=True)
        raise typer.Exit(1)

    typer.echo(
        f"✓ {summary['clusters']} clusters  |  "
        f"{summary['noise_images']} noise → misc  |  "
        f"run: {summary['run_id']}"
    )


@app.command()
def assign(
    path: Optional[Path] = typer.Argument(None, help="Specific image to assign"),
):
    """Assign new image(s) to existing clusters without reclustering."""
    from wpick import config
    from wpick.assigner import assign_image, assign_all_unassigned

    cfg = config.get()
    root = Path(cfg["paths"]["wallpapers"])

    if path:
        result = assign_image(path, root)
        if result:
            typer.echo(f"Assigned {path.name} → {result}")
        else:
            typer.echo(f"Could not assign {path.name} (no clusters or extraction error)")
    else:
        assigned, failed = assign_all_unassigned(root)
        typer.echo(f"Assigned: {assigned}, failed: {failed}")


@app.command()
def pick():
    """Launch rofi wallpaper picker."""
    from wpick.picker import launch_picker
    launch_picker()


@app.command()
def watch():
    """Start filesystem watcher daemon (blocks; use systemd service)."""
    from wpick.orchestrator import start_watcher, WallpaperError
    try:
        start_watcher()
    except WallpaperError as e:
        typer.echo(f"Watcher error: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def stats():
    """Show cluster statistics."""
    from wpick import db
    with db.connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM images").fetchone()[0]
        extracted = conn.execute(
            "SELECT COUNT(*) FROM images WHERE extracted_at IS NOT NULL"
        ).fetchone()[0]
        clusters = conn.execute("SELECT id, member_count FROM clusters ORDER BY member_count DESC").fetchall()

    typer.echo(f"Images: {total} total, {extracted} extracted")
    typer.echo(f"Clusters: {len(clusters)}")
    typer.echo()
    for c in clusters:
        bar = "█" * min(40, c["member_count"] // 2)
        typer.echo(f"  {c['id']:20s}  {c['member_count']:4d}  {bar}")


if __name__ == "__main__":
    app()
```

---

## 7. OKLab Conversion

```python
# src/wpick/oklab.py
"""
sRGB → OKLab conversion.
Reference: https://bottosson.github.io/posts/oklab/

No external dependency. ~30 lines, correct.
"""
from __future__ import annotations

import numpy as np


def _srgb_to_linear(c: float) -> float:
    """Gamma correction: sRGB → linear."""
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def srgb_to_oklab(rgb: np.ndarray) -> np.ndarray:
    """
    Convert sRGB color to OKLab.

    Args:
        rgb: array of shape (3,), values in [0, 1]

    Returns:
        array of shape (3,): [L, a, b]
        L in [0, 1], a and b roughly in [-0.5, 0.5]
    """
    r, g, b = float(rgb[0]), float(rgb[1]), float(rgb[2])

    # Gamma correction
    r = _srgb_to_linear(r)
    g = _srgb_to_linear(g)
    b = _srgb_to_linear(b)

    # Linear sRGB → LMS (Oklab M1 matrix)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b

    # Cube root
    l_ = l ** (1.0 / 3.0)
    m_ = m ** (1.0 / 3.0)
    s_ = s ** (1.0 / 3.0)

    # LMS → OKLab (M2 matrix)
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b_ = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_

    return np.array([L, a, b_], dtype=np.float32)
```

---

## 8. rofi Theme & Picker Script

### `rofi/wpick.rasi`

Adapted from HydeSee's aesthetic. Dark, card-like, wide icon previews:

```rasi
/* wpick.rasi - wallpaper picker theme */

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
    width:          900px;
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
    columns:        1;
    lines:          14;
    scrollbar:      false;
    spacing:        4px;
}

element {
    background-color: transparent;
    border-radius:  6px;
    padding:        6px 8px;
    orientation:    horizontal;
    spacing:        10px;
}

element selected.normal {
    background-color: @selected-col;
    text-color:     #ffffff;
}

element-icon {
    size:           56px;
    border-radius:  4px;
}

element-text {
    vertical-align: 0.5;
    text-color:     inherit;
}
```

### `rofi/wpick-picker.sh`

Wrapper script for keybind or `.desktop` shortcut:

```bash
#!/usr/bin/env bash
# wpick-picker.sh — launch wallpaper picker
# Bind to: $mainMod + W  (in hyprland.conf)

set -euo pipefail

# Prefer uv tool install path, fallback to uv run
if command -v wpick &>/dev/null; then
    wpick pick
else
    cd ~/.config/wpick
    uv run wpick pick
fi
```

```bash
chmod +x ~/.config/wpick/rofi/wpick-picker.sh
```

### Hyprland keybind (`~/.config/hypr/hyprland.conf`)

```ini
bind = $mainMod, W, exec, ~/.config/wpick/rofi/wpick-picker.sh
```

---

## 9. swww + matugen Integration

### What wpick does

```
wpick pick → user selects → set_wallpaper(path) called
  → swww img <path> [transition flags]
  → matugen image <path>
```

matugen handles all theme generation. wpick only calls it; it doesn't touch matugen's config, templates, or output.

### swww transition presets

Add these to `config.toml` as needed:

```toml
# Fade
[swww]
transition_type     = "fade"
transition_duration = 1.0

# Grow from cursor
[swww]
transition_type = "grow"
transition_pos  = "0.5,0.5"

# Wipe (HydeSee default feel)
[swww]
transition_type = "wipe"
transition_angle = 30
```

### Restoring wallpaper on login

```bash
# ~/.config/hypr/hyprland.conf
exec-once = swww-daemon
exec-once = wpick restore   # (add this command — see below)
```

Add `restore` command to `cli.py`:

```python
@app.command()
def restore():
    """Re-apply the most recently set wallpaper (useful on login)."""
    from wpick import db
    from wpick.orchestrator import set_wallpaper, WallpaperError
    with db.connection() as conn:
        row = conn.execute(
            """
            SELECT i.path FROM history h
            JOIN images i ON h.image_id = i.id
            ORDER BY h.set_at DESC LIMIT 1
            """
        ).fetchone()
    if not row:
        typer.echo("No wallpaper history found.")
        return
    try:
        set_wallpaper(Path(row["path"]), log=False)
    except WallpaperError as e:
        typer.echo(f"Restore failed: {e}", err=True)
        raise typer.Exit(1)
```

---

## 10. Error Handling Strategy

### Principle: fail loudly in dev, degrade gracefully in daemon

|Situation|Response|
|---|---|
|Corrupt/truncated image|Log warning, skip, continue scan|
|Zero images found|Error + exit with message|
|Too few images to cluster|Error with clear instruction|
|swww not found|Raise `WallpaperError`, print install hint|
|swww daemon not running|Auto-start, retry once|
|matugen not found|Log warning, continue (wallpaper still sets)|
|matugen non-zero exit|Log warning, continue|
|rofi not found|Log error, exit gracefully|
|User cancels rofi (ESC)|returncode != 0, silently return|
|New image, no clusters yet|Quarantine (cluster_id = NULL), log info|
|Low similarity on assignment|Assign to "misc" with log note|
|DB locked (concurrent write)|WAL mode handles this; retry once if still locked|
|Wallpaper path deleted|Log error during set, skip history log|

### Global logging setup (`src/wpick/__init__.py`)

```python
import logging
import sys

def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stderr,
    )

# Auto-setup on import with default level
# CLI can call setup_logging("DEBUG") if --verbose flag passed
setup_logging()
```

---

## 11. Tests

### `tests/conftest.py`

```python
"""Shared fixtures."""
import pytest
import numpy as np
from pathlib import Path
from PIL import Image


FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(autouse=True)
def isolated_config(tmp_path, monkeypatch):
    """Redirect all storage to tmp_path so tests don't touch real DB."""
    import wpick.config as cfg_module
    cfg_module._cfg = {
        "paths": {
            "wallpapers": str(tmp_path / "wallpapers"),
            "cache": str(tmp_path / "cache"),
            "storage": str(tmp_path / "storage"),
        },
        "extraction": {
            "sample_size": 64,
            "n_colors": 4,
            "extensions": ["jpg", "jpeg", "png"],
        },
        "clustering": {
            "min_cluster_size": 2,
            "min_samples": 1,
        },
        "thumbnails": {"size": 64, "quality": 75},
        "swww": {
            "transition_type": "fade",
            "transition_pos": "0.5,0.5",
            "transition_fps": 30,
            "transition_duration": 0.5,
        },
        "matugen": {"enabled": False, "extra_flags": []},
        "watcher": {"enabled": False, "debounce_seconds": 1},
    }
    yield
    cfg_module._cfg = None


@pytest.fixture
def solid_red(tmp_path) -> Path:
    p = tmp_path / "red.png"
    Image.new("RGB", (64, 64), (220, 50, 50)).save(p)
    return p


@pytest.fixture
def solid_blue(tmp_path) -> Path:
    p = tmp_path / "blue.png"
    Image.new("RGB", (64, 64), (50, 80, 220)).save(p)
    return p


@pytest.fixture
def solid_green(tmp_path) -> Path:
    p = tmp_path / "green.png"
    Image.new("RGB", (64, 64), (40, 180, 80)).save(p)
    return p


@pytest.fixture
def corrupt_file(tmp_path) -> Path:
    p = tmp_path / "corrupt.png"
    p.write_bytes(b"\x89PNG notanimage")
    return p


@pytest.fixture
def rgba_image(tmp_path) -> Path:
    p = tmp_path / "rgba.png"
    img = Image.new("RGBA", (64, 64), (100, 150, 200, 128))
    img.save(p)
    return p
```

---

### `tests/test_oklab.py`

```python
import numpy as np
import pytest
from wpick.oklab import srgb_to_oklab


def test_black():
    result = srgb_to_oklab(np.array([0.0, 0.0, 0.0]))
    assert result[0] == pytest.approx(0.0, abs=1e-4)


def test_white():
    result = srgb_to_oklab(np.array([1.0, 1.0, 1.0]))
    assert result[0] == pytest.approx(1.0, abs=1e-3)
    # Achromatic: a and b near 0
    assert abs(result[1]) < 0.01
    assert abs(result[2]) < 0.01


def test_red_vs_blue_hue():
    red = srgb_to_oklab(np.array([1.0, 0.0, 0.0]))
    blue = srgb_to_oklab(np.array([0.0, 0.0, 1.0]))
    # Red and blue should have distinct a,b values
    assert not np.allclose(red[1:], blue[1:], atol=0.05)


def test_output_shape():
    result = srgb_to_oklab(np.array([0.5, 0.3, 0.8]))
    assert result.shape == (3,)
    assert result.dtype == np.float32


def test_grey_is_achromatic():
    """Mid-grey should have near-zero a and b."""
    grey = srgb_to_oklab(np.array([0.5, 0.5, 0.5]))
    assert abs(grey[1]) < 0.01
    assert abs(grey[2]) < 0.01
```

---

### `tests/test_extractor.py`

```python
import pytest
import numpy as np
from pathlib import Path
from wpick.extractor import extract_features, scan_and_extract, ExtractionError
from wpick import db


def test_extract_red(solid_red, tmp_path):
    result = extract_features(solid_red)
    assert "vector" in result
    assert isinstance(result["vector"], np.ndarray)
    assert len(result["vector"]) == 4 * 4 + 6  # n_colors=4 * 4 dims + 6 stats
    assert result["palette"]
    assert 0 <= result["stats"]["brightness"] <= 1


def test_extract_corrupt(corrupt_file):
    with pytest.raises(ExtractionError):
        extract_features(corrupt_file)


def test_extract_rgba(rgba_image):
    """RGBA images should be handled without error."""
    result = extract_features(rgba_image)
    assert result["vector"] is not None


def test_scan_nested(tmp_path):
    from PIL import Image
    # Create nested structure
    (tmp_path / "wallpapers" / "scifi").mkdir(parents=True)
    (tmp_path / "wallpapers" / "nature").mkdir()
    Image.new("RGB", (64,64), (200,50,50)).save(tmp_path / "wallpapers/scifi/a.jpg")
    Image.new("RGB", (64,64), (50,200,50)).save(tmp_path / "wallpapers/nature/b.jpg")

    db.init_schema()
    total, extracted, errors = scan_and_extract(tmp_path / "wallpapers")
    assert total == 2
    assert extracted == 2
    assert errors == 0


def test_scan_skips_corrupt(tmp_path):
    from PIL import Image
    (tmp_path / "wallpapers").mkdir()
    Image.new("RGB", (64,64)).save(tmp_path / "wallpapers/good.jpg")
    (tmp_path / "wallpapers" / "bad.jpg").write_bytes(b"notanimage")

    db.init_schema()
    total, extracted, errors = scan_and_extract(tmp_path / "wallpapers")
    assert errors == 1
    assert extracted == 1


def test_scan_idempotent(tmp_path):
    """Running scan twice without --force should not re-extract."""
    from PIL import Image
    (tmp_path / "wallpapers").mkdir()
    Image.new("RGB", (64,64)).save(tmp_path / "wallpapers/img.jpg")

    db.init_schema()
    _, e1, _ = scan_and_extract(tmp_path / "wallpapers")
    _, e2, _ = scan_and_extract(tmp_path / "wallpapers")
    assert e1 == 1
    assert e2 == 0  # already extracted, skip
```

---

### `tests/test_clusterer.py`

```python
import pytest
import numpy as np
from PIL import Image
from wpick import db
from wpick.extractor import scan_and_extract
from wpick.clusterer import run_clustering, ClusteringError


def _make_image_cluster(root, folder, color, count):
    """Create count images of a solid color in root/folder/."""
    (root / folder).mkdir(parents=True, exist_ok=True)
    for i in range(count):
        Image.new("RGB", (64, 64), color).save(root / folder / f"img_{i}.jpg")


def test_cluster_basic(tmp_path):
    walls = tmp_path / "wallpapers"
    _make_image_cluster(walls, "reds", (220, 40, 40), 5)
    _make_image_cluster(walls, "blues", (40, 40, 220), 5)

    db.init_schema()
    scan_and_extract(walls)
    summary = run_clustering()

    assert summary["clusters"] >= 1
    assert summary["total_images"] == 10


def test_cluster_too_few(tmp_path):
    walls = tmp_path / "wallpapers"
    walls.mkdir()
    Image.new("RGB", (64,64)).save(walls / "one.jpg")

    db.init_schema()
    scan_and_extract(walls)
    with pytest.raises(ClusteringError, match="Need at least"):
        run_clustering()


def test_cluster_no_features():
    with pytest.raises(ClusteringError, match="No extracted features"):
        run_clustering()
```

---

### `tests/test_assigner.py`

```python
import numpy as np
import pytest
from wpick.assigner import _cosine_similarity, assign_all_unassigned
from wpick import db
from PIL import Image


def test_cosine_identical():
    v = np.array([1.0, 0.5, 0.3])
    assert _cosine_similarity(v, v) == pytest.approx(1.0, abs=1e-5)


def test_cosine_orthogonal():
    a = np.array([1.0, 0.0, 0.0])
    b = np.array([0.0, 1.0, 0.0])
    assert _cosine_similarity(a, b) == pytest.approx(0.0, abs=1e-5)


def test_cosine_zero_vector():
    a = np.array([0.0, 0.0, 0.0])
    b = np.array([1.0, 0.5, 0.3])
    assert _cosine_similarity(a, b) == 0.0


def test_assign_no_clusters_returns_none(tmp_path):
    from pathlib import Path
    from PIL import Image
    walls = tmp_path / "walls"
    walls.mkdir()
    img = walls / "test.jpg"
    Image.new("RGB", (64,64), (200,100,50)).save(img)

    db.init_schema()
    result = __import__("wpick.assigner", fromlist=["assign_image"]).assign_image(img, walls)
    assert result is None
```

---

### `tests/test_db.py`

```python
import numpy as np
import pytest
from pathlib import Path
from PIL import Image
from wpick import db


def test_image_id_stable():
    p = Path("/home/user/walls/img.jpg")
    assert db.image_id(p) == db.image_id(p)


def test_upsert_idempotent(tmp_path):
    walls = tmp_path / "walls"
    walls.mkdir()
    img = walls / "test.jpg"
    Image.new("RGB", (4,4)).save(img)
    db.init_schema()
    id1 = db.upsert_image(img, walls)
    id2 = db.upsert_image(img, walls)
    assert id1 == id2


def test_store_and_load_features(tmp_path):
    walls = tmp_path / "walls"
    walls.mkdir()
    img = walls / "test.jpg"
    Image.new("RGB", (4,4)).save(img)
    db.init_schema()
    img_id = db.upsert_image(img, walls)

    vec = np.array([0.1, 0.2, 0.3, 0.4], dtype=np.float32)
    db.store_features(img_id, vec, [], {})

    rows = db.load_all_features()
    assert len(rows) == 1
    assert np.allclose(rows[0]["vector"], vec)


def test_assign_updates_image(tmp_path):
    walls = tmp_path / "walls"
    walls.mkdir()
    img = walls / "test.jpg"
    Image.new("RGB", (4,4)).save(img)
    db.init_schema()
    img_id = db.upsert_image(img, walls)
    vec = np.ones(10, dtype=np.float32)
    db.store_features(img_id, vec, [], {})
    centroid = np.ones(10, dtype=np.float32)
    db.store_cluster("cluster_0", 0, centroid, 1, "run_test")
    db.assign_image_to_cluster(img_id, "cluster_0")

    with db.connection() as conn:
        row = conn.execute(
            "SELECT cluster_id FROM images WHERE id = ?", (img_id,)
        ).fetchone()
    assert row["cluster_id"] == "cluster_0"
```

---

### Running tests

```bash
# From project root
uv run pytest

# Specific module
uv run pytest tests/test_extractor.py -v

# With coverage report
uv run pytest --cov=src/wpick --cov-report=html
# Opens: htmlcov/index.html

# Lint
uv run ruff check src/

# Type check
uv run mypy src/wpick/
```

---

## 12. systemd User Service

### `systemd/wpick-watch.service`

```ini
[Unit]
Description=wpick wallpaper watcher
Documentation=https://github.com/yourname/wpick
After=graphical-session.target
PartOf=graphical-session.target

[Service]
Type=simple
# Use uv tool install path; adjust if using uv run instead
ExecStart=%h/.local/bin/wpick watch
Restart=on-failure
RestartSec=5
Environment=HOME=%h
Environment=XDG_RUNTIME_DIR=/run/user/%U

StandardOutput=journal
StandardError=journal
SyslogIdentifier=wpick

[Install]
WantedBy=graphical-session.target
```

### Install the service

```bash
# Copy to systemd user dir
mkdir -p ~/.config/systemd/user/
cp ~/.config/wpick/systemd/wpick-watch.service ~/.config/systemd/user/

# Install wpick as a tool first (so the binary exists)
cd ~/.config/wpick
uv tool install .

# Enable and start
systemctl --user daemon-reload
systemctl --user enable wpick-watch.service
systemctl --user start wpick-watch.service

# Check status
systemctl --user status wpick-watch.service
journalctl --user -u wpick-watch.service -f
```

---

## 13. Production Checklist

### First-time setup

```bash
cd ~/.config/wpick

# 1. Install deps
uv sync

# 2. Install CLI globally
uv tool install .

# 3. Init DB and directories
wpick init

# 4. Set wallpaper path in config
cp config.default.toml config.toml
$EDITOR config.toml   # set paths.wallpapers

# 5. First scan (may take several minutes for 1500 images)
wpick scan

# 6. Cluster
wpick cluster

# 7. Check results
wpick stats

# 8. Test the picker
wpick pick

# 9. Enable watcher service
systemctl --user enable --now wpick-watch.service
```

### Pre-sharing checklist

- [ ] `features.jsonl` and `storage/` in `.gitignore`
- [ ] `config.toml` (user config) in `.gitignore`; only `config.default.toml` committed
- [ ] `uv.lock` committed (reproducible installs)
- [ ] `wpick --help` reads cleanly
- [ ] All tests pass: `uv run pytest`
- [ ] No hardcoded paths in source
- [ ] `README.md` covers: install, first-time setup, keybind
- [ ] `schema.sql` committed (DB init is reproducible)
- [ ] Tested on fresh venv: `uv sync --frozen && wpick init`

### When to recluster

```bash
# After a bulk wallpaper import
wpick scan && wpick cluster

# Cluster quality degraded (misc cluster too large)
wpick stats   # if misc > 20% of total → recluster
wpick cluster

# After tuning min_cluster_size in config.toml
wpick cluster
```

---

## 14. Future: Rust Extractor

When Python extraction becomes the bottleneck (unlikely before 50k+ images), replace `extractor.py` with a compiled binary.

### What changes

```toml
# config.toml addition
[extraction]
backend = "rust"   # or "python" (default)
rust_binary = "~/.local/bin/wpick-extractor"
```

```python
# extractor.py — call Rust binary if configured
def extract_features(path: Path) -> dict:
    if config.get()["extraction"].get("backend") == "rust":
        return _extract_rust(path)
    return _extract_python(path)
```

The Rust binary writes the same feature JSON format to stdout. The Python orchestrator parses it. Nothing else changes.

### Rust binary (when needed)

```toml
# Cargo.toml
[dependencies]
auto-palette = "0.5"
serde_json = "1"
rayon = "1"
```

The binary reads a path, outputs JSON matching the existing `features.jsonl` format, exits 0 on success, 1 on failure. Python consumes it via `subprocess.run`.

---

## 15. Phase Summary

|Phase|What|Command|
|---|---|---|
|0|Setup uv, init project|`uv sync && wpick init`|
|1|Scan + extract all images|`wpick scan`|
|2|Run first clustering|`wpick cluster`|
|3|Test picker|`wpick pick`|
|4|Enable watcher|`systemctl --user enable --now wpick-watch`|
|5|Write tests|`uv run pytest`|
|6|Bind keybind|hyprland.conf|
|7|Recluster after tuning|`wpick cluster`|
|Future|Rust extractor|if needed|
|Future|CLIP embeddings|semantic clustering|
|Future|AUR package|PKGBUILD|

---

_Last updated: 2026-05-23_  
_Stack: Python 3.12 · uv · HDBSCAN · Pillow · Typer · SQLite · swww · matugen · rofi-wayland_