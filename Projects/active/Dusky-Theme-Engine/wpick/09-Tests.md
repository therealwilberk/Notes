---
tags:
  - project
  - wpick
  - testing
parent: "[[wpick]]"
created: 2026-05-23
---

# wpick — Tests

## Strategy

- Isolated config (tmp_path, no real DB)
- Solid color fixtures for deterministic extraction
- Corrupt file handling
- Integration tests for scan → cluster → assign pipeline

## Fixtures

```python
"""Shared fixtures."""
import pytest
import numpy as np
from pathlib import Path
from PIL import Image


FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(autouse=True)
def isolated_config(tmp_path, monkeypatch):
    """Redirect all storage to tmp_path so tests don't touch real DB."""
    import wpick.config as cfg_module
    cfg_module._cfg = {
        "paths": {
            "wallpapers": str(tmp_path / "wallpapers"),
            "cache": str(tmp_path / "cache"),
            "storage": str(tmp_path / "storage"),
        },
        "extraction": {
            "sample_size": 64,
            "n_colors": 4,
            "extensions": ["jpg", "jpeg", "png"],
        },
        "clustering": {
            "min_cluster_size": 2,
            "min_samples": 1,
        },
        "thumbnails": {"size": 64, "quality": 75},
        "swww": {
            "transition_type": "fade",
            "transition_pos": "0.5,0.5",
            "transition_fps": 30,
            "transition_duration": 0.5,
        },
        "matugen": {"enabled": False, "extra_flags": []},
        "watcher": {"enabled": False, "debounce_seconds": 1},
    }
    yield
    cfg_module._cfg = None


@pytest.fixture
def solid_red(tmp_path) -> Path:
    p = tmp_path / "red.png"
    Image.new("RGB", (64, 64), (220, 50, 50)).save(p)
    return p


@pytest.fixture
def solid_blue(tmp_path) -> Path:
    p = tmp_path / "blue.png"
    Image.new("RGB", (64, 64), (50, 80, 220)).save(p)
    return p


@pytest.fixture
def solid_green(tmp_path) -> Path:
    p = tmp_path / "green.png"
    Image.new("RGB", (64, 64), (40, 180, 80)).save(p)
    return p


@pytest.fixture
def corrupt_file(tmp_path) -> Path:
    p = tmp_path / "corrupt.png"
    p.write_bytes(b"\x89PNG notanimage")
    return p


@pytest.fixture
def rgba_image(tmp_path) -> Path:
    p = tmp_path / "rgba.png"
    img = Image.new("RGBA", (64, 64), (100, 150, 200, 128))
    img.save(p)
    return p
```

## Test Files

- `test_oklab.py` — Color space conversion accuracy
- `test_extractor.py` — Feature extraction, corrupt handling, RGBA
- `test_clusterer.py` — HDBSCAN clustering, too-few-images error
- `test_assigner.py` — Cosine similarity, assignment logic
- `test_db.py` — SQLite operations, idempotency

## Running

```bash
uv run pytest
uv run pytest tests/test_extractor.py -v
uv run pytest --cov=src/wpick --cov-report=html
uv run ruff check src/
uv run mypy src/wpick/
```

## See Also

- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/01-Setup]] — Dev dependencies
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/03-Extraction]] — What extraction tests validate
