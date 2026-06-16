---
tags: [rust, exercises, module-6]
parent: "[[Rust -- Map of Content]]"
created: 2026-06-15
status: complete
exercises: "[[exercises/module-6]]"
---

# Module 6: Capstone — Config & Discovery

Difficulty: **Unguided**

Builds on all previous modules.

## Learning Objectives

- Parse TOML config files
- Implement a config hierarchy (defaults → file → CLI flags)
- Aggregate and analyze data across all decks
- Design for testability — target 90%+ coverage on core logic
- Make independent design decisions

## New Concepts

### toml crate

```toml
[dependencies]
toml = "0.8"
serde = { version = "1", features = ["derive"] }
```

```rust
use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct Config {
    pub default_deck: Option<String>,
    pub daily_review_limit: Option<u32>,
    pub theme: Option<String>,
}
```

Read and parse:
```rust
let content = std::fs::read_to_string("./fcard.toml")?;
let config: Config = toml::from_str(&content)?;
```

### Config merging pattern

```
CLI flags (highest priority)
    ↓ override
Config file (~/.config/fcard/config.toml)
    ↓ override
Defaults (hardcoded)
```

Implement a `ConfigBuilder` or use `Option` fields with `.unwrap_or()`:

```rust
impl Config {
    pub fn daily_limit(&self) -> u32 {
        self.daily_review_limit.unwrap_or(20)
    }
}
```

## Exercise

### Requirements

1. **Config file** at `./fcard.toml`:
   ```toml
   default_deck = "japanese-101"
   daily_review_limit = 30
   theme = "dark"
   data_dir = "./decks"
   ```
   All fields optional with sensible defaults.

2. **`Config` struct** — load from default location, with override via
   `--config` flag. Merge with CLI flags (CLI wins).

3. **`--deck` flag** on review/search commands as optional override.
   `fcard review` with no deck name uses `config.default_deck`.

4. **Cross-deck features**:
   - `fcard review` (no deck, uses default from config)
   - `fcard discover` — shows cards from ALL decks that are due today,
     aggregated into one mega-review session
   - `fcard stats --all` — already exists from Module 5, now works with
     config default
   - `fcard recent` — shows recent sessions across all decks

5. **90%+ test coverage** on core modules (`card.rs`, `srs.rs`, `storage.rs`):
   - Every function in those modules has at least one test
   - Error paths are tested (not just happy path)
   - Edge cases: empty decks, single card, max intervals, corrupt files

6. **Clean up and polish**:
   - Remove any remaining `unwrap()` calls in library code (use `?` or
     proper error handling)
   - Consistent exit codes (0 = success, 1 = user error, 2 = system error)
   - Help text should be informative
   - Handle Ctrl+C gracefully during review (use `ctrlc` crate or catch
     `SIGINT`)

### Hints

- Use `std::env::var("FCARD_CONFIG")` to allow env var override of config path
- `toml::from_str` can fail for many reasons — wrap in your error type
- For coverage: `cargo tarpaulin` or `cargo llvm-cov` (install with
  `cargo install cargo-llvm-cov`)
- `discover` mode: load ALL decks, filter due cards, shuffle, present
- This is intentionally under-specified. Make design decisions and justify them.
  Document any tradeoffs you encounter.

### Trap: Config file not found

Don't crash if `fcard.toml` doesn't exist — use defaults. Use
`std::fs::read_to_string().ok()` and `Option` chaining.

### Trap: TOML deserialization errors

TOML is stricter than JSON about types. A string where a number is expected
fails. Handle this as a user-visible error, not a panic.

### Trap: Permissions

If `data_dir` points to a path the user can't write to, fail gracefully with
a clear error message. Check permissions on startup.

### Trap: discover mode borrows

Loading all decks means you have multiple `Deck` values in memory. Their
lifetimes are independent — you can't return references across decks easily.
Design discover to own all data:

```rust
pub fn discover() -> Result<Vec<Card>, StorageError> {
    let deck_names = list_decks()?;
    let mut all: Vec<Card> = Vec::new();
    for name in deck_names {
        let deck = load_deck(&name)?;
        all.extend(deck.cards.into_iter().filter(|c| c.is_due()));
    }
    Ok(all)
}
```

### Verification

```bash
cargo test                              # All tests pass, 90%+ coverage on core
echo 'default_deck = "japanese-101"' > fcard.toml
cargo run -- review                     # Uses default deck from config
cargo run -- discover                   # Mega review across decks
cargo run -- recent                     # Recent sessions
cargo run -- stats --all                # Global stats
cargo run -- review --deck "spanish-101"  # Explicit override
```

## Completion Checklist

- [ ] All 6 modules built and working
- [ ] `cargo test` passes with 90%+ coverage on core modules
- [ ] Config file loads with graceful fallback
- [ ] `discover` mode works across decks
- [ ] No `unwrap()` in library code
- [ ] Meaningful error messages for all user-facing errors
- [ ] Project feels like a real CLI tool

Congratulations — you just built a production-quality CLI app from scratch
using only Ch 4-7 principles + the concepts you picked up along the way.
