# Theme Selector Unification + Post-Apply Hooks

**Date:** 2026-05-26
**Status:** Planning — reviewed & superseded
**Branch:** `feature/theme-selector`

---

## Review of Original Plan

### What's correct

| Part | Verdict | Why |
|------|---------|-----|
| Hooks first (Part 1) | ✅ Correct | Enabler for everything else, ~3 lines |
| Merge v2 UX + opencode engineering (Part 2) | ✅ Correct | Both files have complementary strengths |
| Cleanup dead files (Part 3) | ✅ Correct | Already done — `rofi_theme_selector.sh` removed |
| Don't add features during merge | ❌ **Wrong for this project** | The user wants god tier. "Ship clean then iterate" is safe but boring. The merged script is the one place users interact with the theme system daily. It should feel premium on day one. |

### What's missing from the plan

| Missing | Impact |
|---------|--------|
| **CLI surface** | No `--help`, `--random`, `--mode`, `--dry-run`, `--version` flags. Selector is GUI-only. |
| **Config file** | No `~/.config/theme-selector/config`. User can't set defaults (view mode, columns, thumb size, animations). |
| **View modes** | Only grid. No list view for speed, no compact view for density. Users have one option. |
| **Animations** | Rofi supports `-theme-str` transitions: fade, slide, wipe between views. Currently instant/invisible. |
| **Theme info/hover** | No color swatches, no centroid preview, no wallpaper count shown until you pick. |
| **Favorites/Starring** | No way to mark frequent themes. They get buried in alphabetical sort. |
| **Search by color** | No way to say "show me warm/blue/muted themes." |
| **Keyboard UX** | Only Alt+M and Alt+R. No `Ctrl+F` search, no `Alt+S` view toggle, no `Esc` feedback. |
| **Wallpaper details** | No image dimensions, aspect ratio, or file size shown before applying. |
| **Dry-run** | Can't preview what would happen before committing. |
| **No animation transition** | Between theme grid → wallpaper grid is instant cut. Rofi can do fade. |
| **uwsm-app hardcoded** | v2 hardcodes `uwsm-app -- rofi` with no fallback to bare `rofi`. |

---

## Superseding Plan: Merged Selector + Backlog

**Scope rule:** Ship the merge. Everything else is v2.

**Accepted additions to merge scope:**
1. Config file sourcing (`~/.config/theme-selector/config` — ~3 lines at top)
2. `--mode` and `--random` CLI flags (headless mode, already implied by v2)
3. uwsm fallback (bare `rofi` if `uwsm-app` missing)

**Backlogged to v2:**
- Three view modes (grid/list/compact) + `Alt+S` toggle
- Favorites system (`Alt+F`, integrates with existing `theme_favorites_ctl.sh`)
- Theme info panel (`Alt+I`, reads `cluster_v2.json`)
- Animations between views (rofi `-theme-str` transitions)
- Search by color (`--hue-min/--hue-max`)
- Wallpaper details (dimensions, aspect ratio, file size)

### Architecture

```
~/.config/theme-selector/              ← user config (created by first run)
├── config                              ← sourced by the script
├── hooks/                              ← user hook overrides
│   └── theme-set.d/                    ← sourced not subprocessed
└── favorites                           ← one theme name per line

~/.cache/theme-selector/                ← runtime artifacts
├── theme-thumbs/{Dark,Light}/
├── wallpaper-thumbs/
├── preview-{dark,light}.png
└── rofi-colors.rasi                    ← generated matugen colors for rofi

~/.local/state/theme-selector/          ← last-session state
└── last-mode
```

### CLI

```bash
theme-selector                          # GUI mode (rofi grid)
theme-selector --help                   # full usage
theme-selector --mode dark              # start in dark mode
theme-selector --view list              # start in list mode
theme-selector --random                 # pick + apply random (no GUI)
theme-selector --random dark            # random from dark mode
theme-selector --dry-run --random        # show what would be picked
theme-selector --prune-cache            # clean thumbnails
theme-selector --version                # show version
theme-selector --favorites              # show only favorited themes
```

### Config file (`~/.config/theme-selector/config`)

```bash
# View modes: grid | list | compact
THEME_SELECTOR_VIEW=grid

# Max columns in grid mode (auto = monitor-aware)
THEME_SELECTOR_MAX_COLUMNS=5

# Thumbnail size for wallpaper grid
THEME_SELECTOR_THUMB_SIZE=300

# Mode detection: auto | dark | light
THEME_SELECTOR_MODE=auto

# Animations: on | off
THEME_SELECTOR_ANIMATIONS=on

# Default rofi theme path
THEME_SELECTOR_THEME_GRID="${HOME}/.config/theme-selector/wallpaper-grid.rasi"
THEME_SELECTOR_THEME_LIST="${HOME}/.config/theme-selector/theme-list.rasi"
```

