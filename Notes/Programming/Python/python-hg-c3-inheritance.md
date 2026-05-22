---
tags:
  - python
  - inheritance
  - oop
  - composition
aliases:
  - "C3"
  - "Inheritance"
parent: "[[Python — Map of Content]]"
created: 2026-05-21
status: complete
---

# C3 — Inheritance and When to Avoid It

> **What this fixes:** Either never using inheritance (and duplicating code), or overusing it (and creating fragile class trees that break when anything changes).
>
> **The shift:** Inheritance is for *is-a* relationships. Composition is for *has-a* relationships. When in doubt, start with composition.

---

## What inheritance actually is

Inheritance lets one class acquire the attributes and methods of another. The child class gets everything the parent has — and can extend or override it.

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def breathe(self):
        return f"{self.name} breathes"

    def speak(self):
        return "..."

class Dog(Animal):              # Dog inherits from Animal
    def speak(self):            # overrides Animal.speak
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"

dog = Dog("Rex")
print(dog.breathe())    # "Rex breathes" — inherited from Animal
print(dog.speak())      # "Rex says Woof!" — overridden in Dog
```

`Dog` didn't redefine `breathe` — it inherited it. It only defined what's different: `speak`. That's the point of inheritance — share what's common, specialise what's different.

---

## The one test: "is-a" vs "has-a"

This is the clearest rule in all of OOP:

- **Inheritance** → *is-a* relationship. A Dog **is an** Animal. A Manager **is an** Employee. A SavingsAccount **is a** BankAccount.
- **Composition** → *has-a* relationship. A Car **has an** Engine. A User **has a** TaxCalculator. An Order **has** line items.

```python
# is-a → inheritance makes sense
class Employee:
    ...

class Manager(Employee):   # A Manager IS an Employee ✅
    ...

# has-a → composition makes sense
class User:
    def __init__(self):
        self.tax_calculator = TaxCalculator()  # A User HAS a TaxCalculator ✅

# Wrong — inheriting TaxCalculator into User
class User(TaxCalculator):   # A User IS NOT a TaxCalculator ❌
    ...
```

If you can't honestly say "X is a Y" — don't use inheritance.

---

## `super()` — calling the parent

When you override a method in a child class, you often still want the parent's version to run first. `super()` gives you access to the parent class.

```python
class Employee:
    def __init__(self, name, id_number, gross_salary):
        self.name = name
        self.id_number = id_number
        self.gross_salary = gross_salary

class Manager(Employee):
    def __init__(self, name, id_number, gross_salary, team_size):
        super().__init__(name, id_number, gross_salary)  # run Employee's __init__
        self.team_size = team_size     # then add Manager-specific state

    def team_bonus(self):
        return self.gross_salary * 0.1 * self.team_size

manager = Manager("Alice", "EMP042", 150000, team_size=8)
print(manager.name)         # "Alice" — set by Employee.__init__ via super()
print(manager.team_bonus()) # 120000.0
```

**Always call `super().__init__()` in a child's `__init__`** if the parent has one. Skipping it means the parent's attributes never get set — everything inherited from the parent breaks.

---

## Method overriding

A child class can replace any parent method by defining one with the same name:

```python
class Notification:
    def send(self, message):
        print(f"Sending: {message}")

class EmailNotification(Notification):
    def __init__(self, email):
        self.email = email

    def send(self, message):                        # overrides Notification.send
        print(f"Emailing {self.email}: {message}")

class SMSNotification(Notification):
    def __init__(self, phone):
        self.phone = phone

    def send(self, message):                        # overrides Notification.send
        print(f"Texting {self.phone}: {message}")

# Polymorphism — same interface, different behaviour
notifications = [
    EmailNotification("wilber@example.com"),
    SMSNotification("+254712345678"),
]

for n in notifications:
    n.send("Your order is ready")
# Emailing wilber@example.com: Your order is ready
# Texting +254712345678: Your order is ready
```

This is polymorphism — different classes responding to the same method call in different ways. It's one of the main legitimate reasons for inheritance.

---

## Composition — the often better alternative

Composition means building a class by *containing* instances of other classes rather than *inheriting* from them.

```python
# Inheritance approach — fragile
class LoggingDB(Database):          # LoggingDB IS-A Database?
    def query(self, sql):
        print(f"Running: {sql}")
        return super().query(sql)   # tightly coupled to Database internals

# Composition approach — flexible
class LoggingDB:
    def __init__(self, database):
        self._db = database         # HAS-A Database

    def query(self, sql):
        print(f"Running: {sql}")
        return self._db.query(sql)  # delegates to the database
```

With composition, `LoggingDB` doesn't care about `Database`'s internals. You can swap out any database that has a `.query()` method. Nothing breaks.

### The practical case: a Textual-style widget

In Textual, `Widget` is inherited because a `Button` genuinely *is* a `Widget`. But the button's click handler *has* a reference to whatever logic it needs to run — that's composition:

```python
# Inheritance — correct, Button IS a Widget
class ConfirmButton(Button):
    def on_click(self):
        self.action()

# Composition — correct, button HAS a handler
class JobCard(Widget):
    def __init__(self, job_listing):
        super().__init__()
        self.job = job_listing     # HAS a JobListing, doesn't inherit it
