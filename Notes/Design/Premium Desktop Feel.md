---
tags: [design, desktop, hyprland, dusky, aesthetics]
aliases: ["Premium Desktop Feel", "Dusky Premium Aesthetic"]
created: 2026-05-23
status: done
---

# Premium Desktop Feel — Design Language

The visual philosophy for Dusky Linux. Sharp, frosted, minimal. Every pixel earns its place.

## Core Principles

1. **Sharp over soft.** Zero border-radius everywhere. No rounded corners, no pill shapes. Edges are edges.
2. **Frosted over opaque.** Semi-transparent backgrounds with blur create depth. The desktop bleeds through — you see what's behind, but it's softened.
3. **Shadows are noise.** No drop shadows. Flat layering. Windows stack cleanly without visual weight pulling them down.
4. **Borders are guides, not walls.** 1px borders. Visible enough to separate surfaces, thin enough to not intrude.
5. **Spacing is breathing room.** Wide gaps on single-window layouts (14px outer). Tight inner gaps (4px). The space around content matters as much as the content.

## Aesthetic References

- **Mako** (notification daemon) — the original inspiration. Sharp corners, semi-transparent backgrounds, thin borders. Notifications look like frosted glass panels floating over the desktop.
- **Operator console** — terminal-native, monochrome, typographic. No decorative elements.

## Implementation

### Hyprland (`edit_here/source/appearance.lua`)

| Property | Value | Rationale |
|---|---|---|
| `decoration.rounding` | `0` | Sharp corners, no exceptions |
| `decoration.rounding_power` | `1.0` | Triangular curve (sharp, not circular) |
| `decoration.active_opacity` | `0.95` | Near-opaque. Enough transparency for blur to show |
| `decoration.inactive_opacity` | `0.85` | Slight dim on inactive. Not glassy, just subordinate |
| `decoration.blur.enabled` | `true` | Frosted glass — the premium signature |
| `decoration.blur.size` | `13` | Rich frosted effect. Upstream is 6 — we doubled it |
| `decoration.shadow.enabled` | `false` | No shadows. Flat, clean layering |
| `general.border_size` | `1` | 1px minimum. Thin separator, not a frame |
| `w[tv1] gaps_out` | `14` | Wide breathing room for single-window focus |

### Rofi (`~/.config/rofi/config.rasi`, `wallpaper.rasi`)

| Property | Value | Rationale |
|---|---|---|
| `border-radius` | `0px` | Sharp corners on all elements |
| `border` | `1px` | Thin, minimal separator |
| Background | Alpha via matugen tokens | `@surface` at 40% opacity, `@surface-container` at 30% |

### Matugen Template (`rofi-colors.rasi`)

The alpha values in the matugen template are what make the frosted glass work:

| Token | Alpha | Effect |
|---|---|---|
| `surface` | `66` (40%) | Main window background — visible blur |
| `surface-container` | `4D` (30%) | Input/message backgrounds — deeper frost |
| `surface-dim` | `66` (40%) | Dimmed variant |
| `surface-bright` | `66` (40%) | Bright variant |

These are matugen template variables — they regenerate with each wallpaper change, keeping the frost consistent across themes.

### Mako (`~/.config/mako/config`)

The notification daemon that started it all:

| Property | Value | Effect |
|---|---|---|
| `border-radius` | `0` | Sharp corners |
| `border-size` | `1` | Thin border |
| `background-color` | `#0f15134d` | ~30% opacity — deep frost |
| `padding` | `8,14` | Tight internal spacing |

## Layer Rules (Hyprland)

Blur is applied per-layer via `hl.layer_rule()`:

- **Rofi**: `blur = true`, `ignore_alpha = 0.0` — full blur even on semi-transparent pixels
- **Mako**: `blur = true`, `ignore_alpha = 0.0` — notifications get the same frost
- **Waybar**: `blur = true` — bar blends with desktop

## What We Explicitly Rejected

| Rejected | Why |
|---|---|
| `border-radius > 0` | Soft corners feel generic. Sharp is intentional |
| `shadow.enabled = true` | Shadows add visual weight and noise. Flat is clean |
| `border_size = 0` | Invisible borders make windows bleed together. 1px is the sweet spot |
| `blur.size = 6` (upstream) | Too subtle. 13 gives the frosted glass premium feel |
| `active_opacity = 0.75` | Too transparent. 0.95 keeps readability while allowing frost |
| `gaps_out = 6` (upstream) | Too tight for single-window layouts. 14 gives breathing room |

## Design Mantra

> Sharp edges. Frosted glass. No shadows. One pixel. Breathe.

## Related

- [[Dusky Theme Engine]]
- [[Hyprland Configuration]]
