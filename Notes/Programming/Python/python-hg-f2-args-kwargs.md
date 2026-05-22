---
tags:
  - python
  - functions
  - args
  - kwargs
aliases:
  - "F2"
  - "args and kwargs"
parent: "[[Python — Map of Content]]"
created: 2026-05-21
status: draft
---
# F2 — `*args` and `**kwargs`

> **What this fixes:** Functions that break when you add a new parameter, or that need five different versions to handle slightly different inputs.
> 
> **The shift:** `*args` and `**kwargs` are not magic — they're just packing and unpacking. Once you see that, everything clicks.

---

## The bridge from C/Rust

In C, functions have fixed signatures — you define exactly how many arguments they take, and that's it. Variadic functions (`printf`, etc.) exist but require `stdarg.h` and are verbose. In Rust, there's no native variadic syntax at all outside of macros.

Python takes a different approach: you can write functions that accept any number of arguments natively, with clean syntax. The mechanism is packing — Python collects the extra arguments into a standard data structure (tuple or dict) and hands it to you.

---

## The problem they solve

```python
# You write this:
def log(message, level):
    print(f"[{level}] {message}")

# Then you need a timestamp too:
def log(message, level, timestamp):
    ...

# Then a source module:
def log(message, level, timestamp, module):
    ...

# Every change breaks every existing call to log()
```

`*args` and `**kwargs` let you write functions that stay stable even when the number or names of inputs change.

---

## `*args` — variable positional arguments

The `*` tells Python: "collect all extra positional arguments into a tuple called `args`."

```python
def log(*args):
    print(args)

log("hello")                    # ('hello',)
log("hello", "INFO")            # ('hello', 'INFO')
log("hello", "INFO", "main")    # ('hello', 'INFO', 'main')
```

`args` is just a regular tuple inside the function. The name `args` is convention — the `*` is what matters.

```python
def add(*numbers):
    return sum(numbers)     # numbers is a tuple — sum() works on it

print(add(1, 2))            # 3
print(add(1, 2, 3, 4, 5))  # 15
print(add())                # 0 — empty tuple, sum returns 0
```

### Mixing regular params with `*args`

Regular parameters come first, `*args` catches everything after:

```python
def log(level, *messages):
    for msg in messages:
        print(f"[{level}] {msg}")

log("INFO", "Server started")
log("ERROR", "Connection failed", "Retrying...", "Attempt 3")
# [ERROR] Connection failed
# [ERROR] Retrying...
# [ERROR] Attempt 3
```

> ⚠️ **Trap:** Any parameter _after_ `*args` becomes keyword-only — it can only be passed by name, not position:
> 
> ```python
> def fn(*args, separator):
>     return separator.join(str(a) for a in args)
> 
> fn(1, 2, 3, separator="-")   # "1-2-3" ✅
> fn(1, 2, 3, "-")             # TypeError — separator must be keyword ❌
> ```
> 
> This is actually a useful pattern for forcing callers to be explicit.

---

## `**kwargs` — variable keyword arguments

The `**` tells Python: "collect all extra keyword arguments into a dict called `kwargs`."

```python
def show(**kwargs):
    print(kwargs)

show(name="Wilber", role="admin")   # {'name': 'Wilber', 'role': 'admin'}
show(city="Nairobi")                # {'city': 'Nairobi'}
```

`kwargs` is a regular dict inside the function. Use it like one.

```python
def create_user(**kwargs):
    # Set defaults, then override with whatever was passed
    user = {
        "role": "viewer",
        "active": True,
        "theme": "light"
    }
    user.update(kwargs)     # kwargs overwrites defaults where keys match
    return user

print(create_user(name="Wilber", role="admin"))
# {'role': 'admin', 'active': True, 'theme': 'light', 'name': 'Wilber'}
```

### Real use case — passing config through

`**kwargs` shines when you need to pass a variable set of options through layers of functions without knowing all the keys upfront:

```python
def make_request(url, **options):
    timeout = options.get("timeout", 10)
    retries = options.get("retries", 3)
    headers = options.get("headers", {})
    print(f"GET {url} | timeout={timeout} | retries={retries}")

make_request("https://api.example.com/jobs")
make_request("https://api.example.com/jobs", timeout=30, retries=1)
make_request("https://api.example.com/jobs", headers={"Authorization": "Bearer xyz"})
```

---

## The full parameter order

Python enforces a strict order when combining all parameter types:

```python
def fn(regular, *args, keyword_only, **kwargs):
    pass
```

In plain English:

```
1. regular parameters          → positional, required unless defaulted
2. *args                       → catches remaining positional args as a tuple
3. keyword-only parameters     → must be passed by name (come after *args)
4. **kwargs                    → catches remaining keyword args as a dict
```

Full example:

