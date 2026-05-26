---
type: research
tags: [theming, hyprland, rofi, wpick, pipeline]
created: 2026-05-25
status: in-progress
parent: "[[Projects/active/Dusky-Theme-Engine/Dusky-Theme-Engine.md]]"
---
# HyDE Theme Study — Pipeline Plan

**Status:** In Progress  
**Started:** 2026-05-25  
**Purpose:** Research HyDE's theme selector and rofi config to inform wpick's theme system design

## Pipeline

| Phase | Issue | Task | Agent | Status |
|-------|-------|------|-------|--------|
| 1 | HER-53 | Clone & Map Theme/Rofi Architecture | Hermes | Running |
| 2 | HER-54 | Theme Selector Deep Dive | Hermes | Pending |
| 3 | HER-55 | Rofi Config Deep Dive | Hermes | Pending |
| 4 | HER-56 | Assemble Obsidian Report | Hermes | Pending |

## Flow

```
Phase 1 (clone & map)
    ├── Phase 2 (theme selector)  ──┐
    └── Phase 3 (rofi config)    ──┤
                                    └── Phase 4 (assemble report)
```

Phases 2 and 3 run in parallel after Phase 1 completes.  
Phase 4 assembles everything into the final Obsidian note.

## Deliverables

- `/tmp/hyde-study/PHASE1-MAP.md` — Directory and file map
- `/tmp/hyde-study/PHASE2-THEME-SELECTOR.md` — Theme selector analysis
- `/tmp/hyde-study/PHASE3-ROFI.md` — Rofi config analysis
- `~/Documents/Text/Notes/Hyde-Theme-Study.md` — **Final report**

## Scope

Research only. No code changes to wpick.  
After completion, findings get discussed with opencode for wpick mapping.
