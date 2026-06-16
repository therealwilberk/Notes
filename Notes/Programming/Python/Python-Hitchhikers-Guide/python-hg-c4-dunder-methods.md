---
tags:
  - python
  - dunder
  - oop
aliases:
  - "C4"
  - "Dunder Methods"
parent: "[[Python — Map of Content]]"
created: 2026-05-21
status: draft
---
# C4 — Dunder Methods

> **What this fixes:** Objects that print as `<__main__.Invoice object at 0x7f3a1b2c>`, can't be compared, can't be iterated, and feel foreign instead of Pythonic.
> 
> **The shift:** Dunder methods are the hooks Python calls behind the scenes. Implement them and your objects plug into Python's built-in syntax naturally.

---

## What dunder methods are

"Dunder" = double underscore. Also called _magic methods_ or _special methods_.

When you write `len(my_list)`, Python calls `my_list.__len__()`. When you write `a + b`, Python calls `a.__add__(b)`. When you write `print(obj)`, Python calls `obj.__str__()`. These are not things Python does mysteriously — they're hooks that you can implement in your own classes to make your objects behave like built-in types.

```python
# Every time you use Python's built-in syntax on an object,
# a dunder method is being called behind the scenes:

len(my_list)         # → my_list.__len__()
a + b                # → a.__add__(b)
a == b               # → a.__eq__(b)
a < b                # → a.__lt__(b)
str(obj)             # → obj.__str__()
repr(obj)            # → obj.__repr__()
obj[key]             # → obj.__getitem__(key)
for x in obj:        # → obj.__iter__()
with obj as x:       # → obj.__enter__() / obj.__exit__()
```

You've been using dunder methods all along — on lists, strings, dicts. Now you learn to define them on your own classes.

---

## The three every class should have

According to Python Morsels, there are three dunder methods that most classes should have: `__init__`, `__repr__`, and `__eq__`. You already know `__init__`. Here are the other two.

### `__repr__` — the developer representation

`__repr__` returns a string that unambiguously describes the object. The goal: ideally, it should be a string that could recreate the object. It's what shows up in the REPL and in debuggers.

```python
class Invoice:
    def __init__(self, number, customer, amount):
        self.number = number
        self.customer = customer
        self.amount = amount

    def __repr__(self):
        return f"Invoice(number={self.number!r}, customer={self.customer!r}, amount={self.amount})"

inv = Invoice("INV-001", "Duka Moja", 50000)
print(repr(inv))   # Invoice(number='INV-001', customer='Duka Moja', amount=50000)
inv                # Same — the REPL calls __repr__ automatically
```

Note the `!r` format — it adds quotes around strings, making the output unambiguous. Use it for string fields in `__repr__`.

### `__str__` — the user-facing representation

`__str__` returns a human-readable string. What shows up when you `print()` the object or use it in an f-string. If only one is defined, implement `__repr__` — Python falls back to it when `__str__` is missing. If both are defined, `__str__` is used for display, `__repr__` for debugging.

```python
class Invoice:
    def __init__(self, number, customer, amount, paid=False):
        self.number = number
        self.customer = customer
        self.amount = amount
        self.paid = paid

    def __repr__(self):
        # For developers — unambiguous, recreatable
        return f"Invoice(number={self.number!r}, customer={self.customer!r}, amount={self.amount}, paid={self.paid})"

    def __str__(self):
        # For users — clean, readable
        status = "✓ PAID" if self.paid else "UNPAID"
        return f"Invoice {self.number} | {self.customer} | KES {self.amount:,.0f} | {status}"

inv = Invoice("INV-001", "Duka Moja", 50000)
print(inv)       # Invoice INV-001 | Duka Moja | KES 50,000 | UNPAID  ← __str__
print(repr(inv)) # Invoice(number='INV-001', customer='Duka Moja', amount=50000, paid=False) ← __repr__
```

> **Rule:** Always implement `__repr__`. Add `__str__` when the repr format isn't human-friendly enough for display.

---

### `__eq__` — equality

By default, Python compares objects by _identity_ — two objects are equal only if they're the same object in memory. Usually you want value equality — two invoices with the same number should be equal.

