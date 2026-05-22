---
title: "How to Set Up a Grok Sub in Hermes Agent (And Some Cool Ways to Use it)"
source: https://youtube.com/watch?v=sPK8oIGOOLY
type: youtube-notes
date: 2026-05-22
tags: [hermes-agent, grok, xai, supergrok, text-to-speech, image-generation, video-generation, provider]
---

# How to Set Up a Grok Sub in Hermes Agent

## Key Concepts
- xAI now offers Grok as an official provider inside Hermes Agent via **Super Grok subscription** (OAuth), separate from the direct API
- Grok 4.3 supports text conversations, Grok TTS (text-to-speech), and Grok Imagine (image + video generation)
- **1 million context window** — even larger than GPT 5.5's usable context window
- Grok has native X (Twitter) integration — can read/summarize tweets that other models can't fetch (X blocks direct HTTP access)
- Grok Imagine for video is a differentiator — OpenAI/Codex can't do video generation currently
- Responses are notably faster than other frontier models

## Prerequisites
- **Super Grok subscription** ($30/month) — NOT the Grok access from X Premium
- Free 3-day trial available (credit card required, auto-charges after trial)
- Website: grok.com

## Step-by-Step Setup/Configuration

1. **Update Hermes Agent** to get the latest provider list:
   ```bash
   hermes update
   ```
2. **Run Hermes setup** to add provider:
   ```bash
   hermes setup
   ```
3. Select **xAI Grok OAuth** from the provider list (NOT the direct API option)
4. Open the authorization URL in browser → authorize → connection confirmed
5. Select **Grok 4.3** as the model
6. Verify with `hermes chat` — confirm you see "Grok 4.3" and get a response

## Configuring Image Generation with Grok

1. Run Hermes tools:
   ```bash
   hermes tools
   ```
2. Navigate to: **Reconfigure an existing tools provider API key** → **Image generation**
3. Select **xAI Grok Imagine** (choose quality level: high quality or faster)
4. No separate API key needed — uses the OAuth subscription

## Configuring Video Generation with Grok

1. Run `hermes tools` → **Video generation** → select **xAI Grok Imagine**
2. **Critical gotcha**: Go to **Configure all platforms** and **check Video generation** — it may NOT be enabled by default
3. If unchecked, Grok won't be able to use the video tool at all

## Key Features Demonstrated

### X/Twitter Summarization
- Can directly read and summarize X posts that Claude and other models can't access (X returns HTTP 80 blocks to non-Grok agents)
- No X API costs — included in Super Grok subscription
- Prompt: "Please summarize this tweet" + link

### Text-to-Speech (Grok TTS)
- Configure via `hermes setup` → TTS provider → xAI
- Available voices (e.g., "E" voice)
- Significantly more natural-sounding than the default Edge TTS (Microsoft)
- Edge TTS sounds robotic by comparison

### Image Generation (Grok Imagine)
- ~27 seconds generation time
- Follows prompts more closely than GPT Images (doesn't add unprompted elements like credits)
- Fast overall response times

### Video Generation (Grok Imagine)
- Unique capability not available through Codex/OpenAI
- Can add audio/speech to generated video
- Prompt example: "Cartoon robots and shrimp working in a garage as the words OnChain AI Garage fall down and bounce on the ground"
- Beat MiniMax video generator in comparison test

### Coding/Spec Analysis
- Can read advanced spec files and design implementation plans
- Identifies weaknesses in specs and suggests improvements
- Grok Build (agentic CLI) is in early beta for Super Grok Heavy subscribers

## Tips & Gotchas
- **Credit card required** for free trial — will auto-charge after 3 days if not cancelled
- Super Grok ≠ X Premium Grok access — must be the standalone subscription
- Must run `hermes update` first if you haven't — OAuth option won't appear otherwise
- Video generation tool must be explicitly enabled in platform config
- 1M context window is a major advantage for large codebases/documents
- Grok's X integration is the primary differentiator vs Claude/GPT

## Timestamps & Chapters
- 0:00 - Intro: xAI + Hermes Agent announcement
- 2:36 - Setting up Super Grok account at grok.com
- 3:50 - Configuring Grok OAuth in Hermes Agent
- 5:27 - Testing basic chat with Grok 4.3
- 6:16 - X/Twitter post summarization (vs Claude's failure)
- 8:35 - Text-to-speech: Grok TTS vs Edge TTS comparison
- 10:35 - Image generation: Grok Imagine setup and demo
- 13:26 - Video generation: Grok Imagine setup and demo
- 16:39 - Spec file analysis and coding plan design

## Summary
Super Grok integrates into Hermes Agent as an OAuth provider, offering Grok 4.3 text (with 1M context), natural TTS, and Grok Imagine for image/video generation. The key differentiators are native X/Twitter data access, fast response times, and video generation capability that OpenAI currently lacks. Setup requires a $30/month Super Grok subscription and a few Hermes config steps. Video generation must be manually enabled in platform settings.
