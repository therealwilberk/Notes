---
tags:
  - project
  - wpick
  - setup
parent: "[[wpick]]"
created: 2026-05-23
---

# wpick — Setup

## Install uv

```bash
uv --version
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Init project

```bash
mkdir -p ~/.config/wpick
cd ~/.config/wpick
uv init --name wpick --python 3.12
```

## Dependencies

```bash
# Core
uv add pillow hdbscan numpy scikit-learn typer tomllib-backport

# Watching
uv add watchdog

# Dev/test
uv add --dev pytest pytest-cov pytest-mock ruff mypy
```

## pyproject.toml

```toml
[project]
name = "wpick"
version = "0.1.0"
description = "Wallpaper clustering and smart picker for Hyprland"
requires-python = ">=3.12"
dependencies = [
    "pillow>=10.0",
    "hdbscan>=0.8.33",
    "numpy>=1.26",
    "scikit-learn>=1.4",
    "typer>=0.12",
    "watchdog>=4.0",
]

[project.scripts]
wpick = "wpick.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/wpick"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src/wpick --cov-report=term-missing -v"

[tool.ruff]
line-length = 100
src = ["src"]

[tool.mypy]
strict = false
ignore_missing_imports = true
```

## Config

### config.default.toml

```toml
[paths]
wallpapers = "~/wallpapers"
cache      = "~/.cache/wpick"
storage    = "~/.local/share/wpick"

[extraction]
sample_size = 256
n_colors    = 8
extensions  = ["jpg", "jpeg", "png", "webp", "bmp"]

[clustering]
min_cluster_size = 8
min_samples      = 3

[thumbnails]
size    = 256
quality = 85

[swww]
transition_type   = "grow"
transition_pos    = "0.5,0.5"
transition_fps    = 60
transition_duration = 1.5

[matugen]
enabled = true
extra_flags = []

[watcher]
enabled         = true
debounce_seconds = 5
```

### User override

```bash
cp config.default.toml config.toml
$EDITOR config.toml  # set paths.wallpapers
```

## Verify

```bash
uv run python --version
uv run pytest --collect-only
```

## See Also

- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/00-Architecture]] — Module overview
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/02-Database]] — Schema details
- [[10-Deployment]] — Production setup
