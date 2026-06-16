---
tags: [rust, project, fcard, cli]
parent: "[[Projects -- Map of Content]]"
status: planning
start: 2026-06-16
target: 2026-08-31
estimate: 11 weeks @ ~8 hrs/wk
---

# Rust — Flashcard CLI & Codebase Study

## Scope

Two tracks running in parallel:

1. **Codebase study** — learn how pros write Rust by reading idiomatic open-source projects
2. **fcard exercises** — build the CLI flashcard/SRS tool module by module, applying what you learn

**Total: ~11 weeks at ~8 hrs/week** (~88 hrs)

---

## Codebase Study Track

The recommended codebases for learning idiomatic Rust, ordered from simpler to more complex:

### Primary: `ripgrep` (BurntSushi/ripgrep)

The gold standard. Clean crate structure, excellent trait usage, extensive testing, well-documented. CLI tool (not networking), widely used, actively maintained.

- ~30 crates in workspace, good for learning crate decomposition
- Heavy use of iterators, traits, error handling patterns
- Excellent test suite — good example of testing strategy
- `grep-regex` / `grep-searcher` / `grep-cli` is a good entry point

### Secondary (choose 1 after ripgrep):

- **`just`** (casey/just) — smaller, focused, very clean. Good for seeing minimal Rust done well.
- **`bat`** (sharkdp/bat) — cat clone. Clean architecture, good use of syntect for syntax highlighting, well-structured.

### Study Process

For each codebase:

1. **Day 1 — High-level** (1 hr): Read the README, `Cargo.toml`, crate structure. What problem does it solve? How is it decomposed?
2. **Day 2 — Module deep-dive** (2 hrs): Pick one crate/module. Read the source. Note patterns, idioms, design decisions.
3. **Day 3 — Apply** (1 hr): Write a tiny thing that mimics one pattern you saw.

---

## fcard Exercise Track

6 modules, progressive difficulty. See `Notes/Programming/Rust/exercises/README.md` for full details.

| Module | Topic | Difficulty | Est. Time |
|--------|-------|------------|-----------|
| 1 | Foundation — Data Model & CLI | G → SG | 10 hrs |
| 2 | Persistence & Errors | G | 8 hrs |
| 3 | SRS Engine & State Machine | SG | 8 hrs |
| 4 | Search, Tags & HashMap | U | 6 hrs |
| 5 | CLI Polish & Stats | U | 6 hrs |
| 6 | Config & Discovery | U | 8 hrs |

Difficulty key: G = Guided (goals + hints), SG = Semi-guided, U = Unguided (goal only)

---

## Weekly Distribution

### Track A: Codebase Study (~2 hrs/wk)

| Week | Focus |
|------|-------|
| 1-2  | ripgrep high-level + grep-cli module |
| 3-4  | ripgrep deep-dive (grep-regex / search patterns) |
| 5-6  | ripgrep deep-dive (parallelism, output) |
| 7-8  | just or bat — secondary codebase |
| 9-10 | just or bat — deep-dive |
| 11   | Final reflection: patterns summary |

### Track B: fcard Exercises (~6 hrs/wk)

| Week | Module | Cumulative Hours |
|------|--------|------------------|
| 1-2  | M1: Foundation | 20 |
| 3-4  | M2: Persistence & Errors | 28 |
| 5-6  | M3: SRS Engine | 36 |
| 7-8  | M4: Search & Tags | 42 |
| 9-10 | M5: CLI Polish | 48 |
| 11   | M6: Config & Capstone | 56 |

### Combined Weekly Schedule

| Week | Codebase (2h) | fcard (6h) |
|------|---------------|------------|
| 1    | ripgrep intro | M1 start |
| 2    | grep-cli | M1 finish |
| 3    | grep-regex | M2 start |
| 4    | search patterns | M2 finish |
| 5    | parallelism | M3 start |
| 6    | output/formatting | M3 finish |
| 7    | just intro | M4 |
| 8    | just deep-dive | M4 cont. |
| 9    | bat intro | M5 |
| 10   | bat deep-dive | M5 cont. |
| 11   | Patterns summary | M6 |

**End date target: 2026-08-31**