### Three view modes — **v2 backlog**

```
grid (default)
  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
  │ ████ │ │ ████ │ │ ████ │ │ ████ │
  │Nord  │ │Copper│ │Forest│ │Teal  │
  │ 12   │ │ 8    │ │ 15   │ │ 6    │
  └──────┘ └──────┘ └──────┘ └──────┘
  4 columns, thumbnails, wallpaper count

list
  Nord ........... 12 wallpapers
  Copper ......... 8 wallpapers
  Forest ......... 15 wallpapers  ← active
  Teal ........... 6 wallpapers
  No thumbnails. Fast for large collections (50+ themes).

compact
  ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐
  │Nu│ │Co│ │Fo│ │Te│ │Or│ │Ma│
  └──┘ └──┘ └──┘ └──┘ └──┘ └──┘
  8+ columns, tiny thumbnails (100px), names hidden.
  For power users who know their themes by color.
```

### Animations & transitions (rofi `-theme-str`) — **v2 backlog**

```bash
# Fade between views
rofi_cmd+=(-theme-str "window { transition: fade; transition-duration: 150; }")

# Slide for mode toggle (dark ↔ light)
rofi_cmd+=(-theme-str "window { transition: slide; transition-duration: 200; }")

# Notification animations via notify-send urgency + hints
notify-send -a "Theme" -u low -h int:transient:1 "${theme_name}" "${mode^}"
```

Rofi's animation support is limited to `transition` and `transition-duration` in the window config. That's enough for:
- **Fade** between theme grid → wallpaper grid
- **Slide** on Alt+M mode toggle
- **Instant** when applying (rofi closes immediately, async apply)

### Keybindings (merge scope)

| Key | Action | Stage available |
|-----|--------|-----------------|
| `Enter` | Select / Apply | Theme grid, wallpaper grid |
| `Esc` | Back | All (one level up or exit) |
| `Alt+M` | Toggle dark/light mode | Theme grid |
| `Alt+R` | Random theme / random wallpaper | Theme grid, wallpaper grid |
| `Ctrl+F` | Search/filter (rofi built-in) | All |

### Theme info panel (Alt+I) — **v2 backlog**

```
┌──────────────────────────────────────┐
│  Forest                              │
│  15 wallpapers  ★ Favorited          │
│                                      │
│  ████████████████  hue= 89.9°       │
│  ████████████████  sat=  0.44       │
│  ████████████████  light= 0.42       │
│                                      │
│  Sample:  #c4efb7  #8bbb7d  #a1ab31 │
│  Dir:     ~/Pictures/themes/Dark/    │
│  Apply:   theme_ctl theme set ...    │
└──────────────────────────────────────┘
```

This is a rofi notification or a secondary rofi instance. Not an overlay — rofi can't do overlays natively. But a second rofi `-dmenu` with one entry that shows multi-line info works well.

### Favorites system — **v2 backlog** (theme_favorites_ctl.sh already exists)

```
~/.config/theme-selector/favorites
┌─────────────────────┐
│ Nord                │
│ Forest              │  ← one theme name per line
│ Catppuccin          │
└─────────────────────┘
```

In grid view, favorited themes appear **first**, separated by a line, then the rest sorted alphabetically. `Alt+F` toggles the star.

### Search by color — **v2 backlog**

```bash
# Filter: show themes with hue in warm range (0-60)
theme-selector --hue-min 0 --hue-max 60

# Filter: show only muted themes (sat < 0.2)
theme-selector --sat-max 0.2
```

This reads from `cluster_v2.json` and builds a filtered rofi grid. The JSON already has centroid data — this is a filter pass on top of the existing theme list.

### Wallpaper details (dimensions, aspect ratio) — **v2 backlog**

### Merged script structure

