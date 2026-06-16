---
tags: [rust, if-let, let-else, control-flow, pattern-matching]
aliases: ["if let", "let else", "let...else"]
parent: "[[Rust — Map of Content]]"
created: 2026-06-12
status: complete
---

# R7 -- `if let` & `let...else`

## 80/20

```rust
use std::net::IpAddr;

// if let -- match one pattern, ignore everything else
let addr: Option<IpAddr> = Some(IpAddr::from([127, 0, 0, 1]));

if let Some(ip) = addr {
    println!("{ip}");
}
// None case is silently ignored

// if let with else -- also handle the non-match
let config: Option<String> = std::env::var("CONFIG").ok();

if let Some(path) = config {
    println!("loading config from {path}");
} else {
    println!("using defaults");
}

// let...else -- extract or bail out (diverges on non-match)
fn parse_port(val: Option<String>) -> u16 {
    let s = val else {
        return 8080;
    };
    s.parse().unwrap_or(8080)
}

// let...else with early return from a function
fn get_auth_header(headers: &[(String, String)]) -> Option<&str> {
    let (_, value) = headers.iter().find(|(k, _)| k == "Authorization")?;
    Some(value)
}
```

## `if let` -- Concise Single-Pattern Match

`if let` is sugar for `match` with one interesting arm and `_ => ()`:

```rust
// Instead of:
match config_max {
    Some(max) => println!("max is {max}"),
    _ => (),
}

// Write:
if let Some(max) = config_max {
    println!("max is {max}");
}
```

The pattern goes on the left of `=`, the expression on the right. If the pattern matches, the variable bindings are available in the body.

### Matching on enum variants

```rust
enum Message {
    Quit,
    Write(String),
    Move { x: i32, y: i32 },
}

let msg = Message::Write(String::from("hello"));

if let Message::Write(text) = &msg {
    println!("{text}");
}
```

Works with any pattern -- tuples, structs, literals:

```rust
let pair = (10, 20);

if let (0, y) = pair {
    println!("on y-axis at {y}");
}

if let (x, 0) = pair {
    println!("on x-axis at {x}");
}
```

### `if let` with `else`

This is `match` with two arms -- one for the pattern, one catch-all:

```rust
if let Some(max) = config_max {
    println!("max is {max}");
} else {
    println!("no max set");
}

// Equivalent match:
match config_max {
    Some(max) => println!("max is {max}"),
    _ => println!("no max set"),
}
```

### Chaining: `else if` and `else if let`

```rust
if let Some(val) = a {
    val
} else if let Some(val) = b {
    val
} else if let Some(val) = c {
    val
} else {
    0
}
```

Works but gets noisy quickly. For more than 2-3 branches, use `match`.

## `let...else` -- Extract or Diverge

`let...else` binds a pattern or returns/breaks/panics:

```rust
let Some(val) = optional else {
    return None;
};
// val is available here (after the else block)
```

The `else` block must **diverge** -- `return`, `break`, `continue`, `panic!`, or `exit`. It cannot "fall through" to the code after the `let`.

This is the idiomatic way to handle "extract or abort" without nesting.

### Use case: validating early in a function

```rust
use std::str::FromStr;

enum Cmd {
    Quit,
    Set(String, String),
    Print,
}

fn parse_cmd(input: &str) -> Option<Cmd> {
    let mut parts = input.trim().splitn(3, ' ');

    let cmd = parts.next()?;

    match cmd {
        "quit" | "q" => Some(Cmd::Quit),
        "set" => {
            let key = parts.next()?;
            let value = parts.next()?;
            Some(Cmd::Set(key.to_string(), value.to_string()))
        }
        "print" | "p" => Some(Cmd::Print),
        _ => None,
    }
}

// Without let...else -- deeply nested
fn get_config_val(key: &str) -> Option<String> {
    let raw = std::env::var(key).ok()?;
    Some(raw)
}

// Without let...else (old style, avoid):
fn old_style(key: &str) -> Option<String> {
    match std::env::var(key).ok() {
        Some(val) => {
            if val.is_empty() {
                None
            } else {
                Some(val)
            }
        }
        None => None,
    }
}

// With let...else and early returns:
fn with_let_else(key: &str) -> Option<String> {
    let val = std::env::var(key).ok() else {
        return None;
    };
    if val.is_empty() { None } else { Some(val) }
}
```

