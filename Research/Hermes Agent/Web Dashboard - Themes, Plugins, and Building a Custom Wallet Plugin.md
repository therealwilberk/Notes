---
title: "Hermes Agent Web Dashboard Themes + Plugins: I Built My Own Plugin!"
source: https://youtube.com/watch?v=kLDUh20-AJA
type: youtube-notes
date: 2026-05-22
tags: [hermes-agent, dashboard, plugins, themes, wallet, solana, jupiter-api, community]
parent: "[[MOCs/Hermes Agent MOC.md]]"
---

# Hermes Agent Web Dashboard: Themes, Plugins & Building a Custom Wallet Plugin

## Key Concepts
- New **local web dashboard** for managing Hermes Agent — browser-based, highly customizable
- Launch with `hermes dashboard` — starts local server, opens in browser
- Dashboard sections: Sessions, Analytics, Logs, Cron, Skills, Config, Keys, Docs
- Supports **themes** (color schemes), **UI plugins**, and **backend plugins**
- Community-built plugins installable via repo URL
- Built a **crypto wallet plugin** from scratch using Hermes Agent itself
- Plugin SDK docs are critical — include them in your spec file

## Dashboard Features

### Built-in Sections
- **Sessions:** Browse all past sessions (CLI, TUI, cron source labeled)
- **Analytics:** Token usage, per-model breakdown, daily/30-day stats, top skills
- **Logs:** Gateway logs, agent.log files, error filtering
- **Cron:** List/add scheduled jobs
- **Skills:** All installed skills + toolsets
- **Config:** Edit `config.yaml` directly in browser (agent max turns, personality, memory, etc.)
- **Keys:** Store all provider API keys (OpenRouter, Anthropic, Tavily, etc.)
- **Docs:** Full documentation reference
- **Gateway controls:** Restart gateway, update Hermes from dashboard

### Built-in Themes
- **Hermes Teal** (default) — green, papery texture
- **Midnight** — deep blue
- **Ember** — warm tones
- **Cyberpunk** — very dark
- **Rosé** — pink tones
- Language switching (e.g., Chinese)

## Installing Community Plugins

### Chronos Forge Command Center (by JoeyNYC / AI Joey)
```bash
# In Hermes TUI, paste the repo URL and say "install it"
# Or clone and run install script
git clone <repo-url>
# Plugin appears under Sessions → Command Center tab
```

Features: token burn tracking, skill heat map, source mix, model burn, capabilities overview — single command center view.

### General Plugin Install Pattern
1. Clone the plugin repo
2. Run the install script (or paste repo URL in Hermes TUI)
3. Plugin appears in dashboard navigation
4. `hermes dashboard` restart to load

## Building a Custom Wallet Plugin

### Why
- Agents increasingly need wallets for trading, X402 payments, API purchases
- Phantom MCP server had issues — simpler manual import approach chosen
- Supports **Solana** and **EVM** chains

### Architecture
- **Backend API** for wallet management + balance fetching
- **Storage** for wallet addresses (JSON file)
- **Jupiter API** for Solana token metadata + prices (raw chain only gives address + balance, no ticker/prices)
- **Dust filtering** to hide scam/spam tokens
- **Frontend** portfolio table with token name, balance, USD value

### Building Process
1. **Write a thorough spec file** — agent reads this to build the plugin
2. **Include links to dashboard plugin SDK docs** — critical for accurate building
3. Give spec to Hermes Agent in TUI
4. Agent builds plugin structure, implements backend + frontend
5. Restart dashboard to load

### Spec File Must Include
- Plugin purpose and features
- **Links to dashboard plugin SDK reference docs**
- Technical requirements (RPC endpoints, APIs)
- UI layout description
- Data flow (addresses → fetch balances → enrich with Jupiter → display)

### What Got Built
- ✅ "Watch Wallets" tab in dashboard navigation
- ✅ Add wallet by address (Solana or EVM)
- ✅ Fetch balances from chain RPCs
- ✅ Enrich with Jupiter API (token name, ticker, USD price)
- ✅ Portfolio table with balance + USD value
- ✅ Dust/scam token filtering
- ✅ Import/export JSON for bulk operations
- ✅ Copy address, remove wallet

### Debug: Token-2022 Program
- One token lookup failed initially — Token-2022 program address wasn't handled
- Quick fix: agent patched it immediately
- After fix, all tokens (including newer Token-2022 standard) resolved correctly

### Open Source
- Repository: `tombiostudio/hermes-dashboard-wallet`
- Install: clone repo + run install script

## Config Editing via Dashboard
- No need to manually edit `config.yaml`
- Change: agent max turns, personality, memory functions, memory plugins
- All provider API keys stored and editable
- Changes apply on gateway restart

## Tips & Gotchas
- **Include plugin SDK docs links in your spec** — without them, agent struggles to build correctly
- Jupiter API required for Solana token metadata (raw RPC only gives address + balance)
- Token-2022 program needs separate handling vs standard SPL tokens
- Dust filtering is important — every wallet accumulates scam tokens
- Restart dashboard after installing plugins to see them
- Community plugins: just paste repo URL in Hermes TUI and say "install it"
- Themes switch instantly — no restart needed

## Timestamps & Chapters
- 0:01 - Intro: new local web dashboard
- 1:47 - Starting the dashboard (`hermes dashboard`)
- 2:08 - Dashboard overview: sessions, analytics, logs
- 3:05 - Analytics deep dive: token usage, per-model stats
- 4:27 - Skills and toolsets view
- 5:00 - Config editing, keys, docs
- 6:10 - Theme demos (Teal, Midnight, Cyberpunk, Rosé)
- 7:05 - Installing Chronos Forge community plugin
- 9:16 - Planning custom wallet plugin
- 10:46 - Spec file and build process
- 13:15 - Testing the wallet plugin (adding Solana wallet)
- 14:52 - Portfolio view with Jupiter-enriched token data
- 15:44 - Token-2022 bug fix
- 16:45 - Open source release

## Summary
The Hermes Agent web dashboard (`hermes dashboard`) provides a full browser-based management UI with sessions, analytics, config editing, and extensibility via themes and plugins. Community plugins install with a repo URL. Built a crypto wallet plugin that fetches Solana/EVM balances, enriches with Jupiter API for token metadata/prices, and displays a clean portfolio table. Key success factor: include dashboard plugin SDK docs in your spec file for accurate code generation.
