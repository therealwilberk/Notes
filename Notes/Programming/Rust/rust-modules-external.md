---
tags: [rust, modules, external, crates, dependencies]
aliases: ["External Crates", "Dependencies", "Cargo.toml", "Nested Paths", "Glob"]
parent: "[[Rust — Map of Content]]"
created: 2026-06-16
status: complete
---

# R10 -- External Crates, Nested Paths & Glob

## 80/20

```toml
# Cargo.toml
[dependencies]
serde = { version = "1", features = ["derive"] }
serde_json = "1"
reqwest = { version = "0.12", features = ["json"] }
```

```rust
// External crate: use <crate_name>::<module>::<Item>
use serde::{Deserialize, Serialize};
use reqwest::Client;

// Nested paths -- collapse repeated prefixes
use std::{io, fs};                     // same as: use std::io; use std::fs;
use std::io::{self, Read, Write};      // self brings io itself into scope

// Glob -- bring everything public into scope
use std::io::prelude::*;               // common in trait imports
use serde_json::*;                     // ⚠ makes it hard to know origins

// The standard library (std) is implicitly available
// -- no Cargo.toml entry needed
```

## External Crates

Adding an external dependency:

```toml
# Cargo.toml
[dependencies]
serde_json = "1.0"
```

```rust
// src/lib.rs or src/main.rs
use serde_json::to_string;

let json = to_string(&some_struct).unwrap();
```

The crate name in `Cargo.toml` becomes the root module name in code. `serde_json = "1.0"` means `use serde_json::...`.

### The Standard Library (`std`)

`std` is always available without adding it to `Cargo.toml`:

```rust
use std::collections::HashMap;
use std::fs;
use std::io::Read;
```

It is the only crate with this special treatment. Everything else must be listed in `[dependencies]`.

### Crate Name vs Package Name

```toml
[dependencies]
# Usually the crate name matches the package name
tokio = "1"

# Rename the local alias -- use when two crates conflict
toml_edit = { package = "toml_edit", version = "0.22" }
toml_old = { package = "toml", version = "0.5" }
```

```rust
use tokio::net::TcpListener;
use toml_edit::Document;
use toml_old::Value as TomlValue;  // separate from serde's Value
```

## Nested Paths

Without nested paths:

```rust
use std::io;
use std::io::Read;
use std::io::Write;
use std::fs;
use std::fs::File;
```

With nested paths:

```rust
use std::io::{self, Read, Write};
use std::fs::{self, File};
```

`self` in a nested path means "bring the parent module itself into scope":

```rust
use std::io::{self, Read};

// io is now available as a module
// Read is available directly

fn main() {
    io::stdin();        // through io module
    let _: &dyn Read;   // directly
}
```

### Nesting Arbitrarily Deep

```rust
use std::path::{Path, PathBuf};
use std::collections::{HashMap, HashSet, BTreeMap};
use tokio::net::{TcpListener, TcpStream, UdpSocket};
```

Maximum nesting is one level deep. For example:

```rust
// ✅ OK
use a::b::{c, d, e};

// ❌ Not valid syntax
use a::{b::{c, d}, e};
```

If you need deeper, declare intermediate `use` statements:

```rust
use a::b;
use b::{c, d};
```

## Glob Operator (`*`)

Brings all public items in a module into scope:

```rust
use std::io::prelude::*;           // brings all traits from prelude
use serde_json::*;                 // brings everything from serde_json
```

### When to Use

| Use case | Do this |
|----------|---------|
| Bringing traits into scope for method calls | `use SomeCrate::prelude::*;` |
| Testing (`tests/` module needs everything from the parent) | `use super::*;` |
| Quick REPL-style prototyping | `use crate::*;` |
| Library public API re-exports | Avoid globs -- explicit is clearer |

### When NOT to Use

```rust
// ❌ Bad -- impossible to tell where things come from
use std::*;
use serde::*;
use crate::utils::*;

// ✅ Good -- explicit, easy to trace
use std::collections::HashMap;
use serde::{Serialize, Deserialize};
use crate::utils::{parse_config, validate_port};
```

**Trap**: glob can silently shadow names and make refactoring dangerous. Adding a new public item to a module can break code that glob-imported it. Only use globs for prelude modules and test helpers.

## Internal vs External Imports

| | Internal Module | External Crate |
|---|---|---|
| Path start | `crate::`, `self::`, `super::` | `<crate_name>::` |
| Declaration | `mod foo;` in some ancestor | `[dependencies]` in Cargo.toml |
| Visibility | Controlled by `pub` | Controlled by the crate's `pub` API |
| Re-export | `pub use crate::foo::Bar` | `pub use serde::Serialize` |
| Loading | Compiler loads from filesystem | Cargo fetches + compiles separately |

Both use the same `use` syntax after they are available. The only difference is **how they are declared**.

```rust
// Internal -- must be declared with `mod` somewhere up the tree
mod network;                         // declares internal module
use crate::network::connect;         // use internal path

// External -- must be in Cargo.toml [dependencies]
// [dependencies]
// serde = "1"
use serde::Serialize;                // use external path
```

## Binary + Library in the Same Package

When a package has both `src/main.rs` and `src/lib.rs`:

```rust
// Cargo.toml
[package]
name = "my_app"
```

```rust
// src/lib.rs
pub mod db;
pub fn start() {}
```

```rust
// src/main.rs
// The lib crate is available under the package name
use my_app::db;
use my_app::start;

fn main() {
    start();
}
```

The binary crate treats the library crate as if it were an external dependency. They share the package but have separate crate roots.

## Traps

- **External crates need `[dependencies]` entry.** The compiler does not search the filesystem for them. Cargo must fetch them first.
- **`std` is implicit but still needs `use`.** `use std::fs;` brings it into scope. The path `std::` is always available without Cargo.toml entries.
- **Crate name in Cargo.toml becomes module name.** `serde_json = "1"` means `serde_json::...` in code. Rename via `[dependencies].foo = { package = "serde_json", version = "1" }`.
- **Glob hides origins.** `use module::*;` makes it impossible to grep where a name came from. Restrict to prelude modules and `super::*` in tests.
- **`self` in nested paths is not optional.** `use std::{io, io::Read}` is redundant. Write `use std::io::{self, Read}` instead -- `self` brings `io` itself, `Read` brings the child.
- **Binary crate is separate from library crate** even in the same package. Items in `src/lib.rs` are NOT magically in scope in `src/main.rs`. Use `package_name::item` to access them.
