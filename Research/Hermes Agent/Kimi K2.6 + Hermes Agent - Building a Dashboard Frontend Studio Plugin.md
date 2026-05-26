---
title: "Kimi K2.6 + Hermes Agent: The Coding Duo that Built My Dashboard Frontend Studio"
source: https://youtube.com/watch?v=C-4UqgXY0KM
type: youtube-notes
date: 2026-05-22
tags: [hermes-agent, kimi-k2.6, dashboard, plugins, frontend, vite, openrouter, hackathon]
parent: "[[MOCs/Hermes Agent MOC.md]]"
---

# Kimi K2.6 + Hermes Agent: Building a Dashboard Frontend Studio Plugin

## Key Concepts
- Built **Hermes Canvas** — a dashboard plugin that turns the web dashboard into a live frontend creation studio
- Used **Kimi K2.6** via OpenRouter for the entire build (good at visual analysis + frontend coding)
- Plugin creates a **split-pane layout**: chat on left, live preview iframe on right
- Hermes Agent can build its own dashboard plugins using the **dashboard plugin system**
- Uses **Git worktrees** for isolated project editing — each edit runs in a separate worktree
- Changes **hot-reload** via Vite dev server integration
- Total build cost: ~$7 for an hour+ of complex coding (compared to much more with Opus API)

## Architecture

### How It Works
1. User opens Hermes Dashboard → clicks "Canvas" tab
2. Frontend preview shows an **iframe** pointing to local dev server (e.g., Vite on port 5173)
3. User types prompt in "Prompt Hermes" text area
4. Hermes spawns as subprocess with frontend-editing system prompt
5. Hermes edits project files in isolated Git worktree
6. Changes sync back to main directory → Vite hot-reloads

### Key Technical Decisions
- **Plain JS** using `React.createElement` — no bundler for hackathon speed
- **Git worktrees** for isolation — prevents concurrent edit conflicts
- **Vite** for dev server + hot reload
- Backend mounts routes for project management + status endpoint

## Building the Plugin

### Prompt Used to Start
```
Please review Hermes Canvas Hackathon spec.md in the directory. 
Do any necessary research. Then plan out this project.
Check the following pages for details about the dashboard:
[link to Hermes Agent dashboard docs]
```

### Important: Be Explicit About No Shortcuts
- LLMs (including Kimi) tend to build the smallest possible MVP
- **Explicitly tell it**: "Please don't take shortcuts. Build out the entire plugin."
- Otherwise you get a skeleton that isn't actually useful

### What Got Built
- ✅ Backend API for project management
- ✅ Frontend split-pane layout (chat + preview)
- ✅ Vite dev server integration
- ✅ Selection mode (click elements to target edits)
- ✅ Hot reload on file changes
- ✅ Git worktree isolation per edit job
- ✅ Status endpoint for dev server

## Selection Mode
- Click specific UI elements to select them
- Selected element info shown (tag, class, etc.)
- Type prompt → "Send to Hermes" → targeted edit
- Works for React-based projects (not plain HTML — requires structured JSON)

## Bug Found & Fixed: Worktree State Persistence
**Problem:** Each worktree created a new isolated branch from original HEAD commit. Making change A then change B would revert change A.

**Fix:** Commit synced changes back to main repo after each job. Next worktree starts from last committed state.

```bash
# The fix: auto-commit after each Hermes edit job
git add -A && git commit -m "Hermes canvas edit"
```

## Using It on Existing Sites
- Drop any project into Hermes Agent's directory
- Open in Canvas tab → live preview
- Edit via chat prompts (e.g., "remove the header at the top", "change button color to red")
- Works with existing Vite/React projects

## Cost & Performance
- Planning + research: $0.20
- Full build (1 hour): ~$4-7 total
- Kimi K2.6 via OpenRouter — significantly cheaper than Opus API
- Good balance of coding ability + visual analysis

## Tips & Gotchas
- Include **links to dashboard plugin docs** in your spec file — agent builds much more accurately
- Tell it explicitly not to take shortcuts / build MVP skeleton
- Selection mode only works with structured projects (React/JSON), not plain HTML
- Git must be initialized in project — backend should auto-init git on project creation
- Each edit creates a new worktree — must commit between edits or changes get lost
- Test cost was $7 for 1+ hour session — cheap compared to Opus API

## Timestamps & Chapters
- 0:00 - Intro: building Hermes Canvas dashboard plugin
- 0:32 - Dashboard overview and split-pane concept
- 3:30 - Using Hermes Agent itself (not Claude Code/Codex) for the build
- 4:20 - Kimi K2.6 model choice via OpenRouter
- 4:49 - Opening prompt and research phase
- 8:26 - Plugin manifest and structure being written
- 11:05 - Testing: dashboard Canvas tab live
- 12:17 - Prompt-based editing demo (change button color)
- 14:43 - Selection mode demo
- 15:48 - Worktree bug discovered and fixed
- 17:35 - Testing on existing website (Tombio Studio)
- 20:20 - Final layout tweaks and summary

## Open Source
- Repository: `tombiostudio/hermes-canvas` on GitHub
- Submitted to Nous Research creative hackathon

## Summary
Built a Hermes Agent dashboard plugin called "Hermes Canvas" using Kimi K2.6 via OpenRouter. The plugin creates a split-pane UI with chat + live frontend preview, supporting prompt-based and selection-mode editing with hot reload. Key learning: include dashboard plugin docs in spec, explicitly forbid shortcuts, and ensure Git worktree state persists between edits via auto-commit. Total cost ~$7 for an hour of complex coding.
