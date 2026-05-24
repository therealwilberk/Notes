---
tags: [ai, philosophy, benchmarks, frames, dan-shipper]
aliases: ["Frames vs Framers", "The Frame Is Not the Framer"]
created: 2026-05-24
status: done
related: "[[After Automation — Dan Shipper]]"
---

# Frames vs Framers

The philosophical core of Shipper's argument. Every benchmark measures how well a model climbs inside a frame we supplied. That's not the same as the model becoming us.

## What's a Frame?

A frame is any fixed problem setup: a prompt, a benchmark, a task specification. You freeze a problem into something measurable. Without a frame, a model is "just an inert set of almost-infinite possibilities."

The Senior Engineer benchmark example: Shipper gives a model a broken vibe-coded codebase and says "rewrite from first principles." The model's score (62/100 for GPT-5.5) measures how well it performs *inside that specific prompt*. Change the prompt to "fix the errors one by one" and the score drops to near zero.

## The Smuggled Intelligence Problem

GDPval shows models beating human experts 40-49% of the time. But the prompts contain enormous pre-existing human judgment: which metrics to test, what confidence intervals to use, how results should be formatted.

> The hard human work that GDPval does not measure has already been done before the model begins.

The benchmark doesn't measure "can the model do this job?" It measures "given that a human already framed the problem perfectly, can the model execute inside that frame?"

## The Cycle

1. We set a frame (benchmark, task, prompt)
2. Models hill-climb that frame, scores go up
3. We panic: "it caught us!"
4. But it caught the *frame*, not the *framer*
5. We shift the frame, zero out the scores
6. Repeat

> We point to the latest edge we drew and say: This is us. Then, when the model climbs it, it feels like it has caught us. But it has caught the frame, not the framer.

## Why Frames Are Necessary

Frames aren't bad. They're how we get traction on the world. But they're frozen, partial, and therefore optimizable. The framer is the one still in contact with what the frame has to discard: "the whole situation as it appears to them, moment to moment."

The moment you try to describe "the whole situation," you've already started another frame. You can't say what it is, but it exists because you exist.

## Connection to [[After Automation — Dan Shipper|After Automation]]

This is the resolution to [[Zeno's Paradox of AI]]. The gap keeps regenerating because frames are always partial, and framers (humans) are always alive to the next moment.

## Connection to [[Agents Without Agency]]

Models can climb frames with increasing competence. But they can't *choose* frames for themselves, because they have no ends of their own. That's the job of the framer.
