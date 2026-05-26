---
type: project
tags: [project, quickshell, qml, planning]
parent: "[[Projects/active/Dusky-Theme-Engine/wpick- Wallpaper Clustering & Smart Picker.md]]"
status: in-progress
---

# QuickShell Port: Omarchy → Dusky

## Current State

- QuickShell (`qs`) is NOT installed yet
- Omarchy is NOT installed
- Hyprland IS running (Lua config at `~/.config/hypr/edit_here/`)
- matugen IS installed, has a quickshell.qml template already
- bjarneo/quickshell `desktop/` config is fully analyzed (663-line doc)

## The Problem

QuickShell's `desktop/` config was built for Omarchy. It hardcodes:
- Omarchy paths for theme files
- Omarchy menu items and command dispatchers
- Omarchy hooks system (post-boot.d)
- Omarchy theme browser that scans Omarchy theme dirs
- `omarchy-update-available` probe
- `setsid -f uwsm-app` launch convention

None of this exists on Dusky. We need to port it.

---

## What to Replace (by file)

### Tier 1: Theme Path (Critical — blocks everything)

**File: `Theme.qml`**
- Hardcoded: `~/.config/omarchy/current/theme/colors.toml`
- Replace with: `~/.config/dusky/current/colors.toml`
- Hardcoded: `~/.config/omarchy/current/theme.name` (reload trigger)
- Replace with: `~/.config/dusky/current/theme.name`
- Hardcoded: `~/.local/state/quickshell-desktop/corners` → keep as-is (not Omarchy-specific)

**File: `Palette.js`**
- No Omarchy hardcodes. The TOML parser and key mapper are generic. Keep as-is.

### Tier 2: Menu Data (High — breaks command palette)

**File: `Data.js`**
- `omarchyItems` (167 entries): Every menu action dispatches Omarchy CLI commands
- Replace: Map each entry to Dusky equivalents or shell commands
- Categories to audit:
  - **Style** → `omarchy-theme-set` → `dusky-theme-set`
  - **Setup** → Omarchy-specific install/update commands → Dusky equivalents or remove
  - **Install/Remove/Update** → Omarchy package commands → remove or replace with pacman/yay
  - **Toggle/Trigger** → Most are Hyprland/system commands → keep as-is
  - **Capture/Share** → Screenshot tools → keep as-is (not Omarchy-specific)
  - **Learn** → Omarchy docs links → Dusky docs or remove

**File: `Themes.qml`**
- Scans `$OMARCHY_PATH/themes`, `~/.local/share/omarchy/themes`, `~/.config/omarchy/themes`
- Replace with: `~/.config/dusky/themes/` (our theme dir from Dusky Theme Engine spec)

### Tier 3: Autostart & Hooks (Medium — breaks auto-launch)

**File: `contrib/post-boot.d/quickshell-desktop`**
- Installs to `~/.config/omarchy/hooks/post-boot.d/`
- Replace with: Hyprland autostart entry in `~/.config/hypr/edit_here/source/autostart.lua`
- Add: `exec-once = qs -n -d -c desktop`

### Tier 4: System Probes (Low — cosmetic or removable)

**File: `Navbar.qml`**
- `omarchyUpdateProbe` (6h timer): calls `omarchy-update-available`
- Replace with: `checkupdates` (arch) or remove entirely
- `omarchyUpdateAvailable`, `omarchyLatestTag` properties → remove or repurpose
- `omarchy glyph` in Bar.qml left cluster → replace with Dusky glyph/icon

**File: `Navbar.qml` / various**
- `setsid -f uwsm-app -- bash -c "..."` launch convention
- Replace with: plain `setsid -f bash -c "..."` or `exec-once` in Hyprland
- uwsm is not installed on Dusky

### Tier 5: Keep As-Is