```python
# Without __eq__ — identity comparison (default)
inv1 = Invoice("INV-001", "Duka Moja", 50000)
inv2 = Invoice("INV-001", "Duka Moja", 50000)
print(inv1 == inv2)    # False — different objects in memory

# With __eq__ — value comparison
class Invoice:
    def __init__(self, number, customer, amount):
        self.number = number
        self.customer = customer
        self.amount = amount

    def __eq__(self, other):
        if not isinstance(other, Invoice):
            return NotImplemented             # not False — NotImplemented
        return self.number == other.number    # invoices are equal if numbers match

inv1 = Invoice("INV-001", "Duka Moja", 50000)
inv2 = Invoice("INV-001", "Duka Moja", 50000)
print(inv1 == inv2)    # True ✅
```

> **Important:** Return `NotImplemented` (not `False`, not `raise`) when the other object is not the right type. This tells Python to try the comparison from the other side — which is the correct, Pythonic behaviour.

> **Trap:** If you define `__eq__`, Python automatically makes your object unhashable (sets `__hash__ = None`). This means you can't put it in a set or use it as a dict key. If you need both equality and hashability, also define `__hash__`:
> 
> ```python
> def __hash__(self):
>     return hash(self.number)   # hash based on the same field(s) as __eq__
> ```

---

## Comparison methods

### `__lt__`, `__le__`, `__gt__`, `__ge__` — ordering

Define how your objects sort and compare:

```python
from functools import total_ordering

@total_ordering    # generates all comparisons from __eq__ and __lt__
class Invoice:
    def __init__(self, number, amount):
        self.number = number
        self.amount = amount

    def __eq__(self, other):
        if not isinstance(other, Invoice):
            return NotImplemented
        return self.amount == other.amount

    def __lt__(self, other):
        if not isinstance(other, Invoice):
            return NotImplemented
        return self.amount < other.amount

invoices = [
    Invoice("INV-003", 80000),
    Invoice("INV-001", 50000),
    Invoice("INV-002", 65000),
]

sorted_invoices = sorted(invoices)
for inv in sorted_invoices:
    print(inv.number, inv.amount)
# INV-001 50000
# INV-002 65000
# INV-003 80000
```

`@total_ordering` is a decorator from `functools` — define `__eq__` and `__lt__`, and it automatically generates `__le__`, `__gt__`, `__ge__` for you. Use it instead of implementing all four manually.

---

## Container methods

These let your objects behave like lists, dicts, or sets.

### `__len__` — support `len()`

```python
class JobQueue:
    def __init__(self):
        self._jobs = []

    def add(self, job):
        self._jobs.append(job)

    def __len__(self):
        return len(self._jobs)

    def __bool__(self):
        return len(self._jobs) > 0    # truthy if there are jobs

queue = JobQueue()
print(len(queue))    # 0
queue.add("Job A")
print(len(queue))    # 1
if queue:            # calls __bool__
    print("Queue has jobs")
```

> **Note:** Python uses `__len__` as a fallback for `__bool__` if `__bool__` isn't defined — an empty object is falsy, a non-empty one is truthy. Define `__bool__` explicitly when you want different truthiness logic.

### `__getitem__` — support indexing and `in`

```python
class JobQueue:
    def __init__(self):
        self._jobs = []

    def add(self, job):
        self._jobs.append(job)

    def __len__(self):
        return len(self._jobs)

    def __getitem__(self, index):
        return self._jobs[index]      # delegate to the underlying list

queue = JobQueue()
queue.add("Job A")
queue.add("Job B")
queue.add("Job C")

print(queue[0])         # "Job A"
print(queue[-1])        # "Job C"
print(queue[1:])        # ["Job B", "Job C"] — slicing works too
print("Job A" in queue) # True — __getitem__ + __len__ enables `in`
```

### `__iter__` and `__next__` — support `for` loops

```python
class JobQueue:
    def __init__(self):
        self._jobs = []

    def add(self, job):
        self._jobs.append(job)

    def __iter__(self):
        return iter(self._jobs)    # delegate to the list's iterator

queue = JobQueue()
queue.add("Job A")
queue.add("Job B")

for job in queue:       # calls __iter__
    print(job)
# Job A
# Job B

jobs_list = list(queue)     # also works — list() uses __iter__
```

---

## Arithmetic operators

Let your objects support `+`, `-`, `*`, etc:

```python
class Money:
    def __init__(self, amount, currency="KES"):
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, factor):
        if not isinstance(factor, (int, float)):
            return NotImplemented
        return Money(self.amount * factor, self.currency)

    def __repr__(self):
        return f"Money({self.amount}, {self.currency!r})"

    def __str__(self):
        return f"{self.currency} {self.amount:,.2f}"

price = Money(1000)
tax = Money(160)
total = price + tax
print(total)           # KES 1,160.00

doubled = price * 2
print(doubled)         # KES 2,000.00
```

---

