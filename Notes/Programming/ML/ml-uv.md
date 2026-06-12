---
tags: [ml, python, uv, package-manager]
aliases: ["uv cheatsheet"]
created: 2026-06-11
status: complete
parent: "[[MOCs/ML & Data Science Packages -- Map of Content]]"
---

## 80/20

```bash
uv init <name>        # create project (pyproject.toml + venv)
uv add <pkg>          # add runtime dep + resolve + update uv.lock
uv add --dev <pkg>    # add dev-only dep
uv remove <pkg>       # remove dep + prune lock
uv sync               # install everything from uv.lock
uv sync --frozen      # CI-safe: fail if uv.lock != pyproject.toml
uv lock               # regenerate uv.lock without installing
uv run <cmd>          # run in project venv (no activation needed)
uv run python --version
uv tree               # dependency tree
uv python list        # list installed Python versions
uv python install 3.12  # install a Python version
```

uv replaces pip + poetry + virtualenv with a single Rust binary. `pyproject.toml` is the single source of truth. `uv.lock` pins every transitive dep -- commit it, never gitignore it.

## Core commands

| Command | What it does | When |
|---------|-------------|------|
| `uv init` | scaffold project, create pyproject.toml, venv, basic dirs | start of project |
| `uv add` | add dep to pyproject.toml, resolve tree, write uv.lock | adding a library |
| `uv remove` | remove dep, prune lock | cleanup |
| `uv sync` | install all deps matching uv.lock exactly | after git pull, in CI |
| `uv sync --frozen` | same but refuses to modify pyproject.toml or uv.lock | CI/CD |
| `uv lock` | regenerate lock from pyproject.toml | after manual pyproject.toml edits |
| `uv run` | run any command inside project's venv | every Python command |
| `uv tree` | show full dependency tree | debugging conflicts |
| `uv add --dev` | add to `[tool.uv.dev-dependencies]` | dev tooling |

## Convention

```bash
# before commit
uv lock                    # if pyproject.toml changed
uv sync --frozen           # verify lock is in sync
uv run pytest              # run tests
uv run ruff check          # lint

# in CI
uv sync --frozen
uv run pytest
```

## Traps

- **Do not activate venv manually** -- always use `uv run`. This is the canonical invocation pattern.
- **`uv sync --frozen` fails** -- uv.lock is out of sync with pyproject.toml. Run `uv sync` locally.
- **Old uv version** -- older `uv init` creates different structure. Keep uv updated: `uv self update`.
- **`uv` not found after install** -- `~/.local/bin` may not be on PATH. Restart shell or add manually.
- **Never gitignore uv.lock** -- it is the reproducibility contract for the project.
