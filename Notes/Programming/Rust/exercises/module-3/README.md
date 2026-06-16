---
tags: [rust, exercises, module-3]
parent: "[[Rust -- Map of Content]]"
created: 2026-06-15
status: complete
exercises: "[[exercises/module-3]]"
---

# Module 3: SRS Engine & State Machine

Difficulty: **Semi-guided**

Builds on Modules 1-2.

## Learning Objectives

- Design a state machine with enums and match
- Implement the SM-2 spaced repetition algorithm
- Use `From`/`Into` traits for type conversions
- Work with `Duration` and date/time (`chrono`)
- Navigate borrow checker traps with `iter_mut()` and indexed access
- Write thorough unit tests for algorithmic logic

## New Concepts

### From / Into trait

```rust
impl From<Rating> for chrono::Duration {
    fn from(rating: Rating) -> Self {
        match rating {
            Rating::Again => chrono::Duration::minutes(1),
            Rating::Hard => chrono::Duration::minutes(5),
            Rating::Good => chrono::Duration::minutes(10),
            Rating::Easy => chrono::Duration::minutes(15),
        }
    }
}
```

`From` auto-provides `Into`. `chrono::Duration::from(Rating::Good)` and
`chrono::Duration::from(rating)` both work.

### chrono crate

```toml
[dependencies]
chrono = { version = "0.4", features = ["serde"] }
```

```rust
use chrono::{DateTime, Utc};

pub struct Card {
    // ...
    pub next_review: Option<DateTime<Utc>>,
    pub interval: f64,         // days
    pub ease_factor: f64,      // multiplier, starts at 2.5
}
```

### iter_mut borrow trap

Iterating over `&mut Vec<Card>` and trying to mutate while borrowing:

```rust
// This won't compile:
for card in deck.cards.iter_mut() {
    let new_status = advance_card(&card);
    // ... calculate new interval using card data
    card.status = new_status;      // ✅ fine
}
```

But if you try to borrow the whole deck while iterating:

```rust
// This won't compile:
for card in deck.cards.iter_mut() {
    deck.add_card(Card::new("x", "y"));   // ❌ can't borrow deck as mutable
}
```

Use indexed access when you need both the card and the deck simultaneously:

```rust
for i in 0..deck.cards.len() {
    let card = &mut deck.cards[i];  // fine
    // use card
}
```

### Option<T> and match

`next_review: Option<DateTime<Utc>>` is `None` for new cards. Use match:

```rust
match card.next_review {
    Some(dt) if dt > Utc::now() => println!("not due yet"),
    Some(_) => println!("due now"),
    None => println!("never reviewed"),
}
```

## SM-2 Algorithm (Simplified)

The algorithm tracks each card's:
- **Interval** (days until next review)
- **Ease factor** (multiplier, starts at 2.5, min 1.3)

After a review, the user rates the card: Again (forgot), Hard, Good, Easy.

| Rating | Interval Change | Ease Factor Change |
|--------|----------------|--------------------|
| Again | Reset to 0 | No change |
| Hard | interval × 1.2 | EF -= 0.15 |
| Good | interval × EF | No change |
| Easy | interval × EF × 1.3 | EF += 0.15 |

For new cards (interval = 0):
- Again: stays 0
- Hard: 1 day
- Good: 1 day
- Easy: 2 days

Ease factor floor: 1.3. If EF drops below, clamp to 1.3.

## Exercise

### Requirements

Extend your project:

1. **`Rating` enum** — variants: `Again`, `Hard`, `Good`, `Easy`.
   Derive `Debug`, `Clone`, `Copy`, `PartialEq`, `Serialize`, `Deserialize`.

2. **Card fields** — add to `Card`:
   - `interval: f64` — current interval in days (0.0 for new cards)
   - `ease_factor: f64` — starts at 2.5
   - `next_review: Option<DateTime<Utc>>` — when this card is due
   - Add `#[serde(default)]` for backward compat with old JSON files

3. **`Card::new_with_srs(front, back) -> Card`** — sets interval to 0.0,
   ease_factor to 2.5, next_review to `None`.

4. **`Card::review(&mut self, rating: Rating)`** — updates the card's interval,
   ease_factor, and next_review based on the SM-2 algorithm above.
   - Use `Utc::now() + chrono::Duration::days(interval as i64)` to set
     `next_review`
   - Clamp ease_factor to min 1.3

5. **Quiz engine** in `src/quiz.rs`:
   - `QuizSession` struct — holds a reference to the deck being reviewed,
     tracks current card index, session stats
   - `get_due_cards(deck: &Deck) -> Vec<usize>` — returns indices of cards
     due for review (next_review <= now or None)
   - `rate_card(card: &mut Card, rating: Rating)` — calls `card.review()`
   - CLI flow:
     ```
     fcard review "japanese-101"
     # Shows due cards one by one:
     Card 1/5 — こんにちは
     [Press Enter to reveal answer]
      hello
     Rate: (A)gain / (H)ard / (G)ood / (E)asy >
     ```
   - After all due cards: print session summary (cards reviewed, correct %)

6. **`impl From<Rating> for chrono::Duration`** — matches the initial intervals
   table (1 min / 5 min / 10 min / 15 min) — used for new cards' first review.

7. **Tests**:
   - `test_new_card_review_good` — review a new card with Good, verify
     interval = 1.0, ease_factor = 2.5
   - `test_new_card_review_easy` — interval = 2.0, ease_factor = 2.65
   - `test_review_again` — interval resets to 0
    - `test_ease_factor_floor` — Hard repeatedly until EF < 1.3, verify clamp
    - `test_ease_factor_min_clamp` — verify EF never drops below 1.3 even with repeated Easy
   - `test_get_due_cards` — create cards with various next_review values,
     verify only due cards are returned
   - `test_quiz_session` — full session simulation: review 3 cards, verify
     intervals updated and stats correct

### Hints

- `chrono::Duration::days(1)` gives a 1-day duration
- `Utc::now()` returns the current UTC time
- Use `card.next_review.as_ref().map(|dt| dt <= &Utc::now()).unwrap_or(true)`
  to check if a card is due (None means not yet reviewed = due)
- The quiz loop reads stdin. Use `std::io::stdin().read_line()`.
- The CLI needs to accept single-character input (A/H/G/E). Match on the
  first char of the line.
- `serde_json` stores `Option<DateTime<Utc>>` as an ISO 8601 string or null

### Trap: Floating point comparison

Don't `assert_eq!(card.interval, 1.0)` on computed floats. Use a margin:

```rust
assert!((card.interval - 1.0).abs() < f64::EPSILON);
```

### Trap: chrono::Duration vs std::time::Duration

These are different types. `chrono::Duration` supports calendar days,
`std::time::Duration` is nanoseconds-only. Use `chrono::Duration` for
SRS intervals. Convert with `duration.to_std()` if needed.

### Trap: Mutable borrow while reading stdin

If you borrow `deck` mutably in the quiz loop, you can't also borrow it
immutably for printing. Plan the borrow flow:

```rust
let mut deck = storage::load_deck(&name)?;
let due = get_due_cards(&deck);       // immutable borrow
for idx in due {
    let card = &mut deck.cards[idx];    // mutable borrow — ok, non-overlapping
    // show card, get rating, update
}
```

### Verification

```bash
cargo test
cargo run -- review "japanese-101"
# Interactive quiz — rate each card
cargo run -- review "japanese-101"
# Run again — only due cards should appear
```