## Context managers — `__enter__` and `__exit__`

These make your objects work with the `with` statement — Python's mechanism for guaranteed cleanup (files, connections, locks):

```python
class DatabaseConnection:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        print(f"Connected to {self.db_path}")
        return self.connection        # what gets bound to the `as` variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
            print("Connection closed")
        return False                  # False = don't suppress exceptions

# Usage — connection closes automatically, even if an exception occurs
with DatabaseConnection("jobs.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()
# Connection closed — guaranteed, with or without errors
```

`__exit__` receives exception info if one occurred. Returning `False` (or `None`) lets the exception propagate. Returning `True` suppresses it — only do that intentionally.

---

## `__call__` — making instances callable

If your object defines `__call__`, you can call it like a function:

```python
class RateLimiter:
    def __init__(self, max_per_second):
        self.max_per_second = max_per_second
        self._last_call = 0
        self._call_count = 0

    def __call__(self, func, *args, **kwargs):
        self._call_count += 1
        # rate limiting logic here
        return func(*args, **kwargs)

limiter = RateLimiter(max_per_second=5)
result = limiter(fetch_page, "https://example.com")   # called like a function
```

You'll see this in Textual — widgets and actions are callable objects behind the scenes.

---

## The complete practical set

Most of what you'll actually need falls into these groups:

|Group|Methods|When to add|
|---|---|---|
|**Always**|`__repr__`|Every class — no exceptions|
|**Usually**|`__str__`|When repr isn't human-friendly|
|**Usually**|`__eq__`|When value equality matters|
|**With `__eq__`**|`__hash__`|If objects go in sets/dicts|
|**Ordering**|`__lt__` + `@total_ordering`|When objects need to sort|
|**Collections**|`__len__`, `__getitem__`, `__iter__`|When class wraps a collection|
|**Truthiness**|`__bool__`|When empty/non-empty has meaning|
|**Arithmetic**|`__add__`, `__mul__`, etc.|When objects represent values|
|**Resources**|`__enter__`, `__exit__`|When managing connections/files|
|**Callable**|`__call__`|When instance should act as a function|

---

## Common traps

**Trap 1 — Returning `False` instead of `NotImplemented` from `__eq__`**

```python
def __eq__(self, other):
    if not isinstance(other, Invoice):
        return False          # ❌ prevents Python trying the other side
        return NotImplemented # ✅ correct
```

**Trap 2 — Defining `__eq__` but not `__hash__`**

```python
# After defining __eq__, Python sets __hash__ = None
inv = Invoice("INV-001", "Duka Moja", 50000)
my_set = {inv}   # TypeError: unhashable type: 'Invoice'

# Fix — add __hash__ if you need hashability
def __hash__(self):
    return hash(self.number)
```

**Trap 3 — `__str__` returning a non-string**

```python
def __str__(self):
    return self.amount   # ❌ TypeError — must return str
    return str(self.amount)  # ✅
```

**Trap 4 — Implementing arithmetic dunders for objects that shouldn't support them** Adding `__add__` to an `Employee` class makes no sense. Only implement dunders that are _natural_ for the type. An `Invoice` can be compared by amount — that's natural. An `Employee` being multiplied by another `Employee` is not.

---

## Quick reference card

```
The always-implement set:
  □ __repr__   → unambiguous dev-facing string, use !r for string fields
  □ __str__    → human-friendly display (optional, __repr__ is fallback)
  □ __eq__     → value equality (return NotImplemented for wrong types)
  □ __hash__   → required if __eq__ is defined AND object goes in sets/dicts

Comparison shortcut:
  □ Implement __eq__ + __lt__, add @total_ordering → all comparisons generated

Container protocol:
  □ __len__      → len(obj)
  □ __getitem__  → obj[key], obj[1:3], "x" in obj
  □ __iter__     → for x in obj, list(obj)
  □ __bool__     → truthiness (fallback: len > 0)

Resource management:
  □ __enter__ + __exit__ → with statement, guaranteed cleanup
  □ __exit__ returns False → exceptions propagate (normal)
  □ __exit__ returns True → exceptions suppressed (intentional only)

Rules:
  □ Only implement dunders that are natural for the type
  □ Always return NotImplemented (not False) for unsupported types
  □ __repr__ should ideally recreate the object if eval'd
```

---

## What's next

The OOP section is complete. Next up: the standard library modules that show up in every serious Python codebase — starting with `pathlib`.

→ **Next: S1 — `pathlib`**

---

_Part of the Python Hitchhiker's Guide | Last updated: May 2026_