---
tags:
  - project
  - wpick
  - assignment
parent: "[[wpick]]"
created: 2026-05-23
---

# wpick — Assignment

## Approach

Incremental assignment: new image → nearest existing cluster via cosine similarity. Never triggers a recluster.

## Threshold

`SIMILARITY_THRESHOLD = 0.65` — below this, image goes to "misc"

## assigner.py

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

_SIMILARITY_THRESHOLD = 0.65


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def assign_image(path: Path, wallpapers_root: Path) -> str | None:
    """Extract features for path, find nearest cluster centroid."""
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
        logger.info(f"Low similarity ({best_sim:.3f}) for {path.name} → assigning to misc")
        best_cluster = "misc"

    db.assign_image_to_cluster(result["image_id"], best_cluster)
    logger.info(f"Assigned {path.name} → {best_cluster} (similarity: {best_sim:.3f})")
    return best_cluster


def assign_all_unassigned(wallpapers_root: Path) -> tuple[int, int]:
    """Assign all images that have features but no cluster."""
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

## See Also

- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/04-Clustering]] — When to recluster
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/06-Orchestrator]] — Watcher triggers assignment
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/08-CLI]] — `wpick assign` command
