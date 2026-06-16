---
tags: [rust, structs, methods, oop]
aliases: ["Structs", "Methods", "impl"]
parent: "[[Rust — Map of Content]]"
created: 2026-06-11
status: complete
---

# R4 -- Structs

## 80/20

```rust
// Define
struct ServerConfig {
    host: String,
    port: u16,
    timeout_secs: u64,
    tls: bool,
}

// Instantiate (field order doesn't matter)
let cfg = ServerConfig {
    host: String::from("0.0.0.0"),
    port: 8080,
    timeout_secs: 30,
    tls: true,
};

// Field init shorthand
fn load_config(host: String, port: u16) -> ServerConfig {
    ServerConfig { host, port, timeout_secs: 30, tls: false }
}

// Struct update syntax (..other spreads remaining fields)
let cfg_prod = ServerConfig { host: String::from("prod.example.com"), ..cfg };

// Tuple struct
struct PortRange(u16, u16);
let http_range = PortRange(80, 443);

// Unit-like struct (marker / trait target)
struct Validated;

// Methods
struct SensorReading { temperature: f64, humidity: f64, pm25: f64 }

impl SensorReading {
    fn aqi(&self) -> f64 {                          // &self borrows
        self.pm25 * 0.5 + self.humidity * 0.1
    }
    fn calibrate(&mut self, offset: f64) {          // &mut self mutates
        self.temperature += offset;
    }
    fn from_raw(raw: &[f64]) -> Self {              // associated function (no &self)
        Self { temperature: raw[0], humidity: raw[1], pm25: raw[2] }
    }
}

let reading = SensorReading { temperature: 22.5, humidity: 55.0, pm25: 12.0 };
reading.aqi();
let raw_reading = SensorReading::from_raw(&[23.0, 60.0, 8.0]);   // :: for associated
```

## Defining & Instantiating

A struct groups related data into one type. Fields are named, unlike tuples.

```rust
struct ApiResponse {
    status_code: u16,
    body: String,
    headers: Vec<(String, String)>,
    cached: bool,
}

let response = ApiResponse {
    status_code: 200,
    body: String::from("OK"),
    headers: vec![],
    cached: false,
};

// Mutable instance -- the whole thing is mut or not
let mut resp = ApiResponse { status_code: 404, body: String::from("Not Found"), headers: vec![], cached: false };
resp.status_code = 200;
resp.body = String::from("OK");
```

**No way to make individual fields mutable -- it is all-or-nothing.**

**Field init shorthand**: when a variable name matches the field name, write it once.

```rust
fn ok_response(body: String) -> ApiResponse {
    ApiResponse { status_code: 200, body, headers: vec![], cached: false }
}
```

## Struct Update Syntax

Spread remaining fields from another instance:

```rust
let cached_resp = ApiResponse { cached: true, ..response };
```

**Trap**: spreads **move** heap-allocated fields (String, Vec) and **copy** stack fields (bool, int). After `..response`, `response.status_code` and `response.cached` are still usable, but `response.body` and `response.headers` are moved. To keep both usable, derive `Clone` and call `.clone()`.

## Tuple Structs

A named type wrapping unnamed fields. Different from a regular tuple because the type name matters.

```rust
struct GpsCoord(f64, f64);
struct PixelCoord(u32, u32);

let home = GpsCoord(-33.8688, 151.2093);
let pixel = PixelCoord(1920, 1080);

// GpsCoord and PixelCoord are incompatible -- compiler catches passing one for the other
```

Common uses:
- **Newtype pattern**: wrap a single type to add type safety

```rust
struct Meters(f64);
struct Seconds(f64);

fn speed(dist: Meters, time: Seconds) -> f64 {
    dist.0 / time.0
}

speed(Meters(100.0), Seconds(9.58));    // OK
// speed(Seconds(9.58), Meters(100.0)); // COMPILE ERROR -- wrong order
```

- **Wrapper around external types**: implement traits on types that don't belong to you (orphan rule workaround)

## Unit-Like Structs

No fields at all. Useful as markers, flags, or type-level state machines.

```rust
struct Authenticated;
struct Guest;

struct Session {
    user_id: u64,
    state: Guest,        // or Authenticated
}

// Used with traits to enforce state at compile time
```

The data is in the type itself, not in any fields. Common in type-state patterns and as trait implementors.

## Ownership in Structs

Structs own their data. Using references (`&str` instead of `String`) requires lifetime annotations (chapter 10):

```rust
struct Request<'a> {
    method: &'a str,      // needs lifetime
    path: &'a str,
}

// Without lifetimes:
// struct Request { method: &str }  // ERROR: missing lifetime specifier
```

Until lifetimes are comfortable, use owned types (`String`, `Vec<T>`, `Box<T>`) in structs. The struct takes full ownership and drops everything when it goes out of scope.

## Method Syntax

Methods are functions in an `impl` block. The first parameter is always `self` in some form.

