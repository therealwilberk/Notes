---
tags: [rust, enums, option]
aliases: ["Enums", "Enum Variants", "Option"]
parent: "[[Rust — Map of Content]]"
created: 2026-06-12
status: complete
---

# R5 -- Enums (Defining & Using)

## 80/20

```rust
// Three variant shapes on one enum
enum TicketStatus {
    Open,                              // unit-like: no data
    InProgress(String),                // tuple-like: single payload
    Assigned { user: u64, team: String }, // struct-like: named fields
    Closed { reason: String, by: u64 },
}

// Construct -- variant names are constructor functions
let t1 = TicketStatus::Open;
let t2 = TicketStatus::InProgress(String::from("triaging"));
let t3 = TicketStatus::Assigned { user: 42, team: String::from("platform") };

// Access inner data exclusively via pattern matching
fn status_summary(s: &TicketStatus) -> String {
    match s {
        TicketStatus::Open => "open".to_string(),
        TicketStatus::InProgress(notes) => format!("in progress: {notes}"),
        TicketStatus::Assigned { user, .. } => format!("assigned to user {user}"),
        TicketStatus::Closed { reason, .. } => format!("closed: {reason}"),
    }
}

// Methods on enums (same as structs)
impl TicketStatus {
    fn is_terminal(&self) -> bool {
        matches!(self, TicketStatus::Closed { .. })
    }
}

// Option<T> -- Rust's Maybe (prelude, no import)
struct User { id: u64, name: String }

fn find_user(id: u64) -> Option<User> {
    if id == 42 { Some(User { id, name: String::from("Alice") }) }
    else { None }
}

let user = find_user(42);
// user is Option<User> -- must extract before using inner User
```

## Defining an Enum

An enum is a single type that can be one of several variants. Unlike structs where all fields are always present, an enum value is exactly one variant.

```rust
enum Direction { North, South, East, West }

let d = Direction::North;
```

The `::` syntax namespaces variants under the enum type. Both `Direction::North` and `Direction::South` are the same type `Direction`.

### When enums beat structs

An enum is a single type. Structs are separate types. This matters for functions:

```rust
struct SshCreds { user: String, key_path: String }
struct ApiToken { token: String, scope: String }

// Must write two functions or use a trait
fn use_ssh(c: SshCreds) {}
fn use_token(t: ApiToken) {}

// With an enum, one function handles both
enum AuthMethod {
    Ssh { user: String, key_path: String },
    Token { token: String, scope: String },
}

fn authenticate(auth: AuthMethod) {
    match auth { /* handle both */ }
}
```

## Three Variant Shapes

### Unit-like (no data)

```rust
enum LogLevel { Debug, Info, Warn, Error }
```

Used as flags, markers, or state discriminators. Variants carry zero bytes of payload data -- just the discriminant.

### Tuple-like (anonymous positional data)

```rust
enum Event {
    KeyPress(u32),            // single value
    Resize(u32, u32),         // multiple values: width, height
    Error(u16, String),       // mixed types
}
```

Access by destructuring -- **no field names, just position**.

```rust
match ev {
    Event::Resize(w, h) => println!("{w}x{h}"),
    // ...
}
```

Common for wrappers: `Some(T)`, `Err(E)`, `Ok(T)`.

### Struct-like (named fields)

```rust
enum HttpRequest {
    Get { path: String, headers: Vec<(String, String)> },
    Post { path: String, body: Vec<u8>, headers: Vec<(String, String)> },
}
```

Access by field name -- same syntax as struct patterns:

```rust
match req {
    HttpRequest::Get { path, .. } => println!("GET {path}"),
    HttpRequest::Post { path, body, .. } => println!("POST {path} body={}b", body.len()),
}
```

Use struct-like when the variant has multiple fields and position isn't meaningful. Use tuple-like when order is natural (coordinates, ranges) or there's only one field (wrappers).

## `Option<T>` -- The Null Alternative

Rust has no `null`. Instead, `Option<T>` from the standard library:

```rust
enum Option<T> {
    None,
    Some(T),
}
```

**In the prelude** -- `Option`, `Some`, `None` are available without `use` or `Option::` prefix.

```rust
let a = Some(42);               // inferred as Option<i32>
let b: Option<i32> = None;      // None needs type hint
let c = Some(String::from("hi"));

// Option<T> and T are different types -- compiler prevents mixing
let x: i32 = 5;
let y: Option<i32> = Some(5);
// let sum = x + y;             // COMPILE ERROR
```

**Why this is good:** you cannot accidentally use a possibly-null value as a real value. Every `Option<T>` forces you to handle the `None` case before you can use the `T`.

### Extracting from Option

```rust
fn double(x: Option<i32>) -> Option<i32> {
    match x {
        None => None,
        Some(v) => Some(v * 2),
    }
}

// Or use built-in methods
let v = Some(10);
v.unwrap_or(0);              // 10 -- returns default if None
v.map(|x| x * 2);           // Some(20)
v.and_then(|x| if x > 5 { Some(x) } else { None });  // Some(10)
```

Common in real code: lookups, parsing, finding.

```rust
fn get_env(key: &str) -> Option<String> {
    std::env::var(key).ok()
}

fn parse_port(s: &str) -> Option<u16> {
    s.parse::<u16>().ok().filter(|&p| p > 0)
}

let port = get_env("PORT")
    .and_then(|s| parse_port(&s))
    .unwrap_or(8080);
```

## Enums vs Structs -- Decision Table

| Need | Use |
|------|-----|
| A value is always one of several categories | Enum |
| All fields always present together | Struct |
| You need to add behavior to a closed set of types | Enum (via match) |
| You need to extend types later (open set) | Trait + structs |
| A field is sometimes absent | `Option<T>` (in struct or enum variant) |

## Real-World Patterns

### State machine with typed transitions

```rust
enum ConnectionState {
    Disconnected,
    Connecting { attempt: u8, addr: String },
    Connected { session_id: u64 },
    Failed(String),
}

impl ConnectionState {
    fn transition(self, event: ConnectionEvent) -> Self {
        match (self, event) {
            (ConnectionState::Disconnected, Connect(addr)) =>
                ConnectionState::Connecting { attempt: 1, addr },
            (ConnectionState::Connecting { attempt, addr }, Timeout) =>
                ConnectionState::Connecting { attempt: attempt + 1, addr },
            (ConnectionState::Connecting { .. }, Established(id)) =>
                ConnectionState::Connected { session_id: id },
            (s, Reset) => ConnectionState::Disconnected,
            _ => self,  // ignore invalid transitions
        }
    }
}
```

### Error type with context

```rust
enum ApiError {
    Http { status: u16, body: String },
    Tls { cause: String },
    Timeout { elapsed: std::time::Duration },
    RateLimited { retry_after: u64 },
}
```

Better than a flat string -- each variant carries exactly the info relevant to that error.

### Enum in an API response

```rust
enum ApiResult<T> {
    Success { data: T, cached: bool },
    Failure { code: u16, message: String },
    Pending { request_id: u64 },
}
```

## Traps

- **Enum variants are constructors, not standalone types** -- `TicketStatus::Open` is a `TicketStatus`, not a separate type. You cannot have a function that accepts only the `Open` variant.
- **Pattern matching is the only way to get data out** -- no `variant.field` access like in C or Java. This is intentional: you must handle every variant.
- **`None` needs a type annotation** -- `let x = None;` won't compile. The compiler can't infer what `T` is.
- **`Option<T>` is NOT `T`** -- trying to use `Some(5)` as `5` is a compile error. You must extract.
- **Option has zero overhead** -- the discriminant is optimized away when `None` can be represented as a niche (e.g., `Option<Box<T>>` is pointer-sized, no extra byte).
- **Deeply nested enums are noisy** -- `match` inside `match` inside `match`. Consider flattening or using `if let` chains.
- **Adding a variant breaks every `match`** -- that's the point. The compiler tells you everywhere you need to handle the new case.
