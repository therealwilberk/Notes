---
title: "How Hermes Agent Can Save You 85% (Or More) in BG Task Token Cost"
source: https://youtube.com/watch?v=NoF-YajElIM
type: youtube-notes
date: 2026-05-22
tags: [hermes-agent, auxiliary-models, cost-optimization, config, open-router, local-llm, compression]
---

# How Hermes Agent Can Save You 85%+ in Background Task Token Cost

## Key Concepts
- Hermes runs **8 background (auxiliary) tasks** silently on top of your chat — most users never configure them
- By default, auxiliary tasks either **inherit your expensive main model** (Opus, Sonnet, GPT-5) or fall back to Gemini Flash via an auto-detect chain (OpenRouter → NeuPortal → Codex)
- Each task has different needs — you should match the model to the task
- **Compression is the #1 cost driver** — fires every time context fills to threshold (10-20x/day for heavy users)
- Going **local** for auxiliary tasks makes them cost $0 while keeping your frontier model for main chat
- Demonstrated **85% savings** on compression: Opus = $0.13/pass vs Kimi K2 = ~$0.02/pass (50K token window)

## The 8 Auxiliary Tasks

| Task | What It Does | Cost Priority |
|------|-------------|---------------|
| **Compression** | Summarizes conversation when context hits threshold | 🔴 Highest — fires 10-20x/day |
| **Flush Memories** | Writes durable facts from chat to memory files on session end (`/new`, `/end`) | 🟡 Medium |
| **Web Extract** | Summarizes web pages after Hermes fetches them | 🟡 Medium (if doing research) |
| **Vision** | Analyzes images and browser screenshots | 🟡 Per-call expensive (images eat tokens) |
| **Session Search** | Summarizes past sessions when searching | 🟢 Lower |
| **Skills Hub** | Matches query to installed skill | 🟢 Lower |
| **MCP Dispatch** | Dispatches MCP tool calls | 🟢 Lower |
| **Approval** | Classifies risky commands in smart approval mode | 🟢 Lower |

## Step-by-Step Setup/Configuration

1. **Locate config file:**
   - Path: `~/.hermes/config.yaml`
   - On WSL: navigate to `\\wsl$\Ubuntu\home\<username>\.hermes\config.yaml`
   - Look around line 100 for the `auxiliary:` section

2. **Configure each auxiliary task** with provider + model:
   ```yaml
   auxiliary:
     compression:
       provider: openrouter
       model: moonshotai/kimi-k2
     flush_memories:
       provider: openrouter
       model: openai/gpt-4o-mini
     web_extract:
       provider: anthropic
       model: claude-haiku-4-5
     vision:
       provider: openrouter
       model: google/gemini-2.5-flash
   ```

3. **Restart session** after config changes — new session required to pick up changes

4. **Verify** by checking API spend before/after compression

## Using Local Models for Auxiliary Tasks

```yaml
auxiliary:
  compression:
    base_url: http://localhost:11434  # Ollama example
    model: llama3
    api_key: placeholder  # Not actually used, but required
    timeout: 120  # Set higher for local (slower inference)
```

- Setting `base_url` **overrides** the `provider` field — Hermes goes directly to your local endpoint
- Common local providers: **Ollama**, **LM Studio**, **vLLM**, **llama.cpp**
- API key can be literally `"placeholder"` — not used for local

## Recommended Model Choices

- **Compression:** Kimi K2, Claude Haiku 4.5, Gemini 2.5 Flash — need clean summaries + long context handling
- **Flush Memories:** GPT-4o Mini, Gemini 4.5 Flash — small, fast, structured extraction
- **Web Extract:** Claude Haiku 4.5, Gemini Flash — want factual preservation (worth a slightly heavier model if doing lots of research)
- **Vision:** Must be multimodal — Gemini 2.5 Flash, GPT-4o, GLM 5D Turbo

## Compression Config: Gotcha! ⚠️

There are **TWO places** to set compression config:
1. **Top-level** `compression:` in config.yaml
2. **Auxiliary** `auxiliary.compression:` section

- If **both are set**, `auxiliary.compression` wins
- If you set `provider: auto` in auxiliary, it **overrides your top-level choice** and falls back to Gemini Flash
- This is why you might see mysterious Gemini Flash charges even with OpenRouter configured

## Cost Math (Real-World)

- **15 compressions/day with Opus API:** ~$60/month
- **15 compressions/day with Kimi K2:** ~$9/month
- **15 compressions/day with local model:** $0/month
- **Savings: $50+/month** on compression alone — stack with other tasks for more

## Tips & Gotchas
- Default `auto` setting routes through OpenRouter → NeuPortal → Codex → Gemini Flash — you may get surprise Gemini charges
- After changing config, you **must start a new session** for changes to take effect
- Vision model must be multimodal — don't set a text-only model for vision tasks
- If your local model can't handle your main coding task, it can still handle auxiliary tasks for free savings
- Config version matters — Hermes updates frequently (as of April 2026), check docs for latest task list

## Timestamps & Chapters
- 0:00 - Intro: 8 hidden auxiliary models
- 0:38 - Why auxiliary costs matter (frontier model users)
- 1:47 - The 8 tasks explained
- 4:04 - Where to find config (WSL path walkthrough)
- 6:20 - Recommended models per task
- 7:41 - Going local with auxiliary tasks
- 9:09 - Compression config gotcha (two locations)
- 10:31 - Live demo: Opus vs Kimi K2 compression cost
- 16:45 - Summary and real-world savings math

## Summary
Hermes Agent silently runs 8 background auxiliary tasks that most users never configure. By default they either inherit your expensive frontier model or auto-route to Gemini Flash. Setting explicit cheap/local models for each task — especially compression — can save $50+/month. The config lives in `~/.hermes/config.yaml` under the `auxiliary:` section, and local models work by setting `base_url` to your local server endpoint.
