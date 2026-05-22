# C2 — Classes Properly

> **What this fixes:** Understanding the syntax but not what `self` actually is, or being confused about why some attributes are shared and some aren't.
>
> **The shift:** A class is a blueprint. `self` is the specific object built from it. Everything else follows from that.

---

## The blueprint analogy

A class is an architectural blueprint. It describes what a building will have — rooms, doors, windows — but it is not a building itself. When you build from the blueprint, you get an *instance* — an actual building with its own specific address, colour, and occupants.

```python
class Employee:          # the blueprint
    pass

wilber = Employee()      # an instance — a specific employee
morris = Employee()      # another instance — a different employee

print(wilber is morris)  # False — they are different objects
```

Every call to `Employee()` creates a new, independent object. That's instantiation.

---

## `__init__` — the initializer

`__init__` is the method Python calls automatically when you create a new instance. Its job is to set up the initial state of the object — give it its starting values.

```python
class Employee:
    def __init__(self, name, id_number, gross_salary):
        self.name = name
        self.id_number = id_number
        self.gross_salary = gross_salary

wilber = Employee("Wilber Kamau", "EMP001", 85000)
print(wilber.name)          # "Wilber Kamau"
print(wilber.gross_salary)  # 85000
```

`__init__` is not a constructor in the C++ sense — Python creates the object before `__init__` runs. `__init__` just *initialises* it. That's why it's called `__init__`, not `__new__`.

> **Best practice:** Define ALL instance attributes inside `__init__`. Don't scatter them across other methods. When someone reads your `__init__`, they should be able to see the full shape of the object immediately.

```python
# Bad — attributes spread across methods, hard to know what the object "is"
class Scraper:
    def __init__(self, url):
        self.url = url

    def connect(self):
        self.session = requests.Session()   # ← hidden here

    def fetch(self):
        self.last_response = None           # ← and here

# Good — full shape visible upfront
class Scraper:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.last_response = None
```

---

## `self` — demystified

`self` is the single most confusing thing about Python classes for beginners. Here's what it actually is:

**`self` is a reference to the specific instance that the method is being called on.**

When you call `wilber.calculate_paye()`, Python translates that internally to `Employee.calculate_paye(wilber)` — it passes `wilber` as the first argument. `self` is just that first argument. The name `self` is a convention, not a keyword — but you should always use it.

```python
class Employee:
    def __init__(self, name, gross_salary):
        self.name = name                # store on THIS specific instance
        self.gross_salary = gross_salary

    def calculate_paye(self):
        # self.gross_salary reads from THIS specific instance
        if self.gross_salary <= 24000:
            return 0
        return (self.gross_salary - 24000) * 0.25

wilber = Employee("Wilber", 85000)
morris = Employee("Morris", 50000)

# Each instance has its own gross_salary — self points to the right one
print(wilber.calculate_paye())   # 15250.0
print(morris.calculate_paye())   # 6500.0
```

Every instance method takes `self` as its first parameter. That's how the method knows *which* object it's operating on.

---

## Instance attributes vs class attributes

This is where a lot of bugs hide. There are two places to define attributes in a class — and they behave very differently.

### Instance attributes — unique to each object

Defined inside `__init__` using `self`. Every instance gets its own copy.

```python
class Product:
    def __init__(self, name, price):
        self.name = name      # instance attribute — unique per product
        self.price = price    # instance attribute — unique per product

unga = Product("Unga", 220)
sugar = Product("Sugar", 145)

print(unga.price)   # 220
print(sugar.price)  # 145 — completely independent
```

### Class attributes — shared across all instances

Defined directly in the class body, outside any method. One copy, shared by every instance.

```python
class Product:
    VAT_RATE = 0.16           # class attribute — shared by all products
    _instance_count = 0       # class attribute — tracks total products created

    def __init__(self, name, price):
        self.name = name
        self.price = price
        Product._instance_count += 1

    def price_with_vat(self):
        return self.price * (1 + Product.VAT_RATE)  # access via class name

unga = Product("Unga", 220)
sugar = Product("Sugar", 145)

print(unga.price_with_vat())    # 255.2
print(sugar.price_with_vat())   # 168.2
print(Product._instance_count)  # 2
```