```

---

## When to use inheritance — the short list

Use it when all of these are true:

1. **The "is-a" test passes** — genuinely, not just for convenience
2. **The child needs most of the parent's behaviour** — not just one or two methods
3. **The hierarchy is shallow** — one or two levels deep, not five
4. **You're extending, not just reusing** — the child adds or specialises, not just borrows

Real examples where inheritance is the right call:
- `Manager(Employee)` — a Manager is an Employee with extra responsibilities
- `SavingsAccount(BankAccount)` — a SavingsAccount is a BankAccount with interest rules
- `Button(Widget)` in Textual — a Button is a Widget that responds to clicks
- Custom exceptions: `InvoiceError(Exception)` — an InvoiceError is an Exception

---

## When to use composition instead

Use composition when:

- The "is-a" test fails — "a User is not a TaxCalculator"
- You want to reuse *behaviour* without the full type relationship
- The class needs to be flexible — swappable components, not locked inheritance
- You're starting to build deep hierarchies (more than 2 levels)
- Multiple inheritance starts looking tempting (usually a signal to step back)

```python
# Inheritance abuse — User IS NOT a Logger or a Validator
class User(Logger, Validator, EmailSender):
    ...

# Composition — User HAS these capabilities
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self._logger = Logger()
        self._validator = EmailValidator()
        self._mailer = EmailSender()

    def register(self):
        if not self._validator.is_valid(self.email):
            raise ValueError("Invalid email")
        self._logger.log(f"Registering {self.name}")
        self._mailer.send_welcome(self.email)
```

---

## Multiple inheritance — use with extreme caution

Python supports inheriting from multiple parents. It can be useful for Mixins (small, focused behaviour additions), but it creates complexity fast.

```python
# Mixin pattern — acceptable multiple inheritance
class TimestampMixin:
    """Adds created_at and updated_at to any class."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def touch(self):
        self.updated_at = datetime.now()

class Invoice(TimestampMixin, BaseDocument):
    def __init__(self, number, amount):
        super().__init__()    # super() handles MRO correctly
        self.number = number
        self.amount = amount
```

Mixins work when they:
- Add a small, focused capability (timestamps, logging, serialisation)
- Don't carry complex state of their own
- Use `super()` correctly throughout

### The diamond problem

Multiple inheritance can cause the diamond problem — where two parents both inherit from the same grandparent, and Python has to decide whose version of a method to use:

```python
class A:
    def method(self): print("A")

class B(A):
    def method(self): print("B")

class C(A):
    def method(self): print("C")

class D(B, C):   # D inherits from both B and C
    pass

D().method()    # "B" — Python uses MRO (Method Resolution Order): D → B → C → A
```

Python resolves this with the MRO — check it with `ClassName.__mro__`. But when your class hierarchy is complex enough that you're regularly checking MRO to understand your own code, that's a signal to reach for composition instead.

---

## The rule of thumb

From the Gang of Four design patterns book — one of the most influential books in software engineering:

> *"Favour object composition over class inheritance."*

And from Real Python: *"If you see yourself beginning to use multiple inheritance and a complicated class hierarchy, it's worth asking yourself if you can achieve code that is cleaner and easier to understand by using composition instead."*

Start with composition. Use inheritance only when the is-a relationship is genuine and the hierarchy stays shallow. If you're unsure which to use, composition is easier to refactor later than a tangled inheritance tree.

---

## Side-by-side decision

| Situation | Use |
|---|---|
| `Manager` and `Employee` | Inheritance — Manager is an Employee |
| `User` needs logging | Composition — User has a Logger |
| `Button` in a UI framework | Inheritance — Button is a Widget |
| `Order` needs tax calculation | Composition — Order has a TaxCalculator |
| Adding timestamps to many classes | Mixin (multiple inheritance, carefully) |
| Sharing a `.query()` method across DB wrappers | Composition — each wrapper has a DB |
| Custom exceptions | Inheritance — `PaymentError(Exception)` |
| Deep hierarchy, 4+ levels | Red flag — refactor to composition |

---

## Quick reference card

```
The is-a test:
  □ "X is a Y" passes genuinely → inheritance may be right
  □ "X has a Y" → composition is right
  □ "X uses Y" → composition is right

super():
  □ Always call super().__init__() in child __init__
  □ super() gives access to the parent class
  □ Required for multiple inheritance to work correctly

Inheritance — use when:
  □ is-a relationship is genuine
  □ Child needs most of parent's behaviour
  □ Hierarchy stays shallow (1-2 levels)
  □ You're specialising, not just reusing

Composition — use when:
  □ has-a relationship
  □ You want flexibility / swappable components
  □ Hierarchy is getting deep
  □ Multiple inheritance is starting to look necessary
  □ You're unsure — composition is easier to refactor

Mixins — acceptable multiple inheritance:
  □ Small, focused capability (timestamps, logging)
  □ Little or no state of their own
  □ Always use super() throughout

Red flags:
  □ "X IS-A Y" test fails but you're inheriting anyway
  □ More than 2-3 levels of inheritance
  □ Child overrides most of the parent's methods
  □ You're checking __mro__ to understand your own code
```

---

## What's next

You know inheritance — when it's right and when it isn't. Now: the dunder methods that make your classes behave like proper Python objects.

→ **Next: C4 — Dunder methods**

---

*Part of the Python Hitchhiker's Guide | Last updated: May 2026*
