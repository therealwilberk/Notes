---
tags:
  - project
  - wpick
  - clustering
  - hdbscan
parent: "[[wpick]]"
created: 2026-05-23
---

# wpick — Clustering

## Approach

HDBSCAN — density-based clustering. Handles noise (images that don't fit any cluster go to "misc"). No need to pre-specify k.

## Parameters

| Parameter | Default | Description |
|---|---|---|
| min_cluster_size | 8 | Minimum images per cluster |
| min_samples | 3 | Core point threshold |
| metric | euclidean | Distance metric |
| cluster_selection_method | eom | Excess of mass |

## When to Recluster

- After bulk wallpaper import
- When misc cluster > 20% of total
- After tuning min_cluster_size

**Never** automatically on new image — causes cluster drift.

## Cluster Naming

Auto-generate human-readable names from centroid OKLAB values:

```python
def _name_cluster(centroid: np.ndarray) -> str:
    """Generate name from centroid OKLAB values."""
    L = centroid[0]  # lightness: 0=dark, 1=light
    a = centroid[1]  # green-red axis
    b = centroid[2]  # blue-yellow axis

    # Lightness prefix
    if L < 0.3:
        prefix = "dark"
    elif L < 0.6:
        prefix = "muted"
    else:
        prefix = "bright"

    # Hue from a,b
    hue = np.degrees(np.arctan2(b, a))
    if hue < -150:
        name = "green"
    elif hue < -90:
        name = "teal"
    elif hue < -30:
        name = "cyan"
    elif hue < 30:
        name = "neutral"
    elif hue < 90:
        name = "warm"
    elif hue < 150:
        name = "rose"
    else:
        name = "purple"

    return f"{prefix} {name}"
```

## clusterer.py

```python
"""
Clustering: all feature vectors → cluster map.

FULL recluster. Run manually or after bulk additions.
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


def _name_cluster(centroid: np.ndarray) -> str:
    """Generate human-readable name from centroid OKLAB values."""
    L = float(centroid[0])
    a = float(centroid[1])
    b = float(centroid[2])

    if L < 0.3:
        prefix = "dark"
    elif L < 0.6:
        prefix = "muted"
    else:
        prefix = "bright"

    hue = np.degrees(np.arctan2(b, a))
    if hue < -150:
        name = "green"
    elif hue < -90:
        name = "teal"
    elif hue < -30:
        name = "cyan"
    elif hue < 30:
        name = "neutral"
    elif hue < 90:
        name = "warm"
    elif hue < 150:
        name = "rose"
    else:
        name = "purple"

    return f"{prefix} {name}"


def run_clustering() -> dict:
    """Load all features, run HDBSCAN, store results."""
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

    for label in cluster_labels:
        mask = labels == label
        cluster_id = f"cluster_{label}"
        members = matrix[mask]
        centroid = members.mean(axis=0)
        name = _name_cluster(centroid)
        db.store_cluster(cluster_id, label, centroid, int(mask.sum()), run_id, name)
        for img_id in np.array(image_ids)[mask]:
            db.assign_image_to_cluster(img_id, cluster_id)

    if noise_count > 0:
        misc_mask = labels == -1
        misc_members = matrix[misc_mask]
        misc_centroid = misc_members.mean(axis=0)
        db.store_cluster("misc", -1, misc_centroid, noise_count, run_id, "misc")
        for img_id in np.array(image_ids)[misc_mask]:
            db.assign_image_to_cluster(img_id, "misc")

    db.store_cluster_run(
        run_id=run_id,
        cluster_count=cluster_count + (1 if noise_count else 0),
        noise_count=noise_count,
        image_count=len(rows),
        params={"min_cluster_size": min_cluster_size, "min_samples": min_samples},
    )

    return {
        "run_id": run_id,
        "total_images": len(rows),
        "clusters": cluster_count,
        "noise_images": noise_count,
        "labels": cluster_labels,
    }
```

## See Also

- [[03-Extraction]] — How features are computed
- [[05-Assignment]] — Incremental assignment (no recluster)
- [[08-CLI]] — `wpick cluster` command
