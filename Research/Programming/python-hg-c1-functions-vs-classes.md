---
tags:
  - python
  - functions
  - classes
aliases:
  - "C1"
  - "Functions vs Classes"
parent: "[[Python — Map of Content]]"
created: 2026-05-21
status: complete
---

# C1 — Functions vs Classes

> **What this fixes:** Defaulting to classes for everything because it feels "proper", or avoiding them entirely because they feel complex — neither is right.
>
> **The shift:** The question is never "functions or classes?" It's one specific question: **does this thing need to remember state?**

---
## The one rule that clears it up

Every other heuristic you'll read about this is downstream of one thing:

> **If your code needs to remember information between calls — use a class. If it doesn't — use a function.**

State is the deciding factor. Everything els4555e follows.

```python
# No state — same inputs always give same outputs — function
def calculate_vat(amount, rate=0.16):
    return amount * rate

# State — the balance needs to persist between deposits and withdrawals — class
class BankAccount:
    def __init__(self, owner, balance=0.0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
```

`calculate_vat` has no memory. Call it a thousand times — it doesn't accumulate anything. `BankAccount` has memory — `self.balance` persists and changes across every call. That's the line.

---

## The analogy

Think of it this way:

- **Function** = a vending machine button. Press it with an input, get an output, done. It doesn't remember the last person who used it.
- **Class** = a bank account. It has an owner, a balance, a history. It persists over time. Every action changes its state.

---

## Four signals you need a class

### Signal 1 — You're passing the same arguments to multiple functions

When you find yourself doing this:

```python
def fetch_jobs(api_key, base_url, timeout):
    ...

def post_job(api_key, base_url, job_data, timeout):
    ...

def delete_job(api_key, base_url, job_id, timeout):
    ...
```

`api_key`, `base_url`, and `timeout` are travelling everywhere together. That's state that belongs in a class:

```python
class JobsAPIClient:
    def __init__(self, api_key, base_url, timeout=10):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout

    def fetch_jobs(self):
        ...

    def post_job(self, job_data):
        ...

    def delete_job(self, job_id):
        ...

# Now: clean call sites
client = JobsAPIClient(api_key="xyz", base_url="https://api.example.com")
client.fetch_jobs()
client.post_job({"title": "Engineer"})
```

A useful heuristic: when your functions keep taking the same arguments, those arguments are crying out to become a class.

### Signal 2 — You need state to persist between calls

A counter, a cache, a connection, a running total — anything that accumulates or changes over time:

```python
# Without a class — ugly global state
_request_count = 0

def make_request(url):
    global _request_count
    _request_count += 1
    ...

# With a class — clean, encapsulated
class Scraper:
    def __init__(self):
        self.request_count = 0
        self.session = requests.Session()

    def fetch(self, url):
        self.request_count += 1
        return self.session.get(url)
```

### Signal 3 — You need multiple instances of the same thing

If you need two scrapers running independently, two API clients hitting different endpoints, two counters counting different things — you need a class. Functions can't be instantiated.

```python
brightermonday = Scraper()
fuzu = Scraper()

# Each has its own independent request_count, session, state
brightermonday.fetch("https://brightermonday.co.ke/jobs")
fuzu.fetch("https://fuzu.com/kenya-jobs")

print(brightermonday.request_count)  # 1
print(fuzu.request_count)            # 1 — independent
```

### Signal 4 — You're modelling a real entity with properties and behaviours

When your domain has things — users, orders, invoices, employees — that have both data (attributes) and actions (methods) that belong together:

```python
class Employee:
    def __init__(self, name, id_number, gross_salary):
        self.name = name
        self.id_number = id_number
        self.gross_salary = gross_salary

    def calculate_paye(self):
        ...

    def calculate_nssf(self):
        ...

    def net_salary(self):
        return self.gross_salary - self.calculate_paye() - self.calculate_nssf()
```

Classes are great when you need to keep state, because they containerize data (variables) and behavior (methods) that act on that data and should logically be grouped together.

---

## Four signals you should just use a function

### Signal 1 — It's a single operation with no memory

Validation, formatting, calculation, conversion — pure input → output:

```python
def format_phone(number: str) -> str:
    digits = number.replace(" ", "").replace("-", "")
    return f"+254{digits[-9:]}"

def is_valid_kra_pin(pin: str) -> bool:
    return len(pin) == 11 and pin[0].isalpha() and pin[1:].isdigit()
```

No reason for a class here. A class would just add `__init__`, `self`, and boilerplate for zero benefit.

