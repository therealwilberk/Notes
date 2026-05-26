---
type: moc
tags: [moc, wpick, theming, desktop, project]
aliases: ["wpick MOC", "Wallpaper Picker"]
status: active
created: 2026-05-23
parent: "[[Projects/active/Dusky-Theme-Engine/wpick- Wallpaper Clustering & Smart Picker.md]]"
---

# wpick — Wallpaper Clustering & Smart Picker

> Wallpaper-driven mood system for Hyprland. Cluster by color, pick by vibe, theme follows.

## Pipeline

```
wallpapers/ (dark/ & light/)
       ↓  scan
auto-palette (Rust)
       ↓
features.jsonl
       ↓  cluster
HDBSCAN
       ↓
clusters.json (with named centroids)
       ↓  pick
rofi card grid (Hyde-style)
       ↓
swww img <path> + matugen image <path>
```

**Key separation:** matugen is downstream. Clustering = navigation. Theme accuracy = matugen's job.

## Subdocs

- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/00-Architecture]] — Mental model, data flow, module map
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/01-Setup]] — uv, dependencies, config.toml
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/02-Database]] — SQLite schema, db.py operations
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/03-Extraction]] — auto-palette integration, feature vectors
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/04-Clustering]] — HDBSCAN, cluster naming, recluster strategy
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/05-Assignment]] — Incremental assignment, cosine similarity
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/06-Orchestrator]] — Watcher, swww, matugen integration
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/07-Picker]] — rofi card grid, Hyde-style UI, thumbnails
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/08-CLI]] — Entry points, commands, keybinds
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/09-Tests]] — Fixtures, test strategy

## Stack

- Python 3.12+ (uv managed)
- auto-palette (Rust binary, extraction)
- HDBSCAN + scikit-learn (clustering)
- Pillow (thumbnails)
- Typer (CLI)
- SQLite (storage)
- swww (wallpaper)
- matugen (theming)
- rofi-wayland (picker UI)

## References

- [[Projects/active/Dusky-Theme-Engine/wpick- Wallpaper Clustering & Smart Picker]] — Parent project spec
- [[Projects/active/Dusky-Theme-Engine/quickshell-analysis]] — QuickShell deep dive (Phase 2)
- [[Projects/active/Dusky-Theme-Engine/research-existing-solutions]] — Competitive research
- Hyde-project/hyde — Card grid reference
- bjarneo/quickshell — Keyboard-first shell base

## Source

- Spec: `Projects/active/Dusky-Theme-Engine/wpick- Wallpaper Clustering & Smart Picker.md`
- Project dir: `~/.config/wpick/`