```rust
#[derive(Debug)]
struct HttpRequest {
    method: String,
    path: String,
    headers: Vec<(String, String)>,
    body: Vec<u8>,
}

impl HttpRequest {
    // &self -- read the data
    fn path(&self) -> &str { &self.path }

    fn header(&self, name: &str) -> Option<&str> {
        self.headers.iter()
            .find(|(k, _)| k == name)
            .map(|(_, v)| v.as_str())
    }

    // &mut self -- mutate the data
    fn add_header(&mut self, name: &str, value: &str) {
        self.headers.push((name.to_string(), value.to_string()));
    }

    // self -- consume the data (rare, usually for transformation)
    fn into_bytes(self) -> Vec<u8> {
        let mut buf = vec![];
        buf.extend_from_slice(&self.body);
        buf
    }
}
```

**When to use which:**

| Form | Borrow | Use case |
|------|--------|----------|
| `&self` | Immutable ref | Reading / querying data |
| `&mut self` | Mutable ref | Updating data |
| `self` | Ownership | Consuming, transforming into something else |

## Multiple Parameters

Methods can take additional arguments beyond `self`:

```rust
impl HttpRequest {
    fn with_header(mut self, name: &str, value: &str) -> Self {
        self.headers.push((name.to_string(), value.to_string()));
        self
    }

    fn is_method(&self, method: &str) -> bool {
        self.method == method
    }
}

// Builder-style chaining
let req = HttpRequest {
    method: String::from("POST"),
    path: String::from("/api/data"),
    headers: vec![],
    body: vec![],
}.with_header("Content-Type", "application/json")
 .with_header("Accept", "application/json");
```

## Associated Functions

Functions in `impl` that do NOT take `self`. Called with `Type::function()`. Used as constructors.

```rust
impl HttpRequest {
    fn get(path: &str) -> Self {
        Self {
            method: String::from("GET"),
            path: path.to_string(),
            headers: vec![],
            body: vec![],
        }
    }

    fn post(path: &str, body: &[u8]) -> Self {
        Self {
            method: String::from("POST"),
            path: path.to_string(),
            headers: vec![],
            body: body.to_vec(),
        }
    }
}

let req = HttpRequest::get("/health");
let req = HttpRequest::post("/api/data", b"{\"key\":\"val\"}");
```

`Self` inside the `impl` block is an alias for the type name.

## Multiple impl Blocks

Methods can be split across multiple `impl` blocks. Not useful yet, but essential with generics and trait implementations:

```rust
impl HttpRequest {
    fn path(&self) -> &str { &self.path }
}

impl HttpRequest {
    fn header(&self, name: &str) -> Option<&str> { /* ... */ }
}

// Same as one block -- purely organizational
```

## Auto-Deref on Method Calls

When calling a method, Rust automatically inserts `&`, `&mut`, or `*` to match the method signature. This means:

```rust
let req = HttpRequest::get("/");
let ref_req = &req;

ref_req.path();     // Rust does (*ref_req).path() -- auto-deref
(&req).path();      // explicit -- same thing
req.path();         // Rust does (&req).path() -- auto-ref
```

This is why method calls work on references without explicit dereferencing. The compiler inserts the right amount of `&` / `*` automatically.

## Real-World Patterns

**Builder pattern** (associated function + consuming builder):

```rust
impl HttpRequest {
    fn builder() -> HttpRequestBuilder {
        HttpRequestBuilder::new()
    }
}

struct HttpRequestBuilder {
    method: String,
    path: String,
    headers: Vec<(String, String)>,
    body: Vec<u8>,
}

impl HttpRequestBuilder {
    fn new() -> Self {
        Self { method: String::from("GET"), path: String::new(), headers: vec![], body: vec![] }
    }
    fn method(mut self, method: &str) -> Self { self.method = method.to_string(); self }
    fn path(mut self, path: &str) -> Self { self.path = path.to_string(); self }
    fn header(mut self, name: &str, value: &str) -> Self {
        self.headers.push((name.to_string(), value.to_string())); self
    }
    fn body(mut self, body: &[u8]) -> Self { self.body = body.to_vec(); self }
    fn build(self) -> HttpRequest {
        HttpRequest { method: self.method, path: self.path, headers: self.headers, body: self.body }
    }
}

let req = HttpRequest::builder()
    .method("POST")
    .path("/api/data")
    .header("Content-Type", "application/json")
    .body(b"{}")
    .build();
```

**Validation at construction:**

```rust
struct Port(u16);

impl Port {
    fn new(value: u16) -> Result<Self, String> {
        if value < 1024 {
            Err(format!("port {value} is privileged, use >= 1024"))
        } else {
            Ok(Self(value))
        }
    }
}

let port = Port::new(8080).unwrap();
// Port::new(80);   // Error: "port 80 is privileged, use >= 1024"
```

## Traps

- **Struct update syntax moves heap fields** -- after `..other`, `other.string_field` is moved (dead). Stack fields (bool, int) are fine.
- **No per-field mutability** -- either the whole instance is `mut` or none of it is.
- **References in structs need lifetimes** -- use owned types (`String`, `Vec`) until comfortable with lifetime syntax.
- **Auto-deref hides what's happening** -- method calls auto-insert `&`/`*`. The code compiles but the borrow semantics are happening invisibly.
- **Associated functions use `::` not `.`** -- `Type::function()`, not `Type.function()`.
- **`self` (no ref) consumes ownership** -- use `&self` for reading, `&mut self` for writing. `self` is for builders and conversions only.
- **Newtype ergonomics** -- accessing the inner value requires `.0` syntax. Can be noisy. Implement `Deref` or `Into` to smooth it out.
