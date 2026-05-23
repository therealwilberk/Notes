---
tags: [project, research, matugen, theming]
parent: "[[Dusky-Theme-Engine]]"
status: complete
---

# Research: Existing matugen/theme solutions

> Parent project: [[Dusky-Theme-Engine]]

## 1. matugen Integrations

**matugen** (InioX/matugen) is a Rust-based Material You and base16 color generation tool (1.5k+ stars, GPL-2.0). It extracts colors from images or accepts direct color input, outputs Material You / base16 palettes, and has a built-in templating engine (Chumsky-based). Latest: v4.1.0 (March 2026). Available on Linux, Windows, macOS, NetBSD.

Key repos:
- **InioX/matugen** — core tool (Rust). Generates palettes, custom keywords, template rendering, wallpaper setting hooks. `cargo install matugen` or AUR: `matugen` / `matugen-git`.
- **InioX/matugen-themes** — community templates repo with 50+ app templates (Waybar, Kitty, Hyprland, Rofi, Neovim, GTK, SwayNC, etc.) and website themes (YouTube, Bitwarden, GitHub via Firefox UserContent.css).
- **KAGEYAM4/matugen-themes**, **Senal-D-A-Gunaratna/matugen-themes**, **zydezu/matugen-themes** — active forks adding more templates.

Tools that use matugen:
- **vsHypr Theme Manager** — Python-based full Hyprland theme system. Uses matugen for `dynamic-dark` / `dynamic-light` themes. Applies to Kitty, Waybar, SwayNC, Hyprland, Hyprlock, Rofi, EWW, Wlogout, GTK3/4, Qt5/6, Kvantum. Features Rofi picker with wallpaper thumbnails and color preview.
- **Matuwall** — GTK4/libadwaita wallpaper picker for Wayland. Triggers matugen on wallpaper change. Supports all matugen scheme types. Optional wall-only mode via `awww`.
- **anand-dots** — production-grade Hyprland dotfiles with matugen. Settings GUI (GTK4/libadwaita), 9 scheme styles, auto low-saturation detection.
- **ekremx25/quickshell** — Quickshell desktop shell with matugen theming.

## 2. Wallpaper-Based Theming Tools

### pywal (dylanaraps/pywal)
- 9k+ stars. Python. The original wallpaper-to-theme tool.
- Extracts 16-color terminal palettes from images.
- Exports to: CSS, SCSS, JSON, YAML, shell variables.
- Supports: i3, sway, polybar, dunst, and any app via `-o script` hook.
- Backends: multiple color extraction algorithms.
- **Status**: No longer actively maintained (last release 2020). Community has forked to **pywal16** (maintained fork with 16-color + terminal sequences fix).

### wpgtk (deviantfero/wpgtk)
- Python/GTK. Uses pywal as backend, adds GUI, template system, color editing, wallpaper-color pairing.
- Features: auto color-scheme sorting, saturation/brightness adjustment, dark/light theme variants, JSON import/export, preset themes.
- CLI (`wpg`) and GUI (`wpgtk`).
- **Status**: Active. v6.7.0 on PyPI. Adds template system on top of pywal.

### wallust
- Rust. pywal-compatible color generation. Used by **WaybarDynamicTheme**.
- Multiple backends, color spaces (labmixed), dark16 palette.
- Template-driven export per-app.

### Others:
- **themer** (Python) — Jinja2 + YAML config templater, theme directories, plugin-based color parsers.
- **tinct** (Rust) — Plugin-based theme/templating tool inspired by pywal and matugen. Multiple input sources (images, AI, remote themes, manual). 25+ apps. Smart WCAG contrast checking.

## 3. Color Clustering Tools

| Tool                           | Language  | Algorithm                  | Features                                                                                               |
| ------------------------------ | --------- | -------------------------- | ------------------------------------------------------------------------------------------------------ |
| **auto-palette** (t28hub)      | Rust      | DBSCAN, KMeans, SLIC, SNIC | Wasm + CLI. Theme-based swatch selection (Colorful, Vivid, Muted, Light, Dark). Multiple color spaces. |
| **huex** (khzaw)               | Rust      | k-means++ in Oklab         | JSON output, SVG swatches, color harmonies, Delta-E merge, stdin support.                              |
| **Okolors** (IanManske)        | Rust      | k-means in Oklab           | Multi-lightness output, SIMD via quantette, fast. Inspired by kmeans-colors.                           |
| **swatchify** (james-see)      | Go        | k-means++                  | CLI + REST API + JS. PNG palette output, white/black exclusion, quality control.                       |
| **pigmnts** (blenderskool)     | Rust/Wasm | k-means++                  | Web + CLI. Multiple output formats, fast Wasm extraction.                                              |
| **dominant-colours** (llaisdy) | Rust      | k-means (linfa)            | SVG swatches, percentage reports, simple CLI.                                                          |
| **MareArts Xcolor**            | Python    | KMeans, DBSCAN             | GPU acceleration, LAB space, CLAHE preprocessing, mask support.                                        |

All these can cluster images by dominant color for grouping. **auto-palette** and **huex** are the most feature-complete for a theme engine use case.

## 4. Theme Managers for Wayland/Hyprland

