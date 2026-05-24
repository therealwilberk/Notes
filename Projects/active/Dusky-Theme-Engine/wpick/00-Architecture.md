---
tags:
  - project
  - wpick
  - architecture
parent: "[[wpick]]"
created: 2026-05-23
---

# wpick — Architecture

## Mental Model

```
wallpapers/           ← nested dirs, read-only from wpick's perspective
  ├── dark/
  └── light/

       ↓  scan

auto-palette (Rust)   ← extracts dominant colors + OKLAB vectors
       ↓
features.jsonl        ← one JSON object per line, source of truth

       ↓  (first time or manual recluster)

clusterer             ← HDBSCAN, reads all features, outputs cluster map
       ↓
clusters.json         ← {cluster_id → [image_ids], centroid → [...], name → "warm amber"}

       ↓  (on new images)

assigner              ← cosine similarity against stored centroids
       ↓
updates DB only       ← no full recluster

       ↓  (user action)

picker                ← rofi card grid, shows thumbnails grouped by cluster
       ↓
selected path
       ↓
swww img <path>       ← sets wallpaper
       ↓
matugen image <path>  ← generates color scheme
```

## Module Map

| Module | File | Purpose |
|---|---|---|
| Storage | db.py | SQLite operations, no business logic |
| Config | config.py | TOML loader, merges defaults + user |
| Extraction | extractor.py | Calls auto-palette, computes stats |
| Clustering | clusterer.py | HDBSCAN, full recluster |
| Assignment | assigner.py | New image → nearest cluster |
| Orchestrator | orchestrator.py | Watcher + swww + matugen |
| Picker | picker.py | rofi UI + thumbnail gen |
| CLI | cli.py | Typer entry points |
| OKLab | oklab.py | Color space conversions (stats only) |

## Data Flow

1. `wpick scan` → auto-palette extracts → features.jsonl + SQLite
2. `wpick cluster` → HDBSCAN → clusters.json + SQLite
3. `wpick pick` → rofi card grid → swww + matugen
4. `wpick watch` → filesystem watcher → auto-assign new images

## Design Decisions

- **auto-palette over Pillow+KMeans** — Rust, fast, battle-tested OKLAB
- **HDBSCAN over KMeans** — density-based, handles noise, no pre-specified k
- **SQLite over JSON files** — concurrent-safe, indexed, WAL mode
- **Incremental assignment** — no recluster on new images, prevents cluster drift
- **Separate extraction and clustering** — extraction is per-image, clustering is batch

## See Also

- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/01-Setup]] — Environment and dependencies
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/03-Extraction]] — auto-palette integration details
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/04-Clustering]] — HDBSCAN parameters and strategy
