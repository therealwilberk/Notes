# Theme Selector v2 — Architecture

## 1. Selector Flow

```
Open selector (uwsm-app -- rofi)
  │
  ├─ 1. Auto-detect system mode (gsettings)
  │
  ├─ 2. Theme grid rofi (first invocation)
  │     Grid of theme thumbnails + name + wallpaper count
  │     Alt+M      — toggle dark/light mode (reloads grid)
  │     Alt+R      — pick random theme, apply random wallpaper
  │     Enter      — go to wallpaper grid for selected theme
  │     Enter (no sel) — nothing (filter is for searching)
  │     Esc        — exit
  │
  ├─ 3. Wallpaper grid rofi (second invocation)
  │     Thumbnail grid of wallpapers for selected theme
  │     Enter      — apply selected wallpaper
  │     Alt+R      — apply random wallpaper from this theme
  │     Esc        — back to theme grid
  │
  └─ 4. Async apply (background subshell)
        notify-send "Applying: ThemeName"
        bash theme_ctl.sh theme set --mode <M> <Theme> <Wallpaper>
        notify-send "Theme applied"
```

### Key difference from v1
No mode picker stage. Mode is auto-detected. The Alt+M hotkey lets the user override without a separate rofi screen. Max 2 rofi invocations instead of 3.

---

## 2. Mode Detection

### Primary: gsettings
```bash
gsettings get org.gnome.desktop.interface color-scheme
# Returns 'prefer-dark' or 'prefer-light'
```
Mapped: `prefer-dark` → `dark`, `prefer-light` → `light`.

### Fallback: state.conf
If gsettings call fails (no display / wayland not ready), fall back to `THEME_MODE` from `state.conf`.

### Mode override
- Alt+M toggles to opposite mode
- Toggled mode is ephemeral (not written to state.conf unless user applies a theme)
- When theme is applied, the mode in the apply call overrides state.conf

### Preview on toggle
When Alt+M is pressed, before reloading the grid:
1. Show a notification with the preview composite image: `notify-send -i <preview-file> "Switched to Light mode"`
2. Then immediately launch the theme grid for the new mode

---

## 3. Preview System

### Purpose
Give visual context when toggling dark/light mode — a quick glance at what themes look like in that mode.

### Generation
```bash
# Collect up to 6 theme thumbnails for each mode
# Stitch into a 2x3 grid
magick montage thumb1 thumb2 thumb3 thumb4 thumb5 thumb6 \
  -geometry 300x300+10+10 \
  /tmp/theme-selector-arch/preview-dark.png
```

### Storage
- `~/.cache/theme-selector/dark-preview.png`
- `~/.cache/theme-selector/light-preview.png`

### Invalidation
Check mtimes of theme directories vs the preview file. Regenerate when:
- Preview file doesn't exist
- Any theme directory in that mode is newer than the preview

### Display
When Alt+M is pressed:
```bash
notify-send -i "$preview_file" -a "Theme Selector" "Mode: ${mode^}"
```
This shows the composite as a notification image — quick visual feedback without blocking.

---

## 4. Cache Strategy

### Thumbnail cache (already exists)
- `~/.cache/rofi-wallpaper-thumbs/theme-selector-300/thumbs/`
- 300x300 thumbnails, hashed by wallpaper path (sha256)
- Generated on-demand with ImageMagick
- Already populated from v1 usage

### Theme thumbnails (new)
- `~/.cache/theme-selector/theme-thumbs/{mode}/{theme}.png`
- Generated from the first wallpaper in each theme
- Invalidated when theme directory mtime changes
- Used in the theme grid

### Preview composites (new)
- `~/.cache/theme-selector/{dark,light}-preview.png`
- 2x3 montage of 6 theme thumbnails
- Invalidated when any theme in that mode changes

### Wallpaper list cache (refined)
- `~/.cache/theme-selector/{mode}-{theme}.list`
- Cached list of wallpaper paths for a theme
- Invalidated when theme directory changes (mtime check)
- Prevents repeated `find` calls when navigating back and forth

### Theme list
- No cache needed. A single `find` pass over `~/Pictures/themes/{mode}/*/` is fast enough.