These files have NO Omarchy dependencies:
- `shell.qml` — entry point, generic
- `Bar.qml` — visual chrome, uses `root:` injection
- `Module.qml`, `Workspace.qml`, `Bloom.qml`, `Separator.qml` — bar widgets
- `TooltipOverlay.qml`, `CardWindow.qml` — popup chrome
- `CalendarPopup.qml`, `WeatherPopup.qml`, `DisplayPopup.qml` — popups
- `OmniMenu.qml` — the palette itself (reads from Data.js, which we fix)
- All `Quick*Body.qml` panels — detail panels, system-level
- `AppScan.qml`, `FileSearch.qml`, `GhSearch.qml`, `Processes.qml` — system tools
- `Bookmarks.qml` — uses `~/.cache/quickshell/`, not Omarchy

---

## Execution Plan

### Step 1: Install QuickShell
- Build from source or AUR: `quickshell-git`
- Verify `qs` binary works: `qs --version`

### Step 2: Clone & Scaffold
- Clone bjarneo/quickshell
- Copy `desktop/` to `~/.config/quickshell/desktop/`
- Verify it loads (will fail on missing Omarchy — that's expected)

### Step 3: Theme Path Swap (Theme.qml)
- Change `paletteFile` path from `~/.config/omarchy/...` to `~/.config/dusky/current/colors.toml`
- Change theme name reader from `~/.config/omarchy/...` to `~/.config/dusky/current/theme.name`
- Test: create a dummy `colors.toml`, verify Theme.qml picks it up

### Step 4: Menu Data Rewrite (Data.js)
- Go through all 167 `omarchyItems`
- Keep: all Hyprland/system/tools entries (majority)
- Replace: Omarchy-specific commands with Dusky equivalents
- Remove: entries with no Dusky equivalent (Omarchy install/update/remove)
- This is the biggest single task — ~100 entries to audit

### Step 5: Theme Browser (Themes.qml)
- Change scan paths to `~/.config/dusky/themes/`
- Adjust active-theme detection (byte-comparison of colors.toml)

### Step 6: Autostart
- Remove Omarchy hook dependency
- Add `exec-once = qs -n -d -c desktop` to Hyprland autostart.lua

### Step 7: Cleanup
- Remove `omarchyUpdateProbe` from Navbar.qml
- Replace omarchy glyph in Bar.qml with Dusky icon
- Remove `uwsm-app` wrappers, use plain `setsid -f`

### Step 8: Matugen Integration
- The existing `~/.config/matugen/templates/quickshell.qml` already generates JSON
- Wire matugen output to write to `~/.config/dusky/current/colors.toml`
- Theme.qml's FileView auto-picks up changes (hot-reload)

---

## Risk Areas

1. **Data.js is 316 lines of hand-written menu entries.** Mapping 167 items is tedious but not hard — most are system commands that don't change.
2. **Themes.qml scans 3 paths.** If we only have `~/.config/dusky/themes/`, we need to make sure the scanner doesn't crash on missing dirs.
3. **Process launching.** The `setsid -f uwsm-app` pattern is used everywhere for app launching. Need to verify plain `setsid -f` works or find equivalent.
4. **DBus signal.** `org.omarchy.Theme.Changed` — we either emit our own signal or use the IPC `theme apply` path directly (which doesn't need DBus).

---

## Files Modified Count

- **Tier 1:** 1 file (Theme.qml)
- **Tier 2:** 2 files (Data.js, Themes.qml)
- **Tier 3:** 1 file (autostart)
- **Tier 4:** 2 files (Navbar.qml, Bar.qml)
- **Total: 6 files modified** out of ~40 QML/JS files

Everything else is generic and works as-is.

---

## Dependencies

| Need | Status |
|---|---|
| quickshell (qs) | NOT installed |
| hyprland | Running |
| matugen | Running |
| pamixer | Check |
| brightnessctl | Check |
| hyprsunset | Config exists |
| iwctl (iwd) | Check |
| bt-adapter (bluez-tools) | Check |
| python3 | Installed |
| fd | Check |
| gh | Check |
| jq, curl | Installed |
