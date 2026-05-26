---
type: project
tags: [project, wpick, matugen, research]
created: 2026-05-25
status: done
parent: "[[Projects/active/Dusky-Theme-Engine/wpick- Wallpaper Clustering & Smart Picker.md]]"
---

# Matugen Color Scheme Options — Research Report

**Date:** 2026-05-25
**Purpose:** Document all matugen CLI options that wpick currently ignores, with empirical comparisons and recommendations.

---

## Executive Summary

wpick currently calls `matugen image <path>` with **zero flags**, relying entirely on defaults. Matugen supports **15+ CLI flags** across 6 categories. Testing reveals **4 high-impact options** wpick should expose (color scheme type, contrast, source-color-index, prefer), **2 medium-impact** (lightness-dark/light, mode), and **5 niche/low-priority** (resize-filter, fallback-color, opacity, prefix, base16-backend).

---

## 1. Color Scheme Types (`--type` / `-t`)

**9 available types, default: `scheme-tonal-spot`**

These control HOW the three accent colors (primary/secondary/tertiary) are derived from the source color. The differences are dramatic.

### Empirical Comparison (Wallpaper 0001.jpg, source: #36599d, dark mode)

| Scheme | primary | secondary | tertiary | Character |
|---|---|---|---|---|
| `scheme-content` | #afc6ff | #bac6e7 | #f4aff7 | **Harmonious.** All hues near the source blue. Tertiary is a soft pink complement. |
| `scheme-expressive` | #99d596 | #eeb8c9 | #bfc2fa | **Wild.** Green primary from blue source! Pink secondary. Unpredictable. |
| `scheme-fidelity` | #afc6ff | #bac6e7 | #ffb868 | **True to source.** Primary matches content, but tertiary is a warm orange — surprising split. |
| `scheme-fruit-salad` | #55d6f4 | #85d2e7 | #afc6ff | **Complementary.** Cyan primary from blue source. Cool, cohesive palette. |
| `scheme-monochrome` | #ffffff | #c6c6c6 | #e2e2e2 | **Grayscale.** Pure white primary. No chromatic info. All surfaces neutral gray. |
| `scheme-neutral` | #c2c6d6 | #c5c6d0 | #bfc6dc | **Desaturated.** Muted blue-gray tones. Subtle, professional. |
| `scheme-rainbow` | #afc6ff | #bfc6dc | #dfbbde | **Evenly spaced.** Primary matches source, tertiary is pink. Widest hue spread. |
| `scheme-tonal-spot` | #afc6ff | #bfc6dc | #dfbbde | **Default.** Primary=source, secondary/tertiary are desaturated complements. |
| `scheme-vibrant` | #afc6ff | #c2c3eb | #cdbef7 | **High saturation.** Same primary as tonal-spot but secondary/tertiary are more chromatic. |

### Second Wallpaper (0010.jpg, source: #80699d purple, dark mode)

| Scheme               | primary | secondary | tertiary | Character                                                      |
| -------------------- | ------- | --------- | -------- | -------------------------------------------------------------- |
| `scheme-content`     | #d6bcf5 | #cfc1db   | #fbb2ce  | Purple + pink. Harmonious.                                     |
| `scheme-expressive`  | #74d7cb | #ecb8ce   | #e7b7e8  | Teal primary from purple! Very unexpected.                     |
| `scheme-fidelity`    | #d6bcf5 | #cfc1db   | #cdca7c  | Purple primary, but **yellow** tertiary — split complementary. |
| `scheme-fruit-salad` | #a3c9ff | #a3c9fe   | #d7bafb  | Blue primary from purple source. Cool.                         |
| `scheme-monochrome`  | #ffffff | #c6c6c6   | #e2e2e2  | Same gray regardless of source.                                |
| `scheme-neutral`     | #cdc3d4 | #ccc4cf   | #cfc2da  | Muted lavender.                                                |
| `scheme-rainbow`     | #d9b9ff | #cfc2da   | #f2b7c1  | Wide hue spread.                                               |
| `scheme-tonal-spot`  | #d7bafb | #cfc2da   | #f2b7c1  | Default. Balanced.                                             |
| `scheme-vibrant`     | #d9b9ff | #dabde2   | #ebb6e4  | More saturated version of tonal-spot.                          |

### Third Wallpaper (0016.jpg, source: green-dominated, dark mode)

