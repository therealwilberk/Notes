---
title: "Hermes Agent Masterclass: 1. Installation, Setup, Basic Commands"
source: https://youtube.com/watch?v=R3YOGfTBcQg
type: youtube-notes
date: 2026-05-22
tags: [hermes-agent, masterclass, 1, installation, setup, cli]
---

# Hermes Agent Masterclass: 1. Installation, Setup, Basic Commands

## Key Concepts
- Hermes Agent is an open-source AI agent built by Nous Research (the lab behind the Hermes model family)
- Provider-agnostic: works with Claude, GPT, Grok, Kimi, local Ollama models, etc.
- Runs as CLI in terminal or as gateway connecting to 16+ messaging platforms (Telegram, Discord, Slack, iMessage, WeChat)
- **Compounding value**: every session feeds the next — records trajectories, extracts reusable skills, gets faster and cheaper over time
- Compounding loop: Task → Record trajectory → Extract skill → Next run is faster
- A 3-month Hermes install is fundamentally better than a fresh one

## Prerequisites & Platform Support
- **macOS**: native support
- **Linux**: native support
- **Windows**: requires WSL 2 (Windows Subsystem for Linux)
- WSL install: `wsl --install` (in PowerShell as Administrator)
- Default WSL distro is Ubuntu; Debian also works

## Step-by-Step Setup/Configuration

1. **Install WSL** (Windows only): Open PowerShell as Admin → `wsl --install`
2. **Launch WSL**: `wsl` in PowerShell
3. **Quick install**: Clone from `nousresearch/hermes-agent` repo — single install command runs installer
4. **Dependencies auto-installed**: Python, Git, Node.js
5. **Choose setup mode**: Quick setup (fast defaults) or Full setup (all options)
6. **Configure AI provider** — pick from: Nous Portal, OpenRouter, Anthropic, OpenAI, Qwen, GitHub Copilot, Hugging Face
7. **Add API key** (e.g., OpenRouter: go to openrouter.com → get API key → paste `sk-...`)
8. **Select model** (e.g., Mimo V2 Pro via OpenRouter, or cheaper options)
9. **Configure fallback/rotation**: Add second API key for auto-rotation when primary is rate-limited or exhausted
10. **Set max tool calling**: 90 recommended
11. **Tool progress**: All (show every call), Only New, or Off
12. **Context compression threshold**: 0.75 is middle ground (higher = later compression, depends on model context window)
13. **Session reset mode**: Inactivity + Daily reset recommended
14. **Platforms**: Skip during initial setup — configure in Episode 2
15. **Search provider**: Tavily (AI-native) or DuckDuckGo (free). Tavily gives 1,000 free credits at tavily.com
16. **Image generation**: FAL.ai (optional, sign in with GitHub)

## Key Files & Paths

Everything lives in `~/.hermes/`:
```bash
~/.hermes/
├── config.yaml      # Main configuration (settings)
├── .env             # Secrets: API keys, passwords
├── memories/        # memory.md and user.md
├── sessions/        # Every past conversation
├── skills/          # Built-in and installed skills
├── logs/            # Agent logs and error logs
├── state.db         # SQLite DB with all session data
└── .sole_file       # History
```

⚠️ **Do NOT manually edit** `sessions/` or `crone/` — ask the agent to do it.

## Commands & Config Snippets

### CLI Commands
```bash
hermes chat          # Launch TUI (terminal user interface)
hermes gateway       # Start messaging gateway (for Telegram/Discord)
hermes doctor        # Check for issues
hermes model         # Switch provider/model interactively
hermes status        # Show full configuration (providers, keys, paths)
hermes insights      # Usage statistics
hermes sessions browse  # Cursor picker to resume sessions
hermes skills browse    # Discover and install skills
hermes skills search "email"  # Search for specific skills
hermes config show   # Display configuration
hermes update        # Pull latest version
```

### In-Chat Slash Commands
```
/new                  # Start fresh conversation
/model                # Swap model mid-session (e.g., /model zai/glm-5.1)
/fast                 # Priority routing through OpenAI/Anthropic
/background "prompt"  # Side task while Hermes is working
/Q "prompt"           # Queue next task
/compress             # Manually compact context
/skills               # Browse or invoke skills
/yolo                 # Toggle dangerous command approvals (careful!)
/help                 # List all commands and skills
/exit                 # Exit chat
```

### Setting up web search (Tavily)
```bash
# 1. Get API key from tavily.com (1000 free credits)
# 2. Add via setup:
hermes setup          # Quick setup → configure missing items
# Toggle Tavily API key → paste key
# Verify:
hermes status         # Check Tavily is set
```

## Tips & Gotchas
- **Provider rotation** is powerful: set up a fallback API key so sessions don't interrupt when primary is exhausted
- **Web search** is essential for real tasks — configure Tavily or DuckDuckGo early
- The agent auto-creates `memory.md` and `user.md` from your first conversation
- **Compounding value** is real: memory files grow, skills get extracted, trajectories improve over time
- If `hermes` command doesn't work after install, reload your shell (`source ~/.bashrc` or restart terminal)
- `/model` mid-session is seamless — no restart needed

## Timestamps & Chapters
- 0:00 - Introduction & what is Hermes Agent
- 2:17 - Compounding value thesis
- 5:10 - Platform support & prerequisites
- 7:00 - WSL setup for Windows
- 9:00 - One-command install
- 11:00 - Full setup walkthrough (providers, API keys)
- 17:00 - Configuration options (compression, sessions, platforms)
- 22:00 - First launch & CLI commands tour
- 25:00 - In-chat slash commands
- 27:00 - Where files live (`~/.hermes/`)
- 28:00 - Live demo: competitor research task

## Summary
First module covers full Hermes Agent installation from scratch on Windows (via WSL), Linux, or macOS. Walks through provider selection (OpenRouter recommended for beginners), API key setup, and a complete tour of CLI commands (`hermes chat`, `hermes status`, `hermes skills browse`) and in-chat slash commands (`/model`, `/compress`, `/skills`). Demonstrates the compounding value thesis with a live competitor research task showing the agent's web search and memory in action.
