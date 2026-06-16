---
tags: [rust, exercises, programming]
parent: "[[Rust -- Map of Content]]"
created: 2026-06-15
status: complete
---

# Rust Exercises — `fcard` Project

Progressive CLI flashcard/SRS tool. Each module builds on the last.

## Difficulty Key

| Icon | Level | Description |
|------|-------|-------------|
| G | Guided | Goals + concept explanations + hints for traps |
| SG | Semi-guided | Goals + concept explanations, no step-by-step |
| U | Unguided | Goal only. Figure it out. |

## Modules

| # | Module | Difficulty | Concepts Introduced |
|---|--------|------------|-------------------|
| 1 | [[module-1/README\|Foundation — Data Model & CLI]] | G → SG | `clap`, `lib.rs`/`main.rs`, `Display`, unit tests |
| 2 | [[module-2/README\|Persistence & Errors]] | G | `serde`, `thiserror`, `PathBuf`, `Result`, `?` |
| 3 | [[module-3/README\|SRS Engine & State Machine]] | SG | SM-2 intervals, `From`/`Into`, `Duration`, `iter_mut` |
| 4 | [[module-4/README\|Search, Tags & HashMap]] | U | `HashMap`, iterator adapters, lifetime annotations |
| 5 | [[module-5/README\|CLI Polish & Stats]] | U | `colored`, integration tests, data aggregation |
| 6 | [[module-6/README\|Capstone — Config & Discovery]] | U | `toml`, config merging, cross-deck stats, 90% coverage |
