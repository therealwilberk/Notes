---
type: research
tags: [theming, hyprland, linux, dotfiles, dusky, omarchy]
created: 2026-05-23
status: complete
parent: "[[Projects/active/Dusky-Theme-Engine/Dusky-Theme-Engine.md]]"
---

# Omarchy TUI Config on Dusky Linux — Compatibility Analysis

**Date:** 2026-05-23
**Status:** Research complete, no code changes made
**System:** Arch Linux + Hyprland, running Dusky Linux dotfiles (bare git repo)

---

## TL;DR

Omarchy's **config architecture** is brilliant and worth adopting. Omarchy's **actual config files** are incompatible with Dusky (different format, different tools). The play is to adopt Omarchy's *philosophy* — three-layer config separation, single CLI dispatcher, hook system, update-safe user zones — on top of your existing Dusky setup.

**Verdict: Adopt the architecture, not the configs.**

---

## What You're Running Now (Dusky)

### Config Structure
```
~/.config/hypr/
├── edit_here/              <-- YOUR customizations (user-safe zone)
│   ├── hyprland.lua        <-- main user config (Lua format)
│   └── source/
│       ├── keybinds.lua
│       ├── appearance.lua
│       ├── monitors.lua
│       ├── autostart.lua
│       ├── trackpad.lua
│       ├── input.lua
│       ├── window_rules.lua
│       ├── workspace_rules.lua
│       ├── plugins.lua
│       ├── environment_variables.lua
│       ├── default_apps.lua
│       └── backups/        <-- auto-backups with timestamps
├── source/                 <-- Dusky defaults (overwritten on update)
│   ├── animations/         <-- 12 animation presets (lua)
│   ├── keybinds.lua
│   ├── appearance.lua
│   └── ... (mirrors edit_here structure)
├── shaders/                <-- GLSL shaders (user-safe)
├── hypridle.conf
└── xdph.conf

~/.config/waybar/
├── 01_mechabar_h/          <-- 18 waybar themes (horizontal/vertical)
├── 02_reminiscent_h/
├── ... (numbered theme dirs)
└── 18_notch_2/

~/user_scripts/             <-- TUI tools + scripts (scattered)
├── dusky_tui/              <-- Generic TUI framework (Python + Bash)
│   ├── python/
│   │   ├── main/main.py    <-- Router/dispatcher
│   │   ├── frontend/ui.py  <-- TUI frontend
│   │   └── engines/        <-- Config format parsers
│   │       ├── lua.py      <-- Hyprland Lua engine
│   │       ├── ini.py      <-- INI/config engine
│   │       ├── hyprlang.py <-- Hyprland native format
│   │       ├── systemd.py  <-- systemd unit engine
│   │       ├── cmdline.py  <-- Command-line engine
│   │       ├── monitor_engine.py
│   │       └── trackpad.py
│   └── bash/               <-- Older bash TUI versions
├── dusky_system/
│   └── control_center/     <-- GUI control center (YAML-driven)
│       └── dusky_config.yaml  <-- 3042 lines, defines all GUI pages
├── hypr/
│   ├── visual/tui_appearance.py    <-- Appearance TUI
│   ├── monitor/tui_monitors.py     <-- Monitor config TUI
│   ├── input/tui_trackpad.py       <-- Trackpad TUI
│   ├── input/tui_input.py          <-- Input TUI
│   ├── misc/tui_autostart.py       <-- Autostart TUI
│   └── rules/
│       ├── tui_window_rules_tui.py <-- Window rules TUI
│       └── tui_workspace_rules.py  <-- Workspace rules TUI
├── mako_osd/
│   ├── mako_tui/tui_mako.py        <-- Notification config TUI
│   └── dusky_glance/tui_mako.py    <-- Glance TUI
├── hypridle/tui_dusky_hypridle.py  <-- Idle config TUI
├── services/tui_service_toggle.py  <-- Service toggle TUI
├── theme_matugen/                  <-- Matugen theming
├── arch_setup_scripts/
│   ├── ORCHESTRA.sh                <-- Master installer (~80 subscripts)
│   └── scripts/                    <-- Individual setup scripts
└── ... (many more)
```

### What Dusky Does Well
- **Lua config format** — more powerful than standard Hyprland .conf
- **edit_here/ separation** — user customizations survive upstream updates
- **Auto-backups** with timestamps before any config change
- **Extensive TUI tools** for almost every config surface
- **Matugen theming** — universal light/dark across all apps
- **~900MB RAM, ~5GB disk** — genuinely lightweight
- **ORCHESTRA.sh** — modular, idempotent, re-runnable installer

