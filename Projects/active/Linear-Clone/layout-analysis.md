---
type: project
tags: [project, linear, design, research]
aliases: ["Linear Layout Analysis"]
parent: "[[MOCs/Linear Clone — Map of Content.md]]"
created: 2026-05-21
status: paused
---

# Linear.app — Layout Analysis

> **Goal:** Document every section, color, font, and spacing value so you can rebuild it in Framer without constantly alt-tabbing back to the live site.
>
> **How to fill this in:** Open [linear.app](https://linear.app) → Right-click → Inspect → Click elements → Read the Styles/Computed panel. Fill in the blanks.

---

## 1. Colors

| What | Value | Notes |
|---|---|---|
| Page background | `#` | Near-black, not pure black |
| Heading text | `#` | Almost white |
| Body/subtitle text | `#` | Muted gray |
| Primary accent (links, buttons) | `#` | Indigo-ish |
| Card/section background | `#` | Slightly lighter than page bg |
| Border/divider | `#` | Subtle, barely visible |
| Error/destructive | `#` | Red |
| Success | `#` | Green |

**How to find:** Click element → look at `color` (text) or `background-color` in Styles panel.

---

## 2. Typography

### Font Family
- Primary: ``
- Monospace: `` (used in code blocks)

### Type Scale

| Element | Size | Weight | Line Height | Letter Spacing |
|---|---|---|---|---|
| H1 (hero headline) | px | | px | px |
| H2 (section heading) | px | | px | px |
| H3 (card heading) | px | | px | — |
| Body text | px | | px | — |
| Nav links | px | | — | — |
| Small/caption | px | | — | — |
| Button text | px | | — | — |

**How to find:** Click the element → look at `font-size`, `font-weight`, `line-height`, `letter-spacing` in Computed tab.

---

## 3. Spacing & Layout

### Page Structure
- Content max-width: `px`
- Section vertical padding: top `px` / bottom `px`
- Between-section gap: `px`
- Nav height: `px`
- Main content top padding: `px`

### Internal Spacing (within sections)
- Card padding: `px`
- Heading → subtitle gap: `px`
- Subtitle → CTA gap: `px`
- List item gap: `px`

**How to find:** Click element → look at the **Box Model** diagram in Computed tab. Margin = outside gap, Padding = inside gap.

---

## 4. Border Radius

| Element | Radius |
|---|---|
| Primary buttons | px (pill / rounded) |
| Cards / containers | px |
| Small badges / tags | px |
| Images | px |
| Inputs | px |

**How to find:** Click element → `border-radius` in Styles.

---

## 5. Section Map (top to bottom)

### Section 1: Navbar
- Height: `px`
- Position: sticky / static?
- Background: transparent / solid / blur?
- Layout: Logo (left) | Nav links (center) | Auth buttons (right)
- Links: Product, Resources, Customers, Pricing, Now, Contact
- Mobile behavior: hamburger menu?

### Section 2: Hero
- H1 text: "The product development system for teams and agents"
- Subtitle text: "Purpose-built for planning and building products..."
- CTA: "Issue tracking is dead →" (link, not button?)
- Alignment: center / left?
- Height: `px`
- Padding: `px`

### Section 3: App Mockup
- What it shows: Linear UI screenshot (sidebar + issue list + detail panel)
- Rounded corners? `px`
- Shadow / glow effect?
- Width: full / contained?
- Height: `px`

### Section 4: Logo Strip
- Company logos (how many?)
- Grayscale / color?
- Spacing between logos: `px`
- Alignment: center?

### Section 5: Features (first block)
- Heading: "A new species of product tool"
- Layout: text left / image right? or centered?
- Section height: `px`

### Section 6: Feature Cards / Grid
- How many columns?
- Card contents: icon + heading + description?
- Card background color: `#`
- Gap between cards: `px`

### Section 7: Social Proof / Testimonials
- Quotes from customers?
- Layout: carousel / grid / single quote?

### Section 8: CTA Section
- Heading text: ?
- Button text: ?
- Background: same dark / different?

### Section 9: Footer
- Columns: ?
- Links per column: ?
- Background: `#`
- Font size: `px`

---

## 6. Breakpoints

> Resize the browser window and watch when the layout changes. Write down those widths.

| Breakpoint | Width | What changes |
|---|---|---|
| Desktop | px+ | Full layout |
| Tablet | ~px | ? |
| Mobile | ~px | ? |

**How to find:** Drag the browser window edge narrower. When the layout shifts, check the width in DevTools (top-right corner shows viewport size).

---

## 7. Screenshots

> Take a screenshot of each section and save to `~/Documents/Text/Linear-Clone/screenshots/`

- [ ] Full page (wide)
- [ ] Navbar (desktop)
- [ ] Hero section
- [ ] App mockup
- [ ] Logo strip
- [ ] Features section
- [ ] Footer
- [ ] Mobile view (375px width)

---

## 8. Notes & Observations

_(Write anything else you notice — scroll animations, hover effects, subtle gradients, how elements transition, etc.)_

-
-
-

---

*Template created: 2026-05-20*
*Source: https://linear.app*