### `let...else` with struct destructuring

```rust
struct Request {
    method: String,
    path: String,
    headers: Vec<(String, String)>,
}

fn requires_auth(req: Request) -> bool {
    let Request { headers, .. } = req else {
        // This always succeeds -- Request has no other variants,
        // but let...else can still destructure structs.
        unreachable!();
    };
    headers.iter().any(|(k, _)| k == "Authorization")
}
```

More realistically, use `let...else` with enums:

```rust
enum UploadResult {
    Success { url: String, size: u64 },
    Failure(String),
}

fn handle_upload(result: UploadResult) -> String {
    let UploadResult::Success { url, .. } = result else {
        return String::from("upload failed");
    };
    url
}
```

## `if let` vs `match` vs `let...else`

| Situation | Tool |
|-----------|------|
| One variant matters, rest ignored | `if let` |
| One variant matters, rest handled one way | `if let`/`else` |
| Extract or bail from a function | `let...else` |
| Multiple variants need different handling | `match` |
| Need exhaustiveness check | `match` |
| Short-circuit on `None`/`Err` in a chain | `?` operator (see chapter 9) |

### Decision flow

```
Need to handle every variant?           -> match
Only one case matters, rest ignored?    -> if let
Only one case matters, rest same?       -> if let / else
Need to extract or exit the function?   -> let...else
Need to chain fallible operations?      -> ? operator
```

## Real-World Patterns

### Processing optional config

```rust
fn load_config() -> Config {
    let mut cfg = Config::default();

    if let Ok(host) = std::env::var("HOST") {
        cfg.host = host;
    }

    if let Ok(port) = std::env::var("PORT").and_then(|s| s.parse().ok()) {
        cfg.port = port;
    }

    cfg
}
```

### Ignoring `None` results in a loop

```rust
for line in io::stdin().lock().lines() {
    let line = line else { continue };
    // line is String, not Result
    process(&line);
}
```

### Parsing with fallback

```rust
fn parse_query(input: &str) -> Params {
    let mut params = Params::new();

    for pair in input.split('&') {
        let Some((k, v)) = pair.split_once('=') else { continue };
        params.insert(k.to_string(), v.to_string());
    }

    params
}
```

### Guarding with extra conditions

```rust
if let Some(val) = maybe_val {
    if val > 0 {
        println!("positive: {val}");
    }
}

// Combine with a single if:
if let Some(val) = maybe_val && val > 0 {
    println!("positive: {val}");
}
```

The `&&` after the pattern is a **match guard** combined with `if let` -- both conditions must hold.

## Traps

- **`if let` loses exhaustiveness** -- the compiler won't warn if you add a new enum variant and forget to handle it here. Use `match` when exhaustive coverage matters.
- **`let...else` must diverge** -- the `else` block must `return`, `break`, `continue`, `panic!`, or call `std::process::exit`. It cannot just assign a default and continue.
- **Pattern on the left, value on the right** -- `if let Some(x) = expr`, not `if let expr = Some(x)`.
- **`if let` vs `if`** -- `if let` is not the same as `if`. `if let Some(x) = opt` tests the pattern. `if opt.is_some()` just tests a boolean. Use `if let` when you need the inner value.
- **Over-nesting** -- too many `if let` chains are harder to read than a single `match`. If you have 3+ `if let` / `else if let`, switch to `match`.
- **`let...else` with non-enum types** -- works with structs, tuples, and literals too, but the else arm must diverge even when the pattern always matches.