```python
def pipeline(source, *transforms, output="stdout", **options):
    print(f"Source:     {source}")
    print(f"Transforms: {transforms}")
    print(f"Output:     {output}")
    print(f"Options:    {options}")

pipeline(
    "brightermonday",
    "clean_html", "extract_jobs", "deduplicate",
    output="database",
    batch_size=100,
    dry_run=False
)
# Source:     brightermonday
# Transforms: ('clean_html', 'extract_jobs', 'deduplicate')
# Output:     database
# Options:    {'batch_size': 100, 'dry_run': False}
```

---

## Unpacking — the `*` and `**` operators in calls

The same symbols work in reverse when _calling_ a function — they unpack a list or dict into individual arguments.

### Unpack a list with `*`

```python
def add(a, b, c):
    return a + b + c

numbers = [1, 2, 3]
print(add(*numbers))    # same as add(1, 2, 3) → 6
```

### Unpack a dict with `**`

```python
def greet(name, greeting):
    return f"{greeting}, {name}!"

data = {"name": "Wilber", "greeting": "Habari"}
print(greet(**data))    # same as greet(name="Wilber", greeting="Habari")
```

### Practical use — merging dicts

```python
defaults = {"timeout": 10, "retries": 3, "verify_ssl": True}
overrides = {"timeout": 30, "debug": True}

config = {**defaults, **overrides}
# {'timeout': 30, 'retries': 3, 'verify_ssl': True, 'debug': True}
# overrides wins on conflict (timeout: 30, not 10)
```

This dict-merging pattern is everywhere in real Python code.

---

## The decorator connection

This is where F1 (scope) and F2 meet. When you write a decorator (F3), you almost always need `*args, **kwargs` in the wrapper — because the decorator doesn't know what arguments the decorated function will receive:

```python
def log_call(func):
    def wrapper(*args, **kwargs):       # accept whatever the original function takes
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)  # pass everything through unchanged
        print(f"Done")
        return result
    return wrapper

@log_call
def add(a, b):
    return a + b

add(3, 4)
# Calling add
# Done
# → 7
```

Without `*args, **kwargs` in the wrapper, the decorator would only work for functions with a specific signature. With them, it works for any function. This pattern is used throughout Textual's event system.

---

## When to use them — and when not to

|Situation|Use|
|---|---|
|Function needs to accept any number of values of the same kind|`*args`|
|Function takes optional named configuration|`**kwargs`|
|Writing a decorator or wrapper|Both — `*args, **kwargs`|
|Forwarding arguments to another function|Both — pass them through unchanged|
|Merging dicts|`**` unpacking|
|You know exactly what parameters the function takes|Neither — be explicit|

> ⚠️ **Trap — overusing them:** `*args` and `**kwargs` are flexible, but flexibility hides intent. If your function always takes a name, email, and age — write `def fn(name, email, age)`, not `def fn(**kwargs)`. Explicit signatures are readable, autocomplete-friendly, and self-documenting.
> 
> From the Python community's own guideline: _"Use `*args` and `**kwargs` only when the number of arguments is truly variable. Prefer explicit parameters when arguments have fixed meaning."_

---

## Common traps summary

**Trap 1 — Mutating `args` or `kwargs` and expecting it to affect the caller** `args` is a tuple (immutable), `kwargs` is a new dict. Mutating `kwargs` inside the function doesn't affect what was passed.

**Trap 2 — Wrong order**

```python
def fn(**kwargs, *args):  # SyntaxError — *args must come before **kwargs
```

**Trap 3 — Forgetting `*args` eats all remaining positionals**

```python
def fn(*args, extra):
    ...

fn(1, 2, 3, 4)   # TypeError — extra wasn't given as a keyword argument
fn(1, 2, 3, extra=4)  # ✅
```

**Trap 4 — Using `**kwargs` when you mean a dict parameter**

```python
# Bad — hides what the function actually needs
def save_user(**kwargs):
    db.insert(kwargs)

# Good — explicit, readable, type-checkable
def save_user(name: str, email: str, role: str = "viewer"):
    db.insert({"name": name, "email": email, "role": role})
```

---

## Quick reference card

```
*args:
  □ Collects extra positional arguments into a TUPLE
  □ Name is convention — the * is what matters
  □ Must come after regular parameters
  □ Parameters after *args are keyword-only

**kwargs:
  □ Collects extra keyword arguments into a DICT
  □ Must come last (after *args and keyword-only params)
  □ Use .get() with defaults for optional keys

Full order:
  def fn(regular, *args, keyword_only, **kwargs)

Unpacking in calls:
  fn(*my_list)    → unpacks list into positional args
  fn(**my_dict)   → unpacks dict into keyword args
  {**a, **b}      → merges two dicts (b wins on conflict)

Rule: be explicit when you know the signature.
      use *args/**kwargs only when variability is the point.
```

---

## What's next

You now understand how Python functions handle flexible arguments, and you've seen a preview of decorators. Time to make that explicit.

→ **Next: F3 — Decorators**

---

_Part of the Python Hitchhiker's Guide | Last updated: May 2026_