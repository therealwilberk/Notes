---
type: project
tags: [project, wpick, matugen, tasks]
created: 2026-05-25
status: in-progress
parent: "[[Projects/active/Dusky-Theme-Engine/wpick- Wallpaper Clustering & Smart Picker.md]]"
---

# wpick Matugen Integration — Task Breakdown

**Date:** 2026-05-25
**Research:** [[wpick-matugen-research.md]]
**Critique:** [[wpick-matugen-critique.md]]
**Status:** Ready to execute

---

## Task 1: Fix config deep merge (pre-requisite)
**File:** `src/wpick/config.py`
**Effort:** 15 min
**Blocks:** Everything

The shallow `raw.update(user_raw)` destroys nested sections. A user setting just `scheme = "scheme-vibrant"` loses all other matugen defaults.

```python
def _deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge override into base."""
    result = base.copy()
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result
```

Replace `raw.update(user_raw)` with `raw = _deep_merge(raw, user_raw)`.

**Verify:** Test that setting `[matugen] scheme = "scheme-vibrant"` preserves other matugen defaults.

---

## Task 2: Expand MatugenConfig model
**File:** `src/wpick/models.py`
**Effort:** 15 min
**Depends on:** Task 1

Add new fields with validators:

```python
class MatugenConfig(BaseModel):
    """matugen colour generation settings."""
    enabled: bool = True
    scheme: str = "scheme-tonal-spot"
    mode: str = "dark"
    prefer: str = "saturation"
    contrast: float = Field(default=0.0, ge=-1.0, le=1.0)
    source_color_index: int | None = None
    lightness_dark: float | None = Field(default=None, le=1.0)
    lightness_light: float | None = Field(default=None, ge=-1.0)
    extra_flags: list[str] = Field(default_factory=list)
```

