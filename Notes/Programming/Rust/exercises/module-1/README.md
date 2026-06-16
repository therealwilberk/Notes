---
tags: [rust, exercises, module-1]
parent: "[[Rust -- Map of Content]]"
created: 2026-06-15
status: complete
exercises: "[[exercises/module-1]]"
---

# Module 1: Foundation — Data Model & CLI

Difficulty: **Guided → Semi-guided**

## Learning Objectives

- Define structs, enums, and impl methods
- Set up a dual `lib.rs` / `main.rs` crate
- Use `clap` derive API for CLI argument parsing
- Implement `Display` for custom types
- Write unit tests for core logic

## New Concepts

### lib.rs + main.rs pattern

A binary crate can have both `src/lib.rs` (library root) and `src/main.rs` (binary
entry point). The binary depends on the library — it calls into `lib.rs` like an
external crate.

```
fcard/
  Cargo.toml
  src/
    lib.rs         # Public API, modules
    main.rs        # Thin: parse args, call lib
    card.rs        # Card-related types
    deck.rs        # Deck-related types
    cli.rs         # CLI argument definitions
```

`main.rs` stays thin. Business logic lives in `lib.rs` and its submodules:

```rust
// src/main.rs
use clap::Parser;
use fcard::cli::Cli;

fn main() {
    let cli = Cli::parse();
    // dispatch to lib
}
```

### clap derive API

Add to `Cargo.toml`:
```toml
[dependencies]
clap = { version = "4", features = ["derive"] }
```

Define subcommands with enums:
```rust
#[derive(Parser)]
#[command(name = "fcard")]
pub struct Cli {
    #[command(subcommand)]
    pub command: Command,
}

#[derive(Subcommand)]
pub enum Command {
    New { name: String },
    Add { deck: String, front: String, back: String },
    List { deck: String },
    Review { deck: String },
    Stats,
}
```

### Display trait

```rust
use std::fmt;

impl fmt::Display for Card {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "[{}] {}", self.status, self.front)
    }
}
```

### Unit tests

Tests live in the same file as the code, in a `#[cfg(test)]` module:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_default_status() {
        let card = Card::new("q", "a");
        assert_eq!(card.status, CardStatus::New);
    }
}
```

Run with `cargo test`.

## Exercise

### Scaffold

```bash
cargo new fcard
cd fcard
```

Add `clap` and `serde` (for later) to `Cargo.toml`. Set up the module tree:

```
src/
  lib.rs
  main.rs
  card.rs
  deck.rs
  cli.rs
```

### Requirements

1. **`CardStatus` enum** — variants: `New`, `Learning`, `Review`, `Mastered`.
   Derive `Debug`, `Clone`, `Copy`, `PartialEq`.

2. **`Card` struct** — fields: `id: u64`, `front: String`, `back: String`,
   `status: CardStatus`. Derive `Debug`, `Clone`, `PartialEq`. Implement:
   - `Card::new(front, back) -> Card` — auto-assigns an id (use a monotonic
     counter or timestamp), status starts as `New`
   - `impl Display` — format: `[{status}] {front}`

3. **`Deck` struct** — fields: `name: String`, `cards: Vec<Card>`.
   Derive `Debug`, `Clone`. Implement:
   - `Deck::new(name) -> Deck`
   - `Deck::add_card(&mut self, card: Card)`
   - `Deck::card_count(&self) -> usize`
   - `Deck::display_summary(&self)` — prints a table of cards with status

4. **`CardStatus::progress(&self) -> CardStatus`** — a method that returns the
   "next" status. `New → Learning → Review → Mastered`. This is a stub — the
   actual SRS algorithm comes in Module 3.

5. **CLI with `clap`** — define subcommands:
   - `fcard new <deck-name>` — creates a new deck
   - `fcard add <deck-name> --front "..." --back "..."` — adds a card
   - `fcard list <deck-name>` — lists cards in a deck
   - `fcard review <deck-name>` — placeholder (prints "starting review")
   - `fcard stats` — placeholder

6. **Unit tests** in `#[cfg(test)]`:
   - `test_card_creation` — verify id assignment and default status
   - `test_status_progression` — verify `New → Learning → Review → Mastered`
   - `test_add_card_to_deck` — verify card count increases
   - `test_empty_deck` — verify `card_count()` is 0 for new deck

### Hints

- Use associated constant or `AtomicU64` for card id counter:
  `static NEXT_ID: AtomicU64 = AtomicU64::new(1);`
- `CardStatus` should derive `Display` too — use a simple match
- The `lib.rs` declares modules: `pub mod card; pub mod deck; pub mod cli;`
- `main.rs` calls `fcard::cli::Cli::parse()` then matches on the command
- `serde` isn't needed yet but add it to `Cargo.toml` now: `serde = { version = "1", features = ["derive"] }` to avoid churn later

### Trap: Display Trait signature

`fmt` returns `fmt::Result` (which is `Result<(), fmt::Error>`). The `write!`
macro returns `fmt::Result` too. If you add a semicolon to suppress the
return value, the function signature expects `()` — compile error:

```rust
// Won't compile — write! returns fmt::Result, function expects ()
impl fmt::Display for Card {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "[{}] {}", self.status, self.front);  // ❌ semicolon!
    }
}
```

The fix: no semicolon (expression return) or add `?` and a semicolon
(propagate then return unit — but that changes the return type).
```rust
// Correct — last expression is returned
impl fmt::Display for Card {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "[{}] {}", self.status, self.front)
    }
}
```

### Trap: Module declarations

`mod card;` tells Rust to load `card.rs`. If `card.rs` has a typo or doesn't
exist, the error says "file not found for module `card`". Always create the file
before declaring it.

### Trap: `use` paths

`main.rs` uses `use fcard::cli::Cli;` — note `fcard` is the crate name (from
`Cargo.toml` `name`), not a file path. Inside `lib.rs`, sibling modules use
`crate::card::Card`.

### Verification

```bash
cargo test          # All 4+ tests pass
cargo run -- new "my-deck"     # Creates deck
cargo run -- add "my-deck" --front "Q" --back "A"   # Adds card
cargo run -- review "my-deck"  # Prints "starting review"
```