### What Dusky Doesn't Have
- **No single CLI dispatcher** — TUI tools are scattered across `~/user_scripts/`
- **No hook system** — no automated actions on theme change, update, etc.
- **No config refresh with diff** — updates just `git checkout -f` overwrites
- **No migration system** — breaking changes require manual intervention
- **GUI Control Center** — the `dusky_config.yaml` is GUI-focused (3042 lines)

---

## What Omarchy Does (Architecture Only)

### Three-Layer Config Separation
```
Layer 1: SYSTEM SOURCE (read-only, git-managed, overwritten on update)
~/.local/share/omarchy/
├── bin/          # omarchy-* CLI commands
├── config/       # Default config templates
├── default/      # System defaults
├── themes/       # Stock themes
├── migrations/   # Timestamped migration scripts
└── install/      # Installation scripts

Layer 2: USER CONFIG (update-safe, survives updates)
~/.config/omarchy/
├── current/theme/       # Active theme
├── themes/              # User-created themes
├── backgrounds/         # User backgrounds
├── hooks/               # User hook scripts
│   ├── theme-set.d/     # Run after theme change
│   ├── post-update.d/   # Run after update
│   └── font-set.d/      # Run after font change
└── themed/              # User template overrides

Layer 3: APPLICATION CONFIG (written by refresh utilities)
~/.config/hypr/          # Hyprland config
~/.config/waybar/        # Waybar config
~/.config/tmux/          # Tmux config
~/.config/walker/        # Walker launcher
~/.config/alacritty/     # Terminal config
```

### Single CLI Dispatcher
```bash
omarchy theme set catppuccin    # Theme management
omarchy refresh waybar          # Reset config (backup + diff + copy)
omarchy restart waybar          # Restart service
omarchy toggle nightlight       # Toggle feature
omarchy update                  # System update (Btrfs snapshot + migrations)
omarchy commands                # List all available commands
```

### Config Refresh System
- `omarchy-refresh-config` — generic copier from defaults to `~/.config/`
- Creates **timestamped backup** before overwriting
- Shows **diff** if files differ
- Component-specific: `omarchy-refresh-waybar`, `omarchy-refresh-hyprland`, etc.

### Hook System
```bash
~/.config/omarchy/hooks/
├── theme-set        # Runs after theme change ($1 = theme name)
├── font-set         # Runs after font change
└── post-update      # Runs after omarchy update
```

### TUI Tools (replaces GUIs)
- `lazygit` — Git client
- `lazydocker` — Docker management
- `btop` — System monitor
- `fzf` — Fuzzy finder (used throughout)
- `tmux` — Terminal multiplexer
- `nvim` — Text editor
- `Walker` — App launcher (SUPER+SPACE)
- `omarchy-menu` — Central menu system (SUPER+ALT+SPACE)

---

## Compatibility Analysis

### What's Directly Compatible

| Component | Dusky | Omarchy | Compatible? |
|-----------|-------|---------|-------------|
| Base OS | Arch Linux | Arch Linux | YES |
| WM | Hyprland | Hyprland | YES |
| Status Bar | Waybar | Waybar | YES |
| Theming | Matugen | Matugen | YES |
| Terminal | Kitty/Alacritty | Alacritty/Kitty | YES |
| Notifications | Mako/SwayNC | Mako | YES |
| Shell | Zsh | Bash/Zsh | YES |
| Editor | Neovim | Neovim | YES |
| TUI tools | lazygit, btop, fzf | lazygit, btop, fzf | YES |

### What's Incompatible

| Component | Dusky | Omarchy | Issue |
|-----------|-------|---------|-------|
| Config format | **Lua** (.lua) | **Hyprland native** (.conf) | Different parsers, can't swap |
| Config location | `~/.config/hypr/edit_here/` | `~/.config/hypr/` | Different paths |
| Launcher | **Rofi** | **Walker** | Different tools entirely |
| Update method | `git checkout -f` | `omarchy-update` + migrations | Incompatible update flows |
| Theme path | `~/user_scripts/theme_matugen/` | `~/.config/omarchy/themes/` | Different locations |
| CLI | Scattered scripts | Single `omarchy` dispatcher | No unified CLI |

### What Can Be Adopted (Architecture)

