from __future__ import annotations

import json
from pathlib import Path

import pytest

from wpick.db import WallpaperDB, init_schema
from wpick.models import ClusterRow, DatabaseError, FeatureRow, ImageRow


def test_init_schema_creates_tables(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    init_schema(db_path)
    db = WallpaperDB(db_path)
    db.connect()
    tables = db._conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    names = {r["name"] for r in tables}
    assert "images" in names
    assert "features" in names
    assert "clusters" in names
    assert "image_cluster" in names
    assert "history" in names
    assert "cluster_runs" in names
    assert "schema_migrations" in names
    db.close()


def test_init_schema_idempotent(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    init_schema(db_path)
    init_schema(db_path)
    db = WallpaperDB(db_path)
    db.connect()
    count = db._conn.execute("SELECT COUNT(*) as c FROM schema_migrations").fetchone()["c"]
    assert count == 1
    db.close()


def test_init_schema_missing_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "wpick.db.Path",
        lambda p: type("FakePath", (), {"exists": lambda: False, "parent": tmp_path})()
        if "schema.sql" in str(p)
        else Path(p),
    )
    from wpick import db as db_module

    fake = tmp_path / "nonexistent" / "schema.sql"
    monkeypatch.setattr(db_module, "__file__", str(fake))
    with pytest.raises(DatabaseError, match="schema file not found"):
        init_schema(tmp_path / "test.db")


def test_schema_version_applied(tmp_db: WallpaperDB) -> None:
    row = tmp_db._conn.execute(
        "SELECT version FROM schema_migrations ORDER BY version DESC LIMIT 1"
    ).fetchone()
    assert row is not None
    assert row["version"] == 1


def test_connect_and_close(tmp_path: Path) -> None:
    init_schema(tmp_path / "test.db")
    db = WallpaperDB(tmp_path / "test.db")
    db.connect()
    assert db._conn is not None
    db.close()
    assert db._conn is None


def test_context_manager(tmp_path: Path) -> None:
    init_schema(tmp_path / "test.db")
    with WallpaperDB(tmp_path / "test.db") as db:
        assert db._conn is not None
    assert db._conn is None


def test_double_connect_is_noop(tmp_path: Path) -> None:
    init_schema(tmp_path / "test.db")
    db = WallpaperDB(tmp_path / "test.db")
    db.connect()
    conn_id = id(db._conn)
    db.connect()
    assert id(db._conn) == conn_id
    db.close()


def test_insert_and_get_image(tmp_db: WallpaperDB) -> None:
    tmp_db._conn.execute(
        "INSERT INTO images (image_id, path) VALUES (?, ?)",
        ("abc123", "/path/to/img.png"),
    )
    row = tmp_db.get_image("abc123")
    assert row is not None
    assert row.image_id == "abc123"
    assert row.path == "/path/to/img.png"


def test_get_image_nonexistent(tmp_db: WallpaperDB) -> None:
    assert tmp_db.get_image("nonexistent") is None


def test_get_all_images(tmp_db: WallpaperDB) -> None:
    tmp_db._conn.execute(
        "INSERT INTO images (image_id, path) VALUES (?, ?)", ("a", "/a.png")
    )
    tmp_db._conn.execute(
        "INSERT INTO images (image_id, path) VALUES (?, ?)", ("b", "/b.png")
    )
    images = tmp_db.get_all_images()
    assert len(images) == 2


def test_insert_feature_and_get(tmp_db: WallpaperDB) -> None:
    tmp_db._conn.execute(
        "INSERT INTO images (image_id, path) VALUES (?, ?)", ("img1", "/img1.png")
    )
    vector = [0.1, 0.2, 0.3]
    tmp_db._conn.execute(
        "INSERT INTO features (image_id, oklab_vector, color_count) VALUES (?, ?, ?)",
        ("img1", json.dumps(vector), 3),
    )
    row = tmp_db.get_features("img1")
    assert row is not None
    assert row.image_id == "img1"
    assert row.oklab_vector == vector
    assert row.color_count == 3


def test_get_features_nonexistent(tmp_db: WallpaperDB) -> None:
    assert tmp_db.get_features("no_such_image") is None


def test_get_all_features(tmp_db: WallpaperDB) -> None:
    for i in range(2):
        tmp_db._conn.execute(
            "INSERT INTO images (image_id, path) VALUES (?, ?)", (f"img{i}", f"/img{i}.png")
        )
        tmp_db._conn.execute(
            "INSERT INTO features (image_id, oklab_vector, color_count) VALUES (?, ?, ?)",
            (f"img{i}", json.dumps([float(i)]), 1),
        )
    rows = tmp_db.get_all_features()
    assert len(rows) == 2


def test_get_unextracted_images(tmp_db: WallpaperDB) -> None:
    tmp_db._conn.execute(
        "INSERT INTO images (image_id, path) VALUES (?, ?)", ("extracted", "/e.png")
    )
    tmp_db._conn.execute(
        "INSERT INTO features (image_id, oklab_vector, color_count) VALUES (?, ?, ?)",
        ("extracted", "[]", 0),
    )
    tmp_db._conn.execute(
        "INSERT INTO images (image_id, path) VALUES (?, ?)", ("unextracted", "/u.png")
    )
    unextracted = tmp_db.get_unextracted_images()
    assert len(unextracted) == 1
    assert unextracted[0].image_id == "unextracted"


def test_get_unassigned_images(tmp_db: WallpaperDB) -> None:
    tmp_db._conn.execute(
        "INSERT INTO images (image_id, path) VALUES (?, ?)", ("a", "/a.png")
    )
    tmp_db._conn.execute(
        "INSERT INTO images (image_id, path) VALUES (?, ?)", ("b", "/b.png")
    )
    tmp_db._conn.execute(
        "INSERT INTO clusters (cluster_id, centroid, label, member_count, run_id) "
        "VALUES (?, ?, ?, ?, ?)",
        (1, json.dumps([0.5] * 3), "c", 0, "r1"),
    )
    tmp_db.assign_image_cluster("a", 1)
    unassigned = tmp_db.get_unassigned_images()
    assert len(unassigned) == 1
    assert unassigned[0].image_id == "b"


def test_cluster_operations(tmp_db: WallpaperDB) -> None:
    tmp_db._conn.execute(
        "INSERT INTO clusters (cluster_id, centroid, label, member_count, run_id) "
        "VALUES (?, ?, ?, ?, ?)",
        (1, json.dumps([0.5, 0.5, 0.5]), "dark", 3, "run1"),
    )
    clusters = tmp_db.get_clusters()
    assert len(clusters) == 1
    c = clusters[0]
    assert c.cluster_id == 1
    assert c.label == "dark"
    assert c.member_count == 3


def test_assign_image_cluster(tmp_db: WallpaperDB) -> None:
    tmp_db._conn.execute(
        "INSERT INTO images (image_id, path) VALUES (?, ?)", ("img1", "/img1.png")
    )
    tmp_db._conn.execute(
        "INSERT INTO clusters (cluster_id, centroid, label, member_count, run_id) "
        "VALUES (?, ?, ?, ?, ?)",
        (1, json.dumps([0.5] * 3), "test", 0, "r1"),
    )
    tmp_db.assign_image_cluster("img1", 1)
    assignments = tmp_db.get_assignments()
    assert ("img1", 1) in assignments


def test_assign_image_cluster_replaces(tmp_db: WallpaperDB) -> None:
    tmp_db._conn.execute(
        "INSERT INTO images (image_id, path) VALUES (?, ?)", ("img1", "/img1.png")
    )
    tmp_db._conn.execute(
        "INSERT INTO clusters (cluster_id, centroid, label, member_count, run_id) "
        "VALUES (?, ?, ?, ?, ?)",
        (1, json.dumps([0.5] * 3), "a", 0, "r1"),
    )
    tmp_db._conn.execute(
        "INSERT INTO clusters (cluster_id, centroid, label, member_count, run_id) "
        "VALUES (?, ?, ?, ?, ?)",
        (2, json.dumps([0.5] * 3), "b", 0, "r1"),
    )
    tmp_db.assign_image_cluster("img1", 1)
    tmp_db.assign_image_cluster("img1", 2)
    assignments = tmp_db.get_assignments()
    assert ("img1", 2) in assignments
    assert len(assignments) == 1


def test_get_empty_clusters(tmp_db: WallpaperDB) -> None:
    assert tmp_db.get_clusters() == []


def test_get_empty_assignments(tmp_db: WallpaperDB) -> None:
    assert tmp_db.get_assignments() == []


def test_operation_on_closed_db(tmp_path: Path) -> None:
    init_schema(tmp_path / "test.db")
    db = WallpaperDB(tmp_path / "test.db")
    with pytest.raises(DatabaseError, match="not connected"):
        db.get_all_images()


def test_transaction_rollback(tmp_db: WallpaperDB) -> None:
    tmp_db._conn.execute(
        "INSERT INTO images (image_id, path) VALUES (?, ?)", ("img1", "/a.png")
    )
    tmp_db._conn.execute(
        "INSERT INTO images (image_id, path) VALUES (?, ?)", ("img2", "/b.png")
    )
    with pytest.raises(DatabaseError), tmp_db._transaction() as cur:
        cur.execute(
            "INSERT INTO images (image_id, path) VALUES (?, ?)", ("img3", "/c.png")
        )
        cur.execute(
            "INSERT INTO nonexistent_table (x) VALUES (?)", (1,)
        )
    assert tmp_db.get_image("img3") is None


def test_image_row_type(tmp_db: WallpaperDB) -> None:
    tmp_db._conn.execute(
        "INSERT INTO images (image_id, path) VALUES (?, ?)", ("x", "/x.png")
    )
    row = tmp_db.get_image("x")
    assert isinstance(row, ImageRow)


def test_feature_row_type(tmp_db: WallpaperDB) -> None:
    tmp_db._conn.execute(
        "INSERT INTO images (image_id, path) VALUES (?, ?)", ("x", "/x.png")
    )
    tmp_db._conn.execute(
        "INSERT INTO features (image_id, oklab_vector, color_count) VALUES (?, ?, ?)",
        ("x", json.dumps([0.1, 0.2, 0.3]), 3),
    )
    row = tmp_db.get_features("x")
    assert isinstance(row, FeatureRow)


def test_cluster_row_type(tmp_db: WallpaperDB) -> None:
    tmp_db._conn.execute(
        "INSERT INTO clusters (cluster_id, centroid, label, member_count, run_id) "
        "VALUES (?, ?, ?, ?, ?)",
        (1, json.dumps([0.5] * 3), "c", 0, "r1"),
    )
    rows = tmp_db.get_clusters()
    assert all(isinstance(r, ClusterRow) for r in rows)
