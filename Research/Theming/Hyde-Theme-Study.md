---
type: research
tags: [theming, hyprland, rofi, wpick, desktop]
created: 2026-05-25
status: in-progress
parent: "[[Projects/active/Dusky-Theme-Engine/Dusky-Theme-Engine.md]]"
---
# HyDE Theme & Rofi System — Research Report

> Research compiled from HyDE source code analysis. Goal: extract patterns worth adopting for wpick's theme selector.

---

## Overview

HyDE (Hyprland Desktop Environment) is a dotfile framework that turns Hyprland into a fully themed desktop. 812 indexed files. The architecture rests on three pillars:

1. **Theme directories** — each theme is a folder in `~/.config/hyde/themes/<name>/` containing a master config (`hypr.theme`), wallpapers, and optional static component overrides.
2. **Wallbash** — an engine that extracts dominant colors from the active wallpaper via ImageMagick and generates theme files for rofi, kitty, waybar, GTK, Qt, and more.
3. **Rofi** — the universal UI layer. Not just an app launcher: it's the selector for themes, wallpapers, styles, animations, clipboard, bookmarks, web search, emojis, and games.

Entry points are wired to keybindings (`Super+Shift+T` for theme selector, `Super+Shift+W` for wallpaper, etc.) and dispatched through `hyde-shell`, a unified script runner.

---

## Theme System

### Theme Definition Format

Each theme lives in `~/.config/hyde/themes/<ThemeName>/`:

```
~/.config/hyde/themes/Catppuccin Mocha/
├── hypr.theme              # Master config: all theme variables + hyprland overrides
├── wall.set                # Symlink → current wallpaper file
├── wallpapers/             # Available wallpapers for this theme
├── logo/                   # Theme logo (optional, used in rofi)
├── .sort                   # Numeric sort order (optional, default "0")
└── kitty.theme             # Static kitty theme (optional)
```

`hypr.theme` is a hybrid file: shell variables at the top, Hyprland config sections below:

```bash
# Output target + optional post-update command
$HOME/.config/hypr/themes/theme.conf|> $HOME/.config/hypr/themes/colors.conf

# Theme variables
$GTK_THEME=Catppuccin-Mocha
$ICON_THEME = Tela-circle-dracula
$COLOR_SCHEME = prefer-dark
$CURSOR_THEME = Bibata-Modern-Ice
$FONT = Cantarell
$MONOSPACE_FONT = CaskaydiaCove Nerd Font Mono

# Hyprland config sections
general {
    gaps_in = 3
    gaps_out = 8
    border_size = 2
    col.active_border = rgba(ca9ee6ff) rgba(f2d5cfff) 45deg
    col.inactive_border = rgba(b4befecc) rgba(6c7086cc) 45deg
}
```

Recognized variables: `$GTK_THEME`, `$ICON_THEME`, `$CURSOR_THEME`, `$CURSOR_SIZE`, `$FONT`, `$FONT_SIZE`, `$FONT_STYLE`, `$DOCUMENT_FONT`, `$MONOSPACE_FONT` and their size variants.

Themes come from three sources:
- **Bundled** — 12 official themes in `themepatcher.lst`, each a branch on `HyDE-Project/hyde-themes`
- **Gallery** — `theme.import.py` clones `hyde-gallery.git`, shows fzf multi-select with previews
- **Manual** — drop a directory into `~/.config/hyde/themes/`

### Theme Selector Mechanism

**Flow:** `Super+Shift+T` → `hyde-shell themeselect` → `themeselect.sh` → `theme.select.sh`

The selector generates a rofi grid with thumbnail entries:
```bash
${thmList[$i]}\x00icon\x1f$thmbDir/$(set_hash "${thmWall[$i]}").${thmbExtn}
```

Two layout styles:]
- **Square (default):** Large 500×500 thumbnails, text hidden, 23em icon size
- **Quad:** Smaller triangular-cropped thumbnails, 20em icon size

Column count is dynamically calculated from monitor resolution (capped at 5):
```bash
col_count=$((max_avail / elm_width))
[[ $col_count -gt 5 ]] && col_count=5
```

Theme discovery (`get_themes()` in `globalcontrol.sh`) scans `~/.config/hyde/themes/`, reads `wall.set` symlinks, auto-fixes broken symlinks, and sorts by `.sort` file then alphabetically.

