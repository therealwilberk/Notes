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
- Noise points are assigned to a stable `misc` cluster, not dropped
- Cluster centroids are stored in DB and used by assigner

---

## Tasks

### Task 1 — Add clustering types to `models.py`

```python
@dataclass
class ClusterRow:
    cluster_id: int          # -1 reserved for misc/noise
    label: str               # human-readable name, e.g. "warm-dark"
    centroid: list[float]    # mean oklab_vector of members
    member_count: int
    run_id: str              # UUID of the clustering run that created this

@dataclass
class ClusterRunRecord:
    run_id: str
    ran_at: str              # ISO 8601
    image_count: int
    cluster_count: int
    noise_count: int
    params: str              # JSON snapshot of HDBSCAN params used
```

Add `ClusterRunRecord` to `schema.sql` and `WallpaperDB`:

```sql
CREATE TABLE IF NOT EXISTS cluster_runs (
    run_id        TEXT PRIMARY KEY,
    ran_at        TEXT NOT NULL DEFAULT (datetime('now')),
    image_count   INTEGER NOT NULL,
    cluster_count INTEGER NOT NULL,
    noise_count   INTEGER NOT NULL,
    params        TEXT NOT NULL
);
```

### Task 2 — Rewrite `run_clustering`

Signature:

```python
def run_clustering(db: WallpaperDB, config: WpickConfig) -> ClusterRunRecord:
    """
    Run HDBSCAN on all extracted features.
    Returns a record of the run. Raises ClusteringError on failure.
    """
```

Logic:
1. `features = db.get_all_features()` — abort with `ClusteringError` if fewer than `config.min_cluster_size * 2` features
2. Build numpy array from `oklab_vector` fields
3. Run HDBSCAN with params from config: `min_cluster_size`, `min_samples`
4. Compute centroid per cluster label (mean of member vectors)
5. Assign noise points (label == -1) to `cluster_id = -1`, label = `"misc"`
6. Call `db.upsert_cluster(...)` for each cluster
7. Call `db.assign_image_cluster(image_id, cluster_id)` for every image
8. Record run in `cluster_runs` table via `db.log_cluster_run(...)`
9. Return `ClusterRunRecord`

Wrap the HDBSCAN call in try/except — it can raise on degenerate input (all identical vectors, single point). Raise `ClusteringError` with the original message.

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

### Task 6 — Validate HDBSCAN params at config load time

In `config.py` validation (see 01-Setup Task 5), add:
- `min_cluster_size >= 2`
- `min_samples >= 1`
- `min_samples <= min_cluster_size`

Raise `ConfigError` with message explaining the constraint if violated.

---

## Constraints
- `ClusteringError(WpickError)` is the only exception that escapes `clusterer.py`
- `cluster_id = -1` is permanently reserved for `misc` — never assign a real cluster this ID
- Centroid computation uses numpy — no manual mean loops
- `run_clustering` must accept `WallpaperDB` and `WpickConfig` — no internal config loading
- basedpyright zero errors on `clusterer.py` after changes
