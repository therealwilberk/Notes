# F3 — Decorators

> **What this fixes:** Seeing `@something` above a function and having no idea what's happening, or copy-pasting the same logic (logging, timing, validation) into every function that needs it.
>
> **The shift:** A decorator is just a function that takes a function and returns a new function. That's it. Everything else follows from that.

---

## The foundation — functions are objects

Before decorators make sense, one thing has to click: **in Python, functions are objects.** They can be assigned to variables, passed as arguments, and returned from other functions — exactly like integers or strings.

```python
def greet(name):
    return f"Hello, {name}!"

# Assign to a variable
say_hello = greet
print(say_hello("Wilber"))   # "Hello, Wilber!" — same function, different name

# Pass as an argument
def call_twice(fn, value):
    return fn(value), fn(value)

print(call_twice(greet, "Morris"))  # ('Hello, Morris!', 'Hello, Morris!')

# Return from a function
def get_greeter():
    def inner(name):
        return f"Habari, {name}!"
    return inner                     # returning the function, not calling it

greeter = get_greeter()
print(greeter("Wilber"))    # "Habari, Wilber!"
```

This is called **first-class functions** — the foundation that makes decorators possible.

---

## Building a decorator from scratch

A decorator is a function that:
1. Takes a function as input
2. Defines a new (wrapper) function inside itself
3. Returns the wrapper

Let's build one step by step.

**Step 1 — A plain function:**
```python
def add(a, b):
    return a + b
```

**Step 2 — A wrapper function that adds logging:**
```python
def logged_add(a, b):
    print(f"Calling add({a}, {b})")
    result = add(a, b)
    print(f"Result: {result}")
    return result
```

This works, but it's tied to `add` specifically. What if you want to log *any* function?

**Step 3 — A decorator that logs any function:**
```python
def log_call(func):               # takes a function as input
    def wrapper(*args, **kwargs): # wrapper accepts whatever func accepts
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)  # call the original function
        print(f"Result: {result}")
        return result             # return the original result
    return wrapper                # return the wrapper, not the result
```

**Step 4 — Apply it manually:**
```python
def add(a, b):
    return a + b

logged_add = log_call(add)   # add is passed in, logged_add is returned
print(logged_add(3, 4))
# Calling add
# Result: 7
# 7
```

**Step 5 — Use the `@` syntax (syntactic sugar):**
```python
@log_call
def add(a, b):
    return a + b

print(add(3, 4))
# Calling add
# Result: 7
# 7
```

`@log_call` above `add` is *exactly* the same as writing `add = log_call(add)` after the function definition. The `@` is just cleaner syntax.

---

## The `functools.wraps` essential fix

There's a problem with the basic decorator above. The wrapper replaces the original function — which means it also replaces its name, docstring, and other metadata:

```python
@log_call
def add(a, b):
    """Add two numbers."""
    return a + b

print(add.__name__)   # 'wrapper' — wrong, should be 'add'
print(add.__doc__)    # None — the docstring is gone
```

The fix is `functools.wraps` — always use it. It copies the original function's metadata onto the wrapper:

```python
import functools

def log_call(func):
    @functools.wraps(func)          # ← add this, always
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Result: {result}")
        return result
    return wrapper

@log_call
def add(a, b):
    """Add two numbers."""
    return a + b

print(add.__name__)   # 'add' ✅
print(add.__doc__)    # 'Add two numbers.' ✅
```

> **Rule:** Every decorator you write should use `@functools.wraps(func)` on the wrapper. No exceptions.

---

## The decorator template

Here is the base template. Copy this every time you write a new decorator:

```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # --- before the function runs ---
        result = func(*args, **kwargs)
        # --- after the function runs ---
        return result
    return wrapper
```

Everything else is variations on this pattern.

---

## Real decorator examples

### Timing a function

```python
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"{func.__name__} took {duration:.4f}s")
        return result
    return wrapper

@timer
def scrape_jobs(url):
    time.sleep(1)   # simulate network call
    return ["Job A", "Job B"]

jobs = scrape_jobs("https://brightermonday.co.ke")
# scrape_jobs took 1.0012s
```

### Retrying on failure

```python
import functools
import time

def retry(max_attempts=3, delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    print(f"Attempt {attempt} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2.0)
def fetch_page(url):
    # might fail due to network issues
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.text
```

### Validating inputs

```python
import functools

def require_positive(*param_names):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for name, value in kwargs.items():
                if name in param_names and value <= 0:
                    raise ValueError(f"'{name}' must be positive, got {value}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@require_positive("price", "quantity")
def calculate_total(price, quantity, discount=0):
    return price * quantity * (1 - discount)

calculate_total(price=100, quantity=5)    # ✅ 500
calculate_total(price=-10, quantity=5)   # ValueError: 'price' must be positive
```

---

## Decorators with arguments — the extra layer

A plain decorator takes a function. A decorator *with arguments* needs one extra layer: a function that takes the arguments and *returns* a decorator.