**Use class attributes for:**
- Constants shared across all instances (`VAT_RATE`, `MAX_RETRIES`)
- Counters or state that tracks the class itself, not a specific instance
- Configuration that should be the same for every instance

**Do NOT use class attributes for:**
- Data that differs per instance — that's what `self` is for

### The mutable class attribute trap

This catches everyone once:

```python
# TRAP — mutable class attribute shared across ALL instances
class Order:
    items = []    # ← class attribute, mutable list

    def add_item(self, item):
        self.items.append(item)

order1 = Order()
order2 = Order()

order1.add_item("Unga")
print(order2.items)   # ["Unga"] — order2 is contaminated!
```

Both `order1` and `order2` share the same list. When `order1` mutates it, `order2` sees the change.

**Fix — always use instance attributes for mutable data:**

```python
class Order:
    def __init__(self):
        self.items = []     # ← fresh list for each instance

    def add_item(self, item):
        self.items.append(item)

order1 = Order()
order2 = Order()

order1.add_item("Unga")
print(order2.items)   # [] — clean, independent
```

---

## The three types of methods

### Instance methods — the default

Takes `self`. Operates on the specific instance. This is what you'll write 90% of the time.

```python
class Employee:
    def __init__(self, name, gross_salary):
        self.name = name
        self.gross_salary = gross_salary

    def net_salary(self):              # instance method
        return self.gross_salary * 0.7 # operates on this specific employee
```

### Class methods — operate on the class itself

Takes `cls` instead of `self`. Useful for alternative constructors — creating instances from different input formats.

```python
class Employee:
    def __init__(self, name, gross_salary):
        self.name = name
        self.gross_salary = gross_salary

    @classmethod
    def from_dict(cls, data: dict):
        """Create an Employee from a dictionary."""
        return cls(data["name"], data["gross_salary"])

    @classmethod
    def from_csv_row(cls, row: str):
        """Create an Employee from a CSV string."""
        name, salary = row.split(",")
        return cls(name.strip(), float(salary.strip()))

# Multiple ways to create the same thing
e1 = Employee("Wilber", 85000)
e2 = Employee.from_dict({"name": "Morris", "gross_salary": 70000})
e3 = Employee.from_csv_row("Alice, 95000")
```

### Static methods — utility functions that live in a class

No `self`, no `cls`. Just a regular function that happens to live inside the class because it's conceptually related. Doesn't access any instance or class state.

```python
class Employee:
    @staticmethod
    def validate_id_number(id_number: str) -> bool:
        """Kenyan ID numbers are 7-8 digits."""
        return id_number.isdigit() and 7 <= len(id_number) <= 8

    @staticmethod
    def format_salary(amount: float) -> str:
        return f"KES {amount:,.2f}"

# Called on the class — no instance needed
print(Employee.validate_id_number("12345678"))  # True
print(Employee.format_salary(85000))            # "KES 85,000.00"
```