| Scheme | primary | secondary | tertiary | Character |
|---|---|---|---|---|
| `scheme-content` | #ffffff | #baccb2 | #ffffff | White primary — green source clips to max! |
| `scheme-expressive` | #ffb3ac | #a7d0b7 | #8dd3cb | **Red** primary from green source! High contrast. |
| `scheme-fidelity` | #ffffff | #baccb2 | #ffffff | Same as content. Source too saturated. |
| `scheme-fruit-salad` | #e8c349 | #e1c46d | #a4d397 | **Yellow** primary from green. Warm. |
| `scheme-monochrome` | #ffffff | #c6c6c6 | #e2e2e2 | Same gray. |
| `scheme-neutral` | #bfcab7 | #c2c8bc | #baccb2 | Muted sage green. |
| `scheme-rainbow` | #93d786 | #baccb2 | #a0cfd3 | Green primary, teal tertiary. |
| `scheme-tonal-spot` | #a4d397 | #baccb2 | #a0cfd3 | Default. Natural green. |
| `scheme-vibrant` | #00e628 | #a9d0b3 | #92d4bc | **Neon green!** Extreme saturation. |

### Key Observations

- **`scheme-expressive`** is the most unpredictable — it deliberately rotates hues far from the source. A blue wallpaper gets a green primary; a green wallpaper gets red.
- **`scheme-monochrome`** ignores source color entirely — always grayscale.
- **`scheme-content`** and **`scheme-fidelity`** are nearly identical for primary/secondary but differ on tertiary.
- **`scheme-vibrant`** can produce extremely saturated colors (neon green #00e628) that may be hard on the eyes.
- **`scheme-tonal-spot`** (default) is a safe middle ground — primary matches source, complements are muted.
- **`scheme-neutral`** produces the most muted/subdued palettes — good for minimal setups.

---

## 2. Source Color Index (`--source-color-index`)

**Range: 0–3 (help says 0–4, but 4 errors), default: shows interactive prompt**

When an image has multiple prominent colors, this selects which one to use as the source color. Matugen extracts up to 4 dominant colors from the image.

### Test: Wallpaper 0004.jpg (multi-color, purple/pink tones)

| Index | source_color | primary | secondary | tertiary |
|---|---|---|---|---|
| 0 | #6c5589 (purple) | #d8bafb | #cfc1da | #f2b7c1 |
| 1 | #a45e85 (magenta) | #fbb0d7 | #dfbecc | #f3ba9c |
| 2 | #7d5280 (dark purple) | #ebb5ec | #d7bfd5 | #f6b8ad |
| 3 | #fee4e5 (light pink) | #ffb2b9 | #e5bdbf | #e8c08e |

**Impact:** Huge. Index 0 gives purple primary, index 1 gives pink, index 3 gives peach. The entire palette shifts dramatically.

### Important Notes

- Most wallpapers only have **1 dominant color** (index 0 only). Multi-color images are common with complex/abstract wallpapers.
- Without `--source-color-index`, matugen shows an **interactive prompt** (breaks non-interactive use in wpick daemon).
- wpick MUST pass either `--source-color-index 0` or `--prefer` to avoid the prompt. Currently it does neither — this is a **bug** for daemon mode.
- The actual number of extractable colors depends on the image. Some images only yield 1 color; complex images yield up to 4.

---

## 3. Contrast (`--contrast`)

**Range: -1 to 1, default: 0**

Adjusts the contrast of the generated scheme. Primarily affects **surface/container colors** (backgrounds) and **text/icon colors** (on_primary, on_surface).

### Test: Wallpaper 0001.jpg, scheme-tonal-spot

| Contrast      | primary | surface_container | surface_container_high | on_primary |
| ------------- | ------- | ----------------- | ---------------------- | ---------- |
| -1.0          | #7890c7 | #1e1f25           | #282a2f                | #2a4476    |
| -0.5          | #7b94cb | #1e1f25           | #282a2f                | #022354    |
| 0.0 (default) | #afc6ff | #1e1f25           | #282a2f                | #132f60    |
| +0.5          | #cfdcff | #26282d           | #313238                | #032355    |
| +1.0          | #ecefff | #2f3036           | #3a3b41                | #000000    |

**Impact:** Moderate-high. Primary shifts from muted (#7890c7) to near-white (#ecefff). Surfaces get lighter at high contrast. The on_primary text goes to black at max contrast.

**Use case:** Users with accessibility needs (low vision) or bright environments may want higher contrast. Users who prefer softer aesthetics want lower contrast.

---

## 4. Lightness Control (`--lightness-dark` / `--lightness-light`)

**Ranges: lightness-dark: -∞ to 1, lightness-light: -1 to +∞, default: 0**

Fine-tunes how light/dark surfaces and containers are. This is an affine transformation on the lightness scale.

### lightness-dark Test (Wallpaper 0001.jpg, dark mode)

| Value         | surface | surface_container | background | primary | primary_container |
| ------------- | ------- | ----------------- | ---------- | ------- | ----------------- |
| -0.3          | #000000 | #000000           | #000000    | #a3b9ee | #0e1626           |
| -0.1          | #000000 | #09090b           | #000000    | #abc1f9 | #22365c           |
| 0.0 (default) | #121318 | #1e1f25           | #121318    | #afc6ff | #2d4678           |
| +0.1          | #262833 | #32343e           | #262833    | #b2caff | #375593           |
| +0.3          | #50546b | #5b5e70           | #50546b    | #bad2ff | #4b75c9           |

**Impact:** Dramatic. At -0.3, everything is pure black. At +0.3, surfaces are medium gray (#50546b). This controls the "darkness depth" of dark mode.

### lightness-light Test (Wallpaper 0001.jpg, light mode)

| Value         | surface | surface_container | background | primary | primary_container |
| ------------- | ------- | ----------------- | ---------- | ------- | ----------------- |
| -0.3          | #afaeb2 | #a6a5aa           | #afaeb2    | #304165 | #979eb2           |
| -0.1          | #e1e0e5 | #d6d5db           | #e1e0e5    | #3e5482 | #c2cbe5           |
| 0.0 (default) | #faf9ff | #eeedf4           | #faf9ff    | #455e91 | #d8e2ff           |
| +0.1          | #ffffff | #ffffff           | #ffffff    | #4b679f | #edf8ff           |
| +0.3          | #ffffff | #ffffff           | #ffffff    | #597abc | #ffffff           |

**Impact:** At +0.3, light mode surfaces are all pure white, and containers collapse to white too. At -0.3, surfaces become medium gray — very unusual for light mode.

---

## 5. Light/Dark Mode (`--mode` / `-m`)

**Values: light, dark, default: dark**

Switches the entire scheme between light and dark variants. This is a fundamental toggle.

### Comparison (Wallpaper 0010.jpg, scheme-tonal-spot)

| Role              | Dark Mode | Light Mode |
| ----------------- | --------- | ---------- |
| primary           | #d7bafb   | #6c538c    |
| on_primary        | #3c255a   | #ffffff    |
| primary_container | #533b72   | #eedcff    |
| surface           | #151218   | #fff7ff    |
| surface_container | #211e24   | #f3ecf4    |
| background        | #151218   | #fff7ff    |
| on_surface        | #e7e0e8   | #1d1a20    |

**Impact:** Complete inversion. Dark surfaces become light, primary colors swap from light to dark variants.

---

## 6. `--prefer` (Color Selection Strategy)

**Values: darkness, lightness, saturation, less-saturation, value, closest-to-fallback**

Controls which color is chosen when the image has multiple candidate source colors.

### Test: Wallpaper 0016.jpg (green-dominated landscape)

| Prefer              | source_color                | primary |
| ------------------- | --------------------------- | ------- |
| darkness            | #ba969a (muted rose)        | #ffb2bc |
| lightness           | #c4efb7 (bright green)      | #a4d397 |
| saturation          | #c4efb7 (bright green)      | #a4d397 |
| less-saturation     | #ba969a (muted rose)        | #ffb2bc |
| value               | #ba969a (muted rose)        | #ffb2bc |
| closest-to-fallback | (requires --fallback-color) | —       |

**Impact:** Significant. `saturation` picks the most vivid color (green), while `darkness` picks the darkest (rose). Can completely change the palette mood.

**Critical for wpick:** This replaces the interactive prompt. If `--prefer` is set, matugen never prompts.

---

## 7. Resize Filter (`--resize-filter`)

**Values: nearest, triangle, catmull-rom, gaussian, lanczos3**

Controls how the image is downscaled before color extraction.

### Test Results

All filters produced nearly identical results for primary color (#a4d396–#abd28f range). Source color varied by ~10 hex values. **Minimal visual impact.**

**Verdict:** Niche. The difference is negligible for practical use.

---

## 8. Other Options

| Option             | What it does                           | Impact                           | wpick relevance                       |
| ------------------ | -------------------------------------- | -------------------------------- | ------------------------------------- |
| `--fallback-color` | Color used when image extraction fails | Safety net                       | Low — only matters for broken images  |
| `--prefix`         | Path prefix for template output        | File paths only                  | Low — for custom output locations     |
| `--opacity`        | Alpha value for colors                 | No visible effect in JSON output | Low — affects template rendering only |
| `--base16-backend` | Backend for base16 generation          | Only `wal` available             | Niche — only for base16 users         |
| `--dry-run`        | Don't generate templates               | Testing only                     | Not for user config                   |

---

## 9. What wpick Currently Does vs. What It Should Do

### Current Code (orchestrator.py, line 84-88)

```python
matugen_result = subprocess.run(
    ["matugen", "image", str(path)],
    capture_output=True,
    text=True,
)
```

**Zero flags. Relies on all defaults.**

### Current Config Model (models.py, line 64-68)

```python
class MatugenConfig(BaseModel):
    enabled: bool = True
    extra_flags: list[str] = Field(default_factory=list)
```

**Only `enabled` and a generic `extra_flags` escape hatch.**

### Bug: Interactive Prompt

Without `--prefer` or `--source-color-index`, matugen may show an **interactive color selection prompt** when it finds multiple source colors. In daemon/watcher mode, this will hang indefinitely.

---

## 10. Recommendations

### Priority 1 — MUST ADD (fixes bugs, high user impact)

| Option | Config Key | Type | Default | Why |
|---|---|---|---|---|
| `--type` | `scheme` | `str` | `"scheme-tonal-spot"` | **Biggest visual impact.** Lets users choose palette personality. 9 options, each produces distinctly different results. |
| `--prefer` | `prefer` | `str` | `"saturation"` | **Fixes daemon hang bug.** Without this, matugen prompts interactively for multi-color images. Also lets users control which color is extracted. |
| `--mode` | `mode` | `str` | `"dark"` | **Fundamental toggle.** Light/dark mode is a core user preference. Easy to implement. |

### Priority 2 — SHOULD ADD (meaningful customization)

| Option | Config Key | Type | Default | Why |
|---|---|---|---|---|
| `--contrast` | `contrast` | `float` | `0.0` | Accessibility and aesthetics. Range -1 to 1. Simple to add. |
| `--source-color-index` | `source_color_index` | `int` | `None` | Lets users pick which dominant color to use. Important for multi-color wallpapers. Should be optional (omit flag to use --prefer instead). |

### Priority 3 — NICE TO HAVE

| Option | Config Key | Type | Default | Why |
|---|---|---|---|---|
| `--lightness-dark` | `lightness_dark` | `float` | `None` | Fine-tune dark mode depth. Power users love this. |
| `--lightness-light` | `lightness_light` | `float` | `None` | Fine-tune light mode brightness. Same audience. |

### Priority 4 — SKIP / KEEP IN extra_flags

| Option | Why skip |
|---|---|
| `--resize-filter` | Negligible visual impact. |
| `--fallback-color` | Edge case for broken images. |
| `--prefix` | Template output path. Niche. |
| `--opacity` | No visible effect in color output. |
| `--base16-backend` | Only `wal` available. Niche. |

---

## 11. Suggested Config Model Changes

```python
class MatugenConfig(BaseModel):
    """matugen colour generation settings."""
    enabled: bool = True
    scheme: str = "scheme-tonal-spot"  # NEW: color scheme type
    mode: str = "dark"                  # NEW: light or dark
    prefer: str = "saturation"          # NEW: source color selection strategy
    contrast: float = Field(default=0.0, ge=-1.0, le=1.0)  # NEW
    source_color_index: int | None = None  # NEW: 0-3, None = use prefer
    lightness_dark: float | None = None    # NEW: fine-tune dark surfaces
    lightness_light: float | None = None   # NEW: fine-tune light surfaces
    extra_flags: list[str] = Field(default_factory=list)
```

## 12. Suggested Orchestrator Changes

```python
def _build_matugen_cmd(path: Path, cfg: MatugenConfig) -> list[str]:
    """Build the matugen command with all configured flags."""
    cmd = ["matugen", "image", str(path)]
    cmd.extend(["--type", cfg.scheme])
    cmd.extend(["--mode", cfg.mode])
    cmd.extend(["--prefer", cfg.prefer])
    if cfg.contrast != 0.0:
        cmd.extend(["--contrast", str(cfg.contrast)])
    if cfg.source_color_index is not None:
        cmd.extend(["--source-color-index", str(cfg.source_color_index)])
    if cfg.lightness_dark is not None:
        cmd.extend(["--lightness-dark", str(cfg.lightness_dark)])
    if cfg.lightness_light is not None:
        cmd.extend(["--lightness-light", str(cfg.lightness_light)])
    cmd.extend(cfg.extra_flags)
    return cmd
```

## 13. Implementation Complexity

| Change | Effort | Notes |
|---|---|---|
| Add `scheme` field | ~15 min | Add field + wire to CLI builder. Validate against allowed values. |
| Add `mode` field | ~10 min | Trivial. Just pass to --mode. |
| Add `prefer` field | ~10 min | Trivial. Just pass to --prefer. **Fixes daemon bug.** |
| Add `contrast` field | ~10 min | Add float field with validation. |
| Add `source_color_index` | ~15 min | Optional int. Conditional flag building. |
| Add `lightness_dark/light` | ~15 min | Optional float fields. Conditional flag building. |
| Refactor `_build_matugen_cmd` | ~20 min | Extract helper function for clean flag building. |
| Update config docs | ~10 min | Document new options in config schema. |
| Add validation | ~15 min | Validate scheme against allowed values, mode, prefer. |
| **Total** | **~2 hours** | All changes are additive, no breaking changes. |

---

## Appendix: Raw Color Data

### Full Scheme Comparison — Wallpaper 0001.jpg (dark mode, source: #36599d blue)

**scheme-content:** primary=#afc6ff, secondary=#bac6e7, tertiary=#f4aff7, surface=#121318
**scheme-expressive:** primary=#99d596, secondary=#eeb8c9, tertiary=#bfc2fa, surface=#12131a
**scheme-fidelity:** primary=#afc6ff, secondary=#bac6e7, tertiary=#ffb868, surface=#121318
**scheme-fruit-salad:** primary=#55d6f4, secondary=#85d2e7, tertiary=#afc6ff, surface=#10131c
**scheme-monochrome:** primary=#ffffff, secondary=#c6c6c6, tertiary=#e2e2e2, surface=#131313
**scheme-neutral:** primary=#c2c6d6, secondary=#c5c6d0, tertiary=#bfc6dc, surface=#131315
**scheme-rainbow:** primary=#afc6ff, secondary=#bfc6dc, tertiary=#dfbbde, surface=#131313
**scheme-tonal-spot:** primary=#afc6ff, secondary=#bfc6dc, tertiary=#dfbbde, surface=#121318
**scheme-vibrant:** primary=#afc6ff, secondary=#c2c3eb, tertiary=#cdbef7, surface=#10131c

### Full Scheme Comparison — Wallpaper 0016.jpg (dark mode, green source)

**scheme-content:** primary=#ffffff, secondary=#baccb2, tertiary=#ffffff, surface=#121410
**scheme-expressive:** primary=#ffb3ac, secondary=#a7d0b7, tertiary=#8dd3cb, surface=#0e1510
**scheme-fidelity:** primary=#ffffff, secondary=#baccb2, tertiary=#ffffff, surface=#121410
**scheme-fruit-salad:** primary=#e8c349, secondary=#e1c46d, tertiary=#a4d397, surface=#0e150c
**scheme-monochrome:** primary=#ffffff, secondary=#c6c6c6, tertiary=#e2e2e2, surface=#131313
**scheme-neutral:** primary=#bfcab7, secondary=#c2c8bc, tertiary=#baccb2, surface=#131412
**scheme-rainbow:** primary=#93d786, secondary=#baccb2, tertiary=#a0cfd3, surface=#131313
**scheme-tonal-spot:** primary=#a4d397, secondary=#baccb2, tertiary=#a0cfd3, surface=#11140f
**scheme-vibrant:** primary=#00e628, secondary=#a9d0b3, tertiary=#92d4bc, surface=#0e150c
