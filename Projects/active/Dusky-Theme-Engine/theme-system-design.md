---
type: project
tags: [project, wpick, theming, design, matugen]
created: 2026-05-26
status: in-progress
parent: "[[Projects/active/Dusky-Theme-Engine/wpick- Wallpaper Clustering & Smart Picker.md]]"
---

# wpick Theme System — Design Doc

**Date:** 2026-05-26
**Status:** In Progress
**Research:** [[Research/Theming/Hyde-Theme-Study]], [[Projects/active/Dusky-Theme-Engine/wpick-matugen-research]]

---

## Core Idea

**Matugen is everything.** No hardcoded theme definitions. The wallpaper's own color determines which theme it belongs to. Matugen extracts the source color, we cluster by hue, and themes emerge from the data.

The goal isn't 200 themes. It's enough groups to give a sense of "sameness" within each, more nuanced than plain dark/light.

---

## How It Works

### The Pipeline (One-Time Setup)

```
1508 wallpapers
  → matugen --dry-run --json hex (parallel, 8 workers)
  → extract source_color from each
  → convert to HSL
  → cluster by hue into named themes
  → output: themed directory structure + report
```

This runs once. Takes ~6 minutes. After this, every wallpaper knows its theme.

### Adding New Wallpapers (Ongoing)

```
new wallpaper arrives
  → run matugen on it (--dry-run, single call, <2 sec)
  → get source_color → HSL → hue
  → match to existing theme cluster
  → drop into that theme folder
```

Seconds, not hours. The initial batch is the heavy lift; everything after is lightweight.

---

## Theme Clusters

Themes are named after known palettes, but they're NOT hardcoded to those palettes. The name is just a label for a hue range. Matugen generates the actual colors from each wallpaper.

| Theme | Hue Range | Description |
|-------|-----------|-------------|
| Nord | 195° - 250° | Cool blues, blue-grays |
| Catppuccin | 250° - 310° | Purples, lavenders, magentas |
| Rosepine | 310° - 360° | Pinks, warm magentas |
| Autumn | 0° - 30° | Reds, oranges, warm tones |
| Sunset | 30° - 65° | Golds, ambers, yellows |
| Forest | 65° - 170° | Greens, teals, emeralds |
| Twilight | 170° - 195° | Cyans, cool teals |
| Muted | any (sat < 0.15) | Low-saturation, grayscale-adjacent |

**These ranges are initial guesses.** After the first batch runs, we review the clustering and adjust. Some themes might merge, some might split. The data tells us.

---

## Directory Structure

```
~/Pictures/wpick-themes/          # Output, separate from wallpapers/
├── extraction_results.json       # Raw matugen output for all wallpapers
├── cluster_summary.json          # Theme groupings + stats
├── THEMING-REPORT.md             # Human-readable report
│
├── Dark/
│   ├── Nord/
│   │   ├── 0001.jpg              # symlink or copy from wallpapers/Dark/
│   │   ├── 0015.jpg
│   │   └── ...
│   ├── Catppuccin/
│   │   ├── 0010.jpg
│   │   └── ...
│   ├── Autumn/
│   └── ...
│
└── Light/
    ├── Nord/
    ├── Forest/
    └── ...
```

Original `~/Pictures/wallpapers/` is untouched. The themed dirs are either symlinks (space-efficient) or copies (portable). Symlinks by default.

---

## Theme Selector — How It Thinks

### The Mental Model

The selector doesn't think in "wallpapers." It thinks in **themes**.

```
User: "I want something blue"
  → Selector shows: Nord theme (47 wallpapers)
  → User picks Nord
  → wpick selects a wallpaper from Nord/
  → matugen generates colors from that wallpaper
  → desktop updates
```

```
User: "Surprise me"
  → Selector shows: random theme
  → wpick picks a random wallpaper from that theme
  → same pipeline
```

```
User: "I want dark purple tonight"
  → Selector filters: Dark + Catppuccin
  → Shows wallpaper grid for that combo
  → User picks one (or random)
```

### The Flow