| Omarchy Pattern | How to Adapt for Dusky |
|-----------------|----------------------|
| Three-layer config | Create `~/.config/dusky/` as Layer 2 safe zone |
| Single CLI | Build `dusky` CLI that dispatches to existing TUI tools |
| Hook system | Add `~/.config/dusky/hooks/` with theme-set.d, post-update.d |
| Config refresh | Wrap existing TUI tools with backup + diff logic |
| Migration system | Add `~/user_scripts/dusky_migrations/` with timestamped scripts |
| `~/.local/state/` | Use for feature toggles (like Omarchy's toggle system) |

---

## Recommended Approach

### Phase 1: Config Separation (No Code Changes)
1. Identify which files in `edit_here/` are truly user-specific vs Dusky defaults
2. Document the update flow: what `git checkout -f` actually overwrites
3. Map all TUI tools to their config surfaces

### Phase 2: Unified CLI (Build `dusky` command)
Create a single dispatcher that wraps existing tools:
```bash
dusky theme set dark          # Wraps theme_matugen/theme_ctl.sh
dusky appearance              # Wraps hypr/visual/tui_appearance.py
dusky monitors                # Wraps hypr/monitor/tui_monitors.py
dusky keybinds                # Wraps hypr/edit_here/source/keybinds.lua
dusky services                # Wraps services/tui_service_toggle.py
dusky refresh waybar          # Backup + diff + reset waybar config
dusky update                  # git pull + run migrations
dusky hooks run theme-set     # Execute user hooks
```

### Phase 3: Hook System
```
~/.config/dusky/hooks/
├── theme-set.d/
│   ├── 01-reload-waybar.sh
│   ├── 02-restart-mako.sh
│   └── 03-notify.sh
├── post-update.d/
│   ├── 01-run-migrations.sh
│   └── 02-backup-configs.sh
└── pre-update.d/
    └── 01-snapshot.sh
```

### Phase 4: Config Refresh with Diff
Wrap existing backup logic (already in Dusky's backup system) with:
- Pre-change backup (already exists in `edit_here/source/backups/`)
- Post-change diff display
- Atomic swap (write to temp, then move)

---

## What Stays Outside Update Scope

Files/dirs that Dusky updates WON'T touch:
- `~/.config/hypr/edit_here/` — already designed as user-safe
- `~/.config/hypr/shaders/` — user shaders
- `~/user_scripts/` — your custom scripts
- `~/.config/dusky/` — NEW: create this as your safe zone
- `~/.local/state/dusky/` — NEW: for toggles and state

Files that Dusky updates WILL overwrite:
- `~/.config/hypr/source/` — Dusky defaults
- `~/.config/waybar/` — waybar configs (bare git checkout)
- Other `~/.config/` dirs managed by the bare repo

---

## Key Differences: Omarchy vs Dusky Philosophy

| Aspect | Omarchy | Dusky |
|--------|---------|-------|
| Philosophy | "Omakase" — chef's choice, opinionated | "Labor of love" — tinkerer's paradise |
| Config format | Standard Hyprland .conf | Lua (more powerful, less standard) |
| GUI vs TUI | TUI-only, no GUIs | TUI + GUI Control Center |
| Update safety | Migrations + snapshots | Bare git checkout (risky) |
| Extensibility | Hooks + themes | Scripts + rofi menus |
| Community | DHH/Rails crowd, 10k+ stars | Discord community, 2.1k stars |
| RAM usage | Similar (~900MB) | ~900MB |

---

## Decision Matrix

| If you want... | Do this |
|-----------------|---------|
| Omarchy's full experience | Install Omarchy alongside or instead of Dusky |
| Omarchy's config architecture on Dusky | Adopt the patterns (Phase 1-4 above) |
| Just the TUI tools | Install lazygit, btop, fzf, tmux (already have most) |
| Single CLI dispatcher | Build `dusky` wrapper command |
| Update-safe configs | Already have `edit_here/`, strengthen with hooks |
| No GUIs at all | Replace Dusky Control Center with TUI alternatives |

---

## Bottom Line

You're already 70% of the way there. Dusky has:
- Extensive TUI tools (just scattered)
- Config separation (`edit_here/` vs `source/`)
- Auto-backups with timestamps
- Lightweight, terminal-first design

What's missing from the Omarchy playbook:
- **Unified CLI** — one command to rule them all
- **Hook system** — automated reactions to config changes
- **Migration system** — safe config evolution across updates
- **Config refresh with diff** — see what changed before accepting

All of these are buildable on top of Dusky without replacing it.

---

## Sources

- Omarchy repo: https://github.com/basecamp/omarchy
- Omarchy docs: https://deepwiki.com/basecamp/omarchy
- Omarchy SKILL.md: dev branch, `default/omarchy-skill/SKILL.md`
- Dusky repo: https://github.com/dusklinux/dusky
- Local analysis: `~/.config/hypr/`, `~/user_scripts/`, `~/.config/waybar/`
