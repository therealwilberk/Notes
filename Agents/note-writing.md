# Note Writing

Two note flavors exist in this vault. Know which one you're writing.

## Flavor 1: Teaching Note

Comprehensive, concept-first. For learning a topic from scratch. Think Rust notes (rust-ownership.md).

- Teaches *why* something works, not just *how*
- Linear progression — each section builds on the last
- Code snippets are minimal, one idea per snippet
- Trap sections include personal anecdotes ("this tripped me up")
- Doubles as future reference material
- Longer form, more prose

## Flavor 2: Reference Note

Dense, actionable. For tools you already understand and need to use fast. Think Python notes (py-pandas.md).

- Opens with an 80/20 cheat sheet (big code block covering daily ops)
- Sections are independent — jump to any one
- Code is realistic and complete (real data, real patterns)
- Traps are numbered, factual, and objective
- Minimal prose, maximum code

## Voice & Tone (both flavors)

- **Prefer third-person, instructional.** For teaching notes, first-person is allowed in trap sections ("This tripped me up"). For reference notes, keep third-person throughout.
- Do not address the reader directly ("you can see", "you should"). Just state facts.
- Concise, direct. No fluff. No introductions or conclusions.
- **No emojis.**

Do:
```
A struct groups related data into one type. Fields are named, unlike tuples.
```

Don't:
```
I found that structs group related data. You can use them to organize your code. 😊
```

## The 80/20 Rule

Reference notes must open with an **80/20 cheat sheet** section. Teaching notes can include one but it's optional (Rust notes skip it).

The cheat sheet is a dense block of code or commands that covers 80% of daily usage in 20% of the content. A future reader should be able to copy-paste from here and be productive immediately.

Structure:
1. `## 80/20` section at the very top (after frontmatter)
2. A single code block showing the most common operations
3. Minimal comments inline -- let the code speak
4. Then expand into details below

## Content Style

- **Examples > prose.** One line of code is worth a paragraph of explanation.
- **Traps drive retention.** Every feature has a footgun. Document it. A "Trap" callout or a dedicated "Traps" section at the end.
- **Real-world use cases.** Do not clone the official docs or book examples. Use examples from: config management, API clients, data processing, CLI tools, networking. Things someone might actually build.
- **Comparisons.** Tables are preferred for comparing options (`| Option | Use |`).
- **Be opinionated.** If there is a "right" way and a "wrong" way, say so. Flag anti-patterns with "Bad order" / "Good order" or "Don't."

## Section Headers

- `##` for major sections
- `###` for subsections
- No extra blank lines after headers
- No period in headers

## Code Blocks

- Always specify language: `` ```rust ```, `` ```yaml ```, `` ```dockerfile ```
- Use `#` comments inside code blocks sparingly, only for clarity
- Show both the correct and incorrect pattern when a trap exists

## Linking

Use `[[wikilink]]` syntax for:
- `parent` in frontmatter
- Cross-references between note files
- MOC entries

Do:
```
parent: "[[Rust -- Map of Content]]"
See [[rust-slices]] for the range syntax.
```

## Git Commits

After writing or editing notes, commit with a message like:
```
notes: add <topic> note
notes: update <topic> with <change>
```
