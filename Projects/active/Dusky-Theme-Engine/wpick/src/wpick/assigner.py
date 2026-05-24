from __future__ import annotations

import logging
from collections.abc import Callable

import numpy as np

from wpick.db import WallpaperDB
from wpick.models import AssignResult, AssignerError, BatchAssignResult

logger = logging.getLogger(__name__)


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    arr_a = np.array(a, dtype=np.float64)
    arr_b = np.array(b, dtype=np.float64)
    norm_a = np.linalg.norm(arr_a)
    norm_b = np.linalg.norm(arr_b)
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return float(np.dot(arr_a, arr_b) / (norm_a * norm_b))


def assign_image(
    image_id: str,
    db: WallpaperDB,
) -> AssignResult:
    features = db.get_features(image_id)
    if features is None:
        raise AssignerError(f"no features found for image: {image_id}")

    clusters = db.get_clusters()
    if not clusters:
        raise AssignerError("no clusters exist — run clustering first")

    vector = features.oklab_vector
    scored = [(_cosine_similarity(vector, c.centroid), c) for c in clusters]
    similarity, best_cluster = max(scored, key=lambda pair: pair[0])

    db.assign_image_cluster(image_id, best_cluster.cluster_id)

    return AssignResult(
        image_id=image_id,
        cluster_id=best_cluster.cluster_id,
        similarity=similarity,
    )


def assign_all_unassigned(
    db: WallpaperDB,
    *,
    force: bool = False,
    on_progress: Callable[[int, int], None] | None = None,
) -> BatchAssignResult:
    if force:
        images = db.get_all_images()
    else:
        images = db.get_unassigned_images()

    total = len(images)
    assigned = 0
    failed = 0
    results: list[AssignResult] = []

    for i, image in enumerate(images):
        try:
            result = assign_image(image.image_id, db)
            results.append(result)
            assigned += 1
        except AssignerError:
            logger.warning("failed to assign image %s", image.image_id)
            failed += 1

        if on_progress:
            on_progress(i + 1, total)

    return BatchAssignResult(
        assigned=assigned,
        failed=failed,
        skipped=0,
        results=results,
    )


def compute_assignment_confidence(db: WallpaperDB) -> float:
    clusters = {c.cluster_id: c for c in db.get_clusters()}
    if not clusters:
        return 0.0

    assignments = db.get_assignments()
    if not assignments:
        return 0.0

    similarities: list[float] = []
    for image_id, cluster_id in assignments:
        features = db.get_features(image_id)
        if features is None:
            continue
        cluster = clusters.get(cluster_id)
        if cluster is None:
            continue
        sim = _cosine_similarity(features.oklab_vector, cluster.centroid)
        similarities.append(sim)

    if not similarities:
        return 0.0

    return float(np.mean(similarities))
