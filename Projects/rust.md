---
tags: [rust, project, fcard, cli]
parent: "[[Projects — Map of Content]]"
status: planning
start: 2026-06-16
target: 2026-08-04
estimate: 100 hrs over 7 weeks
pace: ~14 hrs/wk (2 hrs/day, 6 days)
share: 25%
---

# Rust — Flashcard CLI & Codebase Study

## Scope

Two parallel tracks:

1. **Codebase study** — read idiomatic Rust open-source projects (primary: ripgrep, secondary: just or bat)
2. **fcard CLI** — build the flashcard/SRS tool module by module, applying what you learn

Finishes first (week 7). After that, its 25% redistributes to AutoCADE and ML.

**Target: 7 weeks at ~14 hrs/week** (100 hrs total)

---

## Track A: Codebase Study (~24 hrs)

### Study Process

For each codebase:
1. **High-level** (1 hr): README, Cargo.toml, crate structure. What problem, how decomposed?
2. **Module deep-dive** (2 hrs): Pick one crate/module. Read source. Note patterns, idioms.
3. **Apply** (1 hr): Write a tiny thing mimicking one pattern you saw.

### Codebases

**Primary: ripgrep** (BurntSushi/ripgrep) — the gold standard Rust project. CLI, not networking, clean trait usage, excellent test patterns, active maintenance. ~30 crates.

- Entry points: `grep-cli`, `grep-regex`, `grep-searcher` crates
- Study: crate decomposition, error handling patterns, iterator design, testing strategy

**Secondary (choose 1):**

- **just** (casey/just) — command runner. Small, focused, minimal. Good for seeing compact idiomatic Rust.
- **bat** (sharkdp/bat) — cat clone. Clean, well-structured, good syntect integration.

---

## Track B: fcard Exercises (~76 hrs)

6 modules from `Notes/Programming/Rust/exercises/`.

| # | Module | Difficulty | Hrs |
|---|--------|------------|-----|
| 1 | Foundation — Data Model & CLI | G → SG | 12 |
| 2 | Persistence & Errors | G | 10 |
| 3 | SRS Engine & State Machine | SG | 12 |
| 4 | Search, Tags & HashMap | U | 14 |
| 5 | CLI Polish & Stats | U | 12 |
| 6 | Config & Capstone | U | 16 |

G = guided (goals + hints), SG = semi-guided, U = unguided (goal only)

---

## Weekly Schedule

| Week | Codebase | fcard | Hrs |
|------|----------|-------|-----|
| 1 | ripgrep — high-level + crate structure | M1 start | 14 |
| 2 | ripgrep — grep-cli module deep-dive | M1 finish + M2 start | 14 |
| 3 | ripgrep — grep-regex, search patterns | M2 finish + M3 start | 14 |
| 4 | ripgrep — parallelism, output formatting | M3 finish + M4 start | 14 |
| 5 | just or bat — high-level + deep-dive | M4 finish + M5 start | 14 |
| 6 | just or bat — deep-dive + apply | M5 finish + M6 start | 14 |
| 7 | Patterns summary — what to carry forward | M6 finish | 16 |

**Target end: 2026-08-04** (Week 7)
