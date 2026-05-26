---
title: "Hermes Agent Masterclass: 3. Memory, Plugins, Honcho, and Obsidian"
source: https://youtube.com/watch?v=ZKZLko9kLm4
type: youtube-notes
date: 2026-05-22
tags: [hermes-agent, masterclass, 3, memory, honcho, obsidian, plugins]
parent: "[[MOCs/Hermes Agent MOC.md]]"
---

# Hermes Agent Masterclass: 3. Memory, Plugins, Honcho, and Obsidian

## Key Concepts
- Hermes has **4 memory layers** that stack (not alternatives — all can run simultaneously)
- **Layer 1**: Built-in markdown files (`memory.md` + `user.md`)
- **Layer 2**: FTS5 session search over `state.db` (SQLite, always on)
- **Layer 3**: External provider plugins (Honcho, Memo, Hindsight, Supermemory, etc.)
- **Layer 4**: Obsidian vault skill (structured knowledge base)
- Only **one** memory provider can be active at a time (can't run Honcho + Memo simultaneously)
- Built-in markdown layer is **always on** even with a provider configured
- Switching providers does **NOT** migrate data between them

## Layer 1: Built-in Markdown Memory

### Files
- **Location**: `~/.hermes/memories/`
- **`memory.md`**: Agent's notes about projects, environment, decisions, lessons learned
  - Cap: **2,200 characters** (~800 tokens system prompt budget)
  - Entries separated by `§` (section sign character)
- **`user.md`**: Agent's model of who you are (persona, preferences, communication style)
  - Cap: **1,375 characters** (~500 tokens)
  - Default cap configurable in `config.yaml` under `memory`

### How It Works
- Loaded from disk **once** at session start → frozen snapshot into system prompt
- Agent has a `memory` tool with 3 actions: `add`, `replace`, `remove`
- **No read action**: content is auto-injected into system prompt
- **Replace/remove**: uses substring matching via `old_text` parameter (short unique substring is enough)
- **Duplicate detection**: automatic, returns success silently (no-op, not error)
- **Injection scanning**: entries scanned for prompt injection & credential exfiltration before acceptance

### Frozen Snapshot Pattern
```
Session Start:  memory.md → loaded → system prompt (cached)
Mid-Session:    memory tool writes → disk updated immediately
                BUT system prompt does NOT update until next session
Why:            Changing system prompt mid-session invalidates prompt cache
                Cache = affordable long sessions
```
⚠️ **Memory writes don't appear in the same session — only in the next one.**

### 4 Invisible Safety Features
1. **Cap as feature**: Character limit forces curation. Agent sees usage % in header. Error on overflow.
2. **Save/skip policy**: Ships with clear rules — save: preferences, environment, facts, corrections, conventions. Skip: trivial questions, web-searchable facts, raw data dumps.
3. **Duplicate detection is no-op**: Silent dedup prevents LLM retries from filling memory with slightly different versions of the same fact.
4. **Injection scanning**: Scans for prompt injection patterns, credential exfiltration (SSH keys in facts, invisible Unicode) before accepting entries.

### Seeding Tips
- Manually seed `user.md` with a few key facts about yourself
- Note your short-term goals and active projects
- Keep within the 1,375 character cap

## Layer 2: FTS5 Session Search

- **Database**: `~/.hermes/state.db` (SQLite with FTS5 full-text index)
- **Contains**: Every CLI session, every Telegram message, every Discord exchange
- **How it works**: Agent has `session_search` tool — queries conversation history full-text
- **Summarization**: Results come back with Gemini Flash summarization layer (agent doesn't re-read raw transcripts)
- **Autonomous**: Agent calls this automatically when it expects prior conversation might be relevant
- **Auto-maintenance**: Prune + vacuum on `state.db` at startup (no cron job needed)
- **Cost**: On-demand tokens (only when searched, unlike fixed cost of memory files)

### Comparison: Persistent Memory vs Session Search
| Feature | Persistent (Layer 1) | Session Search (Layer 2) |
|---------|---------------------|-------------------------|
| Capacity | ~1,300 tokens fixed | Unlimited (all sessions) |
| Speed | Instant (in context) | Slower (search + summarize) |
| Use Case | Key facts, always available | "Did we discuss X last week?" |
| Management | Agent-managed | Automatic (every session indexed) |
| Token Cost | Fixed | On-demand |

## Layer 3: Memory Provider Plugins

### Plugin Architecture
- Introduced in Hermes v0.7: pluggable memory provider ABC
- Third-party backends implement interface, register via plugin loader
- **One provider active at a time** — pick one, switch later if needed
- **Switching does NOT migrate data** — plan carefully
- Built-in markdown layer always on alongside provider

### When provider is active, Hermes automatically:
1. Injects provider context into system prompt
2. Prefetches relevant memories before each turn
3. Syncs conversation turns to provider after each response
4. Extracts memories on session end
5. Adds provider-specific tools

### Setup Commands
```bash
hermes memory setup    # Interactive: pick provider, add API key
hermes memory status   # Check current provider
hermes memory off      # Disable provider (built-in remains)
```

### Provider Landscape

**Honcho** (demoed in video) — Nous Research first-party
- Dialectic user modeling: builds running model of preferences, communication patterns, goals
- Hierarchy: Workspace → Peers → Sessions → Messages
- Tools: `honcho_conclude`, `honcho_context`, `honcho_profile`, `honcho_search`
- Config: `~/.hermes/honcho.json`
- Hosting: Cloud (app.honcho.dev) or self-host free
- Key config options: recall_mode, write_frequency (async/per-turn/per-session), dialectic_reasoning_level (minimal→max)
- v0.11.0 shipped major overhaul: auto context injection, cost safety, session isolation

**Memo** — most popular by repo stars
- Server-side LLM extraction: LLM extracts discrete facts, second LLM pass decides insert/update/delete/no-op
- Embeds extracted facts (not raw text) → less recall noise
- Adds LM cost on every write

**Hindsight** — knowledge graph + entity resolution
- Stores full conversation turns with metadata, builds entity relationships
- 3 retrieval strategies
- `reflect` tool: synthesizes across memories (unique in ecosystem)
- Best for: explicit entity relationships needed

**Supermemory** — multi-container partitioning
- Each container gets own retention, search mode, identity
- Context fencing: strips already-recalled memories to prevent recursive pollution
- Session graph ingest at session end
- Best for: multiple memory namespaces (per client/project/team)

### Step-by-Step: Honcho Setup

1. Go to **app.honcho.dev** → sign up
2. Add credit card → get 100 free credits (promotion may vary)
3. Copy API key
4. Run: `hermes memory setup`
5. Select **Honcho** from provider list
6. Choose **Cloud** or local
7. Paste API key
8. Configure:
   - Username: your name
   - AI peer name: e.g., "Hermes"
   - Workspace ID: e.g., "hermes"
   - Observational mode: directional (default, recommended)
   - Write frequency: async (no token cost, recommended)
   - Recall mode: hybrid (default)
   - Dialectic cadence: 2 (every other turn, recommended)
   - Dialectic reasoning level: medium or max
   - Session strategy: per session
9. Verify: `hermes honcho status`

### Honcho Commands
```bash
hermes honcho status      # Check status & observations
hermes honcho peer        # View user & AI peer identities
hermes honcho config      # Show configuration
hermes honcho mode        # Change recall/observation modes
hermes honcho map         # Map directory to session name
```

## Layer 4: Obsidian Vault Skill

- **NOT a plugin** — it's a bundled skill at `skills/note-taking/obsidian`
- File system-based: no MCP server, no Obsidian app needed (works on headless Linux)
- Environment variable: `OBSIDIAN_VAULT_PATH` (set default path)
- ⚠️ The `obsidian_vault` option in config is **no longer in use** — use env var

### How to Use
1. Install Obsidian app locally (optional — for viewing/curating notes)
2. Open a folder as vault
3. Set vault path in environment variables to match
4. In chat: say "use Obsidian skill" or use `/obsidian` slash command
5. Agent creates structured wiki-linked markdown notes in the vault

### When to Use Obsidian
- Large projects with lots of data (not simple memory)
- Long-term knowledge bases you'll return to
- Structured research (providers, models, domain knowledge)
- Agent writes organized markdown with wiki-links for easy retrieval

### Commands
```
/obsidian read <query>     # Read from vault
/obsidian search <query>   # Search vault
/obsidian create <note>    # Create new note
```

## Tips & Gotchas
- **Frozen snapshot** is critical to understand: memory writes mid-session don't appear until next session
- **Don't make memory caps too large**: fills context window with memories instead of actual work
- **Switching providers doesn't migrate data**: if you used Honcho for 3 months then switch to Memo, Honcho memories don't follow
- **Agent auto-manages memory**: it decides what to consolidate when cap is reached — trust the save/skip policy
- **Session search is autonomous**: you don't prompt for it, agent calls it when relevant
- **Auto-prune** on `state.db` means no manual cleanup needed
- The 4 memory layers are **additive** — run all 4 simultaneously for maximum coverage
- **Seed user.md yourself** with key facts for better initial context
- Honcho's dialectic reasoning is unique: models *you* as a person, not just facts about you

## Timestamps & Chapters
- 0:00 - Introduction & memory overview
- 2:00 - Four memory layers explained
- 4:00 - Layer 1: Built-in markdown memory deep dive
- 6:45 - Memory tool actions (add, replace, remove)
- 8:30 - Why it works: 4 invisible safety features
- 10:00 - Frozen snapshot pattern
- 11:15 - Layer 2: FTS5 session search
- 14:00 - Layer comparison table
- 15:00 - Layer 3: Memory provider plugins overview
- 16:00 - Provider landscape (Memo, Hindsight, Supermemory)
- 18:00 - Honcho deep dive & setup demo
- 25:00 - Layer 4: Obsidian vault skill
- 28:00 - Live demo: storing research in Obsidian vault
- 31:30 - All four layers summary
- 33:00 - Preview of Episode 4 (Skills)

## Summary
Module 3 dissects Hermes's 4-layer memory system: built-in markdown files (memory.md/user.md with safety features like injection scanning and dedup), FTS5 session search over SQLite, pluggable providers (Honcho demoed with dialectic user modeling), and the Obsidian vault skill for structured long-term knowledge. Key insight: these layers stack — run all four simultaneously. The frozen snapshot pattern (system prompt cached at session start) means memory writes don't appear until next session, which is critical for understanding agent behavior.
