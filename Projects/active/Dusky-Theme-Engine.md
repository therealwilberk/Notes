---
tags:
  - project
  - desktop
  - theming
  - dusky
aliases:
  - "Dusky Themes"
  - "Theme Engine"
status: planning
created: 2026-05-23
---

# Dusky Theme Engine

> Wallpaper-driven, mood-based theming for Dusky Linux. Matugen extracts colors, wallpapers get clustered by color profile, themes auto-generate. Flow with moods, not configs.

## The Idea

You have 1500+ wallpapers. They're ungrouped. You want to look at a wallpaper and have your entire desktop match its vibe — terminal, waybar, hyprland borders, notifications, everything.

Instead of manually picking colors, matugen does the heavy lifting: it reads the wallpaper, extracts a Material You color scheme, and the system applies it everywhere.

**The flow:**
1. Scan wallpaper dir → matugen extracts colors → cluster by similarity
2. Each cluster = a "theme" (warm-amber, cool-blue, dark-gotham, etc.)
3. Switch theme → wallpaper changes (stays in cluster) + all configs update
4. New wallpaper added → auto-classified into nearest cluster

## Architecture

```
~/.config/dusky/
├── themes/                    # Generated theme directories
│   ├── warm-amber/
│   │   ├── colors.toml        # Matugen-generated color definitions
│   │   ├── wallpapers/        # Symlinks to original files
│   │   │   ├── sunset-01.jpg
│   │   │   └── desert-03.jpg
│   │   └── preview.jpg        # Random pick from wallpapers/
│   ├── cool-blue/
│   │   ├── colors.toml
│   │   ├── wallpapers/
│   │   └── preview.jpg
│   └── dark-gotham/
│       ├── colors.toml
│       ├── wallpapers/
│       └── preview.jpg
├── templates/                 # Config templates with {{ variable }} placeholders
│   ├── waybar.css.tpl
│   ├── foot.ini.tpl
│   ├── hyprland.conf.tpl
│   ├── mako.ini.tpl
│   ├── hyprlock.conf.tpl
│   └── ...
├── current/                   # Active theme state
│   ├── theme.name             # "warm-amber"
│   ├── colors.toml            # Current colors
│   └── wallpaper.jpg          # Current wallpaper
└── scripts/                   # CLI tools
    ├── dusky-theme-scan
    ├── dusky-theme-set
    ├── dusky-theme-switcher
    └── dusky-theme-next
```

## Modules

### Module 1: Wallpaper Classifier
**Goal:** Scan wallpaper directory, extract color profiles, cluster by similarity.

**Input:** `~/Pictures/Wallpapers/` (1500+ images)
**Output:** `~/.config/dusky/themes/*/` with `colors.toml` + wallpaper symlinks

**How it works:**
1. For each wallpaper, run `matugen image <path>` to extract dominant colors
2. Extract the key colors: primary, secondary, tertiary, surface, background
3. Convert to a color space suitable for clustering (LAB or HSL)
4. Run k-means or DBSCAN clustering on the color vectors
5. Assign each wallpaper to its nearest cluster
6. Generate `colors.toml` per cluster (average/median colors)
7. Create wallpaper symlinks in cluster directories

**Tech:** Python (scikit-learn for clustering, Pillow for image ops, subprocess for matugen)

**Key decisions:**
- How many clusters? Auto-detect (silhouette score) or user-specified (8-12 is a good start)
- Cluster naming: auto-generate from dominant color (warm-amber, cool-blue) or user-defined
- Symlinks vs copies: symlinks save space, copies are portable

---

### Module 2: Template Engine
**Goal:** Generate config files from `colors.toml` + template files.

**Input:** `colors.toml` + `~/.config/dusky/templates/*.tpl`
**Output:** Themed config files in their target locations

**How it works:**
1. Parse `colors.toml` into key-value pairs
2. For each template, replace `{{ variable }}` with color values
3. Also support `{{ variable_strip }}` (without `#` prefix) and `{{ variable_rgb }}` (comma-separated RGB)
4. Write output to target locations (waybar, foot, hyprland, mako, etc.)

**Template variables:**
- `{{ accent }}` — primary accent color
- `{{ background }}` — main background
- `{{ foreground }}` — main text color
- `{{ cursor }}` — cursor color
- `{{ selection_background }}` / `{{ selection_foreground }}`
- `{{ color0 }}` through `{{ color15 }}` — terminal palette
- `{{ _strip }}` suffix — hex without `#`
- `{{ _rgb }}` suffix — `R,G,B` format

**Tech:** Bash (sed-based, same approach as Omarchy)

---

### Module 3: Theme Switcher
**Goal:** UI for browsing and selecting themes.

**Input:** `~/.config/dusky/themes/*/`
**Output:** Selected theme applied to system

