---
tags: [rust, pattern-matching, match, control-flow]
aliases: ["match", "Pattern Matching", "Destructuring"]
parent: "[[Rust — Map of Content]]"
created: 2026-06-12
status: complete
---

# R6 -- `match` (Pattern Matching)

## 80/20

```rust
// match on an enum -- each arm destructures the variant
enum HttpEvent {
    Request { method: String, path: String },
    Response(u16, u64),         // status, latency_ms
    Timeout,
}

fn handle(e: HttpEvent) {
    match e {
        HttpEvent::Request { method, path } =>
            println!("{method} {path}"),
        HttpEvent::Response(200, latency) =>
            println!("OK in {latency}ms"),
        HttpEvent::Response(code, _) =>    // _ ignores latency
            println!("error {code}"),
        HttpEvent::Timeout =>
            println!("timed out"),
    }
}

// Binding -- pattern extracts inner data into new variables
let x: Option<i32> = Some(10);
match x {
    None => println!("nothing"),
    Some(val) => println!("{val}"),   // val binds the 10
}

// Catch-all with named variable (binds the matched value)
match code {
    3 => add_hat(),
    7 => remove_hat(),
    other => move_player(other),   // other = the u8 value (not a keyword)
}

// Catch-all with _ (ignores the value)
match code {
    3 => add_hat(),
    7 => remove_hat(),
    _ => reroll(),                 // _ matches anything, binds nothing
}

// Matching on literals, ranges, multiple patterns
match status {
    200 | 201 | 204 => "success",
    300..=399 => "redirect",
    400 | 401 | 403 | 404 => "client error",
    500..=599 => "server error",
    _ => "unknown",
}
```

## How `match` Works

`match` compares a value against patterns in order. The first arm whose pattern matches wins.

```rust
match value {
    pattern1 => expr1,
    pattern2 => expr2,
    // ...
}
```

Unlike `if`, the matched expression can be any type. Each arm produces an expression -- the whole `match` evaluates to the matched arm's value. All arms must return the same type.

```rust
// match as an expression
let description = match code {
    200 => "OK",
    404 => "Not Found",
    _ => "Other",
};
```

## Binding (Destructuring)

**Binding** is when the pattern pulls data out of the matched value and assigns it to a variable.

```rust
enum Message {
    Quit,
    Write(String),
    Move { x: i32, y: i32 },
    ChangeColor(i32, i32, i32),
}

let msg = Message::Write(String::from("hello"));

match msg {
    // No data to bind
    Message::Quit => println!("quit"),

    // Binds the String inside Write to `text`
    Message::Write(text) => println!("{text}"),

    // Binds named fields to `x` and `y`
    Message::Move { x, y } => println!("({x}, {y})"),

    // Binds three i32 values to `r`, `g`, `b`
    Message::ChangeColor(r, g, b) => println!("{r} {g} {b}"),
}
```

The variables (`text`, `x`, `y`, `r`, `g`, `b`) are **new bindings** created by the pattern. They shadow any existing variables with the same name in the outer scope. The data flows from the enum variant into these variables.

### Pattern shapes for binding

| Variant | Pattern | What `x` binds to |
|---------|---------|-------------------|
| `None` | `None` | Nothing (no data) |
| `Some(v)` | `Some(x)` | The inner `T` |
| `Err(e)` | `Err(x)` | The error value |
| `Ok(v)` | `Ok(x)` | The success value |
| `Point { x, y }` | `Point { x, y }` | Each field by name |
| `(a, b, c)` | `(x, y, z)` | Each element by position |

### Ignoring inner data with `_` and `..`

```rust
match event {
    // _ ignores a single field
    HttpEvent::Response(code, _) => println!("{code}"),

    // .. ignores all remaining fields
    Message::Move { x, .. } => println!("x={x}"),

    // .. ignores everything (rare)
    Message::ChangeColor(..) => println!("some color"),
}
```

## Exhaustiveness

**`match` must cover every possible value.** The compiler checks and refuses to compile if any case is missing.

```rust
fn is_weekend(day: u8) -> bool {
    match day {
        6 | 7 => true,
        1..=5 => false,
        // COMPILE ERROR: what about 0, 8, 200?
    }
}
```

Fix with a catch-all:

```rust
fn is_weekend(day: u8) -> bool {
    match day {
        6 | 7 => true,
        _ => false,    // every other value
    }
}
```

For enums, the compiler knows every variant:

```rust
enum Color { Red, Green, Blue }

fn describe(c: Color) -> &'static str {
    match c {
        Color::Red => "warm",
        Color::Green => "nature",
        // COMPILE ERROR: Blue not covered
    }
}
```

This is a feature, not a burden: when you add a variant to an enum, the compiler points at every `match` that needs updating. No runtime surprises.

## Catch-All: `other` vs `_`

Both are catch-all patterns. The difference: **binding**.

