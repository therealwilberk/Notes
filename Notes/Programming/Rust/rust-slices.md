---
tags: [rust, slices, collections]
aliases: ["Slices", "String Slices", "&str"]
parent: "[[Rust — Map of Content]]"
created: 2026-06-11
status: complete
---

# R3 — Slices

A slice is a reference to a **contiguous sequence** of elements. No ownership -- just a window into existing data. Like a reference, but for a range instead of the whole thing.

## String slices

```rust
let s = String::from("hello world");
let hello = &s[0..5];     // "hello"
let world = &s[6..11];    // "world"
```

Syntax: `[start..end]` -- start inclusive, end exclusive.

### Range shorthand

```rust
&s[0..2]     is the same as &s[..2]    // from start
&s[3..len]   is the same as &s[3..]    // to end
&s[0..len]   is the same as &s[..]     // entire string
```

### The type

A string slice's type is **&str** ("string slice").

```rust
let s = "hello world";     // &str -- points into the binary
```

**The insight:** String literals are &str. That's why they're immutable -- &str is an immutable reference into the program's static memory.

**The trap:** I used to think `let s = "hello"` created a String. It doesn't. It creates a &str. If I need to mutate it, I need `let s = String::from("hello")`.

## The real value of slices -- tying data to its index

Before slices, tracking positions was fragile:

```rust
fn first_word(s: &String) -> usize {
    let bytes = s.as_bytes();
    for (i, &byte) in bytes.iter().enumerate() {
        if byte == b' ' { return i; }
    }
    s.len()
}

let mut s = String::from("hello world");
let word = first_word(&s);     // word = 5
s.clear();                      // s is now "", but word still = 5
// word is now garbage -- disconnected from the data
```

This compiled fine. Total time bomb.

With slices, the compiler ties the reference to the data:

```rust
fn first_word(s: &String) -> &str {
    let bytes = s.as_bytes();
    for (i, &byte) in bytes.iter().enumerate() {
        if byte == b' ' { return &s[0..i]; }
    }
    &s[..]
}

let mut s = String::from("hello world");
let word = first_word(&s);
s.clear();                      // ERROR: can't borrow s as mutable
println!("{word}");
// E0502: while immutably borrowed (by word)
```

The slice borrows s immutably. clear() needs a mutable borrow. Compiler blocks it. **This is the whole point of slices** -- they make the connection between data and index explicit so the compiler can enforce validity.

## The idiomatic signature -- &str over &String

```rust
fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();
    for (i, &byte) in bytes.iter().enumerate() {
        if byte == b' ' { return &s[0..i]; }
    }
    &s[..]
}
```

**Why this matters:** &str accepts ALL of these, &String only accepts one:

```rust
first_word(&s[0..6]);          // OK -- slice of String
first_word(&s[..]);            // OK -- full String slice
first_word(&s);                // OK -- &String coerces to &str via deref
first_word("hello world");     // OK -- string literal is already &str
```

Rule of thumb: if my function only needs to read a string, I take `&str`. It's more flexible. I learned this the hard way by rewriting function signatures.

## Array slices

Same concept works on arrays:

```rust
let a = [1, 2, 3, 4, 5];
let slice = &a[1..3];          // &[i32] -- type is [2, 3]
assert_eq!(slice, &[2, 3]);
```

## Memory layout -- what's really on the stack

```
s (String):        [ptr] ------------> "hello world" on heap
                   [len: 11]
                   [cap: 11]

world (&str):      [ptr] ------------> points to byte 6 of same heap
                   [len: 5]
```

A slice is just a pointer + a length. No capacity. No ownership.

**The trap:** &str and String look similar in usage but are fundamentally different in memory. String owns its buffer (and tracks capacity for resizing). &str is just a view (pointer + length, read-only). If I need ownership or mutation, I need String. If I'm just looking, &str is lighter.

## Quick reference

```
&s[..]          full string slice (&str)
&s[0..i]        partial slice from 0 to i-1
&s[i..]         from i to end
fn(s: &str)     accepts String slices, &String, and &str directly
```
> [!Quick Rule]
>A quick rule:
String = owned, mutable, heap-allocated text.
str = actual string data type (rarely used directly).
&str = borrowed view into string data; the most common string type in function parameters.
`String`: "I own this text."
and
`&str`: "I'm borrowing some text."
> 

 
