---
type: topic
tags: [eee, cross-referencing, multi-page, conventions]
created: 2026-06-01
status: building
parent: "[[MOC — Electrical Installation]]"
sources:
  - "[[BMS Controls Training — 6hr Video]]"
  - "[[Upmation — How to Read Electrical Diagrams]]"
---

# Cross-Referencing Multi-Page Diagrams

## The Problem

Real schematic sets span dozens or hundreds of pages. A relay coil on page 3 has contacts on pages 7, 12, and 45. A signal enters on page 1 and reappears on page 8. Without a systematic way to follow these connections, the drawing is useless.

## Page.Column Format

Each page is divided into **numbered columns** (numbers at the top of the page). The cross-reference format is:

**page.column** — e.g., "2.03" means page 2, column 3.

This is how you locate anything in the drawing set. Every contact, coil, and signal has an address.

## How Cross-References Appear

### On a Coil

Below or next to a coil symbol, a list shows **all contacts** belonging to that coil, with their page.column addresses. So if K1's coil is on page 3, the notation below it might show:

```
K1: 5.04, 7.02, 12.06
```

Meaning: K1 has contacts at page 5 column 4, page 7 column 2, and page 12 column 6.

### On a Contact

Next to a contact symbol, the notation shows **where the driving coil lives**. So a NO contact on page 7 would reference back to K1's coil location on page 3.

### Signal Continuation

An arrow with a page.column number means "this wire/signal continues at..." — used when a circuit path crosses from one page to the next.

## The Habit

Reading a multi-page schematic requires **constantly jumping between pages**. A coil on page 130 has contacts on page 2, which reference back to page 130.

> [!tip] Build the habit
> Follow references instead of trying to understand a single page in isolation. A page only makes full sense in the context of the pages it references. Flipping back and forth is not doing it wrong — that's how these drawings are meant to be read.

## Column Numbers as Locators

Within a single page, column numbers help locate components. Combined with the page number, they give a precise address. This is especially useful when discussing a drawing with someone — "look at page 5, column 3" is unambiguous.