```rust
match dice_roll {
    3 => add_hat(),
    7 => remove_hat(),
    other => move_player(other),   // binds the value to `other`
}
```

`other` is a **variable name**, not a keyword. It could be `x`, `rest`, `n`, `catch_all`, anything.

```rust
// All the same -- just variable names
other => move_player(other),
n => move_player(n),
rest => move_player(rest),
```

When `other` matches, the full value (here, the `u8`) is bound to `other` and can be used in the arm's expression.

```rust
match s {
    HttpStatus::Ok => {},
    other => handle_error(other),   // other: HttpStatus (the whole value)
}
```

### `_` -- Discard the value

Use `_` when the value isn't needed:

```rust
match dice_roll {
    3 => add_hat(),
    7 => remove_hat(),
    _ => reroll(),      // reroll doesn't need the value
}
```

`_` matches everything but **does not bind**. No variable, no "unused variable" warning.

### `_` vs `_x` (leading underscore)

Sometimes you want a name for documentation but won't use it:

```rust
match result {
    Ok(_) => println!("ok"),           // Ok value ignored
    Ok(inner) => println!("{inner}"),   // Ok value used

    // vs
    Err(_err) => println!("failed"),   // named but unused (lint will warn less aggressively)
    Err(e) => println!("{e}"),         // used
}
```

Rust warns on unused variables. `_` suppresses the warning entirely. `_err` suppresses it more gently (still catches typos).

### Rules

- **Catch-all must be last.** Arms are checked top-to-bottom. Putting `_` before specific arms means those arms never run -- Rust warns.
- **Named catch-all (`other`) also goes last.**
- **`other` shadows outer variables.** If there's a variable `other` in the enclosing scope, the `match` binding shadows it.

## Matching on Non-Enum Types

`match` works on any type, not just enums.

### Literals

```rust
match x {
    1 => "one",
    2 => "two",
    _ => "many",
}
```

### Ranges (`..=`)

```rust
match score {
    0 => "zero",
    1..=59 => "failing",
    60..=79 => "passing",
    80..=100 => "excellent",
    _ => "invalid",
}
```

### Multiple patterns (`|`)

```rust
match c {
    'a' | 'e' | 'i' | 'o' | 'u' => "vowel",
    'a'..='z' => "consonant",
    _ => "not a letter",
}
```

### Tuples (refutable matching)

```rust
fn describe_point(p: (i32, i32)) -> &'static str {
    match p {
        (0, 0) => "origin",
        (0, y) => "on y-axis at {y}",
        (x, 0) => "on x-axis at {x}",
        (x, y) => "at ({x}, {y})",
    }
}
```

### Destructuring structs

```rust
struct Point { x: i32, y: i32 }

match p {
    Point { x: 0, y } => println!("on y at {y}"),
    Point { x, y } => println!("({x}, {y})"),
}
```

## Real-World Patterns

### Parsing CLI flags

```rust
match arg.as_str() {
    "-v" | "--verbose" => set_verbose(true),
    "-q" | "--quiet" => set_verbose(false),
    "-o" => { output = args.next()?; },
    _ if arg.starts_with('-') => return Err(format!("unknown flag: {arg}")),
    _ => break,     // not a flag, stop parsing
}
```

### State machine transition

```rust
match (current_state, event) {
    (State::Idle, Event::Start) => State::Running,
    (State::Running, Event::Pause) => State::Paused,
    (State::Running, Event::Stop) => State::Idle,
    (State::Paused, Event::Resume) => State::Running,
    (state, _) => state,    // ignore invalid transitions
}
```

### Pattern with guards (`if` in arms)

```rust
match request {
    Request { method, path } if method == "GET" && path == "/health" =>
        Response::ok("healthy"),
    Request { method, .. } if method == "POST" =>
        Response::created(),
    _ =>
        Response::not_found(),
}
```

## Traps

- **`match` must be exhaustive** -- the compiler enforces this. Always add a `_` or named catch-all for non-enum types or when you're not covering every variant.
- **Catch-all last** -- patterns are evaluated in order. Rust warns if an arm can never match because a previous catch-all swallowed it.
- **`other` is not a keyword** -- it's just a variable name. The pattern `other` matches anything and binds to `other`. Change the name to anything else and it still works: `x =>`, `rest =>`, `n =>`.
- **`_` does not bind** -- use `_` to match and discard. Use a name to bind.
- **Shadowing** -- `match x { y => y }` binds a new `y` shadowing any outer `y`. The original `x` is not usable after being matched (moved if not `Copy`).
- **Guard vs pattern** -- `if` guards (`if` after the pattern) are checked after the pattern match. A guard can fail, letting the match fall through to the next arm.
- **All arms must return the same type** -- `match x { 1 => "hi", 2 => 42 }` won't compile. Each arm's expression must be the same type.