---

## 5. Rofi Integration

### Theme grid (new usage of existing grid theme)
- Uses `~/.config/rofi/wallpaper-grid.rasi` as base
- Dynamic column count via `-theme-str` (monitor-aware, max 5 columns)
- Each entry: `name\0icon\x1fthumbnail\x1finfo\x1fcount`
- Custom keybindings:
  - `kb-custom-1` = Alt+M (toggle mode)
  - `kb-custom-2` = Alt+R (random theme)

### Wallpaper grid (unchanged from v1)
- Same grid theme, same approach
- Keybindings:
  - `kb-custom-1` = Alt+R (random wallpaper)

### Dynamic overrides
Column count is calculated at runtime:
```bash
read -r x y <<< "$(hyprctl monitors -j | jq -r '.[0].width, .[0].height')"
col_count=$(( (x * 65 / 100) / 340 ))  # 65% window, 340px per column
[[ $col_count -gt 5 ]] && col_count=5
```
Injected via `-theme-str`:
```
listview { columns: $col_count; }
```

### Frosted glass
- Existing `theme-selector.rasi` and `wallpaper-grid.rasi` already implement the frosted glass aesthetic (blur via transparency, sharp corners, 1px borders, 14px gaps)
- No changes needed to the .rasi files — only dynamic overrides at launch

---

## 6. Script Structure

```bash
theme-selector-v2.sh
├── Paths & constants
├── acquire_lock()        — prevent multiple instances
├── notify()              — notify-send wrapper
├── get_system_mode()     — gsettings → dark/light
├── get_current_theme()   — from state.conf (no subprocess)
├── get_saved_mode()      — from state.conf (fallback)
├── thumbnail helpers
│   ├── thumb_path()      — sha256 hashed path for wallpaper thumb
│   ├── theme_thumb_path() — path for theme thumbnail
│   ├── ensure_theme_thumbnails() — generate theme thumbnails
│   └── ensure_preview_composites() — generate 2x3 montages
├── monitor_columns()     — calculate grid columns from resolution
├── run_rofi()            — generic rofi wrapper
├── show_theme_grid()     — first rofi: theme selection
├── show_wallpaper_grid() — second rofi: wallpaper selection
├── apply_theme()         — async apply (subshell + notify)
├── apply_random_theme()  — pick random theme, apply random wallpaper
└── main()
```

### Function call graph
```
main()
  ├─ acquire_lock()
  ├─ get_system_mode()  → current_mode
  ├─ ensure_preview_composites(current_mode)
  ├─ ensure_theme_thumbnails(current_mode)
  └─ show_theme_grid(current_mode)
       ├─ get_system_mode() (re-read on toggle)
       ├─ run_rofi() (theme grid)
       ├─ Alt+M → show_theme_grid(toggled_mode)
       ├─ Alt+R → apply_random_theme(mode)
       └─ Enter → show_wallpaper_grid(mode, theme)
            ├─ run_rofi() (wallpaper grid)
            ├─ Enter  → apply_theme(mode, theme, wallpaper)
            ├─ Alt+R  → apply_theme(mode, theme, "random")
            └─ Esc    → show_theme_grid(mode) (recurse)
```

---

## 7. Migration Path

### From v1 to v2

| v1 | v2 |
|---|---|
| `theme-selector.sh` | `theme-selector-v2.sh` |
| 3 stages (mode → theme → wallpaper) | 2 stages (theme → wallpaper) |
| Manual mode picker | Auto-detected from gsettings |
| No previews | Cached preview composites on toggle |
| Thumbnail gen on demand | Theme thumbnails pre-generated |
| Lock file | Same lock file |
| Sync apply (rofi waits) | Async apply in background |

### Rollout
1. Install `theme-selector-v2.sh` alongside v1
2. Update keybind to point to v2
3. Keep v1 as fallback for one release cycle
4. After validation, remove v1

### Backward compatibility
- v2 reads the same `state.conf` format
- v2 calls the same `theme_ctl.sh theme set` command
- v2 uses the same thumbnail cache directory
- v2 uses the same theme directory structure
- v2's mode toggle does NOT write to state.conf (mode is ephemeral until apply)
