from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


class WpickError(Exception):
    """Base exception for all wpick errors."""


class ExtractorError(WpickError):
    """Raised when feature extraction fails."""


class ClusterError(WpickError):
    """Raised when clustering operations fail."""


class AssignerError(WpickError):
    """Raised when image assignment operations fail."""


class OrchestratorError(WpickError):
    """Raised when orchestration or command execution fails."""


class PickerError(WpickError):
    """Raised when wallpaper picking or UI operations fail."""


class DatabaseError(WpickError):
    """Raised on database operation failures."""


class ConfigError(WpickError):
    """Raised on configuration validation failures."""


@dataclass
class OklabColor:
    L: float
    a: float
    b: float


@dataclass
class FeatureRow:
    image_id: str
    path: str
    oklab_vector: list[float]
    color_count: int
    extracted_at: str


@dataclass
class ClusterRow:
    cluster_id: int
    label: str
    centroid: list[float]
    member_count: int
    run_id: str


@dataclass
class ClusterRunRecord:
    run_id: str
    ran_at: str
    image_count: int
    cluster_count: int
    params: str


@dataclass
class ScanResult:
    total: int
    extracted: int
    skipped: int
    errors: int


@dataclass
class AssignResult:
    image_id: str
    cluster_id: int
    similarity: float


@dataclass
class BatchAssignResult:
    assigned: int
    failed: int
    skipped: int
    results: list[AssignResult]


@dataclass
class StatsResult:
    total_images: int
    extracted_images: int
    clusters: list[ClusterRow]


@dataclass
class HistoryRow:
    image_id: str
    set_at: str


@dataclass
class ImageRow:
    image_id: str
    path: str
    cluster_id: int | None = None


@dataclass
class RofiEntry:
    display: str
    image_id: str
    path: Path
    cluster_label: str


@dataclass
class ThumbnailResult:
    image_id: str
    thumb_path: Path
    was_generated: bool


@dataclass
class WpickConfig:
    wallpaper_dir: Path = field(default_factory=lambda: Path.home() / "Pictures" / "wallpapers")
    db_path: Path = field(default_factory=lambda: Path.home() / ".local" / "share" / "wpick" / "wpick.db")
    cache_dir: Path = field(default_factory=lambda: Path.home() / ".cache" / "wpick")
    max_colors: int = 16
    cluster_count: int = 6