### Signal 2 — Your "class" would only ever have one method

If your class has a single method in its API, you may not require a class. Use a function unless you need to retain state between calls.

```python
# Overkill — class with one real method
class EmailValidator:
    def validate(self, email):
        return "@" in email and "." in email

# Just use a function
def validate_email(email):
    return "@" in email and "." in email
```

### Signal 3 — It's a script or one-off task

Small command-line scripts, data transformations, file processors — these rarely need classes. A module of well-named functions is cleaner and Pythonic.

### Signal 4 — You only need to store data, no behaviour

If you have a thing with named fields but no methods — use `dataclass`, not a full class:

```python
# Overkill — class just to hold data
class JobListing:
    def __init__(self, title, company, salary):
        self.title = title
        self.company = company
        self.salary = salary

# Right tool — dataclass for pure data
from dataclasses import dataclass

@dataclass
class JobListing:
    title: str
    company: str
    salary: int
```

---

## The spectrum: function → dataclass → class

It's not binary. There's a natural progression:

```
Pure function          → no state, single operation
↓
Module of functions    → related operations, no shared state
↓
Dataclass              → structured data, little or no behaviour
↓
Full class             → data + behaviour + state that persists
↓
Class with inheritance → shared behaviour across related types
```

Start at the top. Only move down when you hit a signal that demands it. Most code lives in the top half. Beginners often jump straight to the bottom.

---

## Side-by-side: the same problem both ways

**Scenario:** An M-Pesa API client that needs to authenticate, make requests, and track rate limits.

**Function approach — starts to break down:**
```python
def get_token(consumer_key, consumer_secret):
    ...

def stk_push(token, phone, amount, consumer_key):
    # Why does stk_push need consumer_key?
    # Because get_token might expire and we'd need to refresh...
    ...

def check_status(token, transaction_id, consumer_key):
    # Same problem — consumer_key and token travel everywhere
    ...
```

The function approach forces you to pass auth credentials into every operation. It gets messy fast.

**Class approach — clean:**
```python
class MpesaClient:
    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self._token = None
        self.request_count = 0

    def _get_token(self):
        # refresh only when needed
        ...
        self._token = new_token

    def stk_push(self, phone, amount):
        if not self._token:
            self._get_token()
        self.request_count += 1
        ...

    def check_status(self, transaction_id):
        if not self._token:
            self._get_token()
        ...

# Clean call site — auth is encapsulated
client = MpesaClient(consumer_key="abc", consumer_secret="xyz")
client.stk_push("0712345678", 500)
client.check_status("ws_CO_123456")
print(client.request_count)  # 2
```

This is the Textual pattern too — every Widget is a class because it has state (is it focused? is it hidden? what's its content?), multiple methods, and multiple instances.

---

## The "stop writing classes" note

There's a famous Python talk called *"Stop Writing Classes"* by Jack Diederich that's worth knowing about. His point: Python beginners, especially those coming from Java, over-use classes. They wrap single functions in classes, create classes with no state, create classes that are basically just namespaces.

Python is not Java. You don't need a class for everything. Unlike Java or C++, Python is multi-paradigm. You don't have to wrap everything in a class. For many scripts and utilities, OOP adds unnecessary complexity.

The default should be: **start with a function. Reach for a class when state demands it.**

---

## Decision flowchart

```
Does it need to remember information between calls?
├── No  → Does it only hold data with no real behaviour?
│         ├── Yes → dataclass
│         └── No  → function (or module of functions)
└── Yes → Do you need multiple independent instances?
          ├── Yes → class
          └── No  → Could also be a closure (F1) — but class is clearer for most cases
```

---

## Quick reference card

```
Use a FUNCTION when:
  □ Input → transform → output, no memory needed
  □ Single operation, no shared state
  □ Would only have one method if it were a class
  □ It's a utility, formatter, validator, or calculator

Use a DATACLASS when:
  □ You need structured data with named, typed fields
  □ Little or no behaviour — just data storage
  □ You'd otherwise use a dict but want consistency

Use a CLASS when:
  □ State needs to persist between calls
  □ The same arguments keep showing up in multiple functions
  □ You need multiple independent instances of the same thing
  □ You're modelling an entity with both data and behaviour
  □ You need to connect to external systems (DB, API, file)

Default: start with functions. Move to classes when state demands it.
```

---

## What's next

You know when to use a class. Now: how to actually write one well.

→ **Next: C2 — Classes properly**

---

*Part of the Python Hitchhiker's Guide | Last updated: May 2026*