> **Rule of thumb:**
> - Does it need `self` (this specific instance's data)? → instance method
> - Does it create instances or need the class itself? → `@classmethod`
> - Is it just a utility that belongs conceptually with the class? → `@staticmethod`
> - Does it not really need the class at all? → move it to a standalone function

---

## Private attributes — the underscore convention

Python doesn't have true private attributes like C++ or Java. Instead it uses naming conventions:

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner          # public — access freely
        self._balance = balance     # "private" — don't access from outside
        self.__pin = "1234"         # "strongly private" — name-mangled by Python

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount

    def get_balance(self):
        return self._balance        # controlled access to internal state
```

- `self.attr` — public. Part of the interface. Access from anywhere.
- `self._attr` — single underscore. Convention: "internal, don't touch unless you know what you're doing." Python doesn't enforce this — it's a signal to other developers.
- `self.__attr` — double underscore. Python mangles the name to `_ClassName__attr`, making accidental access harder (not impossible). Use sparingly.

The community norm: use `_` for internal state and provide methods for controlled access. Don't use `__` unless you have a specific reason.

---

## A complete, well-written class

Putting it all together — this is what a properly structured class looks like:

```python
from dataclasses import dataclass
from typing import Optional


class Invoice:
    """Represents a sales invoice for a Kenyan SME."""

    VAT_RATE = 0.16          # class attribute — constant, shared

    def __init__(
        self,
        invoice_number: str,
        customer_name: str,
        amount: float,
        paid: bool = False
    ):
        # All instance attributes defined here — full shape visible immediately
        self.invoice_number = invoice_number
        self.customer_name = customer_name
        self.amount = amount
        self.paid = paid
        self._vat_amount: Optional[float] = None  # cached, internal

    # --- Alternative constructors ---

    @classmethod
    def from_dict(cls, data: dict) -> "Invoice":
        """Create an Invoice from a dictionary."""
        return cls(
            invoice_number=data["invoice_number"],
            customer_name=data["customer_name"],
            amount=data["amount"],
            paid=data.get("paid", False)
        )

    # --- Instance methods ---

    def vat_amount(self) -> float:
        """VAT amount on this invoice (16%)."""
        if self._vat_amount is None:
            self._vat_amount = self.amount * self.VAT_RATE
        return self._vat_amount

    def total_with_vat(self) -> float:
        """Total amount including VAT."""
        return self.amount + self.vat_amount()

    def mark_paid(self) -> None:
        """Mark this invoice as paid."""
        self.paid = True

    # --- Static utility ---

    @staticmethod
    def validate_invoice_number(number: str) -> bool:
        """Invoice numbers must start with 'INV-' followed by digits."""
        return number.startswith("INV-") and number[4:].isdigit()

    # --- String representation (covered fully in C4) ---

    def __repr__(self) -> str:
        status = "PAID" if self.paid else "UNPAID"
        return f"Invoice({self.invoice_number}, {self.customer_name}, KES {self.amount:,.0f}, {status})"


# Usage
inv = Invoice("INV-001", "Duka Moja Ltd", 50000)
print(inv.total_with_vat())   # 58000.0
print(inv.vat_amount())       # 8000.0
inv.mark_paid()
print(inv)                    # Invoice(INV-001, Duka Moja Ltd, KES 50,000, PAID)

# From dict
inv2 = Invoice.from_dict({"invoice_number": "INV-002", "customer_name": "ABC Co", "amount": 30000})
```

---

## Quick reference card

```
Class anatomy:
  class Name:
      CLASS_ATTR = value          ← shared across all instances (use for constants)

      def __init__(self, ...):    ← initializer, sets up instance state
          self.attr = value       ← instance attribute, unique per object
                                  ← define ALL instance attributes here

      def method(self):           ← instance method, operates on self
          ...

      @classmethod
      def from_x(cls, ...):       ← alternative constructors, factory methods

      @staticmethod
      def utility(...):           ← no self or cls, just a related function

Key rules:
  □ ALL instance attributes defined in __init__ — no exceptions
  □ Never use mutable class attributes (lists, dicts) — use instance attrs
  □ self = this specific object; cls = the class itself
  □ _attr = internal (convention); __attr = strongly internal (name-mangled)
  □ Class attributes for constants/counters; instance attributes for data

Method type quick pick:
  □ Needs self? → instance method
  □ Creates instances / needs the class? → @classmethod
  □ Utility that belongs here conceptually? → @staticmethod
  □ Doesn't really need the class? → standalone function
```

---

## What's next

You can write a class properly. Next: when to use inheritance — and more importantly, when to avoid it.

→ **Next: C3 — Inheritance and when to avoid it**

---

*Part of the Python Hitchhiker's Guide | Last updated: May 2026*