| Tool                             | Language    | Features                                                                                                                 |
| -------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------ |
| **vsHypr Theme Manager**         | Python      | Full Hyprland theme system. Rofi picker, matugen dynamic themes, 15 app types, GTK/Qt support, wallpaper engine.         |
| **theme-switcher** (enes-less)   | Bash        | Template-based, JSON color palettes, swww, jq. 8 apps supported.                                                         |
| **WallTheme** (gb8462)           | Bash        | Lightweight, CLI menu, auto wallpaper sync.                                                                              |
| **theme-switcher** (StephenGunn) | Bash        | Pre-built palettes only (Gruvbox, Catppuccin, etc.), no image generation. pywal as fallback for some apps.               |
| **WaybarDynamicTheme**           | Bash        | Single-script hub. Uses wallust. Full system sync (Hyprland, Waybar, GTK, Kitty, SwayNC, Cava). Visual wallpaper picker. |
| **hypr-bg-manager**              | Bash        | Wallpaper manager with per-workspace/global/timer modes. Multiple backends (swww, hyprpaper, swaybg, mpvpaper).          |
| **anand-dots**                   | Bash/Python | Mature Hyprland config with matugen. Settings GUI, 9 scheme styles, auto low-saturation detection.                       |

**Key observation**: Most existing solutions are opinionated dotfile repos, not reusable theme engines. vsHypr Theme Manager is the closest to a standalone reusable tool, but it's still tied to a specific config layout.

## 5. Speed Considerations (bash vs python vs rust)

- **Rust**: 10-100x faster than Python for image processing. Example: dominant_colours blog post explicitly switched from Python to Rust for speed. Cross-language benchmarks show Rust pixel ops ~7x faster than Python+PIL, ~100x+ faster than pure Python loops. `matugen`, `auto-palette`, `huex`, `Okolors` all in Rust.
- **Python**: Good for glue/prototyping. pywal, wpgtk, vsHypr all Python. For 1500+ images, Python clustering with numpy/scikit-learn works but is slower than Rust. GPU acceleration possible (MareArts Xcolor).
- **Bash**: Fast for orchestration (subprocess calls). A Python script rewritten as Bash one-liner went from 30s to 1s. But limited for actual image processing.

**Recommendation for 1500+ images**: Use Rust for color extraction (matugen or auto-palette) with a thin Python or Bash orchestration layer. Rust CLI tools process an image in ~0.3s (auto-palette benchmark), so 1500 images ≈ 7.5 minutes sequential, easily parallelized.

## 6. Template Engines

| Engine | Used By | Features |
|--------|---------|----------|
| **matugen templates** (Chumsky) | matugen | Built-in, custom keywords, color manipulation filters, multi-format output. |
| **Jinja2** | zenbu, themer, Ansible, dotfiles-jinja2 | Full logic (if/else, loops, macros), filters, template inheritance. Python. |
| **Mustache** | whizkers (deprecated) | Logic-less, portable across languages. |
| **sed** | ad-hoc scripts | Simple variable replacement, regex. Doesn't scale. |
| **envsubst** | CI/CD | POSIX shell variables, simple. |
| **Go templates** | Helm | Conditionals, loops. Go ecosystem. |

**matugen's built-in template engine is already sufficient** for most theming needs. For complex logic, Jinja2 is the most mature option (used by themer, zenbu). The vsHypr approach of injecting colors via CSS custom properties and marker blocks is simpler and works without a template engine.

## 7. QuickShell Themes

QuickShell (QML/QtQuick desktop shell framework) has growing theme support:

- **ulises-jeremias/dotfiles** — Material Design 3 theming via `python-materialyoucolor`. Watches `scheme.json`, auto-reloads Quickshell colors. SCHEME_TYPE config (vibrant, tonalSpot, etc.).
- **BitProtector/quickshell** — pywal integration, reads `~/.cache/wal/colors.json`.
- **doannc2212/quickshell-config** — 206 themes across 6 families (Tokyo Night, Catppuccin, Zen, Arc, Beared, MonkeyType). Theme switcher overlay, persists across restarts, syncs with kitty.
- **ekremx25/quickshell** — matugen color extraction for auto-theming.
- **daltonkyemiller/shell** — configurable Theme.qml, color properties.

QuickShell's theme story is fragmented but growing. There's no dominant standard — each config rolls its own. The doannc2212 theme switcher is the most comprehensive (206 themes).

## Comparison Matrix

| Feature | pywal | wpgtk | matugen | vsHypr | Build from scratch? |
|---------|-------|-------|---------|--------|---------------------|
| Color extraction | Yes | Yes (via pywal) | Yes (Material You) | Yes (via matugen) | Reuse |
| Template engine | Simple ($var) | Template system | Chumsky engine | CSS injection | Reuse matugen |
| GTK theming | No (removed) | Built-in GTK theme | Via templates | Full GTK3/4 | Use vsHypr approach |
| GUI | No | GTK GUI | No | GTK GUI + Rofi | Optional |
| Active maintenance | No (pywal16 fork) | Yes | Yes (v4.1.0) | Yes | N/A |
| Speed | Python | Python | Rust (fastest) | Python | Rust for core |
| Image grouping | No | No | No | No | **Needs building** |
| Desktop-agnostic | Kinda | Kinda | Yes | Hyprland-specific | **Needs building** |

## Recommendation

**Don't build from scratch.** The ecosystem has most pieces:

1. **Use matugen as the color engine** — it's the most modern, well-maintained, and has a built-in template engine. Rust = fast.
2. **Fork/extend vsHypr Theme Manager's approach** for app-specific theming (CSS injection + marker blocks + template rendering).
3. **Build the clustering piece** — no existing tool groups images by color similarity for theme assignment. This is the main gap.
4. **Use auto-palette or huex** if you need standalone color extraction outside of matugen.
5. **QuickShell theming** — follow the doannc2212/ulises-jeremias pattern: QML color properties, Material You pipeline, file-watch for auto-reload.

**Key gaps to fill:**
- Color-based image clustering/grouping
- Desktop-agnostic theme manager (not tied to specific dotfiles)
- Unified template repository spanning all app types
- Batch processing for 1500+ images with parallel color extraction
