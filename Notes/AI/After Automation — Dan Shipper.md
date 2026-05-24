---
tags: [ai, automation, future-of-work, essays, dan-shipper]
aliases: ["After Automation"]
created: 2026-05-24
status: done
source: https://every.to/p/after-automation
author: Dan Shipper
---

# After Automation

Dan Shipper's argument: AI progress creates more work for humans, not less. The more we automate, the more expert human judgment becomes necessary.

## The Paradox

Every has automated everything they can (Codex, Claude Code, customer service, writing). They're a team of ~30. They haven't fired anyone. There's more human work than ever.

> We don't write code by hand anymore. If you @-mention someone in our Slack, it's a toss-up whether you're talking to a human or an agent.

AI responds to 95% of Shipper's work emails. He's at inbox zero. He still reviews every one.

## Two Modes of Working with Agents

**Agent employees** — async delegation. Tag them in Slack, they go off and produce output. Two flavors:
- *Coworker agents* (Claudie for consulting, Andy for editorial, Viktor for org-wide research)
- *Embedded agents* (Fin in customer service: handled 65% of support conversations, closed 40% without humans)

**Human-agent collaboration** — shared operating systems (Codex, Claude Code, Cowork). Not handoff. You and multiple agents working in the same workspace on complex, original work.

> Kieran calls this the human "sandwich" — we're the bread on either end of the AI's work.

## The Cycle

This is the core argument. Four steps that repeat:

1. **AI commoditizes human expertise.** Models are trained on the visible residue of successfully completed tasks. Skills that were rare (coding a PR, making a thumbnail, writing a newsletter) become cheap and available to everyone.

2. **Cheap competence gets adopted everywhere.** Operations people issue PRs. Marketers make YouTube thumbnails. Engineers write product guides. OpenClaw got 44,469 pull requests as of May 2026. Kubernetes got 5,200 in all of 2022.

3. **Abundance creates sameness.** Everyone uses the same models trained on the same corpus. Output ranges from "decent start" to "plain slop." Slop isn't any one mistake. It's visible sameness repeated ad nauseam.

4. **Sameness creates demand for difference.** When everything looks alike, what doesn't fit the pattern becomes rare and valuable. Demand for difference is demand for human experts.

> Once a situation has been reduced to text, once it has become corpus, it is a corpse. Humans are alive to a specific moment, customer, codebase, or conversation in a way the training corpus isn't yet.

## Zeno's Paradox of AI

Borrowed from the Greek paradox where a tortoise beats Achilles because it always has a head start. Humans are the tortoise. We start ahead with millions of years of evolutionary and cultural learning. AI speeds through it all and nips at our heels. But the gap keeps regenerating.

**How benchmarks work:** Every benchmark measures work inside a frame (a specific prompt, a specific problem framing). Models hill-climb that frame. When they saturate it, we zero it out by changing the frame. Progress continues, but the same pattern repeats.

Shipper built a "Senior Engineer benchmark" — give a model a vibe-coded production codebase and ask for a first-principles rewrite. GPT-5.5 scored 62/100. Human senior engineers score 80s-90s. Models will hit 90s within a year. But then the frame shifts: "Can you decide *whether* a rewrite is needed, choose the scope, preserve the right invariants, manage the migration?"

**GDPval example:** Models beat human experts 40-49% of the time. But the prompts contain enormous smuggled intelligence — someone already decided the confidence intervals, which metrics matter, how results should be formatted. The hard human work happened before the model started.

> The score tells us how well the model operates inside a frame we supplied; it does not tell us that the model has become us. That is the category error underneath the panic.

## Agents Without Agency

Two definitions getting mixed up:
- **Agency** = ability to act independently, for oneself
- **Agent** = something that acts on behalf of another

AI is purely the second. They execute goals humans give them. The industry is pouring billions into making them better at exactly that.

**The toddler comparison:** Toddlers can't write code or pass graduate exams. But toddlers have ends. They want to touch the red balloon, poke it with a fork, stuff it out the window. They invent games constantly. They're not waiting for a prompt.

> The toddler is alive inside a field of desire, attention, frustration, delight, fear, imitation, and play.

Model compliance and helpfulness are fundamentally at odds with true agency. Even as models improve, this gap remains.

## The Rabbi Story (Coda)

From Martin Buber's *The Way of Man*: A man so stupid he can't find his clothes in the morning. He writes down where everything is. Next morning he follows the list perfectly — cap on head, pants on legs — then asks in horror: "Where in the world am I?"

The point: you can automate every task and still lose the thing that makes you *you*.

## Key Takeaways

- More automation → more expert work, not less
- AI commoditizes yesterday's competence, creating demand for today's judgment
- Benchmarks measure frames, not framers. The frame is not the framer.
- Agents have autonomy but not agency. They're means to human ends.
- The structurally safe position: use AI to address today's problems as you see them

## Related

- [[Allocation Economy]] — Shipper's 2023 essay predicting work would look like management
- [[AI and Expertise]]
