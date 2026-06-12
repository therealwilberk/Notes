---
tags: [rust, references, borrowing]
aliases: ["References", "Borrowing"]
parent: "[[Rust — Map of Content]]"
created: 2026-06-11
status: complete
---

# R2 — References & Borrowing

References let me use a value without taking ownership. The compiler enforces the rules so I don't accidentally shoot myself in the foot.

## Basics

```
&  = create a reference (borrow, no ownership)
*  = dereference (rarely write it -- Rust auto-derefs for method calls)
```

```rust
fn main() {
    let s1 = String::from("hello");
    let len = calc_len(&s1);       // borrow, not move
    println!("'{s1}' is {len}");   // OK -- s1 still mine
}

fn calc_len(s: &String) -> usize { // &String = reference parameter
    s.len()
}                                   // s goes out of scope
                                    // but s1 is NOT dropped
```

## The Two Rules

```
1. At any time: EITHER one &mut T OR unlimited &T (never both)
2. References must always be valid (no dangling pointers)
```

This is the single most important thing in this chapter. Internalize it.

## Immutable references (&T)

Read-only. I can have as many as I want.

```rust
let s = String::from("hello");
let r1 = &s;             // OK
let r2 = &s;             // OK -- unlimited immut refs
// r1.push_str("!");     // ERROR: can't mutate through &T
```

## Mutable references (&mut T)

Exclusive write access. Only one at a time. This is where people get frustrated.

```rust
let mut s = String::from("hello");

fn change(s: &mut String) {
    s.push_str(" world");
}

change(&mut s);
```

## The exclusivity rule -- where the compiler yells at me

```rust
let mut s = String::from("x");

let r1 = &mut s;
// let r2 = &mut s;      // ERROR: two mutable refs at same time
```

```rust
let mut s = String::from("x");
let r1 = &s;
let r2 = &s;
// let r3 = &mut s;      // ERROR: mutable ref while immut refs alive
```

**Why?** Data races. If one reference writes while another reads, the reader sees garbage. Rust catches this at compile time. Other languages catch it at 3am in production.

**What saved me -- NLL (Non-Lexical Lifetimes):**

The borrow scope ends at the reference's **last use**, not at `}`.

```rust
let mut s = String::from("x");
let r1 = &s;
let r2 = &s;
println!("{r1}, {r2}");          // r1, r2 last used here -- borrowed scope ends
let r3 = &mut s;                  // OK -- scopes don't overlap
```

This alone made borrowing click for me. The compiler isn't mad at me for the whole function. It only cares about overlapping usage.

**The trap I hit most often:** I'd create an immutable reference, do something that needs a mutable reference somewhere across the function, and wonder why it fails. Solution: either reorder so the immutable borrow finishes before the mutable one starts, or use a block to scope it.

```rust
let mut s = String::from("hello");
{
    let r1 = &s;
    println!("{r1}");              // ends here
}
// NOTE:
let r2 = &mut s;                   // OK -- previous scope done
// "The reference can mutate the data.. while in:
// let mut r1 = &s;
// The reference itself can be reassigned, but the data is read-only.

println!("{r2}");
```

## Dangling references

Rust guarantees no dangling pointers at compile time. This doesn't compile:

```rust
fn dangle() -> &String {          // ERROR: missing lifetime specifier
    let s = String::from("hello");
    &s
}                                  // s dropped, reference points to freed memory
```

Fix is simple -- return the owned value instead:

```rust
fn no_dangle() -> String {
    let s = String::from("hello");
    s                               // ownership moves out, nothing dangles
}
```

**The insight:** If I need to return a reference, the data must outlive the function. Either it was passed in (so caller owns it) or it's static. If I created it inside the function, I must return it by value.

## Summary

```
I want to...                     I use...
Read without owning              &T
Mutate without owning            &mut T
Transfer ownership               T (move)
```

More on this when I hit lifetimes in Ch 10.
