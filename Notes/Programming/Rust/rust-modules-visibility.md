---
tags: [rust, modules, visibility, pub, use]
aliases: ["Visibility", "pub keyword", "use paths", "Re-exports"]
parent: "[[Rust — Map of Content]]"
created: 2026-06-16
status: complete
---

# R9 -- Visibility & Paths: `pub`, `use`, Re-exports

## 80/20

```rust
// Everything is private by default.

mod inner {
    pub fn visible() {}
    fn hidden() {}               // private -- no access outside this module
    pub(crate) fn internal() {}  // visible anywhere in THIS crate only
    pub(super) fn parent_visible() {} // visible to parent module only
}

// Bringing paths into scope with `use`
use inner::visible;              // now callable directly as `visible()`
use inner::visible as show;      // renamed import

// Re-exporting
pub use inner::visible;          // makes `visible` part of THIS module's public API

// Absolute vs relative paths
use crate::inner::visible;       // absolute: starts at crate root
use self::inner::visible;        // relative: starts at current module
use super::inner::visible;       // relative: starts at parent module
```

## Privacy Rules

| Visibility | Syntax | Can access from |
|-----------|--------|-----------------|
| Private | (nothing) | Current module + child modules |
| Public | `pub` | Anywhere (external crates included) |
| Crate-wide | `pub(crate)` | Any module in this crate |
| Parent-wide | `pub(super)` | Parent module and its children |
| Restricted | `pub(in path)` | Specific module at `path` |

```rust
mod auth {
    pub fn login() {}

    pub(crate) fn generate_token() { /* internal API */ }

    mod jwt {
        // Even though login() is pub, this module is private
        // So jwt::encode() is only accessible inside auth
        pub fn encode() {}
        fn decode() {}
    }
}
```

## `pub` on Structs vs Enums

```rust
mod types {
    pub struct User {
        pub name: String,          // field is pub
        email: String,             // field is private
    }

    impl User {
        pub fn new(name: &str, email: &str) -> Self {
            Self { name: name.into(), email: email.into() }
        }
    }

    pub enum Status {              // pub enum = all variants are pub
        Active,
        Inactive,
        Banned,
    }
}

use types::User;

let u = User::new("Alice", "alice@example.com");
u.name.to_string();                // OK -- pub field
// u.email                         // ERROR -- private field

let s = types::Status::Active;     // OK -- enum variants are pub when enum is pub
```

**Trap**: making a struct `pub` does NOT make its fields `pub`. Each field must be explicitly `pub` or provide accessor methods.

## Paths: Absolute vs Relative

```rust
// src/lib.rs
mod network;
mod cli;
```

```rust
// src/network.rs
mod io;
mod protocol;
```

```rust
// src/cli.rs
use crate::network::io;        // absolute: starts at crate root
use super::network;            // relative: goes up to lib.rs sibling
use crate::network::io::read;  // absolute to specific function

// self:: refers to current module
// use self::something;        // current module
```

| Path | Meaning | Example |
|------|---------|---------|
| `crate::` | Root of current crate | `crate::network::io::connect()` |
| `self::` | Current module | `self::helper::parse()` |
| `super::` | Parent module | `super::super::cli::run()` |
| `<crate_name>::` | External crate | `serde_json::to_string()` |

## `use` Keyword

`use` creates local bindings so paths don't need to be written every time:

```rust
// Without use
fn call() {
    crate::network::io::connect();
    crate::network::io::read();
}

// With use
use crate::network::io;

fn call() {
    io::connect();
    io::read();
}
```

`use` does NOT link or load anything. It is purely a convenience alias.

### Idiomatic `use` Style

```rust
// Functions -- bring in the parent module, call via parent::fn
use crate::network::io;
io::connect();

// Structs, enums, types -- bring them in directly
use crate::types::User;
let u = User::new("Alice");

// Exception: same-name types from different modules
use std::fmt;
use std::io;
// Then fmt::Result, io::Result -- keeps them distinct
```

### `use` with `as` (Renaming)

```rust
use std::io::Result as IoResult;
use std::fmt::Result as FmtResult;
```

## Re-exports with `pub use`

Re-exports make an item available as if it were defined in the current module. This is how library authors present a clean public API while keeping internal structure flexible.

```rust
// src/lib.rs
mod network;

// Re-export so users do:    my_crate::connect()
// Instead of:               my_crate::network::io::connect()
pub use network::io::connect;
pub use network::protocol::{http, ws};
```

```rust
// User of the crate
use my_crate::connect;
use my_crate::http;

// The internal module structure (network::io, network::protocol) is hidden.
// The crate author can refactor internals without breaking users.
```

## Re-exporting Module Paths

```rust
// src/lib.rs
pub mod network;    // makes network:: visible, but only its pub items

// To expose a private module's items through a public path:
mod crypto;                         // private module
pub use crypto::{hash, encrypt};    // re-exported as if defined at root
```

## Traps

- **`pub` is not recursive.** Making a module `pub` does not make its children `pub`. Each level must opt in.
- **`pub struct` does not make fields `pub`.** Struct fields default to private even on a public struct. Enums are the exception -- public enum = all variants public.
- **`pub use` is not the same as `use`.** `use` is local; `pub use` exports to external users. Forget the `pub` and external consumers see nothing.
- **`self::`, `super::` are relative to the current module.** Writing them in `src/cli.rs` references `cli`'s parent (`lib.rs`), not the filesystem.
- **`use` is a compile-time alias.** You cannot `use` a module or item that does not exist at compile time. No dynamic behavior.
- **Ambiguity with `use`.** If two crates export a `Result` type, bring in the parent modules with `use` rather than the types directly:
  ```rust
  use std::fmt;
  use std::io;
  // fmt::Result, io::Result -- unambiguous
  ```
