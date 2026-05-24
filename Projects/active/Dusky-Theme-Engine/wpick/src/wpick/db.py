from __future__ import annotations

import json
import logging
import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from wpick.models import ClusterRow, DatabaseError, FeatureRow, ImageRow, ScanResult

logger = logging.getLogger(__name__)

SCHEMA_VERSION = 1


def _current_version(conn: sqlite3.Connection) -> int:
    try:
        row = conn.execute("SELECT MAX(version) FROM schema_migrations").fetchone()
        return row[0] if row[0] is not None else 0
    except sqlite3.OperationalError:
        return 0


def init_schema(db_path: Path) -> None:
    schema_path = Path(__file__).parent / "schema.sql"
    if not schema_path.exists():
        raise DatabaseError(f"schema file not found: {schema_path}")
    conn = sqlite3.connect(str(db_path))
    try:
        conn.executescript(schema_path.read_text())
        version = _current_version(conn)
        if version < SCHEMA_VERSION:
            for v in range(version + 1, SCHEMA_VERSION + 1):
                conn.execute(
                    "INSERT INTO schema_migrations (version) VALUES (?)",
                    (v,),
                )
            conn.commit()
    except sqlite3.Error as e:
        raise DatabaseError(f"schema initialization failed: {e}") from e
    finally:
        conn.close()


class WallpaperDB:
    def __init__(self, db_path: str | Path) -> None:
        self._db_path = Path(db_path)
        self._conn: sqlite3.Connection | None = None

    def connect(self) -> None:
        if self._conn is not None:
            return
        try:
            self._conn = sqlite3.connect(str(self._db_path))
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
        except sqlite3.Error as e:
            raise DatabaseError(f"failed to connect to database: {e}") from e

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def __enter__(self) -> WallpaperDB:
        self.connect()
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    @contextmanager
    def _transaction(self) -> Generator[sqlite3.Cursor, None, None]:
        if self._conn is None:
            raise DatabaseError("database not connected")
        try:
            cursor = self._conn.cursor()
            yield cursor
            self._conn.commit()
        except sqlite3.Error as e:
            self._conn.rollback()
            raise DatabaseError(f"transaction failed: {e}") from e

    def _row_to_image(self, row: sqlite3.Row) -> ImageRow:
        return ImageRow(image_id=row["image_id"], path=row["path"])

    def _row_to_feature(self, row: sqlite3.Row) -> FeatureRow:
        return FeatureRow(
            image_id=row["image_id"],
            path=row["path"],
            oklab_vector=json.loads(row["oklab_vector"]),
            color_count=row["color_count"],
            extracted_at=row["extracted_at"],
        )

    def _row_to_cluster(self, row: sqlite3.Row) -> ClusterRow:
        return ClusterRow(
            cluster_id=row["cluster_id"],
            centroid=json.loads(row["centroid"]),
            label=row["label"],
            member_count=row["member_count"],
            run_id=row["run_id"],
        )

    def get_image(self, image_id: str) -> ImageRow | None:
        with self._transaction() as cur:
            cur.execute(
                "SELECT image_id, path FROM images WHERE image_id = ?", (image_id,)
            )
            row = cur.fetchone()
            return self._row_to_image(row) if row else None

    def get_all_images(self) -> list[ImageRow]:
        with self._transaction() as cur:
            cur.execute("SELECT image_id, path FROM images")
            return [self._row_to_image(row) for row in cur.fetchall()]

    def get_unextracted_images(self) -> list[ImageRow]:
        with self._transaction() as cur:
            cur.execute(
                "SELECT i.image_id, i.path FROM images i "
                "LEFT JOIN features f ON i.image_id = f.image_id "
                "WHERE f.image_id IS NULL"
            )
            return [self._row_to_image(row) for row in cur.fetchall()]

    def get_unassigned_images(self) -> list[ImageRow]:
        with self._transaction() as cur:
            cur.execute(
                "SELECT i.image_id, i.path FROM images i "
                "LEFT JOIN image_cluster ic ON i.image_id = ic.image_id "
                "WHERE ic.image_id IS NULL"
            )
            return [self._row_to_image(row) for row in cur.fetchall()]

    def get_features(self, image_id: str) -> FeatureRow | None:
        with self._transaction() as cur:
            cur.execute(
                "SELECT f.image_id, i.path, f.oklab_vector, "
                "f.color_count, f.extracted_at "
                "FROM features f "
                "JOIN images i ON f.image_id = i.image_id "
                "WHERE f.image_id = ?",
                (image_id,),
            )
            row = cur.fetchone()
            return self._row_to_feature(row) if row else None

    def get_all_features(self) -> list[FeatureRow]:
        with self._transaction() as cur:
            cur.execute(
                "SELECT f.image_id, i.path, f.oklab_vector, "
                "f.color_count, f.extracted_at "
                "FROM features f "
                "JOIN images i ON f.image_id = i.image_id"
            )
            return [self._row_to_feature(row) for row in cur.fetchall()]

    def get_clusters(self) -> list[ClusterRow]:
        with self._transaction() as cur:
            cur.execute(
                "SELECT cluster_id, centroid, label, member_count, run_id "
                "FROM clusters ORDER BY cluster_id"
            )
            return [self._row_to_cluster(row) for row in cur.fetchall()]

    def assign_image_cluster(self, image_id: str, cluster_id: int) -> None:
        with self._transaction() as cur:
            cur.execute(
                "INSERT OR REPLACE INTO image_cluster (image_id, cluster_id) "
                "VALUES (?, ?)",
                (image_id, cluster_id),
            )

    def get_assignments(self) -> list[tuple[str, int]]:
        with self._transaction() as cur:
            cur.execute("SELECT image_id, cluster_id FROM image_cluster")
            return [(row["image_id"], row["cluster_id"]) for row in cur.fetchall()]
