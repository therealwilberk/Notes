---
title: "Why I Switched from OpenClaw to Hermes Agent (And How to Do It)"
source: https://youtube.com/watch?v=Bt64sH6IdxI
type: youtube-notes
date: 2026-05-22
tags: [hermes-agent, openclaw, migration, comparison, memory, model-switching, telegram, skills]
parent: "[[MOCs/Hermes Agent MOC.md]]"
---

# Why I Switched from OpenClaw to Hermes Agent (And How to Do It)

## Key Concepts
- Hermes Agent is significantly more **stable** than OpenClaw — doesn't crash, updates don't break it
- **Model switching** is seamless mid-chat in Hermes (no restart needed), vs OpenClaw's limited model list
- Hermes memory is **persistent and accurate** across sessions using plain markdown files (`user.md`, `memory.md`)
- Active **builder community** with 65+ skills, plugins, memory backends
- **Local model friendly** — good integrations with Ollama, vLLM, llama.cpp
- Conversations can be exported as **Hugging Face-ready training data** (same harness Nous Research used to train Hermes)
- Migration from OpenClaw is a single command: `hermes claw migrate`

## Why Switch: 7 Reasons

### 1. Stability / Doesn't Crash
- OpenClaw crashed 2-3 times/week (gateway terminal would close randomly)
- OpenClaw updates broke it ~25% of the time (1 in 3-4 updates required revert)
- Hermes Agent: **zero crashes** in over a month of use
- Critical for remote/automated workflows — can't restart if you're away from laptop

### 2. Smooth Model Switching
- Hermes: `/model` command switches mid-chat, no restart needed
- Works with any OpenRouter model, local models, direct API
- OpenClaw: limited to pre-approved model list, couldn't use newest models (e.g., Qwench 3.6+3 was rejected)
- Hermes has **smart routing** — routes simple one-liners to cheap model, escalates complex prompts

### 3. Superior Memory
- Two plain markdown files: `~/.hermes/user.md` and `~/.hermes/memory.md`
- Open memory in any editor — fully transparent
- Remembers details from months ago (exact dates, cities, project specifics)
- OpenClaw memory was unreliable — daily logs often forgot, session-to-session retention was poor
- Hermes memory works out of the box with no extra plugins needed

### 4. Active Community
- Rapidly growing GitHub contributors
- 65+ community-built skills
- Active Twitter and Discord communities
- Memory backends, plugins, tooling all being built by community

### 5. Local Model Friendly
- Native integrations: Ollama, vLLM, llama.cpp, LM Studio
- Privacy-preserving (data stays local)
- Zero cost for local inference
- Good for experimentation with model architectures

### 6. Custom Skill Development
- Agent automatically creates skills as you work (e.g., created a Solana development skill on its own)
- Skills are specific to your workflow
- 5+ custom skills created automatically from work patterns

### 7. Training Data Export
- Conversations exportable in Hugging Face-ready format
- Same training harness used by Nous Research to train Hermes
- Useful for fine-tuning and reinforcement learning research

## Step-by-Step Migration from OpenClaw

### Prerequisites
- Hermes Agent installed (one-liner from Nous Research GitHub)
- Running in WSL (if on Windows)

### Migration Steps

1. **If OpenClaw was installed on Windows**, specify source path:
   ```bash
   hermes claw migrate --source /mnt/c/Users/<windows_username>/.openclaw
   ```

2. **Dry run first** to see what will migrate:
   ```bash
   hermes claw migrate --dry-run
   ```

3. **Create a fresh profile** to avoid overwriting existing Hermes config:
   ```bash
   hermes profile create openclaw-import
   hermes profile use openclaw-import
   ```

4. **Run migration with override** (for soul file):
   ```bash
   hermes claw migrate --source /mnt/c/Users/<username>/.openclaw --override
   ```

5. **Review preview** — shows exactly what migrates:
   - Soul (personality)
   - Memories (all historical)
   - User profile
   - Skills
   - Configuration
   - Telegram token

6. **Confirm migration** when prompted

7. **Add API keys manually** (or use `--migrate-secrets` flag):
   ```bash
   hermes claw migrate --migrate-secrets
   ```

### What Gets Migrated
- ✅ Soul / personality file
- ✅ All memories (including months-old history)
- ✅ User profile information
- ✅ Skills files
- ✅ Configuration
- ✅ Telegram token
- ⚠️ API keys — add manually or use `--migrate-secrets` flag
- ❌ WhatsApp — requires separate QR pairing

### Post-Migration
- Memories preserve full history (demonstrated remembering Polymarket research from 1+ month ago with exact dates and cities)
- Skills transfer and remain functional
- May need to adjust some settings depending on OpenClaw setup

## Tips & Gotchas
- If OpenClaw was on Windows and you're in WSL, use `--source` flag with `/mnt/c/Users/...` path
- Always create a new profile first to avoid conflicts with existing Hermes profiles
- WhatsApp migration requires manual QR re-pairing
- `--override` flag needed if soul file conflicts exist
- After migration, test in Telegram to verify everything works

## Timestamps & Chapters
- 0:00 - Intro: month-long comparison
- 2:05 - Reason 1: Stability (doesn't crash)
- 3:42 - Reason 2: Model switching
- 5:54 - Reason 3: Memory
- 8:15 - Reason 4: Community
- 9:18 - Reason 5: Local model friendly
- 10:08 - Reason 7: Training data export
- 11:01 - Migration walkthrough begins
- 11:18 - `hermes claw migrate` command and flags
- 13:01 - Creating fresh profile for import
- 14:18 - Running migration with override
- 15:35 - Migration complete, verification

## Summary
Hermes Agent outperforms OpenClaw in stability, model flexibility, memory persistence, and community ecosystem. Migration is straightforward via `hermes claw migrate` — create a fresh profile, run dry-run, then migrate with `--source` flag if needed. All memories, skills, and personality transfer over, preserving months of history. API keys need manual addition or the `--migrate-secrets` flag.
