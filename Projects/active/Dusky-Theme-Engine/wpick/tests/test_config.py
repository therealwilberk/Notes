from __future__ import annotations

from pathlib import Path

import pytest

import wpick.config as cfg_module
from wpick.models import ConfigError, WpickConfig


def test_validate_valid_config(tmp_path: Path) -> None:
    cfg = WpickConfig(
        wallpaper_dir=tmp_path / "exists",
        db_path=tmp_path / "exists" / "wpick.db",
        cache_dir=tmp_path / "cache",
        max_colors=8,
        cluster_count=4,
    )
    cfg.wallpaper_dir.mkdir(parents=True, exist_ok=True)
    cfg.db_path.parent.mkdir(parents=True, exist_ok=True)
    cfg_module.validate_config(cfg)


def test_validate_invalid_wallpaper_dir(tmp_path: Path) -> None:
    cfg = WpickConfig(
        wallpaper_dir=tmp_path / "nonexistent",
        db_path=tmp_path / "db" / "wpick.db",
        cache_dir=tmp_path / "cache",
        max_colors=8,
        cluster_count=4,
    )
    cfg.db_path.parent.mkdir(parents=True, exist_ok=True)
    with pytest.raises(ConfigError, match="wallpaper_dir"):
        cfg_module.validate_config(cfg)


def test_validate_invalid_db_path(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="db_path"):
        cfg_module.validate_config(
            WpickConfig(
                wallpaper_dir=tmp_path,
                db_path=tmp_path / "nonexistent" / "wpick.db",
                cache_dir=tmp_path / "cache",
                max_colors=8,
                cluster_count=4,
            )
        )


def test_validate_low_cluster_count(tmp_path: Path) -> None:
    cfg = WpickConfig(
        wallpaper_dir=tmp_path,
        db_path=tmp_path / "db" / "wpick.db",
        cache_dir=tmp_path / "cache",
        max_colors=8,
        cluster_count=1,
    )
    (tmp_path / "db").mkdir(parents=True, exist_ok=True)
    with pytest.raises(ConfigError, match="cluster_count"):
        cfg_module.validate_config(cfg)


def test_validate_zero_max_colors(tmp_path: Path) -> None:
    cfg = WpickConfig(
        wallpaper_dir=tmp_path,
        db_path=tmp_path / "db" / "wpick.db",
        cache_dir=tmp_path / "cache",
        max_colors=0,
        cluster_count=3,
    )
    (tmp_path / "db").mkdir(parents=True, exist_ok=True)
    with pytest.raises(ConfigError, match="max_colors"):
        cfg_module.validate_config(cfg)


def test_load_config_caches(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cfg_module, "_config", None)
    called = 0

    original_validate = cfg_module.validate_config

    def tracking_validate(*args, **kwargs):
        nonlocal called
        called += 1
        return original_validate(*args, **kwargs)

    monkeypatch.setattr(cfg_module, "validate_config", tracking_validate)
    original_load = cfg_module.load_config
    from wpick.config import load_config
    c1 = load_config()
    called = 0
    c2 = load_config()
    assert c1 is c2
    assert c1.cluster_count == 6


def test_load_config_force_reload(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cfg_module, "_config", None)
    first = cfg_module.load_config()
    monkeypatch.setattr(cfg_module, "_config", None)
    with monkeypatch.context() as m:
        m.setattr(cfg_module, "_config", None)
        second = cfg_module.load_config()
    assert first is not second


def test_load_config_initializes_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cfg_module, "_config", None)
    cfg = cfg_module.load_config()
    assert isinstance(cfg, WpickConfig)
    assert cfg.max_colors == 16
    assert cfg.cluster_count == 6