**Two versions:**
1. **CLI/fzf** — terminal-based, shows theme names + color preview
2. **rofi/wofi** — graphical, shows wallpaper previews

**Features:**
- Show theme preview (random wallpaper from cluster)
- Show color palette strip below preview
- Keyboard navigation (j/k or arrow keys)
- Apply on Enter
- Wallpaper cycling within theme (Super+N or similar)

**Tech:** Bash + fzf (CLI) or Bash + rofi (graphical)

---

### Module 4: Dusky Integration
**Goal:** Apply theme colors to all Dusky components.

**Components to theme:**
- [ ] Waybar (CSS variables)
- [ ] Foot terminal (INI colors)
- [ ] Hyprland (border color, active/inactive)
- [ ] Mako notifications (colors, font)
- [ ] Hyprlock (colors)
- [ ] btop (theme file)
- [ ] Neovim (colorscheme)
- [ ] GTK apps (gtk.css)
- [ ] Cursor theme (optional)

**How it works:**
1. `dusky-theme-set` reads current `colors.toml`
2. Runs template engine on all templates
3. Writes config files to target locations
4. Restarts affected components (waybar, mako, hyprland reload)
5. Sets wallpaper (swaybg or hyprpaper)

---

### Module 5: Auto-Classification Pipeline
**Goal:** New wallpapers automatically get sorted into themes.

**How it works:**
1. Watch `~/Pictures/Wallpapers/` for new files (inotifywait or systemd path unit)
2. On new file, extract colors with matugen
3. Find nearest existing cluster
4. Add symlink to that theme's `wallpapers/` dir
5. If no cluster is close enough, create a new theme or flag for review

**Tech:** Bash + inotifywait, or Python watchdog

---

### Module 6: QuickShell Port (Optional)
**Goal:** Keyboard-first desktop shell, themed via the same `colors.toml`.

**Components:**
- Status bar (replaces waybar)
- App launcher (replaces rofi)
- Notification center
- Calendar popup
- Battery/audio/bluetooth widgets
- Process manager

**Tech:** QML + Qt Quick
**Dependency:** QuickShell runtime

---

## Phases

### Phase 1: Foundation (MVP)
- [ ] Module 1: Basic wallpaper classifier (matugen + simple clustering)
- [ ] Module 2: Template engine (bash, sed-based)
- [ ] Module 4: Apply to waybar + foot + hyprland only
- [ ] Module 3: CLI switcher (fzf)
- **Goal:** Pick a theme, desktop matches the wallpaper vibe

### Phase 2: Polish
- [ ] Module 1: Improve clustering (auto-detect cluster count, better naming)
- [ ] Module 4: Extend to all components (mako, btop, neovim, GTK)
- [ ] Module 3: Rofi switcher with preview images
- [ ] Wallpaper cycling within theme
- **Goal:** Full mood-based theming, smooth switching

### Phase 3: Automation
- [ ] Module 5: Auto-classify new wallpapers
- [ ] Scheduled theme rotation (time-based, random)
- [ ] Theme export/import (share themes)
- **Goal:** Set it and forget it

### Phase 4: QuickShell (Optional)
- [ ] Module 6: Port desktop shell to QuickShell
- [ ] Integrate theme palette into QML components
- [ ] Keyboard-first navigation for everything
- **Goal:** Full TUI desktop, no mouse required

---

## Dependencies

- **matugen** — Material You color generation from images (already on system)
- **Python 3** — clustering, image processing
- **scikit-learn** — k-means/DBSCAN clustering
- **Pillow** — image color extraction (fallback if matugen is slow)
- **fzf** — CLI theme switcher
- **rofi** — graphical theme switcher (optional)
- **swaybg** or **hyprpaper** — wallpaper setting
- **inotifywait** — file watching for auto-classification (optional)

## References

- [Omarchy themes](https://github.com/basecamp/omarchy/tree/dev/themes) — reference structure
- [Omarchy theme switcher](https://github.com/basecamp/omarchy/blob/dev/bin/omarchy-theme-switcher) — UI reference
- [matugen](https://github.com/InioX/matugen) — color extraction tool
- [Omarchy Hub themes](https://omarchy.deepakness.com/themes) — 69 community themes for inspiration
- [QuickShell](https://github.com/bjarneo/quickshell) — QML desktop shell
- [Batman theme](https://github.com/OldJobobo/omarchy-batman-theme) — example community theme structure

## Notes

- Omarchy themes hardcode configs per theme. Dusky version generates from `colors.toml` via templates — adding a theme is just colors + wallpapers, not 20 config files.
- Wallpaper clustering is the hard part. Everything else is plumbing.
- QuickShell is optional but would solve the "TUI for everything" goal.
- This could be packaged as an AUR tool or standalone git repo.
