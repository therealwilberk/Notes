---
tags: [rust, exercises, module-4]
parent: "[[Rust -- Map of Content]]"
created: 2026-06-15
status: complete
exercises: "[[exercises/module-4]]"
---

# Module 4: Search, Tags & HashMap

Difficulty: **Unguided**

Builds on Modules 1-3.

## Learning Objectives

- Use `HashMap` and `BTreeMap` for lookups and grouping
- Chain iterator adapters: `.iter()`, `.filter()`, `.map()`, `.collect()`
- Write functions with lifetime annotations
- Implement substring search and tag-based filtering
- Handle the "string return" lifetime ambush

## New Concepts

### HashMap

```rust
use std::collections::HashMap;

// Group cards by tag
let mut by_tag: HashMap<String, Vec<&Card>> = HashMap::new();
for card in &deck.cards {
    for tag in &card.tags {
        by_tag.entry(tag.clone()).or_default().push(card);
    }
}
```

### Iterator adapters

```rust
let due: Vec<&Card> = deck.cards
    .iter()
    .filter(|c| c.is_due())
    .collect();

let names: Vec<String> = deck.cards
    .iter()
    .map(|c| c.front.clone())
    .collect();
```

### The lifetime ambush

A search function returns a reference to data inside the deck. The returned
lifetime is tied to the deck's borrow:

```rust
// This needs a lifetime annotation:
pub fn search_by_tag<'a>(deck: &'a Deck, tag: &str) -> Vec<&'a Card> {
    let tag_str = tag.to_string();
    deck.cards.iter().filter(|c| c.tags.contains(&tag_str)).collect()
}
```

Without `<'a>`, Rust can't connect the output lifetime to the input borrow.

Add `tags: Vec<String>` to `Card`. It's a new field — `#[serde(default)]` so
existing JSON files still load.

### BTreeMap for sorted output

```rust
use std::collections::BTreeMap;

// Tags displayed alphabetically
let mut sorted: BTreeMap<&String, Vec<&Card>> = BTreeMap::new();
```

## Exercise

### Requirements

1. **Add `tags: Vec<String>` to `Card`** with `#[serde(default)]`.
   Update `Card::new()` to accept tags, or add a `Card::add_tag(&mut self)`.

2. **CLI: tag management** — extend `cli.rs`:
   - `fcard add ... --tags "japanese,verbs"` — comma-separated tags on add
   - `fcard tag <deck> <card-id> <tag>` — tag an existing card
   - `fcard untag <deck> <card-id> <tag>` — remove a tag

3. **Search by content** — `fcard search <deck> <query>`:
   - Case-insensitive substring match on front and back
   - Print matching cards grouped by tag
   - Show match count at the end

4. **Filter by tag** — `fcard list <deck> --tag <tag>`:
   - Only show cards with the given tag
   - If no `--tag`, show all cards (existing behavior)

5. **CLI: `fcard tags`** — list all tags across all decks with card counts:
   ```
   $ fcard tags
   japanese    5 cards
   verbs       3 cards
   greetings   2 cards
   ```

6. **Search function** — `search_cards(deck: &Deck, query: &str) -> Vec<&Card>`:
   - Case-insensitive, matches if query is a substring of front or back
   - This needs a lifetime annotation

7. **Tests**:
   - Test search with matching/non-matching queries
   - Test tag filtering returns correct cards
   - Test tag listing aggregation
   - Test case-insensitive search
   - Test tagging a card and persisting (save + load, verify tag stuck)
   - Test `search_cards` return type compiles with correct lifetime

### Hints

- For case-insensitive: `front.to_lowercase().contains(&query.to_lowercase())`
- `HashMap::entry()` + `or_default()` is the idiomatic way to build maps
- `BTreeMap` gives sorted iteration for free
- Comma-separated tags: split on `,`, trim whitespace, filter empty
- The search function signature is the hardest part — get the lifetime right

### Trap: HashMap key ownership

`entry()` takes a owned key. If you use `&str`, it won't compile. Clone the
string or restructure:

```rust
// Won't compile — entry expects String
by_tag.entry(tag).or_default().push(card);  // if tag is &str

// Works
by_tag.entry(tag.to_string()).or_default().push(card);
// Or use the entry API with borrowed keys (nightly or with compat crate)
```

### Trap: Contains on empty query

An empty `query` matches everything. Decide whether that's intended behavior
or if you should return early with an empty vec for empty input.

### Trap: Lifetime elision

```rust
// Works (elided):
fn first_card(deck: &Deck) -> &Card { &deck.cards[0] }

// Also needs explicit lifetime — multiple params:
fn search(deck: &Deck, query: &str) -> Vec<&Card> {  // ❌ ambiguous
```

With multiple reference params, Rust can't elide. Explicit annotation is
required.

### Verification

```bash
cargo test
cargo run -- add "japanese-101" --front "おはよう" --back "good morning" --tags "greetings,japanese"
cargo run -- add "japanese-101" --front "さようなら" --back "goodbye" --tags "greetings,japanese"
cargo run -- search "japanese-101" "good"   # Should find both
cargo run -- list "japanese-101" --tag "greetings"   # Only greetings
cargo run -- tags   # Show all tags
```
