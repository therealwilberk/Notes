# Lessons Process

Use this process when the user says "I need to learn X" or "create a curriculum for Y". This applies to hands-on topics (Docker, Kubernetes, tools, frameworks) where progressive practice is more valuable than reference docs.

## Step 1: Research

- Search the web for current best practices, common pitfalls, and learning paths for the topic
- Target 2025-2026 sources -- outdated Docker/K8s advice is misleading
- Topics to research: syntax, common patterns, production pitfalls, tool-specific gotchas
- If the topic is large, use a sub-agent for research with a specific brief

## Step 2: Sub-Agent Critique (Draft Curriculum)

Before presenting to the user:

1. Draft a progressive curriculum: 4-7 modules, each building on the last
2. Hand the draft to a sub-agent with instructions to critique:
   - Completeness -- is anything essential missing?
   - Sequence -- should any modules move?
   - Depth -- are modules the right size?
   - Exercise progression -- does guided->unguided ramp make sense?
   - Real-project alignment -- does this prepare for the user's actual stack?
   - Gaps and blind spots
3. Incorporate the critique into a revised curriculum

Curriculum structure per module:
- Module number and title
- Core concepts covered
- Exercise difficulty level (guided / semi-guided / unguided / capstone)

## Step 3: Present Curriculum for Confirmation

Output the full curriculum to the user. Include:
- Module list with concepts and exercise difficulty
- Exercise progression table
- Key changes from the draft (if revised)
- Ask: "Proceed, or adjust?"

## Step 4: Build Modular Notes

After confirmation:

- Break the monolithic reference into one note file per module
- Naming: `<topic>-m<number>-<short-name>.md` (e.g., `docker-m1-containers.md`)
- Each file gets frontmatter with `parent` linking back to the MOC and `exercises` linking to its exercise dir
- The `docker.md` (or `<topic>.md`) becomes the **MOC** -- 80/20 at top, module index table, traps section
- Write all module files before exercises (the exercises reference them)

## Step 5: Build Exercises Per Module

- Create `exercises/<module-n>/README.md` for each module
- Exercise difficulty must progress across modules:
  - Module 1: fully guided (copy-paste commands, expected output shown)
  - Module 2-3: guided to semi-guided (goal stated, hints available)
  - Module 4-5: semi-guided to unguided (goal only, figure it out)
  - Module 6+: unguided / "you're on your own"
  - Final module: capstone exercise applying everything to the user's real project
- Exercises use the user's actual tooling (e.g., `uv` not `pip`)
- Each exercise has learning objectives at the top
- Scaffold files live alongside the README if needed
- Create an `exercises/README.md` index with module difficulty key

## Step 6: Update MOC

Add a row for the new topic in the appropriate MOC with status "Complete".

## Exercise Schema

### Directory Layout

```
exercises/
├── README.md              # Module index (difficulty key, prerequisites, module table)
├── module-1/
│   ├── README.md          # Module instructions (see template below)
│   ├── scaffold/          # Starter code files (optional)
│   └── solutions/         # Answer key (optional)
├── module-2/
│   └── ...
└── module-N/
    └── ...
```

### Module README Template

Every module README must follow this structure:

```yaml
---
tags: [topic, exercise, module-N]
parent: "[[Topic MOC]]"
created: YYYY-MM-DD
status: draft | in-progress | complete
difficulty: guided | semi-guided | unguided | capstone | you're-on-your-own
mode: learning | project
---

# Module N: Topic Name

## Learning Objectives
...

## New Concepts
... (code snippets explaining what you need)

## Requirements / Exercises
1. ...
2. ...

## Hints
...

## Trap: ...
...

## Verification
```bash
...
```
```

### Two Exercise Modes

| Mode | When | Style |
|------|------|-------|
| **learning** | Fresh on the topic, need hand-holding | Concepts explained inline in the module README. Guided exercises with hints, traps, verification. Scaffold provided. Companion teaching notes exist alongside. |
| **project** | Building a real project across modules | Requirements-based. Less hand-holding, more discovery. Exercises build cumulatively (e.g., Rust fcard builds one CLI tool across 6 modules). |

### Progressive Build Pattern (ML/Python series example)

For a topic where exercises build on each other (numpy → pandas → sklearn):

1. Each module takes the **output of the previous module** as its starting point
2. Example: M1 produces a cleaned numpy array → M2 wraps it in a DataFrame, adds datetime → M3 feeds it into a sklearn pipeline
3. The companion notes (teaching or reference) sit alongside `exercises/` at the topic level
4. The capstone module is unguided: "build a complete pipeline from raw data to trained model"

### Modularity Rules

- Each module is self-contained in `module-N/`
- Each module has exactly one `README.md` entry point
- Difficulty must progress across modules: guided → semi-guided → unguided → capstone
- Companion notes sit at the topic level alongside `exercises/` (e.g., `py-pandas.md` and `exercises/` are siblings)
- Scaffold code goes in `module-N/scaffold/`
- Solutions go in `module-N/solutions/` (optional, skip in learning mode)
- Topic-level `exercises/README.md` has the difficulty key + module overview table

### Project Hub Note

When working on a real project (e.g., jua-ml in `~/dev/jua-ml`):

- Create a lightweight README at `Research/<Project-Name>/README.md`
- It links to the repo path, captures architecture decisions and traps encountered
- Cross-references domain notes via wikilinks (e.g., `[[Notes/ML/Tools/ml-sklearn]]`)
- The actual code stays in `~/dev/`

## Git Commits

After building a curriculum, commit module by module or as a batch:
```
curriculum: add <topic> modules M1-M<N>
curriculum: add <topic> exercises M1-M<N>
```