### Application Flow

`theme.switch.sh` is the core engine. Called with `-s <name>` (specific), `-n` (next), or `-p` (previous):

1. **Validate** — verify theme exists, fall back to current if not
2. **State update** — write to `staterc`, re-source `globalcontrol.sh` and `env-theme`
3. **Hyprland config** — disable autoreload, sanitize `hypr.theme` (strip `exec`, shadow directives), write to `theme.conf`
4. **GTK** — update gtk-2.0/3.0/4.0 (symlink for 4.0, fallback to Wallbash-Gtk)
5. **Qt** — update qt5ct.conf, qt6ct.conf, kdeglobals
6. **Cursor/Icons** — update Xresources, Xdefaults, dconf, xsettingsd
7. **Wallpaper** — trigger `wallpaper.sh`, which runs the full wallbash color pipeline

Sanitization strips `exec` commands and deprecated shadow settings from `hypr.theme` before writing to `theme.conf`. Variables that `exec` would have set are instead extracted directly by `load_hypr_variables()`.

### Component Integration

| Component   | Config Target                                    | Update Method                     |
| ----------- | ------------------------------------------------ | --------------------------------- |
| Hyprland    | `~/.config/hypr/themes/theme.conf`               | Sanitized write from `hypr.theme` |
| GTK 2.0/3.0 | `~/.gtkrc-2.0`, `~/.config/gtk-3.0/settings.ini` | sed / toml_write                  |
| GTK 4.0     | `~/.config/gtk-4.0/`                             | Symlink to theme dir              |
| Qt5/Qt6     | `qt5ct.conf` / `qt6ct.conf`                      | toml_write                        |
| Icons       | dconf + XDG default                              | dconf write                       |
| Cursor      | Xresources, Xdefaults                            | sed                               |
| Kitty       | `~/.config/kitty/theme.conf`                     | Wallbash template or static file  |
| Rofi        | `~/.config/rofi/theme.rasi`                      | Wallbash template or static file  |
| Waybar      | waybar CSS                                       | Wallbash template or static file  |
| Wallpaper   | Backend-specific                                 | wallpaper.sh dispatches           |

**No rollback mechanism.** Theme application is one-way: `staterc` is updated immediately, config files are overwritten in-place, GTK4 symlinks are destructive (`rm -rf` + `ln -s`). A failed mid-switch leaves a partially themed state. Only recovery: switch again.

---

## Rofi System

### Config Structure

Three layers:

**Layer 1: Global Colors** (`~/.config/rofi/theme.rasi`)
```css
* {
    main-bg:            #11111be6;
    main-fg:            #cdd6f4ff;
    main-br:            #cba6f7ff;
    main-ex:            #f5e0dcff;
    select-bg:          #b4befeff;
    select-fg:          #11111bff;
    separatorcolor:     transparent;
    border-color:       transparent;
}
```
6 semantic color variables. All `.rasi` themes import this via `@theme`. This file is dynamically regenerated by wallbash on every wallpaper change.

**Layer 2: Style Themes** (`~/.local/share/hyde/rofi/themes/*.rasi`)
24 theme files for different use cases. Each is a complete rofi theme that imports `theme.rasi` for colors.

| File | Purpose |
|------|---------|
| `selector.rasi` | Grid selector (themes, wallpapers, styles) — icon-only, 10 columns |
| `style_1.rasi` through `style_12.rasi` | 12 launcher styles (sidebar list, grid, centered, etc.) |
| `clipboard.rasi` | Clipboard manager with wallpaper thumbnail header |
| `launchpad.rasi` | Fullscreen app grid, 7 columns, blurred wallpaper bg |
| `quickapps.rasi` | Horizontal icon dock |
| `notification.rasi` | Notification center |
| `wallbash.rasi` | Wallbash mode selector |
| `gamelauncher_1-5.rasi` | Game launcher variants |

Launcher styles are discovered by grepping `.rasi` files for `Attr.*launcher.*` in comments.

**Layer 3: Assets** (`~/.local/share/hyde/rofi/assets/*.png`)
Preview images for grid selectors: launcher style previews, theme style previews, specialized backgrounds.

### Launchers & Menus

