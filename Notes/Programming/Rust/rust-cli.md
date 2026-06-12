---
tags: [rust, cli, toolchain]
aliases: ["Rust CLI", "Cargo Commands"]
parent: "[[Rust — Map of Content]]"
created: 2026-06-11
status: complete
---

# C0 — 80/20 CLI Reference

Commands I actually use. The rest I'll look up when I need them.

## rustc (compiler)

| Command | What it does |
|---------|-------------|
| `rustc main.rs` | Compile to binary |
| `rustc --explain E0382` | Explain an error code -- I use this constantly |
| `rustc --edition 2024 main.rs` | Set edition explicitly |
| `rustc -O main.rs` | Compile with optimizations |

Pro tip: I barely ever call rustc directly. Cargo wraps it.

## cargo (build & package manager)

```bash
cargo new <name>          # new binary crate
cargo new <name> --lib    # new library crate
cargo build               # debug build, goes to target/debug/
cargo build --release     # release build, goes to target/release/
cargo run                 # build + run in one step
cargo check               # quick compile check, no binary -- my daily driver
cargo test                # run all tests
cargo test -- --nocapture # run tests with stdout visible (for debugging)
cargo fmt                 # auto-format code via rustfmt
cargo clippy              # linter -- catches stuff I miss
cargo add <crate>         # add dependency to Cargo.toml
cargo remove <crate>      # remove dependency
cargo update              # update Cargo.lock
cargo doc --open          # build docs + open in browser
cargo publish             # publish to crates.io
cargo clean               # delete target/ -- fixes weird build bugs sometimes
```

Watch out: `cargo check` is way faster than `cargo build`. I use it 90% of the time during dev. Only build/run when I actually need to execute.

## rustup (toolchain manager)

```bash
rustup update             # update the whole toolchain
rustup default nightly    # switch to nightly (for unstable features)
rustup target list        # list available targets
rustup target add wasm32-unknown-unknown  # for WebAssembly stuff
rustup show               # see what toolchain is active -- useful when things break
```

## Quick hits

```
rustc --version                          # compiler version
cargo --version                          # cargo version
cargo init                               # init in current dir (no new folder)
cargo run -- <args>                      # pass args to the binary
cargo add <crate> --features <feat>      # add with feature flag
cargo add <crate>@<version>              # add with specific version
cargo remove <crate>                     # remove a dependency
```

One thing that tripped me up: `cargo run -- <args>` -- the `--` separates cargo flags from binary args. Without it, cargo tries to interpret my binary args as its own flags.