```
wpick theme select
  │
  ├─ Step 1: Show theme grid (rofi)
  │   Nord        [47 wallpapers]  [preview thumbnail]
  │   Catppuccin  [32 wallpapers]  [preview thumbnail]
  │   Autumn      [58 wallpapers]  [preview thumbnail]
  │   ...
  │
  ├─ Step 2: User picks a theme (e.g., Nord)
  │
  ├─ Step 3: Show wallpaper grid within that theme
  │   [wallpaper thumbnails, monitor-aware grid, max 5 columns]
  │   [or: "Random" option at the top]
  │
  ├─ Step 4: User picks a wallpaper (or random)
  │
  └─ Step 5: Apply
      ├── matugen image <wallpaper> --type <scheme> --mode dark
      ├── swww wallpaper <wallpaper>
      └── Reload components (rofi, waybar, kitty, Hyprland)
```

### Commands

```bash
wpick theme select              # Full interactive flow (theme → wallpaper → apply)
wpick theme select --random     # Skip grid, pick random theme + wallpaper
wpick theme set nord            # Apply a specific theme (picks random wallpaper within)
wpick theme set nord --random   # Same, explicit
wpick theme next                # Cycle to next theme
wpick theme prev                # Cycle to previous theme
wpick theme list                # CLI list of available themes with counts
wpick theme current             # Show current theme + wallpaper
```

---

## Matugen Integration

Each theme can have a preferred scheme type, but it's a default, not a hardcode.

```toml
# themes.toml (optional overrides per theme)
[themes.nord]
scheme = "scheme-tonal-spot"    # works well for blues
prefer = "saturation"

[themes.catppuccin]
scheme = "scheme-content"       # works well for purples
prefer = "saturation"

[themes.autumn]
scheme = "scheme-vibrant"       # works well for warm tones
prefer = "saturation"
```

If no override exists, use the global default (`scheme-tonal-spot`). The scheme is tested per theme during the initial batch — we try all 9 schemes on a sample from each cluster and pick the one that looks best.

### The Bug Fix

Regardless of theme system design, wpick MUST pass `--prefer saturation` to matugen. Without it, matugen hangs on multi-color images in daemon mode. This is a standalone fix that should land immediately.

---

## What This Is NOT

- **Not a profile system.** No GTK themes, icon themes, cursor themes. Pure color.
- **Not hardcoded.** Themes emerge from wallpaper colors, not from a config file.
- **Not 200 themes.** 6-8 hue clusters. Enough variety without fragmentation.
- **Not a replacement for wallpapers/.** The themed dirs reference the originals.

---

## Open Questions

1. **Symlinks vs copies?** Symlinks are space-efficient but break if originals move. Copies are portable but double storage. Default: symlinks.

2. **Scheme testing per theme?** Should we visually test all 9 scheme types on a sample from each cluster? Or just default to `scheme-tonal-spot` and iterate later?

3. **Muted theme?** Low-saturation wallpapers (grayscale, near-grayscale) are their own thing. Do they get a scheme override (like `scheme-neutral`)?

4. **Light mode handling.** Light wallpapers in dark themes and vice versa. Do we enforce `--mode dark` for Dark/ and `--mode light` for Light/? Or let the user toggle?

5. **Theme naming.** After clustering, do we rename based on what we see? "Nord" for blues is aspirational — the actual colors come from each wallpaper, not from the Nord palette.

---

## Implementation Phases

| Phase | What | Effort |
|-------|------|--------|
| 1 | Batch extraction + clustering (this pipeline) | Done (running now) |
| 2 | Review results, adjust hue ranges | 30 min (manual) |
| 3 | Create themed directory structure (symlinks) | 30 min |
| 4 | Fix matugen `--prefer` bug in wpick | 15 min |
| 5 | Theme selector (rofi grid, wallpaper grid) | 2h |
| 6 | Apply pipeline (matugen → swww → reload) | 1h |
| 7 | CLI commands | 1h |
| 8 | Scheme testing per theme cluster | 1h |

Phases 4-5 can start before 2-3. The bug fix is independent.

---

## References

- [[Hyde-Theme-Study]] — How HyDE does themes (what to adopt, what to avoid)
- [[wpick-matugen-research]] — All matugen CLI flags, empirical comparisons
- [[wpick-matugen-plan]] — MatugenConfig expansion plan (incorporated here)
