from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

import wpick.config as cfg_module
from wpick.db import WallpaperDB, init_schema
from wpick.models import ClusterRow, FeatureRow, WpickConfig


@pytest.fixture(autouse=True)
def isolated_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = WpickConfig(
        wallpaper_dir=tmp_path / "wallpapers",
        db_path=tmp_path / "storage" / "wpick.db",
        cache_dir=tmp_path / "cache",
        max_colors=16,
        cluster_count=6,
    )
    cfg.wallpaper_dir.mkdir(parents=True, exist_ok=True)
    (tmp_path / "storage").mkdir(parents=True, exist_ok=True)
    (tmp_path / "cache").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(cfg_module, "_config", cfg)


@pytest.fixture
def tmp_db(tmp_path: Path) -> WallpaperDB:
    db_path = tmp_path / "test.db"
    init_schema(db_path)
    db = WallpaperDB(db_path)
    db.connect()
    yield db
    db.close()


@pytest.fixture
def jpeg_factory(tmp_path: Path):
    def _make(
        name: str,
        color: tuple[int, int, int] = (128, 64, 32),
        size: tuple[int, int] = (10, 10),
    ) -> Path:
        p = tmp_path / name
        Image.new("RGB", size, color).save(p, "JPEG")
        return p

    return _make


@pytest.fixture
def sample_feature() -> FeatureRow:
    return FeatureRow(
        image_id="abc123",
        path="/tmp/test.jpg",
        oklab_vector=[0.5, 0.1, -0.1, 0.3, 0.2, 0.0],
        color_count=2,
        extracted_at="2024-01-01T00:00:00",
    )


@pytest.fixture
def sample_cluster() -> ClusterRow:
    return ClusterRow(
        cluster_id=0,
        label="dark-warm",
        centroid=[0.5, 0.1, -0.1],
        member_count=5,
        run_id="run-001",
    )
