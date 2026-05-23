---
tags:
  - project
  - wpick
  - todo
  - phase2
parent: "[[wpick]]"
created: 2026-05-23
---

# wpick — Phase 2 Upgrades

> Foundation built (HER-13 through HER-23). These upgrades bring it to spec.

## Required Changes

### 1. Schema: auto-increment → SHA256[:16] IDs

Current schema uses `INTEGER PRIMARY KEY AUTOINCREMENT`. Spec calls for SHA256[:16] as primary key.

**Why:** Deterministic IDs, no collision risk, idempotent upserts.

**Files:** `schema.sql`, `db.py`, `models.py`

---

### 2. Extractor: Pillow → auto-palette

Current: `Pillow.quantize()` with MEDIANCUT. Works but crude.

Target: `auto-palette` Rust binary via subprocess.

```python
def _call_auto_palette(path: Path) -> list[dict]:
    result = subprocess.run(
        ["auto-palette", str(path), "--format", "json"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)
```

**Why:** Rust speed, proper OKLAB native support, population weights.

**Files:** `extractor.py`, `pyproject.toml` (add auto-palette dep)

---

### 3. Clusterer: k-means → HDBSCAN

Current: Custom k-means in pure Python. Requires pre-specifying k.

Target: `hdbscan` library. Density-based, handles noise, no k needed.

**Why:** Better clustering quality, noise handling (misc cluster), no k guessing.

**Files:** `clusterer.py`, `pyproject.toml` (add hdbscan dep)

---

### 4. Picker: basic list → Hyde-style card grid

Current: Simple rofi dmenu list with text entries.

Target: Rofi card grid with:
- `listview { columns: 4; }` (dynamic based on monitor width)
- `element { orientation: vertical; }` (icon on top, text below)
- `element-icon { size: 20em; }` (large preview thumbnails)
- Cluster headers with member count

**Files:** `picker.py`, `rofi/wpick.rasi`

---

### 5. CLI: argparse → Typer

Current: argparse with 3 commands (pipeline, pick, rofi).

Target: Typer with full command set:
- `wpick init` — initialize DB and directories
- `wpick scan` — scan wallpapers, extract features
- `wpick scan --force` — re-extract all
- `wpick cluster` — run HDBSCAN
- `wpick assign` — assign unassigned images
- `wpick assign <path>` — assign specific image
- `wpick pick` — launch rofi picker
- `wpick next` — next wallpaper in cluster
- `wpick prev` — previous wallpaper in cluster
- `wpick watch` — start filesystem watcher
- `wpick restore` — restore last wallpaper
- `wpick stats` — show cluster statistics

**Files:** `cli.py`, `pyproject.toml` (add typer dep)

---

### 6. Cluster naming: auto-generate from OKLAB

Current: No naming. Clusters are `cluster_0`, `cluster_1`.

Target: Human-readable names from centroid OKLAB values:
- L < 0.3 → "dark", L < 0.6 → "muted", else → "bright"
- hue from atan2(b, a): green, teal, cyan, neutral, warm, rose, purple
- Result: "dark forest", "bright warm", "muted teal"

**Files:** `clusterer.py`

---

### 7. Wallpaper cycling: cluster-aware

Current: Cycles through all wallpapers linearly.

Target: `wpick next` / `wpick prev` cycles within current cluster.

**Files:** `orchestrator.py`

---

### 8. Watcher: filesystem monitoring

Current: No watcher.

Target: watchdog-based filesystem monitor with 5s debounce. Auto-extract + assign on new files.

**Files:** `orchestrator.py`, `pyproject.toml` (add watchdog dep)

---

## Priority Order

1. Schema (foundation for everything)
2. Extractor (auto-palette integration)
3. Clusterer (HDBSCAN)
4. Cluster naming
5. Picker (card grid)
6. CLI (full commands)
7. Watcher
8. Wallpaper cycling

## See Also

- [[wpick]] — MOC
- [[00-Architecture]] — Pipeline overview
- [[03-Extraction]] — auto-palette spec
- [[04-Clustering]] — HDBSCAN spec
- [[07-Picker]] — Hyde card grid spec
- [[08-CLI]] — Full command set
