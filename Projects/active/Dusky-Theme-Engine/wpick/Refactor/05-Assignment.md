---
type: project
tags: [project, wpick]
created: 2026-05-24
status: in-progress
---

# 05 — Assignment

## Current State
- `assigner.py` assigns new images to existing clusters without full reclustering
- Likely reads `clusters.json` as centroid source — wrong, must read from DB
- `assign_image` and `assign_all_unassigned` exist but return types are unspecified
- Similarity metric is unconfirmed — may be Euclidean, should be cosine in Oklab space
- No handling for the case where no clusters exist yet

---

## Target
- `assigner.py` reads clusters and features exclusively from `WallpaperDB`
- Cosine similarity used for nearest-centroid matching
- Unassignable images (no clusters, feature missing) fail loudly with typed errors
- `assign_all_unassigned` returns a typed result, not a bare tuple

---

## Tasks

### Task 1 — Add assignment types to `models.py`

```python
@dataclass
class AssignResult:
    image_id: str
    cluster_id: int
    similarity: float    # cosine similarity to winning centroid, 0.0–1.0

@dataclass
class BatchAssignResult:
    assigned: int
    failed: int
    skipped: int         # already assigned, no force flag
    results: list[AssignResult]
```

### Task 2 — Implement cosine similarity

In `assigner.py`:

```python
def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Return cosine similarity between two vectors. Returns 0.0 if either is zero."""
```

Use numpy. Do not use `scipy` — keep the dependency footprint minimal. Handle zero-vector input explicitly (return 0.0, do not divide by zero).

Why cosine over Euclidean here: assignment compares a single image's feature vector to cluster centroids. Centroids are means of variable-length cluster members — their magnitude is not meaningful, only direction. Cosine normalizes this. Extraction (03) still uses Euclidean in Oklab space for HDBSCAN, which operates on raw point distances.

### Task 3 — Rewrite `assign_image`

Signature:

```python
def assign_image(
    image_id: str,
    db: WallpaperDB,
) -> AssignResult:
    """
    Assign a single image to its nearest cluster by cosine similarity.
    Raises AssignerError if image has no features or no clusters exist.
    """
```

Logic:
1. `features = db.get_features(image_id)` — raise `AssignerError` if `None`
2. `clusters = db.get_clusters()` — raise `AssignerError` if empty (clusters not yet run)
3. For each cluster, compute `_cosine_similarity(features.oklab_vector, cluster.centroid)`
4. Select cluster with highest similarity
5. Call `db.assign_image_cluster(image_id, best_cluster.cluster_id)`
6. Return `AssignResult`

Misc cluster (`cluster_id = -1`) participates in assignment normally — an image close to the misc centroid is assigned there. Do not special-case it.

### Task 4 — Rewrite `assign_all_unassigned`

Signature:

```python
def assign_all_unassigned(
    db: WallpaperDB,
    *,
    force: bool = False,
    on_progress: Callable[[int, int], None] | None = None,
) -> BatchAssignResult:
    """
    Assign all images with no cluster assignment.
    If force=True, reassign all images regardless of current assignment.
    """
```

Logic:
1. Get unassigned images from DB (need `db.get_unassigned_images() -> list[ImageRow]`)
2. For each: call `assign_image(image_id, db)`, accumulate results
3. On `AssignerError` per image: log `WARNING`, increment `failed`, continue
4. Call `on_progress(current, total)` after each image if provided
5. Return `BatchAssignResult`

Add `db.get_unassigned_images()` to `WallpaperDB` — images with no entry in the image-cluster join or where `cluster_id IS NULL`.

### Task 5 — Drift detection (informational only)

Add:

```python
def compute_assignment_confidence(db: WallpaperDB) -> float:
    """
    Return mean cosine similarity of all assigned images to their cluster centroid.
    Lower values indicate cluster drift — centroids no longer represent members well.
    """
```

This is read-only. It does not reassign anything. The `stats` CLI command (08-CLI) calls this and prints a warning if confidence drops below 0.6. No auto-recluster.

### Task 6 — Remove `clusters.json` reads from assigner

```bash
grep -r "clusters.json\|open.*json\|json.load" src/wpick/assigner.py
```

Any file read in this module is a violation unless it's reading an image file for feature extraction (which should not happen here anyway). Remove all JSON file reads.

---

## Constraints
- `AssignerError(WpickError)` is the only exception that escapes `assigner.py`
- `assigner.py` must not import `sqlite3` — all DB access via `WallpaperDB`
- Cosine similarity implementation must handle zero-length vectors without raising
- `assign_image` and `assign_all_unassigned` must accept `WallpaperDB` instance — no internal DB construction
- basedpyright zero errors on `assigner.py` after changes
