---
title: "Hermes Agent + HyperFrames: Free Open-Source AI Tools to Create Amazing Videos"
source: https://youtube.com/watch?v=1IsskexiCSw
type: youtube-notes
date: 2026-05-22
tags: [hermes-agent, hyperframes, video-creation, html, canvas, skills, content-creation, shorts]
parent: "[[MOCs/Hermes Agent MOC.md]]"
---

# Hermes Agent + HyperFrames: AI Video Creation with Web Tech

## Key Concepts
- **HyperFrames** = open-source framework for making videos using web technology (HTML, CSS, JavaScript, GSAP, Canvas, WebGL, FFmpeg)
- AI agents understand HTML very well → can generate/edit HyperFrames compositions more reliably than operating traditional video editors
- No video generation model needed — avoids expensive API costs or heavy local GPU requirements
- Great for: website → product videos, animated charts/explainers, kinetic typography shorts
- Hermes Agent has a **HyperFrames skill** (installable from the skills marketplace)
- Can combine with other skills (X posts, YouTube embeds, GitHub repo analysis) for rich compositions

## Step-by-Step Setup

### 1. Update Hermes Agent
```bash
hermes update
```
HyperFrames skill is in a recent release.

### 2. Install the HyperFrames Skill
Simply ask your agent:
```
Install the HyperFrames skill
```
Or point to the specific skill file from the GitHub repo:
- `nousresearch/hermes-agent` → skills → creative → HyperFrames → skill.md
- URL: `https://github.com/nousresearch/hermes-agent/blob/main/skills/creative/hyperframes/skill.md`

### 3. Load the Skill
```
/hyperframes
```
The skill will prompt: "What HyperFrames video should I create?"
Options include: vertical shorts, animated title cards, HTML slides → video conversion, etc.

## Workflow Patterns

### Pattern 1: HTML Slides → Explainer Video
**Prompt example**:
```
Use HyperFrames to turn this existing HTML slide deck into a 16x9 video.
Path: /path/to/slides.html
Make it feel like a [brand] explainer. Add animated title reveals, bullet
point timing, slide in/out transitions, simple lower captions, and a
progress bar. Keep existing slide style. Use 6 seconds per slide.
```
- ~9 minutes generation time for a slide deck
- Produces smooth transitions, timed element reveals, captions, progress bar

### Pattern 2: Reusable YouTube Shorts Template
**Prompt example**:
```
Create a reusable 9:16 YouTube Shorts template from this style.
Use transcript: [paste transcript snippet]
- 35-second short
- Hook text and opener using character image
- Animated captions
- CTA at the end for YouTube channel
- Make as a reusable template
- Create images where appropriate
```
- Once template is created, just drop new transcripts to auto-generate new shorts
- Great for automating short-form content pipeline via cron jobs

### Pattern 3: Website → Promotional Video
**Prompt example**:
```
/website-to-hyperframes create a 25-second promotional video for
onchainai.com promoting the AI Garage Weekly letter.
```
- HyperFrames captures website: screenshots, visible text, colors, fonts, page sections
- Turns source material into script → design reference → storyboard → video
- Hermes Agent Studio shows live preview at localhost during generation
- **Use preview to catch bugs** — assets may not render correctly on first pass

### Pattern 4: GitHub Repo → Architecture Explainer
- Point HyperFrames at a GitHub repo
- Agent reads repo structure and creates animated architecture breakdown
- Combines with **registry blocks**: X post embeds, Reddit posts, YouTube subscribe buttons

### Pattern 5: Advanced HTML/Canvas VFX
- UI shattering into glass effect
- Website content mapped into 3D phone
- Liquid backgrounds
- These require HTML + Canvas composition skills

**Tip**: For advanced effects, point agent to the official HyperFrames docs:
- HTML and Canvas section has specific instructions
- Agent may struggle with complex effects on first pass — iterate

## Registry Blocks (Social Native Elements)
HyperFrames supports embedding:
- **X/Twitter posts** (fake or real quote style)
- **Reddit posts**
- **YouTube** (subscribe buttons, lower thirds)
- **TikTok embeds**
- These create native-looking social media elements in videos

## Prompt Engineering Tips
- **Work with another Hermes agent** to refine prompts — e.g., have "Shrimple" research HyperFrames capabilities and draft detailed prompts
- Build a **knowledge base** about HyperFrames for your agent to reference
- More specific prompts = better results (scenes, motion direction, audio direction)
- Detailed prompts: specify style, core message, scene-by-scene breakdown, motion/audio direction
- Save prompts in a repo for reuse (e.g., `tombstudio/hyperframes-prompts`)
- **Don't expect one-shot perfection** on complex compositions — iterate with feedback

## Agent Studio Preview
- Hermes Agent Studio shows live preview at localhost during generation
- Timeline view with different scenes
- **Critical for catching rendering bugs** before final output
- Tell agent what's wrong → it fixes → re-preview

## Tips & Gotchas
- **Must update Hermes Agent first** — skill is in a recent release
- Load skill with `/hyperframes` before starting work
- Complex VFX (shatter, 3D phone) are hard to one-shot — expect iteration
- Point agent to official HyperFrames docs for HTML/Canvas issues
- Agent generates captions from on-screen text (won't match actual speech unless provided)
- For production output, manual tweaking of timing/effects may be needed
- Combine with cron jobs for automated video pipelines (e.g., pull transcript snippets → generate shorts)
- Prompts can be very long — save them in a repo for team reuse
- HyperFrames is free and open-source — no API costs for video generation

## Why Hermes Agent vs Claude Code / Codex
- Access to other installed skills and memory/project files
- Can set up 24/7 automated workflows (cron jobs)
- Can combine multiple skills (HyperFrames + GitHub analysis + social embeds)
- Template reuse is easier with persistent agent sessions

## Resources
- HyperFrames docs: official documentation from Hay Jin
- Prompts repo: `tombstudio/hyperframes-prompts` (full prompts + research markdown)
- Skill location: `nousresearch/hermes-agent/skills/creative/hyperframes/`

## Timestamps & Chapters
- 0:00 - Intro: HyperFrames skill announcement
- 1:54 - Setup: installing and loading the HyperFrames skill
- 3:52 - Demo 1: HTML slides → explainer video (~9 min)
- 6:14 - Demo 2: Reusable YouTube Shorts template
- 8:43 - Demo 3: Website → promotional video (with live preview)
- 13:17 - Demo 4: GitHub repo → architecture explainer with social embeds
- 17:45 - Demo 5: Advanced HTML/Canvas VFX (shatter effect, 3D phone)
- 23:38 - Summary and why use Hermes Agent for this

## Summary
HyperFrames lets Hermes Agent create videos using HTML/CSS/JS instead of expensive video generation models. Install the skill, load it with `/hyperframes`, and describe what you want — slides to video, website promos, YouTube shorts, repo explainers, or advanced VFX. The agent generates compositions that render via FFmpeg. Work with detailed prompts, use the live preview to catch bugs, and iterate. Combine with cron jobs and other skills for automated content pipelines. All prompts and research available in the `tombstudio/hyperframes-prompts` repo.