```
theme-selector.sh (~500-550 lines)
├── Config & paths
├── CLI parsing (--help, --mode, --view, --random, --dry-run, --prune-cache)
├── Config file loader (sources ~/.config/theme-selector/config)
├── Dep checks (rofi, jq, magick)
├── Lock management (acquire + release with FD tracking)
├── Logging (log, die, notify with urgency levels)
├── Helpers
│   ├── get_system_mode()        ← gsettings → state.conf fallback
│   ├── get_current_theme()      ← reads state.conf directly
│   ├── toggle_mode()
│   └── is_favorite() / toggle_favorite()
├── Thumbnail system
│   ├── wallpaper_thumb()
│   ├── theme_thumb()            ← per-mode cache
│   ├── ensure_preview_composite()
│   └── prune_cache()
├── Rofi wrapper
│   ├── run_rofi()               ← common, with uwsm fallback
│   ├── get_grid_columns()       ← monitor-aware
│   └── ROFI_ANIMATION_STR      ← injected via -theme-str
├── Views
│   ├── show_theme_grid()        ← thumbnail grid + Alt+M/R/S/F
│   ├── show_theme_list()        ← dmenu list (fast)
│   ├── show_theme_compact()     ← mini grid (power user)
│   └── show_wallpaper_grid()    ← parallel thumbs + async apply
├── Info & preview
│   ├── show_theme_info()        ← centroid, colors, sample
│   └── search_by_color()        ← cluster_v2.json filter
├── Apply
│   └── apply_theme()            ← async background subshell
└── main()
```

### Post-apply hooks

```
~/.config/dusky/theme-hooks.d/
├── 01-notify.sh                  ← success notification
├── 10-colors-rofi.sh             ← copy matugen palette → rofi-colors.rasi
├── 20-reload-waybar.sh           ← pkill -SIGUSR2 waybar
└── 30-reload-kitty.sh            ← kitty @ set-colors ...
```

Added to `theme_ctl.sh` `cmd_theme_set()`:
```bash
local hook_dir="${HOME}/.config/dusky/theme-hooks.d"
if [[ -d "$hook_dir" ]]; then
    local hook
    for hook in "$hook_dir"/*; do
        [[ -f "$hook" && -x "$hook" ]] || continue
        THEME_NAME="$name" THEME_MODE="$THEME_MODE" \
            "$hook" 2>/dev/null || true
    done
fi
```

---

## Order of Operations

### Merge scope (ship first)
1. **Post-apply hooks** — ~3 lines in `theme_ctl.sh`, create `~/.config/dusky/theme-hooks.d/` with starter hooks
2. **Config file** — `~/.config/theme-selector/config` with defaults, sourced at top of script
3. **uwsm fallback** — try `uwsm-app -- rofi`, fall back to bare `rofi`
4. **CLI flags** — `--help`, `--mode`, `--random`, `--prune-cache`, `--dry-run`, `--version`
5. **Refactor v2 into unified script** — take v2's grid UX + async apply + auto-mode; add dep checks + lock lifecycle from opencode
6. **Cleanup** — remove v1 `theme-selector.sh`, remove `theme-selector-v2.sh`, update README

### v2 backlog (iterate after)
1. Three view modes (grid/list/compact) + `Alt+S` toggle
2. Favorites system — wire up `theme_favorites_ctl.sh` + `Alt+F`
3. Theme info panel (`Alt+I`) — reads `cluster_v2.json`
4. Animations — rofi `-theme-str` transitions between views
5. Search by color (`--hue-min/--hue-max`) — reads `cluster_v2.json`
6. Wallpaper details (dimensions, aspect ratio, file size)

---

## File Impact

| File | Action |
|------|--------|
| `theme_matugen/theme_ctl.sh` | Add hook runner (~3 lines) |
| `~/.config/dusky/theme-hooks.d/` | Create dir + starter hooks |
| `~/.config/theme-selector/config` | **New** — user config |
| `~/.config/theme-selector/favorites` | **New** — favorites list |
| `theme-selector/theme-selector.sh` | **New unified script** (replaces v1 and v2) |
| `theme-selector/theme-selector-v2.sh` | Delete (merged) |
| `theme-selector/theme-selector.sh` | Delete (old v1, replaced) |
| `theme-selector/README.md` | Update |
| `~/Pictures/themes/HYDE-BRIDGE-ANALYSIS.md` | Update status |

---

## What NOT to do (merge scope)

- Don't add view modes (grid/list/compact) — that's v2
- Don't add favorites — `theme_favorites_ctl.sh` exists, wire it up later
- Don't add theme info panel — reads cluster data, ship merge first
- Don't add animations — polish, not priority
- Don't add search by color — reads cluster_v2.json, ship merge first
- Don't touch `cluster_v2.py` or `extract_and_cluster.py` — clustering is done
- Don't touch matugen templates — 52 templates are already working
- Don't add per-theme metadata — that's a separate project
- Don't rewrite `theme_ctl.sh` — hooks are the only addition
- Don't use `gsettings` as the only mode source — fall back to `state.conf`
- Don't block the apply on slow hooks — background them if needed