Validators:
- `scheme`: against 9 allowed values
- `mode`: light/dark only
- `prefer`: against 5 allowed values (remove `closest-to-fallback` — requires `--fallback-color` which we don't expose)
- `source_color_index`: 0-3 range
- `lightness_dark`: le=1.0
- `lightness_light`: ge=-1.0

**Verify:** `mypy src/wpick/models.py` passes. All validators tested.

---

## Task 3: Extract _build_matugen_cmd + add enabled guard + timeout
**File:** `src/wpick/orchestrator.py`
**Effort:** 20 min
**Depends on:** Task 2

```python
def _build_matugen_cmd(path: Path, cfg: MatugenConfig) -> list[str] | None:
    """Build matugen command. Returns None if disabled."""
    if not cfg.enabled:
        return None
    cmd = ["matugen", "image", str(path)]
    cmd.extend(["--type", cfg.scheme])
    cmd.extend(["--mode", cfg.mode])
    cmd.extend(["--prefer", cfg.prefer])
    if cfg.contrast != 0.0:
        cmd.extend(["--contrast", str(cfg.contrast)])
    if cfg.source_color_index is not None:
        cmd.extend(["--source-color-index", str(cfg.source_color_index)])
    if cfg.lightness_dark is not None:
        cmd.extend(["--lightness-dark", str(cfg.lightness_dark)])
    if cfg.lightness_light is not None:
        cmd.extend(["--lightness-light", str(cfg.lightness_light)])
    cmd.extend(cfg.extra_flags)
    return cmd
```

Update `set_wallpaper`:
- Check `if cmd is None: return` (enabled=false)
- Add `timeout=30` to subprocess.run
- Catch `subprocess.TimeoutExpired`
- Log warning if `extra_flags` contains known structured flags (--type, --mode, --prefer)

**Verify:** `ruff check` passes. Test enabled=false skips matugen. Test timeout handling.

---

## Task 4: Create `wpick set <path>` command with matugen flags
**File:** `src/wpick/cli.py`
**Effort:** 25 min
**Depends on:** Task 3

New command:
```python
@app.command()
def set(
    path: Path = typer.Argument(..., help="Path to wallpaper image"),
    matugen_scheme: str = typer.Option(None, "--matugen-scheme", help="Color scheme type"),
    matugen_mode: str = typer.Option(None, "--matugen-mode", help="Light or dark mode"),
    matugen_prefer: str = typer.Option(None, "--matugen-prefer", help="Source color selection"),
    matugen_contrast: float = typer.Option(None, "--matugen-contrast", help="Contrast (-1 to 1)"),
    matugen_source_index: int = typer.Option(None, "--matugen-source-index", help="Source color index (0-3)"),
    matugen_lightness_dark: float = typer.Option(None, "--matugen-lightness-dark", help="Dark mode lightness"),
    matugen_lightness_light: float = typer.Option(None, "--matugen-lightness-light", help="Light mode lightness"),
    no_matugen: bool = typer.Option(False, "--no-matugen", help="Disable matugen for this wallpaper"),
) -> None:
    """Set a specific wallpaper with optional matugen overrides."""
```

Logic:
1. Load config
2. Apply CLI overrides to cfg.matugen (only non-None values)
3. If `--no-matugen`, set `cfg.matugen.enabled = False`
4. Validate path exists
5. Call `set_wallpaper(path, db, cfg)`

**Verify:** `wpick set --help` shows all flags. Test override flow.

---

## Task 5: Update config.default.toml
**File:** `src/wpick/config.default.toml`
**Effort:** 10 min
**Depends on:** Task 2

```toml
[matugen]
enabled = true
scheme = "scheme-tonal-spot"
mode = "dark"
prefer = "saturation"
contrast = 0.0
# source_color_index = 0  # 0-3, omit to use prefer instead
# lightness_dark = 0.0    # fine-tune dark surfaces (-∞ to 1)
# lightness_light = 0.0   # fine-tune light surfaces (-1 to +∞)
extra_flags = []
```

**Verify:** `wpick init` generates correct config with new fields.

---

## Task 6: Add comprehensive tests
**File:** `tests/test_matugen.py`
**Effort:** 30 min
**Depends on:** Tasks 1-5

Test cases:
- MatugenConfig: default values, valid/invalid scheme, mode, prefer, source_color_index, contrast, lightness ranges
- `_build_matugen_cmd`: default config, all flags, optional flags omitted, enabled=false returns None, timeout handling
- Config deep merge: setting one field preserves others
- `extra_flags` conflict warning
- `closest-to-fallback` rejected (removed from allowed values)

**Verify:** `pytest tests/test_matugen.py -v` passes. No regressions in existing tests.

---

## Task 7: Update existing tests for new behavior
**File:** `tests/test_orchestrator.py`, `tests/test_config.py`
**Effort:** 15 min
**Depends on:** Task 6

- Update `test_calls_swww_and_matugen` — matugen args now include --type, --mode, --prefer
- Update `test_swww_failure_raises` if error path changed
- Add test for enabled=false skipping matugen
- Add test for matugen timeout

**Verify:** `pytest tests/ -x -q` passes. No regressions.

---

## Task 8: Docs update
**File:** `README.md`, config docs
**Effort:** 10 min
**Depends on:** Task 7

Document:
- New MatugenConfig options with examples
- `wpick set` command usage
- Minimum matugen version requirement
- Color scheme types and their characteristics (link to research)

---

## Execution Order

```
Task 1 (deep merge) 
  → Task 2 (model) 
    → Task 3 (cmd builder + enabled + timeout)
      → Task 4 (CLI set command)
      → Task 5 (config default.toml)
        → Task 6 (tests)
          → Task 7 (update existing tests)
            → Task 8 (docs)
```

## Verification Checklist

After each task:
- [ ] `ruff check src/ tests/` passes
- [ ] `mypy src/` passes
- [ ] `pytest tests/ -x -q` passes

After all tasks:
- [ ] `wpick set --help` shows matugen flags
- [ ] `wpick set --matugen-scheme scheme-vibrant <wallpaper>` works
- [ ] `wpick set --no-matugen <wallpaper>` skips matugen
- [ ] Config with only `[matugen] scheme = "..."` preserves defaults
- [ ] Daemon mode doesn't hang on multi-color images
- [ ] Matugen timeout (30s) works
