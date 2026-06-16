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

## Exercise Schema Reference

Exercise modules follow this standardized structure (defined in `note-structure.md`):

```
exercises/
├── README.md              # Index with difficulty key, prerequisites, module overview table
├── module-1/
│   ├── README.md          # Module instructions with frontmatter
│   ├── scaffold/          # Starter code (optional)
│   └── solutions/         # Answer key (optional)
├── module-2/
└── ...
```

Each module README uses the standardized template: frontmatter → Learning Objectives → New Concepts → Requirements → Hints → Traps → Verification.

Supported modes:
- **learning**: concepts explained inline, guided exercises with hints/traps/verification
- **project**: requirements-based, builds cumulative project, less hand-holding (e.g., Rust fcard)

## Git Commits

After building a curriculum, commit module by module or as a batch:
```
curriculum: add <topic> modules M1-M<N>
curriculum: add <topic> exercises M1-M<N>
```
