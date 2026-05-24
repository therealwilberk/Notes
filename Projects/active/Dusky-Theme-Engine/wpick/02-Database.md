---
tags:
  - project
  - wpick
  - database
parent: "[[wpick]]"
created: 2026-05-23
---

# wpick — Database

## Location

`~/.local/share/wpick/wpick.db` (SQLite, WAL mode)

## Schema

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
    version      INTEGER NOT NULL DEFAULT 1
);

-- clusters: output of HDBSCAN run
CREATE TABLE IF NOT EXISTS clusters (
    id            TEXT PRIMARY KEY,   -- "cluster_0", "cluster_1", ..., "misc"
    label         INTEGER NOT NULL,   -- raw HDBSCAN label (-1 = noise → misc)
    centroid      BLOB NOT NULL,      -- numpy float32 bytes
    member_count  INTEGER NOT NULL DEFAULT 0,
    name          TEXT,               -- human-readable: "warm amber", "cool blue"
    created_at    TEXT NOT NULL DEFAULT (datetime('now')),
    run_id        TEXT NOT NULL
);

-- cluster_runs: audit log of recluster events
CREATE TABLE IF NOT EXISTS cluster_runs (
    id           TEXT PRIMARY KEY,
    image_count  INTEGER NOT NULL,
    cluster_count INTEGER NOT NULL,
    noise_count  INTEGER NOT NULL,
    params_json  TEXT NOT NULL,
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

## db.py Operations

- `init_schema()` — Create tables from SQL file
- `image_id(path)` — SHA256[:16] of resolved path
- `upsert_image(path, wallpapers_root)` — Insert or update image record
- `store_features(image_id, vector, palette, stats)` — Store extraction results
- `load_all_features()` — Returns list of {image_id, vector (np.ndarray)}
- `store_cluster_run(...)` — Log clustering event
- `store_cluster(...)` — Store cluster with centroid
- `assign_image_to_cluster(image_id, cluster_id)` — Update image's cluster
- `load_all_centroids()` — Returns list of {cluster_id, centroid}
- `get_images_by_cluster(cluster_id)` — Images in a cluster
- `log_history(image_id)` — Record wallpaper set event
- `get_unextracted_images()` — Images needing extraction
- `get_unassigned_images()` — Images with features but no cluster

## See Also

- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/03-Extraction]] — How features are computed
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/04-Clustering]] — How clusters are created
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/05-Assignment]] — How images are assigned to clusters
