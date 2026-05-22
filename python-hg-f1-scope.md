# F1 — Scope

> **What this fixes:** Mystery `NameError`s, `UnboundLocalError`s you don't understand, and the reflex to make everything global when things don't work.
>
> **The shift:** Scope isn't a Python quirk — it's a lookup system. Once you know the rules, the errors become predictable.

---

## The bridge from C/Rust

In C, scope is block-based — any `{}` creates a new scope. In Rust, it's even stricter — the borrow checker enforces it. Python is different: **scope in Python is function-based, not block-based.**

```python
# In C, this would create a new scope inside the if block.
# In Python, it does NOT.

if True:
    x = 10

print(x)  # 10 — x is accessible here. No block scope in Python.
```

```python
# But a function DOES create a new scope
def my_func():
    y = 20

print(y)  # NameError — y only exists inside my_func
```

This trips up people coming from C. `for` loops, `if` statements, `with` blocks — none of them create a new scope. Only **functions, classes, and modules** create new scopes in Python.

---

## The LEGB rule

When Python encounters a name (variable, function, anything), it searches for it in a specific order. That order is **LEGB**:

```
L — Local       → Inside the current function
E — Enclosing   → Inside any outer functions (if nested)
G — Global      → At the top of the current module/file
B — Built-in    → Python's built-in names (len, print, range, etc.)
```

Python stops at the **first match it finds.** If it exhausts all four levels without finding the name, you get a `NameError`.

```python
x = "global"          # G — Global scope

def outer():
    x = "enclosing"   # E — Enclosing scope

    def inner():
        x = "local"   # L — Local scope
        print(x)      # Prints "local" — found at L, stops there

    inner()
    print(x)          # Prints "enclosing" — found at E

outer()
print(x)              # Prints "global" — found at G
```

### B — Built-in scope

Built-ins are Python's reserved names: `len`, `print`, `range`, `type`, `int`, `list`, `dict`, etc. They live in the `builtins` module and are always available as the last resort.

```python
# Built-ins are always findable — you never import them
result = len([1, 2, 3])  # len found at B — Built-in scope
```

> ⚠️ **Trap:** You can accidentally shadow built-ins with your own names. Python won't stop you — it'll just stop finding the built-in.
>
> ```python
> list = [1, 2, 3]      # You just shadowed the built-in list()
> new = list("hello")   # TypeError — list is now your variable, not the built-in
> ```
>
> Names to **never** use as variable names: `list`, `dict`, `set`, `type`, `id`, `input`, `print`, `len`, `sum`, `min`, `max`, `filter`, `map`, `zip`, `open`.

---

## Local scope

Variables defined inside a function are local. They're created when the function is called and destroyed when it returns. They don't exist outside.

```python
def calculate_vat(price):
    rate = 0.16           # Local — only exists inside calculate_vat
    vat = price * rate    # Local
    return vat

print(rate)  # NameError — rate doesn't exist out here
```

### The `UnboundLocalError` trap

This is the most common scope error in Python, and it's subtle:

```python
count = 0

def increment():
    count += 1    # UnboundLocalError!
    return count
```

Why? Because Python sees the assignment `count += 1` (which is `count = count + 1`) and decides `count` is a local variable — *before* the function runs. Then when it tries to read `count` on the right side of the assignment, the local variable doesn't have a value yet.

The fix is either `global` (see below) or — better — restructure to avoid shared state:

```python
# Better — pass count in, return count out. No shared state.
def increment(count):
    return count + 1

count = 0
count = increment(count)  # count is now 1
```

---

## Global scope

Variables defined at the top level of a module are global. They're accessible anywhere in that module — but **readable only** from inside functions, not writable, unless you declare `global`.

```python
APP_NAME = "Pipeline"     # Global — readable from anywhere in this module

def show_app():
    print(APP_NAME)       # Fine — reading a global variable

show_app()                # "Pipeline"
```

### The `global` keyword

To *modify* a global variable from inside a function, you need to declare it:

```python
request_count = 0

def handle_request():
    global request_count      # "I mean the global one, not a new local"
    request_count += 1

handle_request()
handle_request()
print(request_count)          # 2
```

> ⚠️ **Trap and note:** Using `global` to share mutable state between functions is almost always a design problem. If multiple functions need to read and write the same counter or flag, that's a signal they belong together in a class, or the state should be passed explicitly as an argument.
>
> ```python
> # This pattern — global mutable state — is fragile and hard to test
> total = 0
> def add(x):
>     global total
>     total += x
>
> # This pattern — explicit state — is clean and testable
> def add(total, x):
>     return total + x
>
> total = add(total, 5)
> ```
>
> **Rule:** constants at module level are fine as globals (`MAX_RETRIES = 3`). Mutable variables shared between functions are not.

---

## Enclosing scope and closures

This is where Python scope gets genuinely powerful. When you define a function inside another function, the inner function can see variables in the outer function's scope — even *after* the outer function has finished running.