```python
# Plain decorator — one layer
def log_call(func):
    ...

# Decorator with arguments — two layers
def repeat(times):          # outer: takes the argument
    def decorator(func):    # middle: takes the function
        @functools.wraps(func)
        def wrapper(*args, **kwargs):   # inner: does the work
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def say(message):
    print(message)

say("Hello")
# Hello
# Hello
# Hello
```

Think of it this way:
- `@log_call` → `log_call(func)` — one call
- `@repeat(times=3)` → `repeat(times=3)` returns a decorator, which then receives `func` — two calls

---

## Stacking decorators

You can stack multiple decorators on one function. They apply **bottom-up**:

```python
@timer           # applied second (outermost)
@log_call        # applied first (innermost)
def process():
    time.sleep(0.1)
```

This is equivalent to: `process = timer(log_call(process))`

When `process()` is called: `timer`'s wrapper runs first → calls `log_call`'s wrapper → calls the original `process`.

> **Note:** Order matters. Put the decorators that should run first (closest to the function) at the bottom of the stack.

---

## Decorators in the wild — what you'll see in Textual/Toad

Textual uses decorators extensively. Now you can read them:

```python
from textual.app import App
from textual import on
from textual import work

class MyApp(App):

    @on(Button.Pressed, "#submit")    # event handler decorator with args
    def handle_submit(self, event):
        self.process_form()

    @work(thread=True)                # runs this method in a background thread
    def process_form(self):
        result = heavy_computation()
        self.call_from_thread(self.update_ui, result)
```

`@on(Button.Pressed, "#submit")` is a decorator with arguments — the pattern you just learned. `@work(thread=True)` is the same. Both follow the two-layer structure exactly.

---

## Built-in decorators worth knowing

Python ships with several decorators you'll use constantly:

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self._price = price

    @property                       # turns method into attribute access
    def price(self):
        return self._price

    @price.setter                   # allows setting the property
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value

    @classmethod                    # receives the class (cls) instead of instance
    def from_dict(cls, data):
        return cls(data["name"], data["price"])

    @staticmethod                   # no self or cls — just a regular function in a class
    def format_currency(amount):
        return f"KES {amount:,.2f}"


p = Product("Unga", 220)
print(p.price)                   # 220 — accessed like attribute, not method
p.price = 250                    # uses the setter
p.price = -10                    # ValueError

p2 = Product.from_dict({"name": "Sugar", "price": 145})  # classmethod
print(Product.format_currency(1500))  # "KES 1,500.00"
```

From `functools`:
```python
from functools import lru_cache, cached_property

@lru_cache(maxsize=128)         # memoizes results — same args → cached result
def expensive_lookup(item_id):
    return database.fetch(item_id)

class Report:
    @cached_property            # computed once, then stored as an attribute
    def summary(self):
        return self._build_summary()   # never recomputed after first access
```

---

## Common traps

**Trap 1 — Forgetting to return the result**
```python
def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)   # ❌ result is discarded
    return wrapper

# Fix: return the result
def wrapper(*args, **kwargs):
    return func(*args, **kwargs)   # ✅
```

**Trap 2 — Forgetting to return the wrapper**
```python
def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    # ❌ forgot: return wrapper
    # The decorator returns None — the function disappears
```

**Trap 3 — Calling the function instead of returning it**
```python
def my_decorator(func):
    return func()    # ❌ calls the function immediately at decoration time
    # Fix:
    return func      # ✅ return the function object itself
```

**Trap 4 — Forgetting `functools.wraps`**
Breaks `help()`, `__name__`, `__doc__`, and any introspection tools. Always include it.

---

## Quick reference card

```
Decorator anatomy:
  def decorator(func):
      @functools.wraps(func)      ← always include this
      def wrapper(*args, **kwargs):
          # before
          result = func(*args, **kwargs)
          # after
          return result           ← always return the result
      return wrapper              ← always return wrapper, not wrapper()

Decorator with arguments (extra outer layer):
  def decorator_factory(arg):
      def decorator(func):
          @functools.wraps(func)
          def wrapper(*args, **kwargs):
              return func(*args, **kwargs)
          return wrapper
      return decorator

Stacking — bottom-up:
  @outer     ← runs second
  @inner     ← runs first
  def fn():  ...

Built-ins:
  @property          → method becomes attribute
  @classmethod       → receives cls instead of self
  @staticmethod      → no self or cls
  @lru_cache         → memoize expensive calls
  @cached_property   → compute once, cache forever

Rules:
  □ Always @functools.wraps(func) on every wrapper
  □ Always return the result from wrapper
  □ Always return wrapper (not wrapper()) from decorator
  □ Extra arguments? Add one more outer layer
```

---

## What's next

Functions are fully covered — scope, flexible arguments, and decorators. Now the bigger question: when do you stop writing standalone functions and start reaching for a class?

→ **Next: C1 — Functions vs Classes**

---

*Part of the Python Hitchhiker's Guide | Last updated: May 2026*
