---
type: moc
tags: [moc, wpick, theming, desktop, project, archived]
aliases: ["wpick MOC", "Wallpaper Picker"]
status: archived
created: 2026-05-23
archived: 2026-05-26
reason: "Replaced by shell-based theme pipeline (theme_ctl.sh + cluster_v2.py + rofi_theme_selector.sh)"
---

# wpick — Wallpaper Clustering & Smart Picker [ARCHIVED]

> wpick was replaced by a simpler shell-based approach. Source archived to `~/.local/archive/wpick/`.

## What replaced it

The clustering pipeline (`extract_and_cluster.py` + `cluster_v2.py`) produces themed directories under `~/Pictures/themes/{Dark,Light}/<theme>/`. Theme selection is handled by `theme_ctl.sh` (backend) and `rofi_theme_selector.sh` (UI). No numpy, no SQLite, no Python deps beyond stdlib.

**Active tools:**
- `~/user_scripts/theme_pipeline/` — clustering scripts
- `~/user_scripts/theme_matugen/theme_ctl.sh` — theme state manager
- `~/user_scripts/rofi/rofi_theme_selector.sh` — rofi theme picker
- `~/Pictures/themes/` — 78 themes (54 Dark, 24 Light)

## Original pipeline (for reference)

```
wallpapers/ (dark/ & light/)
       ↓  scan
matugen --dry-run --json hex
       ↓
extraction_results.json
       ↓  cluster (K-means HSL)
cluster_v2.py
       ↓
~/Pictures/themes/{Dark,Light}/<theme>/ (symlinks)
       ↓  pick
rofi_theme_selector.sh
       ↓
theme_ctl.sh theme set <name>
       ↓
swww img + matugen image
```
