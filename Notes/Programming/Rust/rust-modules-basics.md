---
tags: [rust, modules, packages, crates]
aliases: ["Modules Basics", "Crate Root", "mod keyword", "File Tree Convention"]
parent: "[[Rust — Map of Content]]"
created: 2026-06-16
status: complete
---

# R8 -- Modules Basics: Crates, Packages & File Tree

## 80/20

```rust
// ---- Cargo.toml defines a package ----
// [package]
// name = "my_app"
// version = "0.1.0"
//
// # Binary + library in one package
// [lib]
// name = "my_lib"
//
// --- src/lib.rs  -- library crate root ----
// Declare submodules. Rust looks for:
//   src/net/io.rs  OR  src/net/io/mod.rs
mod net {
    pub mod io;          // pub so sibling modules can use it
}

mod config;              // looks for src/config.rs OR src/config/mod.rs

pub fn start() {
    config::load();
    net::io::connect();
}

// --- src/main.rs  -- binary crate root ----
// The binary crate depends on the lib crate (same package):
// use my_lib::start;   // via the lib crate name (package name)

// --- src/net.rs  OR  src/net/mod.rs  ----
pub mod io;               // looks for src/net/io.rs
pub fn resolve() {}

// --- src/net/io.rs  ----
pub fn connect() {}
// Items are private by default.

// --- src/config.rs  ----
pub fn load() {}
```

## Binary Crate vs Library Crate

Every crate has a **crate root** that the compiler compiles first.

| File | Crate Type | Role |
|------|-----------|------|
| `src/main.rs` | Binary crate root | Produces an executable |
| `src/lib.rs` | Library crate root | Produces a reusable library |
| Multiple `src/bin/*.rs` | Extra binary crates | Additional executables in same package |

A **package** (defined by `Cargo.toml`) can have:
- One library crate at most
- Any number of binary crates

```rust
// src/main.rs  -- binary crate using the lib from same package
// The lib crate is implicitly available under the package name
fn main() {
    // If package name is "my_app":
    my_app::start();
}
```

```rust
// src/lib.rs
pub fn start() {
    println!("library code");
}
```

## The `mod` Keyword

`mod` declares a module. It can be **inline** or **file-based**.

### Inline Modules

Modules nested directly in the file:

```rust
mod network {
    pub fn connect() {}

    mod dns {              // private child module
        pub fn lookup() {}
    }
}

// Access: network::connect()
// Access: network::dns::lookup()   // ERROR -- dns is private
```

Useful for small projects or tests. Quickly becomes unwieldy for real apps.

### File-Based Modules

`mod foo;` tells the compiler to load `foo` from a separate file:

```rust
// src/lib.rs
mod network;        // loads src/network.rs
```

```rust
// src/network.rs
pub fn connect() {}
```

The compiler does NOT automatically find files. Every module must be explicitly declared with `mod` at some ancestor level.

## File Tree Convention (Two Styles)

Given `mod network;` in `src/lib.rs`, the compiler resolves it as:

```
src/
  lib.rs            // crate root, declares: mod network;
  network.rs         // ✅ Style 1 (preferred, Rust 2018+)
  network/
    io.rs            // child of network, needs `mod io;` in network.rs
```

Or the older style (still works, but avoid in new code):

```
src/
  lib.rs            // declares: mod network;
  network/
    mod.rs           // network module root
    io.rs            // child of network
```

**Prefer Style 1.** The compiler searches both, but Style 1 avoids the noise of `mod.rs` files everywhere.

### Nested Modules in Files

```rust
// src/lib.rs
mod network;
mod cli;
```

```rust
// src/network.rs
pub mod io;             // looks for src/network/io.rs
pub mod protocol;       // looks for src/network/protocol.rs
mod dns;                // private -- internal to this crate
```

```rust
// src/network/io.rs
pub fn read() {}
pub fn write() {}
pub fn connect() {}
```

```rust
// src/network/protocol.rs
pub fn http() {}
pub fn ws() {}
```

```rust
// src/cli.rs
use crate::network::io;    // absolute path from crate root
use super::network;        // relative path from sibling position
```

Resulting tree:

```
src/
  lib.rs
  cli.rs
  network.rs
  network/
    io.rs
    protocol.rs
    dns.rs              // private, accessed only within network
```

## Real-World Project Structure

A typical REST API crate:

```
src/
  lib.rs                  // crate root: re-exports public API
  main.rs                 // binary: starts the server
  config/
    mod.rs                // or config.rs
    settings.rs
    env.rs
  db/
    mod.rs                // or db.rs
    pool.rs
    migrations.rs
    models.rs
  handlers/
    mod.rs                // or handlers.rs
    users.rs
    posts.rs
    health.rs
  middleware/
    mod.rs
    auth.rs
    logging.rs
  error.rs                // single file, no submodule
```

```rust
// src/lib.rs
mod config;
mod db;
mod handlers;
mod middleware;
mod error;

pub use config::Settings;
pub use db::Pool;
pub use error::AppError;
```

## Traps

- **`mod` declares *and* loads a module.** Adding a new `.rs` file is not enough. Write `mod foo;` in the parent module first.
- **File tree is convention, not magic.** `mod foo;` looks for `foo.rs` or `foo/mod.rs`. It does not scan the directory.
- **`src/main.rs` and `src/lib.rs` are separate crate roots.** Items inside `src/lib.rs` are not automatically visible in `src/main.rs`. The binary must use the library crate by name.
- **Private by default.** A child module's items are invisible to its parent. Parent must use `pub` to expose internal modules.
- **Naming collision**: `foo.rs` and `foo/mod.rs` cannot coexist. If both exist, the compiler errors. Delete one.
