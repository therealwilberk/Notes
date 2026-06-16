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

# Rust — fcard CLI

## Scope

Build the fcard flashcard/SRS tool module by module. Each module adds new concepts and builds on the previous. The learning path also fills your specific knowledge gaps:

- **`#[(_)]` attributes** — what they are, how they work. Introduced from M1 onward (`#[derive]`, `#[test]`, `#[cfg(test)]`, `#[serde(...)]`, `#[from]`).
- **Lifetimes** — explicit `<'a>` annotations. Covered in M4 with full examples.
- **External packages** — finding on docs.rs, reading docs, Cargo.toml version syntax, choosing implementations.

**Side task:** study `bat` (sharkdp/bat) source code — ~1 hr/week, light reading.

**Target: 7 weeks at ~14 hrs/week** (100 hrs total)

---

## Phase 0 — Prep (~4 hrs before starting)

Close specific knowledge gaps that M1 assumes you know.

- [ ] **Attributes**: Read a quick intro. `#[derive(Debug, Clone)]` auto-implements traits. `#[test]` marks a test function. `#[cfg(test)]` conditionally compiles test modules. `#[serde(default)]` is a serde-specific attribute. That's 90% of what you'll see.
- [ ] **External crates 101**: docs.rs — every crate's docs. The `Cargo.toml` `[dependencies]` section. Version specifiers (`"1.0"`, `"0.8"`, `"2"`). How to find what you need.
- [ ] **Lifetimes primer**: Read `rust-references.md` (it's already in your vault). Focus on the "dangling reference" rule — that's the whole reason lifetimes exist. The `<'a>` syntax tells the compiler "these two references live as long as each other."
- [ ] **How to study a module README**: Each module tells you exactly what to build. Read the goals first, then the tasks, then the hints if stuck. The difficulty label tells you how much hand-holding to expect.

---

## Phases

### Phase 1 — Foundation: Data Model & CLI (M1, ~14 hrs)

Difficulty: Guided → Semi-guided. Concepts: structs, enums, `clap`, `Display`, unit tests.

- CardStatus enum: New, Learning, Review, Mastered
- Card struct: id, front, back, status
- Deck struct: name, cards Vec<Card>
- CLI subcommands via clap: new, add, list, review, stats
- Display impl for Card, Deck summary
- Tests: card creation, status progression, deck ops

**Gap filled:** `#[derive(...)]` attributes, `clap` derive API, `lib.rs`/`main.rs` pattern, `#[cfg(test)]`

### Phase 2 — Persistence & Errors (M2, ~12 hrs)

Difficulty: Guided. Concepts: serde, thiserror, PathBuf, Result, ? operator.

- StorageError enum (NotFound, Serialize, Io) with thiserror
- save_deck / load_deck / list_decks
- Wire all CLI commands to real file I/O
- Tests: round-trip save/load, nonexistent deck, corrupt file

**Gap filled:** `#[serde(...)]`, `#[from]`, `serde_json`, external crate versioning, docs.rs workflow

### Phase 3 — SRS Engine & State Machine (M3, ~14 hrs)

Difficulty: Semi-guided. Concepts: SM-2 algorithm, From/Into, chrono, iter_mut borrow trap.

- Rating enum: Again, Hard, Good, Easy
- SM-2 review logic: interval, ease_factor, next_review
- QuizSession: get_due_cards, rate_card, interactive loop
- Tests: SM-2 for each rating, EF floor clamp, quiz simulation

**Gap filled:** `From`/`Into` traits, `chrono::Duration`, working with `Option<DateTime>`

### Phase 4 — Search, Tags & HashMap (M4, ~14 hrs)

Difficulty: Unguided. Concepts: HashMap, iterator adapters, lifetime annotations.

- Tags field on Card with serde(default)
- CLI: tag/untag commands, --tag filter on list
- search_cards(deck, query) -> Vec<&Card> — explicit lifetime
- fcard tags — aggregate tags across decks
- Tests: search, tag filter, tag aggregation

**Gap filled:** Lifetime annotations `<'a>`, `HashMap::entry()` + `or_default()`, iterator chains

### Phase 5 — CLI Polish & Stats (M5, ~14 hrs)

Difficulty: Unguided. Concepts: colored, integration tests, data aggregation.

- Colored output: due/dates/errors color-coded
- Session history log (.sessions.json)
- fcard stats — per-deck and --all
- Integration tests in tests/ directory
- Progress bar, table alignment

**Gap filled:** Integration test pattern, `colored` crate, test organization

### Phase 6 — Config & Capstone (M6, ~16 hrs)

Difficulty: Unguided. Concepts: toml, config merging, cross-deck features, 90% coverage.

- fcard.toml with defaults, CLI overrides, env var FCARD_CONFIG
- fcard discover — all due cards across decks
- fcard recent — recent sessions across decks
- 90%+ coverage on core modules
- Polish: no unwrap in library, exit codes, Ctrl+C handling

**Gap filled:** Config merging pattern, `toml` crate, coverage tools, signal handling

---

## Weekly Schedule

| Week | Phase | Codebase Task | Hrs |
|------|-------|---------------|-----|
| 0 | Prep (gaps) | — | 4 |
| 1 | M1: Data model & CLI | — | 14 |
| 2 | M1 finish + M2: Persistence | — | 14 |
| 3 | M2 finish + M3: SRS start | bat — high-level structure | 14 |
| 4 | M3: SRS engine | bat — deep-dive one module | 14 |
| 5 | M4: Search & tags | bat — another module | 14 |
| 6 | M5: CLI polish | bat — tests, patterns | 14 |
| 7 | M6: Config & capstone | bat — summary notes | 16 |

**End: 2026-08-04** (7 weeks)
