from __future__ import annotations

from wpick.models import ConfigError, WpickConfig


def validate_config(cfg: WpickConfig) -> None:
    if not cfg.wallpaper_dir.is_dir():
        raise ConfigError(f"wallpaper_dir does not exist: {cfg.wallpaper_dir}")
    if not cfg.db_path.parent.exists():
        raise ConfigError(f"db_path parent directory does not exist: {cfg.db_path.parent}")
    if cfg.cluster_count < 2:
        raise ConfigError(f"cluster_count must be >= 2, got {cfg.cluster_count}")
    if cfg.max_colors < 1:
        raise ConfigError(f"max_colors must be >= 1, got {cfg.max_colors}")


_config: WpickConfig | None = None


def load_config(*, force: bool = False) -> WpickConfig:
    global _config
    if _config is not None and not force:
        return _config
    cfg = WpickConfig()
    validate_config(cfg)
    _config = cfg
    return _config
