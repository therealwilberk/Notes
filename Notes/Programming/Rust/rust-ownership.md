---
tags: [rust, ownership, memory]
aliases: ["Ownership", "Rust Ownership Rules"]
parent: "[[Rust — Map of Content]]"
created: 2026-06-11
status: complete
---

# R1 — Ownership


## The Three Rules -- memorize these

```
1. Each value has exactly one owner
2. Only one owner at a time
3. Owner goes out of scope -> value is dropped
```

Everything else in this chapter is just these rules playing out.

## Stack vs Heap

| Stack | Heap |
|-------|------|
| Fixed size, known at compile time | Dynamic size, allocated at runtime |
| LIFO -- push/pop | Allocator finds space, returns pointer |
| Fast | Slower (pointer chasing) |
| integers, bools, floats, fixed arrays | String, Vec, Box |

The whole ownership system exists to manage **heap data**. Stack data handles itself. If I'm using a type that allocates on the heap (String, Vec, etc.), I need to think about ownership. If it's an i32, I don't.

## Move (heap types)

This tripped me up hard at first. Assigning a heap type **moves** ownership. The original is toast.

```rust
let s1 = String::from("hello");
let s2 = s1;                     // s1 MOVED to s2, s1 is now dead

// println!("{s1}");             // ERROR: borrow of moved value
println!("{s2}");                // OK
```

Why does Rust do this? Double-free prevention. Both s1 and s2 would point to the same heap memory. If both tried to free it on drop, that's undefined behavior. So Rust invalidates s1. Only s2 frees.


## Another trap -- reassignment drops immediately

```rust
let mut s = String::from("hello");
s = String::from("ahoy");        // "hello" is dropped RIGHT HERE
println!("{s}");                  // "ahoy"
```

The old value is dropped the instant I reassign, not at end of scope. If "hello" held a file handle or a lock, that handle is closed right at this line. Good to know.

## Copy (stack types)

Types with the `Copy` trait behave like I expect from other languages -- assignment copies the bits and both are valid.

```rust
let x = 5;
let y = x;                       // COPY, not move
println!("{x}, {y}");            // OK, both valid
```

**What types are Copy?**

All of: integers (u32, i64, ...), bool, f32, f64, char, tuples of Copy types only.

None of: String, Vec, Box, or anything that implements Drop.

**The trap:** I once built a tuple like `(i32, String)` and wondered why it moved. Second element is String (no Copy), so the whole tuple doesn't have Copy. Rust doesn't do partial moves by default here.

## Clone (explicit deep copy)

When I actually want to copy heap data:

```rust
let s1 = String::from("hello");
let s2 = s1.clone();             // deep copy -- heap data duplicated
println!("{s1}, {s2}");          // OK, both valid
```

Clone is my signal that expensive work is happening. It's a deliberate choice. If I see `.clone()` in code review, I know to think about whether it's necessary.

## Ownership & Functions

Same rules apply to function calls:

```rust
fn main() {
    let s = String::from("hi");
    takes_ownership(s);           // s MOVED in, gone from main
    // println!("{s}");           // ERROR

    let x = 5;
    makes_copy(x);                // x COPYed in, main still has it
    println!("{x}");              // OK
}

fn takes_ownership(s: String) {
    println!("{s}");
}                                 // s dropped here

fn makes_copy(x: i32) {
    println!("{x}");
}

```


## Return transfers ownership

```rust
fn give() -> String {
    String::from("yours")         // ownership moves to caller
}

fn take_and_give(s: String) -> String {
    s                             // ownership moves back
}
```

Returning via tuple when I need the value back after computing something:

```rust
fn calc_len(s: String) -> (String, usize) {
    let len = s.len();
    (s, len)                      // return ownership + value
}
```

This is tedious. That's why **references** exist. If I find myself doing this pattern a lot, I should use & instead.