```python
def make_greeting(name):
    # 'name' is in the enclosing scope of inner_func
    def inner_func():
        return f"Hello, {name}!"   # 'name' captured from enclosing scope
    return inner_func

greet_wilber = make_greeting("Wilber")
greet_morris = make_greeting("Morris")

print(greet_wilber())   # "Hello, Wilber!" — name is remembered
print(greet_morris())   # "Hello, Morris!" — different name, same structure
```

`make_greeting` has already returned, but `name` is still accessible inside `inner_func`. This is a **closure** — a function that *captures and remembers* variables from its enclosing scope.

### Practical closure — a counter

```python
def make_counter(start=0):
    count = start

    def counter():
        nonlocal count    # modify the enclosing variable (see below)
        count += 1
        return count

    return counter

hits = make_counter()
print(hits())   # 1
print(hits())   # 2
print(hits())   # 3

# Each call to make_counter() creates its own independent count
page_views = make_counter(100)
print(page_views())  # 101
print(hits())        # 4 — hits is unaffected
```

This pattern is used constantly in Textual and similar frameworks — a widget creates a closure that captures its own state.

### The `nonlocal` keyword

To *modify* a variable in the enclosing scope (not global, just outer function), use `nonlocal`:

```python
def outer():
    x = 10

    def inner():
        nonlocal x    # "I mean outer's x, not a new local x"
        x += 1
        return x

    return inner

modify = outer()
print(modify())   # 11
print(modify())   # 12
```

Without `nonlocal`, `x += 1` would throw `UnboundLocalError` — same trap as the `global` case.

> **Note:** `nonlocal` can only be used inside a nested function. You can't use it at module level.

---

## The classic closure trap — loop variables

This one catches almost everyone. If you create functions inside a loop, they all capture the *same variable*, not the value at the time they were created:

```python
# TRAP — all functions end up using the final value of i
functions = []
for i in range(5):
    def fn():
        return i
    functions.append(fn)

print([f() for f in functions])  # [4, 4, 4, 4, 4] — NOT [0, 1, 2, 3, 4]
```

Why? Because `i` is not local to the loop (remember — Python has no block scope). All five functions reference the *same* `i`, which ends up as `4` after the loop finishes.

**Fix — capture the value at creation time using a default argument:**

```python
functions = []
for i in range(5):
    def fn(i=i):    # i=i captures the current value of i as a default
        return i
    functions.append(fn)

print([f() for f in functions])  # [0, 1, 2, 3, 4] — correct
```

---

## LEGB in one diagram

```
┌─────────────────────────────────┐
│  B — Built-in scope             │  len, print, range, int, list...
│  ┌───────────────────────────┐  │
│  │  G — Global scope         │  │  module-level variables and functions
│  │  ┌─────────────────────┐  │  │
│  │  │  E — Enclosing scope │  │  │  outer function's variables (closures)
│  │  │  ┌───────────────┐  │  │  │
│  │  │  │  L — Local    │  │  │  │  variables inside current function
│  │  │  │  scope        │  │  │  │
│  │  │  └───────────────┘  │  │  │
│  │  └─────────────────────┘  │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
              Python searches L → E → G → B, stops at first match
```

---

## Common errors and what they mean

| Error | Cause | Fix |
|---|---|---|
| `NameError: name 'x' is not defined` | Python exhausted all four LEGB levels | Check spelling, check if variable is actually defined before use |
| `UnboundLocalError: local variable 'x' referenced before assignment` | Python decided `x` is local (because you assign to it later in the function), but reads it before the assignment | Restructure to pass as argument, or use `global`/`nonlocal` if intentional |
| `[4, 4, 4, 4, 4]` instead of `[0, 1, 2, 3, 4]` | Closure loop trap — functions share a reference to the loop variable | Use default argument `def fn(i=i)` to capture the value |
| Built-in stopped working (`len`, `list`, etc.) | You shadowed it with a variable of the same name | Rename your variable |

---

## Quick reference card

```
LEGB lookup order:
  L — Local (current function)
  E — Enclosing (outer functions, if nested)
  G — Global (module level)
  B — Built-in (len, print, etc.)
  → Python stops at the first match

Rules:
  □ Only functions (and classes/modules) create new scopes — not if/for/with
  □ Reading a global from inside a function: fine, no keyword needed
  □ Modifying a global from inside a function: declare global x first
  □ Modifying an enclosing variable from a nested function: declare nonlocal x
  □ Never shadow built-in names (list, dict, len, print, type, id...)
  □ Avoid mutable global state — pass values in, return them out

Closure rules:
  □ Inner functions capture variables by reference, not by value
  □ In loops: use default args (def fn(i=i)) to capture current value
  □ Use nonlocal when a closure needs to modify (not just read) the outer variable
```

---

## What's next

Now that scope is clear — including closures — you're ready for `*args` and `**kwargs`, which build directly on your understanding of how Python handles function arguments.

→ **Next: F2 — `*args` and `**kwargs`**

---

*Part of the Python Hitchhiker's Guide | Last updated: May 2026*
