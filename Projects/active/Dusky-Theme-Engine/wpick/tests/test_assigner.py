from __future__ import annotations

import json

import pytest

from wpick.assigner import (
    _cosine_similarity,
    assign_all_unassigned,
    assign_image,
    compute_assignment_confidence,
)
from wpick.db import WallpaperDB, init_schema
from wpick.models import AssignerError


def _seed_db(db: WallpaperDB) -> None:
    for i in range(3):
        db._conn.execute(
            "INSERT INTO images (image_id, path) VALUES (?, ?)",
            (f"img{i}", f"/img{i}.png"),
        )
    db._conn.execute(
        "INSERT INTO clusters (cluster_id, centroid, label, member_count, run_id) "
        "VALUES (?, ?, ?, ?, ?)",
        (1, json.dumps([0.5, 0.4, 0.6]), "warm", 0, "r1"),
    )
    db._conn.execute(
        "INSERT INTO clusters (cluster_id, centroid, label, member_count, run_id) "
        "VALUES (?, ?, ?, ?, ?)",
        (2, json.dumps([0.3, 0.2, 0.1]), "cool", 0, "r1"),
    )
    for i in range(3):
        db._conn.execute(
            "INSERT INTO features (image_id, oklab_vector, color_count) "
            "VALUES (?, ?, ?)",
            (f"img{i}", json.dumps([0.4, 0.35, 0.5]), 1),
        )


class TestCosineSimilarity:
    def test_identical_vectors(self) -> None:
        v = [0.5, 0.5, 0.5]
        assert _cosine_similarity(v, v) == pytest.approx(1.0)

    def test_orthogonal(self) -> None:
        sim = _cosine_similarity([1.0, 0.0], [0.0, 1.0])
        assert sim == pytest.approx(0.0)

    def test_parallel(self) -> None:
        sim = _cosine_similarity([1.0, 2.0], [2.0, 4.0])
        assert sim == pytest.approx(1.0, abs=1e-9)

    def test_opposite(self) -> None:
        sim = _cosine_similarity([1.0, 0.0], [-1.0, 0.0])
        assert sim == pytest.approx(-1.0)

    def test_zero_vector(self) -> None:
        sim = _cosine_similarity([0.0, 0.0], [1.0, 0.0])
        assert sim == pytest.approx(0.0)

    def test_both_zero(self) -> None:
        sim = _cosine_similarity([0.0, 0.0], [0.0, 0.0])
        assert sim == pytest.approx(0.0)


class TestAssignImage:
    def test_assigns_closest_cluster(self, tmp_path: pytest.TempPathFactory) -> None:
        db_path = tmp_path / "test.db"
        init_schema(db_path)
        with WallpaperDB(db_path) as db:
            _seed_db(db)
            result = assign_image("img0", db)
        assert result.image_id == "img0"
        assert result.similarity > 0

    def test_no_features_raises(self, tmp_path: pytest.TempPathFactory) -> None:
        db_path = tmp_path / "test.db"
        init_schema(db_path)
        with WallpaperDB(db_path) as db:
            _seed_db(db)
            with pytest.raises(AssignerError, match="no features"):
                assign_image("nonexistent", db)

    def test_no_clusters_raises(self, tmp_path: pytest.TempPathFactory) -> None:
        db_path = tmp_path / "test.db"
        init_schema(db_path)
        with WallpaperDB(db_path) as db:
            db._conn.execute(
                "INSERT INTO images (image_id, path) VALUES (?, ?)",
                ("img0", "/img0.png"),
            )
            db._conn.execute(
                "INSERT INTO features (image_id, oklab_vector, color_count) "
                "VALUES (?, ?, ?)",
                ("img0", json.dumps([0.5, 0.5, 0.5]), 1),
            )
            with pytest.raises(AssignerError, match="no clusters exist"):
                assign_image("img0", db)


class TestAssignAllUnassigned:
    def test_assigns_only_unassigned(self, tmp_path: pytest.TempPathFactory) -> None:
        db_path = tmp_path / "test.db"
        init_schema(db_path)
        with WallpaperDB(db_path) as db:
            _seed_db(db)
            result = assign_all_unassigned(db)
        assert result.assigned == 3
        assert result.failed == 0

    def test_force_reassigns_all(self, tmp_path: pytest.TempPathFactory) -> None:
        db_path = tmp_path / "test.db"
        init_schema(db_path)
        with WallpaperDB(db_path) as db:
            _seed_db(db)
            assign_all_unassigned(db)
            result = assign_all_unassigned(db, force=True)
        assert result.assigned == 3

    def test_skips_already_assigned(self, tmp_path: pytest.TempPathFactory) -> None:
        db_path = tmp_path / "test.db"
        init_schema(db_path)
        with WallpaperDB(db_path) as db:
            _seed_db(db)
            assign_all_unassigned(db)
            result = assign_all_unassigned(db)
        assert result.assigned == 0

    def test_progress_callback(self, tmp_path: pytest.TempPathFactory) -> None:
        db_path = tmp_path / "test.db"
        init_schema(db_path)
        updates: list[tuple[int, int]] = []

        def on_progress(current: int, total: int) -> None:
            updates.append((current, total))

        with WallpaperDB(db_path) as db:
            _seed_db(db)
            assign_all_unassigned(db, on_progress=on_progress)
        assert len(updates) == 3


class TestComputeConfidence:
    def test_returns_mean_similarity(self, tmp_path: pytest.TempPathFactory) -> None:
        db_path = tmp_path / "test.db"
        init_schema(db_path)
        with WallpaperDB(db_path) as db:
            _seed_db(db)
            assign_all_unassigned(db)
            confidence = compute_assignment_confidence(db)
        assert 0 < confidence <= 1.0

    def test_zero_when_no_clusters(self, tmp_path: pytest.TempPathFactory) -> None:
        db_path = tmp_path / "test.db"
        init_schema(db_path)
        with WallpaperDB(db_path) as db:
            assert compute_assignment_confidence(db) == 0.0

    def test_zero_when_no_assignments(self, tmp_path: pytest.TempPathFactory) -> None:
        db_path = tmp_path / "test.db"
        init_schema(db_path)
        with WallpaperDB(db_path) as db:
            db._conn.execute(
                "INSERT INTO clusters (cluster_id, centroid, label, member_count, run_id) "
                "VALUES (?, ?, ?, ?, ?)",
                (1, json.dumps([0.5] * 3), "x", 0, "r1"),
            )
            assert compute_assignment_confidence(db) == 0.0