---
tags: [rust, exercises, module-2]
parent: "[[Rust -- Map of Content]]"
created: 2026-06-15
status: complete
exercises: "[[exercises/module-2]]"
---

# Module 2: Persistence & Errors

Difficulty: **Guided**

Builds on Module 1. All concepts from M1 are fair game.

## Learning Objectives

- Serialize/deserialize structs with `serde`
- Read/write files with `std::fs` and `std::io`
- Handle errors with `Result`, `?`, and custom error types via `thiserror`
- Use `PathBuf` for filesystem paths
- Test error paths and round-trip serialization

## New Concepts

### serde

Add to `Cargo.toml`:
```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

Derive `Serialize` and `Deserialize` on structs:
```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Card {
    pub id: u64,
    pub front: String,
    pub back: String,
    pub status: CardStatus,         // Must also derive Serialize/Deserialize
}
```

### thiserror

Define custom errors in `src/error.rs`:
```toml
[dependencies]
thiserror = "2"
```

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum StorageError {
    #[error("deck not found: {0}")]
    NotFound(String),

    #[error("failed to serialize deck: {0}")]
    Serialize(#[from] serde_json::Error),

    #[error("I/O error: {0}")]
    Io(#[from] std::io::Error),
}
```

`#[from]` auto-generates `From<serde_json::Error> for StorageError` and
`From<std::io::Error> for StorageError` — which means `?` works automatically.

### PathBuf vs &str

`PathBuf` is an owned, mutable path. `&Path` is a borrowed path slice.
`std::path::Path` has utility methods like `.join()`:

```rust
use std::path::PathBuf;

let data_dir = PathBuf::from("./decks");
let deck_path = data_dir.join("my-deck.json");   // PathBuf
```

### Result + ?

```rust
pub fn save_deck(deck: &Deck) -> Result<(), StorageError> {
    let path = decks_dir().join(format!("{}.json", deck.name));
    let json = serde_json::to_string_pretty(deck)?;       // `?` propagates Serialize error
    std::fs::write(path, json)?;                            // `?` propagates Io error
    Ok(())
}
```

### Error paths in tests

Test that your code handles failure gracefully:
```rust
#[test]
fn test_load_nonexistent_deck() {
    let result = storage::load_deck("nonexistent");
    assert!(result.is_err());
    assert!(matches!(result.unwrap_err(), StorageError::NotFound(_)));
}
```

## Exercise

### Requirements

Create `src/storage.rs` and `src/error.rs`. Wire them into `lib.rs`.

1. **`StorageError` enum** in `src/error.rs` with variants:
   - `NotFound(String)` — deck file doesn't exist
   - `Serialize(serde_json::Error)` — JSON serialization failed
   - `Io(std::io::Error)` — file read/write failed
   - Derive `Error`, `Debug` from `thiserror`

2. **`decks_dir() -> PathBuf`** — returns `"./decks"`. Create the directory if
   it doesn't exist (`std::fs::create_dir_all`).

3. **`save_deck(deck: &Deck) -> Result<(), StorageError>`** in `storage.rs`:
   - Serialize deck to pretty JSON
   - Write to `./decks/{name}.json`
   - Return `Ok(())` on success

4. **`load_deck(name: &str) -> Result<Deck, StorageError>`**:
   - Read `./decks/{name}.json`
   - Deserialize to `Deck`
   - Return `NotFound` if file doesn't exist (check `io::ErrorKind::NotFound`)

5. **`list_decks() -> Result<Vec<String>, StorageError>`**:
   - List `.json` files in `./decks/` directory
   - Return deck names (strip `.json` extension)

6. **Wire CLI commands**:
   - `fcard new <name>` — creates deck, saves it immediately
   - `fcard add <name> --front ... --back ...` — loads deck, adds card, saves
   - `fcard list <name>` — loads deck, displays cards
   - `fcard review <name>` — loads deck, starts review (stub for now)
   - `fcard delete <name>` — deletes deck file
   - `fcard ls` — lists all decks

7. **Tests in `#[cfg(test)]` module**:
   - `test_save_load_roundtrip` — create deck with 2 cards, save then load,
     verify equality
   - `test_load_nonexistent` — verify `NotFound` error
   - `test_corrupt_file` — write garbage to file, verify deserialize error
   - `test_empty_deck_persistence` — save empty deck, load it back

### Hints

- `std::io::Error` has `.kind()` method; match on `ErrorKind::NotFound` to
  distinguish missing file from permission errors
- Use `serde_json::to_string_pretty` for human-readable files (debugging)
- `Path::extension()` and `Path::file_stem()` are useful for listing decks
- Tests should use a temp directory. Prefer the `tempfile` crate for
  zero-effort cleanup. If hardcoding a path, use `#[serial]` and clean up
  in a `Drop` impl or teardown function.

### Trap: Serde on enums with data

`CardStatus` derives `Serialize`/`Deserialize`. By default serde serializes
unit variants as strings (`"New"`, `"Learning"`). If you add associated data
later, the format changes — existing files won't load. Plan for versioning.

### Trap: PathBuf ownership

`decks_dir().join(name)` returns a `PathBuf`. But `std::fs::write` takes
`impl AsRef<Path>`, so `PathBuf` works directly. Don't convert to `&str`.

```rust
// Don't:
let path_str = path.to_str().unwrap();  // unnecessary, fragile

// Do:
std::fs::write(&path, json)?;           // PathBuf works
```

### Trap: Error conversion

`thiserror`'s `#[from]` only works if the source error type matches exactly.
`serde_json::from_reader` returns `serde_json::Error`, but `std::fs::File::open`
returns `std::io::Error`. Both need separate variants in your error enum.

### Verification

```bash
cargo test
cargo run -- new "japanese-101"
cargo run -- add "japanese-101" --front "こんにちは" --back "hello"
cargo run -- add "japanese-101" --front "ありがとう" --back "thank you"
cargo run -- ls
cargo run -- list "japanese-101"
# Check ./decks/japanese-101.json exists
cargo run -- review "japanese-101"   # Should load deck, print "starting review"
cat decks/japanese-101.json          # Inspect the JSON
```
