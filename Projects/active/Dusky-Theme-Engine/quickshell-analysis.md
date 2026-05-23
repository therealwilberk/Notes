---
tags: [project, quickshell, qml, research]
parent: "[[Dusky-Theme-Engine]]"
status: complete
---

# QuickShell `desktop/` — Full Analysis

**Repo:** [bjarneo/quickshell](https://github.com/bjarneo/quickshell)
**Config root:** `~/.config/quickshell/desktop/`
**Process:** Single `qs -n -d -c desktop` daemon hosting a top bar (Navbar) and a fused OmniMenu command palette. Both share one `Theme` instance, so an omarchy theme swap propagates atomically to bar, popups, and palette.

---

## 1. Repo Structure

```
quickshell/
├── desktop/                          # ← THIS ANALYSIS
│   ├── shell.qml                     # Entry point (ShellRoot)
│   ├── Theme.qml                     # Live palette from colors.toml
│   ├── Palette.js                    # colors.toml parser / mapper
│   ├── Data.js                       # All omarchy-menu items, helpers
│   ├── Navbar.qml                    # Bar state, telemetry, probes
│   ├── Bar.qml                       # PanelWindow chrome (the bar itself)
│   ├── Module.qml                    # Bar icon + tooltip + bloom
│   ├── Workspace.qml                 # Kanji workspace cell
│   ├── Separator.qml                 # Hairline between bar sections
│   ├── Bloom.qml                     # Hover-bloom animation
│   ├── TooltipOverlay.qml            # Full-screen tooltip layer
│   ├── CardWindow.qml                # Generic popup chrome
│   ├── CalendarChevron.qml           # Prev/today/next chevron
│   ├── CalendarPopup.qml             # Month grid + holidays
│   ├── WeatherPopup.qml              # wttr.in weather card
│   ├── DisplayPopup.qml              # Warmth/brightness/gamma sliders
│   ├── DisplaySlider.qml             # Slider widget
│   ├── DisplayChip.qml               # Pill-shaped action chip
│   ├── ScreenshotsPopup.qml          # Screenshot browser grid
│   ├── VideosPopup.qml               # Video browser grid
│   ├── AetherPopup.qml               # Blueprint + Wallhaven picker
│   ├── WallhavenSource.qml           # Wallhaven API backend
│   ├── OmniMenu.qml                  # Full-screen command palette
│   ├── NavbarApps.qml                # Navbar popup wrappers for palette
│   ├── AppScan.qml                   # .desktop file scanner
│   ├── Bookmarks.qml                 # Favourites + history persistence
│   ├── FileSearch.qml                # fd-backed file search
│   ├── GhSearch.qml                  # gh-backed repo/PR search
│   ├── Processes.qml                 # ps-driven process list
│   ├── Themes.qml                    # omarchy theme browser
│   ├── Tuis.qml                      # TUI app probe
│   ├── QuickButton.qml               # Mono-caps action button
│   ├── QuickSlider.qml               # Slim horizontal slider
│   ├── QuickBatteryBody.qml          # Battery detail panel
│   ├── QuickAudioBody.qml            # Audio detail panel
│   ├── QuickWifiBody.qml             # Wi-Fi detail panel
│   ├── QuickBluetoothBody.qml        # Bluetooth detail panel
│   ├── QuickWeatherBody.qml          # Weather detail panel
│   ├── QuickDisplayBody.qml          # Display detail panel
│   ├── QuickAetherBody.qml           # Aether detail panel (3 tabs)
│   ├── QuickCpuBody.qml              # CPU/MEM bars + btop launch
│   ├── QuickCalendarBody.qml         # Calendar detail panel
│   ├── QuickScreenshotsBody.qml      # Screenshots detail panel
│   ├── QuickVideosBody.qml           # Videos detail panel
│   ├── QuickPowerBody.qml            # Power actions (lock, reboot...)
│   ├── assets/
│   │   └── preview.png
│   ├── contrib/
│   │   └── post-boot.d/
│   │       └── quickshell-desktop    # Autostart hook script
│   └── README.md
├── battery-drip/                     # Rare battery feedback overlay
├── clipboard-ripple/                 # Clipboard tactile feedback
├── music-wallpaper/                  # Music-reactive wallpaper
├── song-drop/                        # MPRIS notifier (liquid blob)
├── song-slide/                       # MPRIS notifier (slide-in card)
├── theme-wash/                       # Theme-swap animation
├── quickapps/                        # Radial quick-app launcher
├── README.md
└── demo-video.mp4
```

---

## 2. Component Inventory

### 2.1 `shell.qml` — Entry Point

| Property  | Value                                                                |
| --------- | -------------------------------------------------------------------- |
| Imports   | `QtQuick`, `Quickshell`                                              |
| Root type | `ShellRoot`                                                          |
| Children  | `Theme { id: theme }`, `Navbar { id: nav }`, `OmniMenu { id: omni }` |

Connects `nav.onPaletteToggleRequested` → `omni.toggle()`. This is the single QS process: bar + palette are always co-resident.

### 2.2 `Navbar.qml` — Bar State Hub (1815 lines)

The largest component. Owns **all** bar state, IPC handlers, probe timers, and popup surfaces.

**Exposed properties (consumed by all children via `root:` injection):**

| Property group | Details                                                                                                                                                                                                                                                      |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Theme colours  | `paper`, `ink`, `inkDeep`, `sumi`, `indigo`, `seal`, `bg`, `fg`, `muted`, `accent`, `warn`, `sep`                                                                                                                                                            |
| Fonts          | `serif: "serif"`, `mono: "JetBrainsMono Nerd Font"`                                                                                                                                                                                                          |
| Geometry       | `barHeight: 26`, `barEdge` (cycles `top`→`right`→`bottom`→`left`), `isHorizontal`                                                                                                                                                                            |
| Telemetry      | `cpuVal`, `memVal`, `batVal`, `batState`, `batPower`                                                                                                                                                                                                         |
| Time           | `hh`, `mm`, `dd`, `mon` (updated 1 Hz)                                                                                                                                                                                                                       |
| Audio          | `audioIcon`, `audioVol`, `audioMuted`, `audioSinks`                                                                                                                                                                                                          |
| Network        | `netIcon`, `netKind`, `wifiSsid`, `wifiSignal`, `wifiNetworks`                                                                                                                                                                                               |
| Bluetooth      | `btIcon`, `btPowered`, `btCount`, `btDevices`                                                                                                                                                                                                                |
| Weather        | `weatherLocation`, `weatherVisible`, `weatherLoaded`, `weatherTempC`, `weatherFeelsC`, `weatherWindKmh`, `weatherWindDir`, `weatherHumidity`, `weatherUv`, `weatherDesc`, `weatherCode`, `weatherSunrise`, `weatherSunset`, `weatherIcon`, `weatherForecast` |
| Display        | `displayVisible`, `warmthK`, `brightnessPct`, `gammaPct`, `monitorName`, `monitorRes`, `monitorRate`, `monitorScale`, `displayPresets`, `selectedPreset`, `displayRow`                                                                                       |
| Calendar       | `calendarVisible`, `calendarMonthOffset`, `calendarTick`, `selectedDay`                                                                                                                                                                                      |
| Screenshots    | `screenshotsVisible`, `screenshotPage`, `screenshotFiles`, `selectedScreenshot`                                                                                                                                                                              |
| Videos         | `videosVisible`, `videoPage`, `videoFiles`, `selectedVideo`                                                                                                                                                                                                  |
| Aether         | `aetherVisible`, `aetherBlueprints`, `selectedAether`, `aetherQuery`                                                                                                                                                                                         |
| MPRIS          | `musicPlayer`, `musicTitle`, `musicArtist`, `musicPlaying`                                                                                                                                                                                                   |
| Other          | `activeWs`, `existingWs`, `lastDirection`, `tooltipText`, `popupAnchorX/Y`, `omarchyUpdateAvailable`, `powerProfile`, `powerProfiles`                                                                                                                        |

**Signals:**

| Signal                     | Emitted by                                               |
| -------------------------- | -------------------------------------------------------- |
| `paletteToggleRequested()` | Bar's omarchy glyph click → wired to `OmniMenu.toggle()` |
| `netBurst()`               | Network burst detector → arc animation on wifi module    |
| `showTooltip(text, x, y)`  | Any Module/Workspace on hover → `TooltipOverlay`         |
| `hideTooltip(text)`        | Any Module/Workspace on exit                             |

**Popups instantiated as children:**

```
Bar, TooltipOverlay, CalendarPopup, ScreenshotsPopup, VideosPopup,
AetherPopup, DisplayPopup, WeatherPopup
```

**IPC Handlers (8 targets):**

`palette`, `screenshots`, `videos`, `weather`, `aether`, `display`, `calendar`, `corners`

### 2.3 `Bar.qml` — Visual Bar Chrome (493 lines)

A `PanelWindow` with `WlrLayershell.layer: WlrLayer.Top`.

| Feature          | Detail                                                                              |
| ---------------- | ----------------------------------------------------------------------------------- |
| Layout           | `GridLayout` (LTR or TTB based on `isHorizontal`)                                   |
| Left cluster     | omarchy glyph → `Separator` → 10 kanji workspace cells                              |
| Centre           | Clock (`HH:MM` horizontal, stacked vertical); click opens calendar                  |
| Right cluster    | weather → Separator → cpu → bt → wifi → audio → update badge → battery → edge arrow |
| Now-playing pill | MPRIS pill with artist/title, click toggles play/pause, right/→next, middle/←prev   |
| Cloud mode       | When `round && isHorizontal`: the bar gets a rounded backdrop with air gaps         |

**Behaviour:** Idle dim (`IdleMonitor` 60s timeout, bar fades to 0.7 opacity over 6s, restores in 60ms).

### 2.4 `Module.qml` — Reusable Bar Icon (79 lines)

Generic icon + tooltip + bloom + click handler. Props: `root`, `glyph`, `tooltip`, `color`, `fontFamily`, `fontSize`, `glyphYOffset`. Signals: `activated()`, `rightActivated()`.

### 2.5 `Workspace.qml` — Kanji Workspace Cell (70 lines)

Kanji numeral (〇–十) per workspace. Props: `wsId`, `label`, `active`, `present`. Slide-in animation on direction change from `lastDirection`.

### 2.6 `Bloom.qml` — Hover Bloom (51 lines)

Soft accent-tinted halo that radiates from cursor entry point. Used by Module, Workspace, and the clock.

### 2.7 `Separator.qml` — Hairline (15 lines)

1px × 12px rectangle with `root.sep` colour.

### 2.8 `TooltipOverlay.qml` — Full-Screen Tooltip (75 lines)

`PanelWindow` at `WlrLayer.Overlay`. Single `Rectangle` positioned off the bar's inner edge, centred on the hovered icon.

### 2.9 `CardWindow.qml` — Generic Popup Chrome (215 lines)

Reusable `PanelWindow` template. Features: scale-from-centre reveal, `anchorEdge`/`anchorBarX/Y` for bar-anchored popups, `onDismiss`, `onKeyPressed`, `headerRight` slot for chevrons.

Used by: `CalendarPopup`, `WeatherPopup`, `DisplayPopup`, `ScreenshotsPopup`, `VideosPopup`, `AetherPopup`.

### 2.10 `OmniMenu.qml` — Command Palette (1788 lines)

A `PanelWindow` at `WlrLayer.Overlay` with `ExclusionMode.Ignore`. Its `IpcHandler` target is `"palette"`.

**Sources:** `AppScan`, `NavbarApps`, `Tuis`, `Themes`, `Bookmarks`, `FileSearch`, `GhSearch`, `Processes`, and the static `Data.omarchyItems` array.

**Quick tiles (12):** `battery`, `audio`, `network`, `bluetooth`, `weather`, `display`, `aether`, `cpu`, `calendar`, `screenshots`, `videos`, `power` — displayed as a live-tile grid with per-tile detail panels.

**Search:** Multi-token scoring on pre-lowercased `_t`/`_k`/`_c` fields. Weights: prefix 100, title substring 60, keywords 20, category 10. Cap: 250 results.

**Keyboard nav:** Arrow/Tab for selection, PageUp/Down for 8-row jump, Enter to activate, Ctrl+S to star, Backspace to delete char/unwind drill, Esc to cascade-collapse.

**Drill-downs:** Category nav rows (Apps, Style, Files, GitHub, Processes, Themes, Quick, Setup, etc.) pivot the filtered list.

**GlobalShortcut entries:** `palette-toggle` (SUPER+SPACE), `palette-quick` (ALT+SPACE).

### 2.11 `Palette.js` — Theme Parser (50 lines)

| Function                | Purpose                                                                                                              |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `parseAll(text)`        | Parses TOML `key = "value"` pairs → JS object                                                                        |
| `mapKeys(raw)`          | Renames `WANTED` keys (background→paper, foreground→ink, color7→inkDeep, color8→sumi, accent→indigo, color1→sealRaw) |
| `parse(text)`           | Combined `parseAll` + `mapKeys`                                                                                      |
| `apply(theme, palette)` | Writes onto a live `Theme.qml` instance (missing slots left unchanged)                                               |

### 2.12 `Data.js` — Menu Data + Helpers (315 lines)

- `omarchyItems` (167 entries): Every leaf action the omarchy menu can dispatch, with categories: Quick, Style, Setup, Install, Remove, Update, System, Toggle, Trigger, Capture, Share, Learn
- `categoryNav` (19 synthetic rows): Category drill-in nav items
- `fileIcons`: Nerd-font icon map for 80+ file extensions
- `annotate(items)`: Pre-caches lowercased `_t`/`_k`/`_c` on every item
- `scoreItem(item, tokens)`: Multi-token scorer
- Helpers: `basename`, `dirname`, `tildify`, `fileExt`, `fileIcon`, `openUrl`, `formatStars`, `itemKey`

### 2.13 `Theme.qml` — Live Palette (146 lines)

Reads `~/.config/omarchy/current/theme/colors.toml` via `FileView`. Persists corner state to `~/.local/state/quickshell-desktop/corners`.

**Properties:** `paper`, `ink`, `inkDeep`, `sumi`, `indigo`, `sealRaw`, `cornerRadius`, `driftAmount`.

**Computed properties:** `seal` (drift-modulated `sealRaw`), `bg`, `fg`, `muted`, `accent`, `warn`, `sep`, `rowHi`, `rowSel`.

**IPC handlers:** `corners` (set/round/sharp/toggle), `theme` (apply/reload).

**Drift animation:** 1.55s delay → 200ms rise → 2.8s taper on `seal` saturation.

### 2.14 `AppScan.qml` — Desktop File Scanner (105 lines)

Single Python `configparser` pass scanning 6 XDG directories. Filters NoDisplay/Hidden, strips `%f`/`%U` field codes, deduped by name. Returns ~80-200 entries.

### 2.15 `FileSearch.qml` — fd File Search (168 lines)

Debounced (120ms) fd process. Three glob modes: full-path glob, basename glob, fzf-style regex. Heads up to 200 results.

### 2.16 `GhSearch.qml` — GitHub Search (319 lines)

Two surfaces: PRs (when query empty, 4 parallel queries: author/review-requested/mentions/assignee) and repo search (scoped to user+orgs, then broad). All via `gh CLI`.

### 2.17 `Processes.qml` — Process List (135 lines)

`ps -eo pid,user,pcpu,pmem,comm --sort=-pcpu` → top 200. Kill via `kill -15` (or `-9`).

### 2.18 `Themes.qml` — Theme Browser (145 lines)

Scans `$OMARCHY_PATH/themes`, `~/.local/share/omarchy/themes`, `~/.config/omarchy/themes`. Parses each theme's `colors.toml` into swatch strips. Marks active by byte-comparison.

### 2.19 Quick Detail Panels (12 files)

| File                       | Content                                                |
| -------------------------- | ------------------------------------------------------ |
| `QuickBatteryBody.qml`     | Capacity bar, power state, power-profile selector      |
| `QuickAudioBody.qml`       | Mute toggle, volume slider, output sink picker         |
| `QuickWifiBody.qml`        | Radio toggle, scan, network list (iwctl)               |
| `QuickBluetoothBody.qml`   | Power toggle, scan, device list (bluez-tools)          |
| `QuickWeatherBody.qml`     | Current + forecast, refresh/edit actions               |
| `QuickDisplayBody.qml`     | Warmth/brightness/gamma sliders, presets, monitor info |
| `QuickAetherBody.qml`      | 3-tab: Blueprints / Wallhaven / Themes                 |
| `QuickCpuBody.qml`         | CPU + memory bars, btop launch                         |
| `QuickCalendarBody.qml`    | Month grid with day selection                          |
| `QuickScreenshotsBody.qml` | Recent screenshots grid, capture button                |
| `QuickVideosBody.qml`      | Recent videos grid, open folder button                 |
| `QuickPowerBody.qml`       | Lock, Suspend, Hibernate, Logout, Reboot, Shutdown     |

---

## 3. Color / Theme System

### 3.1 Source of Truth

`~/.config/omarchy/current/theme/colors.toml` — a TOML file with 22 keys (`background`, `foreground`, `accent`, `cursor`, `selection_foreground`, `selection_background`, `color0`–`color15`).

### 3.2 Palette.js Mapping

| colors.toml key | Semantic slot | Used for |
|---|---|---|
| `background` | `paper` | Surface base |
| `foreground` | `ink` | Primary text |
| `color7` | `inkDeep` | Secondary text |
| `color8` | `sumi` | Muted decoration |
| `accent` | `indigo` | Info accent |
| `color1` | `sealRaw` | Active markers, alerts |

### 3.3 Derived Colours (Theme.qml)

| Property | Derivation |
|---|---|
| `bg` | `Qt.rgba(paper, 0.94)` |
| `seal` | `sealRaw` with saturation boosted by `driftAmount` (0.05 per unit) |
| `sep` | `Qt.rgba(ink, 0.18)` |
| `rowHi` | `Qt.rgba(ink, 0.06)` |
| `rowSel` | `Qt.rgba(seal, 0.18)` |
| `muted`, `accent`, `warn` | Aliases |
| `serif` | `"serif"` |
| `mono` | `"JetBrainsMono Nerd Font"` |

### 3.4 Theme Refresh Path

1. `omarchy theme set <name>` → hook script (`theme-set`) parses `colors.toml` with `tomlq`, builds JSON payload
2. Hook sends DBus signal to `org.omarchy.Theme.Changed`
3. Hook calls `qs -c desktop ipc call theme apply '<json>'`
4. `Theme.qml` IPC handler receives payload → `Palette.apply(theme, Palette.mapKeys(payload.colors))`
5. `driftAnim` gives `seal` a 200ms saturation rise + 2.8s taper

### 3.5 Corner State

Persisted to `~/.local/state/quickshell-desktop/corners` (one line: `"round"` or `"sharp"`). Flipped via IPC `corners toggle` / `corners round` / `corners sharp`. Default: sharp (radius 0). Round sets radius 6.

---

## 4. System Configs

### 4.1 Hardcoded Paths

| Path | Used by |
|---|---|
| `~/.config/omarchy/current/theme/colors.toml` | Theme.qml live palette |
| `~/.config/omarchy/current/theme.name` | Theme reload trigger |
| `~/.config/omarchy/weather/location` | Weather location override |
| `~/.local/state/quickshell-desktop/corners` | Corner radius persistence |
| `~/.cache/quickshell/omni-menu/state.json` | Bookmarks favourites + history |
| `~/.cache/quickshell-desktop/video-thumbs/` | Cached video thumbnails + metadata |
| `~/.cache/quickshell-desktop/wallhaven/` | Wallhaven thumbnails + palette cache |
| `~/.local/share/aether/wallpapers/` | Downloaded wallhaven full-res images |
| `~/.config/omarchy/hooks/post-boot.d/quickshell-desktop` | Autostart |

### 4.2 System Calls (via Process)

| Command | Frequency | Purpose |
|---|---|---|
| `/proc/stat` + `/proc/meminfo` | 1 Hz | CPU + memory telemetry |
| `/sys/class/power_supply/BAT{0,1}/` | 1 Hz | Battery capacity, status, power draw |
| `date +%H:%M:%d:%b` | 1 Hz | Clock |
| `hyprctl activeworkspace -j` | 2 Hz | Active workspace |
| `hyprctl workspaces -j` | 2 Hz | Existing workspaces |
| `iw dev ...` + `/proc/net/dev` | 3 Hz / 1 Hz | Network type, signal, burst detection |
| `bt-adapter --info` | 5 Hz | Bluetooth power state |
| `pamixer --get-volume --get-mute` | 2 Hz | Audio volume + mute |
| `wtty.in?format=j1` (curl) | 30 min | Weather data |
| `brightnessctl` | On-demand | Display brightness |
| `hyprctl hyprsunset` | On-demand | Colour temperature + gamma |
| `wpctl status` | On-demand | Audio sink list |
| `powerprofilesctl` | On-demand | Power profile |
| `iwctl station <dev> get-networks` | On-demand | Wi-Fi scan |
| `bt-device --info / --list` | On-demand | Bluetooth device list |
| `fd` | On keystroke (120ms debounce) | File search |
| `gh search repos / prs` | On keystroke (350ms debounce) | GitHub search |
| `ps` | On mode entry | Process list |
| `omarchy-update-available` | 6 h | Update check |
| `aether --list-blueprints --json` | On popup open | Blueprint list |
| `aether --extract-palette` | On popup open | Wallhaven palette extraction |

### 4.3 DBus Integration

- **org.omarchy.Theme.Changed** — signal consumed by `Theme.qml` IPC handler (and any external `dbus-monitor` listener)

### 4.4 Process Spawning

All command execution goes through:

```qml
Process { id: runner; running: false }
function run(cmd) {
    runner.command = ["bash", "-lc", cmd];
    runner.running = false;
    runner.running = true;
}
```

Launches use the omarchy convention: `setsid -f uwsm-app -- bash -c "<cmd>" >/dev/null 2>&1`. This detaches the process into a new session, registers it under a systemd-user scope, and suppresses spurious output.

### 4.5 IPC Surface

All surfaces expose `qs -c desktop ipc call <target> <verb>`:

| Target | Verbs |
|---|---|
| `palette` | `toggle`, `open`, `close`, `refresh`, `openCategory(cat)` |
| `screenshots` | `toggle`, `open`, `close` |
| `videos` | `toggle`, `open`, `close` |
| `weather` | `toggle`, `open`, `close`, `refresh` |
| `aether` | `toggle`, `open`, `close` |
| `display` | `toggle`, `open`, `close`, `reset`, `blank` |
| `calendar` | `toggle`, `open`, `close` |
| `corners` | `set(mode)`, `round`, `sharp`, `toggle` |
| `theme` | `apply(json)`, `reload` |

---

## 5. Dependencies

### 5.1 Runtime

| Component | Required | Notes |
|---|---|---|
| **quickshell** | Yes | QML runtime, Wayland layer-shell, IPC |
| **hyprland** | Yes | Workspace state, keybinds, DPMS |
| **omarchy** | Yes | Live palette, `omarchy-menu` dispatcher, hooks |
| **uwsm** | Yes | `uwsm-app` scope wrapper |
| **python3** | Yes | `.desktop` file parsing |
| **pamixer** | Yes | Audio volume + mute query |
| **brightnessctl** | Yes | Backlight control |
| **hyprsunset** | Yes | Colour temperature + gamma |
| **jq, curl** | Yes | Weather data from wttr.in |
| **iwctl** | Yes (iwd) | Wi-Fi scanning + connect |
| **bt-adapter / bt-device** | Yes (bluez-tools) | Bluetooth control |
| **powerprofilesctl** | Optional | Power profile selector |
| **fd** | Optional | File search drill-down |
| **gh** | Optional | GitHub search + PR drill-down |
| **dragon-drop** | Optional | Video drag-and-drop |
| **tomlq** (from `yq`) | Optional (hook) | Theme hook TOML→JSON |
| **ffmpeg/ffprobe** | Optional | Video thumbnail generation |

### 5.2 QML Modules

| Module | Used by |
|---|---|
| `QtQuick` | Every component |
| `QtQuick.Layouts` | Bar, OmniMenu, detail panels |
| `QtQuick.Effects` | OmniMenu (MultiEffect for icon colorization) |
| `Quickshell` | ShellRoot, PanelWindow, GlobalShortcut, IpcHandler, etc. |
| `Quickshell.Wayland` | PanelWindow, WlrLayershell |
| `Quickshell.Io` | Process, FileView, StdioCollector |
| `Quickshell.Services.Mpris` | Navbar MPRIS player |
| `Quickshell.Hyprland` | OmniMenu (Hyprland binds) |

No specific Qt version requirement visible in source; quickshell is built against a recent Qt6.

---

## 6. Keyboard Navigation

### 6.1 Bar

| Key | Action |
|---|---|
| Click | Module activation (varies by module) |
| Right-click | Alternative action (mute toggle, refresh, etc.) |
| Hover (320ms) | Tooltip reveal |

### 6.2 OmniMenu (Root)

| Key | Action |
|---|---|
| Type | Real-time search (letters/digits only) |
| ↑ / ↓ | Move selection, wraps |
| Tab / Shift+Tab | Move selection, wraps |
| PageUp / PageDown | Jump 8 rows, clamps |
| Home / End | First / last result |
| Enter | Activate (run command or drill into category) |
| Ctrl+S | Star / unstar current row |
| Backspace | Delete char; when empty, go up one level |
| Esc | Collapse query → unwind drill → close |

### 6.3 OmniMenu (Quick Mode)

| Key | Action |
|---|---|
| hjkl | Arrow translation (Vim-style grid nav) |
| ↑↓←→ | Move grid selection |
| Tab / Shift+Tab | Step selection |
| Enter | Open detail panel for focused tile |
| Esc | Collapse panel → close |

### 6.4 Popups

| Popup | Navigation keys |
|---|---|
| **Calendar** | ← → ↑ ↓ move day; PageUp/Down month; Home jump today; Q closes |
| **Display** | ↑↓ rows; ←→ adjust slider; 1-4 presets; R reset; B blank; E edit monitors; Q/B/Enter activate |
| **Weather** | R refresh; E edit location; Q close |
| **Screenshots** | ←→↑↓ move grid; N/P page; Enter/O/Space open; C copy; Q close |
| **Videos** | ←→↑↓ move grid; N/P page; Enter/O/Space open; C URI copy; Shift+C byte copy; Q close |
| **Aether** | Tab mode switch; ↑↓ move; Enter apply; M material toggle; backspace search; type to filter |

### 6.5 Quick Detail Panels

Each body implements `kbdHandle(event)` with component-specific keyboard focus chains. Common pattern: ↑/↓ move through controls, ←/→ adjust sliders, Enter activates an action.

---

## 7. Data Flow

### 7.1 Telemetry Pipeline

```
Navbar.qml
  │
  ├── tel (1 Hz)
  │     └── /proc/stat (CPU) + /proc/meminfo (MEM)
  │         + /sys/class/power_supply/BAT* (battery)
  │         + date (clock)
  │         → cpuVal, memVal, batVal, batState, batPower, hh, mm, dd, mon
  │
  ├── wsProbe (2 Hz)
  │     └── hyprctl workspaces/activeworkspace
  │         → activeWs, existingWs, lastDirection
  │
  ├── netProbe (3 Hz)
  │     └── iw dev + ip → netKind, netIcon, wifiSsid, wifiSignal
  │
  ├── netBurstProbe (1 Hz)
  │     └── /proc/net/dev delta → netBurst() signal
  │
  ├── audioProbe (2 Hz)
  │     └── pamixer → audioVol, audioMuted, audioIcon
  │
  ├── btProbe (5 Hz)
  │     └── bt-adapter → btPowered, btIcon, btCount
  │
  └── omarchyUpdateProbe (6 h)
        └── omarchy-update-available → omarchyUpdateAvailable, omarchyLatestTag
```

### 7.2 Theme / Colour Flow

```
~/.config/omarchy/current/theme/colors.toml
  └── Theme.qml::paletteFile (FileView)
        └── Palette.parse() → Palette.apply()
              └── theme.paper, ink, inkDeep, sumi, indigo, sealRaw
                    ├── Navbar re-exports as root.paper, root.ink, etc.
                    │     └── Bar.qml, Module.qml, Workspace.qml, popups
                    └── OmniMenu reads theme directly
                          └── paper, ink, bg, fg, seal, sep, rowHi, rowSel
```

### 7.3 Menu Search Flow

```
OmniMenu.query (keystroke buffer)
  │
  ├── queryTokens (split on whitespace, lowercased)
  │
  └── filter → filter pipeline:
        ├── fileMode? → FileSearch.items (fd)
        ├── ghMode?   → GhSearch.items (gh)
        ├── favMode?  → Bookmarks.favouriteItems
        ├── histMode? → Bookmarks.historyItems
        ├── procMode? → Processes.items
        ├── themeMode?→ Themes.items
        ├── categoryFilter? → allItems.filter(category)
        └── root → navRows.concat(allItems)
              └── scoreItem(title, keywords, category vs tokens)
                    └── sort desc → cap at 250 → resultList
```

### 7.4 Quick Tile Data Flow

```
Twelve static tiles defined in OmniMenu.quickTilesBase (glyph determined
dynamically from navbar state):
        ┌──────────────────────────────────────────┐
        │  Battery  │   Audio   │  Network  │  BT  │
        │ 56% +12W  │   67%     │  WiFi 80% │ ON   │
        ├───────────┼───────────┼───────────┼──────┤
        │  Weather  │  Display  │  Aether   │ CPU  │
        │  +12°C    │ 6500K 100%│  THEMES   │ 23%  │
        ├───────────┼───────────┼───────────┼──────┤
        │ Calendar  │  Shots    │  Videos   │Power │
        │ 23 MAY    │  BROWSE   │  BROWSE   │ MENU │
        └───────────┴───────────┴───────────┴──────┘
```

Each tile opens a per-key detail panel (`Quick{Battery,Audio,...}Body.qml`) with live controls.

---

## 8. Entry Points & Initialization

### 8.1 Launch

```sh
qs -n -d -c desktop
```

- `-c desktop` → resolves to `~/.config/quickshell/desktop/shell.qml`
- `-d` daemonizes
- `-n` idempotent (bails if already running)

### 8.2 Load Order

1. **ShellRoot** created → `shell.qml`
2. **Theme** instantiated — starts `cornerReader` process (reads corner state), sets up `paletteFile` (FileView watching `colors.toml`), registers `corners` and `theme` IPC handlers
3. **Navbar** instantiated — begins all timer probes (1Hz telemetry, 2Hz workspace, 3Hz network, 5Hz BT, 30min weather, 6h update check)
4. **OmniMenu** instantiated:
   - `Component.onCompleted`: annotates `Data.omarchyItems` and `Data.categoryNav`
   - `AppScan` starts: Python configparser pass over XDG `.desktop` dirs
   - `Tuis` starts: probes which TUI binaries are on `$PATH`
   - `Themes` starts: probes available omarchy themes
   - `GhSearch` starts: checks `gh auth status`, fetches identity
5. **Bar** (child of Navbar) rendered as `PanelWindow` with `WlrLayer.Top`
6. **TooltipOverlay** (child of Navbar) rendered as `PanelWindow` with `WlrLayer.Overlay`

### 8.3 Autostart

`contrib/post-boot.d/quickshell-desktop` — a bash script installed to `~/.config/omarchy/hooks/post-boot.d/`:

```sh
#!/bin/bash
qs -n -d -c desktop
```

Runs at every Hyprland session start via omarchy's hook system.

### 8.4 Hot-Reload

Quickshell hot-reloads `.qml` files on save. All edits to `desktop/*.qml` or `desktop/*.js` appear live without restarting the daemon.

---

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────┐
│                   shell.qml (ShellRoot)                   │
│                                                           │
│  ┌─────────┐         ┌──────────────────────────────┐     │
│  │  Theme   │         │         Navbar               │     │
│  │  .qml    │         │   (Bar state + IPC + probes) │     │
│  │          │         │                              │     │
│  │ palette  │         │ ┌────┐ ┌──────┐ ┌─────────┐ │     │
│  │ cornerR  │         │ │Bar │ │Ttip  │ │CalPopup │ │     │
│  │ drift    │         │ │.qml│ │Ovrlay│ │WeathPop │ │     │
│  │ IPC      │         │ │    │ │.qml  │ │DispPop  │ │     │
│  └────┬─────┘         │ └────┘ └──────┘ │ScrnPop  │ │     │
│       │               │                 │VidPop   │ │     │
│       │ theme ×       │                 │AethPop  │ │     │
│       │ corners IPC   │                 └─────────┘ │     │
│       │               └──────────────────────────────┘     │
│       │                                                      │
│       │               ┌──────────────────────────────┐      │
│       └──theme──→     │         OmniMenu              │      │
│                       │   (Palette + drill-downs)     │      │
│                       │                              │      │
│                       │  AppScan  ·  FileSearch      │      │
│                       │  GhSearch ·  Processes       │      │
│                       │  Themes   ·  Tuis            │      │
│                       │  Bookmarks·  NavbarApps      │      │
│                       │                              │      │
│                       │  ┌───────────────────────┐   │      │
│                       │  │ Quick detail panels   │   │      │
│                       │  │ (12 × body .qml files)│   │      │
│                       │  └───────────────────────┘   │      │
│                       └──────────────────────────────┘      │
└──────────────────────────────────────────────────────────┘
```

---

## Key Insights for Porting

1. **Everything reads from `root:` injection.** Each child receives `{ root: navbar }` and accesses `root.paper`, `root.ink`, `root.barHeight`, etc. This is the primary coupling pattern — porting means wrapping a unified state object.

2. **Two files hold 85% of complexity:** `Navbar.qml` (1815 lines, all state + probes) and `OmniMenu.qml` (1788 lines, all search + UI). `Data.js` (315 lines) is the third heaviest.

3. **Theme is a straight key remap** — 6 semantic colours from 22 colors.toml keys. The drift animation is the only dynamic colour transform.

4. **All IPC is string-based.** `qs -c desktop ipc call <target> <verb>` with optional JSON string args. The bar has 8 targets, Theme has 2.

5. **No hard Qt version dependency.** QML features used are baseline QtQuick 6.x — no proprietary Quickshell extension beyond `ShellRoot`, `PanelWindow`, `IpcHandler`, `GlobalShortcut`, `Process`, `FileView`, and `MprisPlayer`.

6. **Palette and shell are coupled by design.** The original comment: "*Combined entry point: one Quickshell process hosting both the navbar and the omni-menu command palette. Both share the same Theme instance, so an omarchy theme swap propagates atomically to bar + popups + palette.*"
