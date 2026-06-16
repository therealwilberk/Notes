---
tags: [rust, exercises, module-5]
parent: "[[Rust -- Map of Content]]"
created: 2026-06-15
status: complete
exercises: "[[exercises/module-5]]"
---

# Module 5: CLI Polish & Stats

Difficulty: **Unguided**

Builds on Modules 1-4.

## Learning Objectives

- Add colored terminal output with `colored` or `owo-colors`
- Aggregate statistics across cards and sessions
- Write integration tests for CLI behavior
- Design clean CLI output (tables, alignment)
- Implement a session log for historical tracking

## New Concepts

### colored crate

```toml
[dependencies]
colored = "3"
```

```rust
use colored::*;

println!("{}", "Correct!".green());
println!("{}", format!("Score: {}/{}", correct, total).yellow());
println!("{}", format!("Error: {}", msg).red().bold());
```

### Integration tests

Integration tests live in `tests/` directory alongside `src/`. Each file in
`tests/` is a separate crate:

```
fcard/
  tests/
    cli_tests.rs
    storage_tests.rs
```

```rust
// tests/cli_tests.rs
use std::process::Command;

#[test]
fn test_cli_new_deck() {
    let output = Command::new("cargo")
        .args(["run", "--", "new", "test-deck"])
        .output()
        .expect("failed to run");
    assert!(output.status.success());
}
```

Tip: use `assert_cmd` and `predicates` crates for better CLI test ergonomics:
```toml
[dev-dependencies]
assert_cmd = "2"
predicates = "3"
```

```rust
use assert_cmd::Command;

#[test]
fn test_list_decks() {
    let mut cmd = Command::cargo_bin("fcard").unwrap();
    cmd.arg("ls").assert().success();
}
```

### Data aggregation

```rust
pub struct SessionStats {
    pub total_cards: usize,
    pub correct_first_try: usize,
    pub total_reviews: usize,
    pub session_start: DateTime<Utc>,
    pub session_end: Option<DateTime<Utc>>,
}

impl SessionStats {
    pub fn retention_rate(&self) -> f64 {
        if self.total_reviews == 0 {
            return 0.0;
        }
        self.correct_first_try as f64 / self.total_reviews as f64 * 100.0
    }
}
```

## Exercise

### Requirements

1. **Colored output** — make the CLI output easier to read:
   - Due card count in yellow
   - Correct answers in green, incorrect in red
   - Section headers in cyan/bold
   - Deck names in a different color
   - Table borders in dimmed color

2. **Session history** — create a session log file `./decks/.sessions.json`:
   - Append a record after each review session
   - Record: date, deck name, cards reviewed, retention rate, duration
   - Use `serde` to serialize/deserialize

3. **`fcard stats`** — comprehensive stats view:
   ```
   $ fcard stats japanese-101
   Deck: japanese-101
   Total cards: 12
   Mastered: 5
   Learning: 4
   New: 3
   Retention rate: 78.3%
   Reviews today: 15
   Streak: 5 days
   Next review due: 7 cards
   ```

4. **Global stats**: `fcard stats --all` — aggregates across all decks

5. **Integration tests** in `tests/`:
   - `test_cli_new_deck_creates_file` — new deck command creates .json
   - `test_cli_add_card` — add card, then list shows it
   - `test_cli_invalid_deck` — review non-existent deck, expect error
   - `test_cli_stats_output` — stats command produces expected output format
   - `test_cli_search_shows_results` — search returns expected cards

6. **Clean up CLI output** — make it feel like a real tool:
   - Alignment: pad columns to fixed widths
   - Truncate long card front/back to fit terminal
   - Show progress: `[▓▓▓▓░░░░] 5/12`

### Hints

- `colored` controls color per-string. Use `.blue()`, `.green()`, `.red()` etc.
- For tables: `format!("| {:<20} | {:<10} |", text, value)` — `:<20` left-pads
- Integration tests that use filesystem need isolation — create temp dirs
- Session log as JSON array: load, push, save each time
- Streak: count consecutive days with sessions by checking the session log

### Trap: Integration test isolation

Integration tests share the filesystem. If one test creates `./decks/`, another
may conflict. Use tempdirs or set a `FCARD_DATA_DIR` env var in each test.

### Trap: Colored output in tests

Colored output in captured test output shows ANSI escape codes. Either:
- Strip colors before asserting (`.replace("\x1b[0m", "")`), or
- Only check for content, not formatting

### Verification

```bash
cargo test
cargo run -- stats japanese-101
cargo run -- stats --all
# Run a review session, then check stats again
cargo run -- review japanese-101
cargo run -- stats japanese-101   # Should show updated numbers
```