**App Launcher** (`rofilaunch.sh`) — 4 modes: drun, window, filebrowser, run. Style resolution chain:
```
ROFI_LAUNCH_{MODE}_STYLE > ROFI_LAUNCH_STYLE > rofiStyle (staterc) > "style_1"
```
Dynamic sizing from Hyprland border settings. Fullscreen state tracked per mode. Toggle behavior: kills rofi if already running.

**Theme Selector** (`theme.select.sh`) — Rofi grid of theme thumbnails. Two layout modes (square/quad). Submenu for picking the selector layout itself.

**Style Selector** (`rofiselect.sh`) — Grid of available launcher styles. Discovers styles dynamically.

**Wallpaper Selector** (`wallpaper/select.sh`) — Rofi grid of wallpaper thumbnails with JSON metadata.

**Wallbash Mode Selector** (`wallbashtoggle.sh`) — 4 modes: theme, auto, dark, light. Uses `wallbash.rasi` with background asset.

**Clipboard Manager** (`cliphist.sh`) — Cursor-position-aware placement, custom keybindings (Alt+c/d/n/w), favorites, pin/unpin.

**Web Search** (`rofi.websearch.sh`) — Two-stage: engine selection (3-column grid), then query input with recent history.

**Others** — Emoji picker, bookmarks, keybinds hint, animations, quick apps, calculator, game launcher.

### Theme Integration

Rofi follows the theme through wallbash:

```
Wallpaper changes
  → wallbash.sh extracts 4 dominant colors (ImageMagick kmeans)
  → Generates .dcol file with hex color variables
  → rofi.dcol template → ~/.config/rofi/theme.rasi
```

The `rofi.dcol` template maps wallpaper colors to the 6 semantic variables:
```css
$HOME/.config/rofi/theme.rasi
* {
    main-bg:            #<wallbash_pry1>B3;
    main-fg:            #<wallbash_1xa9>E6;
    main-br:            #<wallbash_pry3>E6;
    main-ex:            #<wallbash_pry2>E6;
    select-bg:          #<wallbash_4xa8>80;
    select-fg:          #<wallbash_4xa1>E6;
}
```

Suffixes (`B3`, `E6`, `80`) are alpha values. Rofi reads `theme.rasi` at launch time, so it never needs restarting — the next launch picks up new colors automatically.

**Dynamic overrides:** Every script injects `-theme-str` overrides at launch for font, borders, icon theme, and cursor position. These don't modify the `.rasi` files.

**Config variable pattern per script:** Each rofi-using script has `ROFI_*_SCALE`, `ROFI_*_FONT`, `ROFI_*_STYLE` variables, all following the same resolution chain with shared defaults.

---

## Key Takeaways for wpick

### What's worth adopting

1. **Directory-per-theme structure.** `~/.config/hyde/themes/<name>/` is clean and extensible. The `wall.set` symlink as "current wallpaper" is elegant — one readlink to get the active state. wpick should adopt this: each theme folder with a master config, wallpapers dir, and a symlink pointing to the active wallpaper.

2. **The `.sort` file for ordering.** A single numeric file in each theme directory controls sort order. Dead simple, no registry needed. wpick can use this to let users control grid order without a database.

3. **6 semantic color variables.** `main-bg`, `main-fg`, `main-br`, `main-ex`, `select-bg`, `select-fg` is the right abstraction level. Enough for full theming, few enough to manage. wpick's theme format should define exactly these semantic slots.

4. **Wallbash-style color extraction from wallpapers.** Extracting 4 dominant colors via ImageMagick kmeans, generating accent shades via HSB curves, and auto-detecting dark/light mode is a proven pipeline. wpick should replicate this approach rather than inventing its own.

5. **`.dcol` template format.** Two-line files: target path + template with placeholders. Brutally simple to parse and apply. wpick's template system should be this minimal.

6. **Dynamic `-theme-str` overrides.** Never modify the source `.rasi` files; inject overrides at launch. This keeps themes immutable and the runtime flexible. wpick's UI layer should do the same.

7. **Monitor-aware grid sizing.** Calculating column count from monitor resolution with a cap is smart. wpick should do this for its theme/wallpaper grids.

### What's overengineered (avoid)

