---
type: project
tags: [project, wpick]
created: 2026-05-24
status: in-progress
---

# 04 — Clustering

## Current State
- `clusterer.py` runs HDBSCAN on extracted features
- Reads `features.jsonl` as input — wrong, must read from DB
- Writes `clusters.json` as output — wrong, must write to DB
- `run_clustering()` has no typed signature or return
- Cluster naming is unspecified or absent
- No record of when clustering was last run or on how many images
- `ClusteringError` exists in the module but may not be consistently raised

---

## Target
- `run_clustering` reads `FeatureRow` list from `WallpaperDB`, writes `ClusterRow` list back
- `clusters.json` is debug-only, off by default
- Every cluster run is recorded with a `run_id` and image count
- Every image is assigned to a cluster — no noise/misc dumping ground
- Cluster centroids are stored in DB and used by assigner

---

## Tasks

### Task 1 — Add clustering types to `models.py`

```python
@dataclass
class ClusterRow:
    cluster_id: int          # sequential, 0-based
    label: str               # human-readable name, e.g. "dark-warm"
    centroid: list[float]    # mean oklab_vector of members
    member_count: int
    run_id: str              # UUID of the clustering run that created this

@dataclass
class ClusterRunRecord:
    run_id: str
    ran_at: str              # ISO 8601
    image_count: int
    cluster_count: int
    params: str              # JSON snapshot of KMeans params used
```

Add `ClusterRunRecord` to `schema.sql` and `WallpaperDB`:

```sql
CREATE TABLE IF NOT EXISTS cluster_runs (
    run_id        TEXT PRIMARY KEY,
    ran_at        TEXT NOT NULL DEFAULT (datetime('now')),
    image_count   INTEGER NOT NULL,
    cluster_count INTEGER NOT NULL,
    params        TEXT NOT NULL
);
```

### Task 2 — Rewrite `run_clustering`

Signature:

```python
def run_clustering(db: WallpaperDB, config: WpickConfig) -> ClusterRunRecord:
    """
    Run KMeans on all extracted features.
    Returns a record of the run. Raises ClusteringError on failure.
    """
```

Logic:
1. `features = db.get_all_features()` — abort with `ClusteringError` if fewer than `config.cluster_count * 2` features
2. Build numpy array from `oklab_vector` fields
3. Run KMeans with `n_clusters=config.cluster_count`, `random_state=42` for deterministic results
4. Compute centroid per cluster label (mean of member vectors — KMeans already provides centroids via `cluster_centers_`)
5. Call `db.upsert_cluster(...)` for each cluster
6. Call `db.assign_image_cluster(image_id, cluster_id)` for every image
7. Record run in `cluster_runs` table via `db.log_cluster_run(...)`
8. Return `ClusterRunRecord`

Wrap the KMeans call in try/except — it can raise on degenerate input (all identical vectors, fewer distinct points than clusters). Raise `ClusteringError` with the original message.

**Why KMeans over HDBSCAN:**
- `cluster_count` is already in config — user controls granularity
- Deterministic with `random_state=42` — same input, same clusters
- No noise problem — every wallpaper gets assigned
- HDBSCAN failed on small sets (30 images in 36D → all noise)
- Wallpaper libraries are curated sets, not organic clusters — forced N-bucket grouping is the desired behavior

### Task 3 — Cluster naming

Naming is deterministic from the centroid, not LLM-generated. Implement:

```python
def _name_cluster(centroid: list[float], cluster_id: int) -> str:
    """
    Derive a human-readable label from Oklab centroid.
    Format: "{lightness}-{hue}" e.g. "dark-warm", "light-cool", "mid-neutral"
    """
```

Lightness bins: `L < 0.35` → `"dark"`, `L > 0.65` → `"light"`, else `"mid"`
Hue bins from `a` and `b` components: positive `a` → warm, negative `a` → cool, near-zero both → neutral

This is deterministic and requires no external calls. Keep it simple — the label is a navigation aid, not a design system.

### Task 4 — Recluster strategy

Add to `WallpaperDB`:

```python
def get_latest_cluster_run(self) -> ClusterRunRecord | None: ...
def images_since_last_cluster(self) -> int: ...
```

`images_since_last_cluster` returns count of images extracted after `ran_at` of the latest run.

In `cli.py` (note for 08-CLI): the `cluster` command should warn if this count exceeds a threshold (e.g. 20% of last run's `image_count`) but proceed — never auto-recluster silently.

### Task 5 — Remove `clusters.json` as input

```bash
grep -r "clusters.json\|\.json" src/wpick/clusterer.py src/wpick/assigner.py
```

Any read of `clusters.json` is a violation. Remove all read paths. Write path is allowed only if `config.debug.export_artifacts = true`.

### Task 6 — Validate KMeans params at config load time

In `config.py` validation (see 01-Setup Task 5), add:
- `cluster_count >= 2`
- `cluster_count` must be an integer

Raise `ConfigError` with message explaining the constraint if violated.

---

## Constraints
- `ClusteringError(WpickError)` is the only exception that escapes `clusterer.py`
- KMeans `n_clusters` comes from `config.cluster_count` — never hardcoded
- Centroid computation uses numpy — no manual mean loops
- `run_clustering` must accept `WallpaperDB` and `WpickConfig` — no internal config loading
- basedpyright zero errors on `clusterer.py` after changes