1. **The state file fragmentation.** `staterc` + `env-theme` + `config.toml` + `theme-env` (legacy duplicate) is too many sources of truth. wpick should have ONE config file for runtime state and ONE for defaults. No legacy duplicates.

2. **No rollback mechanism.** Theme application is destructive with no backup. wpick should snapshot the previous state before applying a new theme. Even a simple "last known good" symlink would help.

3. **GTK4 symlink dance.** `rm -rf` + `ln -s` for GTK4 theming is fragile. wpick should use a safer approach (rename-then-link, or config file references).

4. **Concurrent access with no locking.** `staterc` is modified via `sed -i` (not atomic). Two simultaneous switches corrupt the file. wpick needs either a lock file or atomic writes.

5. **24 rofi theme files.** Having 12 launcher styles + specialized themes for every use case is maintenance debt. wpick should have 2-3 well-designed layout templates, not 24.

6. **`hypr.theme` hybrid format.** Mixing shell variables and Hyprland config sections in one file is clever but fragile. wpick should use a clean data format (TOML or YAML) with explicit sections.

7. **The `hyq` dependency.** A custom Hyprland config parser with grep fallback adds complexity. wpick should use a standard config parser from the start.

### Patterns for wpick's theme selector specifically

- **Grid of thumbnails with hashed filenames.** SHA1 of wallpaper path as cache key is good. Avoids filename collisions.
- **Two layout modes (square/quad) is enough.** Don't need 12 launcher styles. Pick one excellent default, offer one alternative.
- **Style discovery via metadata comments** (`Attribute: rofilaunch,launcher`) is fragile. wpick should use a proper metadata field in its config format.
- **Column count cap at 5.** Good default. Too many columns makes thumbnails useless.
- **Toggle behavior** (kill rofi if already running) is a nice UX detail. wpick's selector should do the same.

---

## File Reference

| Path | Purpose |
|------|---------|
| `Configs/.local/lib/hyde/theme.switch.sh` | Core theme application engine |
| `Configs/.local/lib/hyde/theme.select.sh` | Rofi theme grid selector |
| `Configs/.local/lib/hyde/themeselect.sh` | Shim → theme.select.sh |
| `Configs/.local/lib/hyde/globalcontrol.sh` | Shared functions, paths, env vars, `get_themes()` |
| `Configs/.local/lib/hyde/wallbash.sh` | Color extraction from wallpaper (ImageMagick) |
| `Configs/.local/lib/hyde/wallpaper.sh` | Wallpaper management + backend dispatch |
| `Configs/.local/lib/hyde/wallpaper/cache.sh` | Thumbnail + dcol cache generation |
| `Configs/.local/lib/hyde/wallbashtoggle.sh` | Wallbash mode selector (theme/auto/dark/light) |
| `Configs/.local/lib/hyde/rofilaunch.sh` | Main app launcher (drun/window/filebrowser/run) |
| `Configs/.local/lib/hyde/rofiselect.sh` | Rofi launcher style selector |
| `Configs/.local/lib/hyde/wallpaper/select.sh` | Wallpaper selector grid |
| `Configs/.local/lib/hyde/cliphist.sh` | Clipboard manager |
| `Configs/.local/lib/hyde/rofi.websearch.sh` | Multi-engine web search |
| `Configs/.local/lib/hyde/theme.import.py` | Gallery theme browser (fzf + git) |
| `Configs/.local/lib/hyde/theme.patch.sh` | Theme installer (git → extract → apply) |
| `Configs/.local/lib/hyde/pyutils/wrapper/rofi.py` | Python rofi wrapper (dmenu + modi) |
| `Configs/.config/rofi/theme.rasi` | Global rofi color variables (wallbash target) |
| `Configs/.local/share/hyde/rofi/themes/*.rasi` | 24 rofi style themes |
| `Configs/.local/share/wallbash/theme/rofi.dcol` | Wallbash → rofi color template |
| `Configs/.local/share/hyde/env-theme` | Default variable baseline |
| `~/.local/state/hyde/staterc` | Runtime state (HYDE_THEME, enableWallDcol, rofiStyle) |
| `~/.config/hypr/themes/theme.conf` | Active Hyprland theme (auto-generated) |
| `Scripts/themepatcher.lst` | Official theme URLs (12 entries) |
| `Configs/.local/bin/hyde-shell` | Unified script dispatcher |
