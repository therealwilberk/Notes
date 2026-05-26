# wpick Matugen Integration — Implementation Plan

**Date:** 2026-05-25
**Research:** [[wpick-matugen-research.md]]
**Status:** Planning

---

## Problem

wpick calls `matugen image <path>` with **zero flags**. This means:
1. **Daemon hang bug**: No `--prefer` or `--source-color-index` → interactive prompt → daemon hangs
2. **Only default scheme**: Users get `scheme-tonal-spot` always — 8 other schemes ignored
3. **No light/dark toggle**: Hardcoded to dark mode
4. **No contrast/lightness tuning**: Accessibility and aesthetic options missing

---

## Implementation Tasks

### Task 1: Expand MatugenConfig model
**File:** `src/wpick/models.py`
**Effort:** 15 min

```python
class MatugenConfig(BaseModel):
    """matugen colour generation settings."""
    enabled: bool = True
    scheme: str = "scheme-tonal-spot"  # NEW
    mode: str = "dark"                  # NEW
    prefer: str = "saturation"          # NEW (fixes daemon bug)
    contrast: float = Field(default=0.0, ge=-1.0, le=1.0)  # NEW
    source_color_index: int | None = None  # NEW: 0-3
    lightness_dark: float | None = None    # NEW
    lightness_light: float | None = None   # NEW
    extra_flags: list[str] = Field(default_factory=list)

    @field_validator("scheme")
    @classmethod
    def validate_scheme(cls, v: str) -> str:
        allowed = {
            "scheme-content", "scheme-expressive", "scheme-fidelity",
            "scheme-fruit-salad", "scheme-monochrome", "scheme-neutral",
            "scheme-rainbow", "scheme-tonal-spot", "scheme-vibrant",
        }
        if v not in allowed:
            raise ValueError(f"Invalid scheme: {v}. Allowed: {sorted(allowed)}")
        return v

    @field_validator("mode")
    @classmethod
    def validate_mode(cls, v: str) -> str:
        if v not in {"light", "dark"}:
            raise ValueError(f"Invalid mode: {v}. Must be 'light' or 'dark'")
        return v

    @field_validator("prefer")
    @classmethod
    def validate_prefer(cls, v: str) -> str:
        allowed = {"darkness", "lightness", "saturation", "less-saturation", "value", "closest-to-fallback"}
        if v not in allowed:
            raise ValueError(f"Invalid prefer: {v}. Allowed: {sorted(allowed)}")
        return v

    @field_validator("source_color_index")
    @classmethod
    def validate_source_color_index(cls, v: int | None) -> int | None:
        if v is not None and not (0 <= v <= 3):
            raise ValueError(f"source_color_index must be 0-3, got {v}")
        return v
```

### Task 2: Extract _build_matugen_cmd helper
**File:** `src/wpick/orchestrator.py`
**Effort:** 20 min

```python
def _build_matugen_cmd(path: Path, cfg: MatugenConfig) -> list[str]:
    """Build the matugen command with all configured flags."""
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

### Task 3: Wire set_wallpaper to use _build_matugen_cmd
**File:** `src/wpick/orchestrator.py`
**Effort:** 10 min

```python
def set_wallpaper(path: Path, db: WallpaperDB, cfg: Config, log: bool = True) -> None:
    """Set desktop wallpaper via swww and generate colours via matugen."""
    # ... swww code stays the same ...
    
    matugen_cmd = _build_matugen_cmd(path, cfg.matugen)
    matugen_result = subprocess.run(matugen_cmd, capture_output=True, text=True)
    # ... error handling stays the same ...
```

### Task 4: Add CLI flags for matugen options
**File:** `src/wpick/cli.py`
**Effort:** 20 min

Add to the `set` command:
```python
@cli.command()
def set(
    # ... existing args ...
    matugen_scheme: str = typer.Option(None, "--matugen-scheme", help="Color scheme type"),
    matugen_mode: str = typer.Option(None, "--matugen-mode", help="Light or dark mode"),
    matugen_prefer: str = typer.Option(None, "--matugen-prefer", help="Source color selection strategy"),
    matugen_contrast: float = typer.Option(None, "--matugen-contrast", help="Contrast (-1 to 1)"),
    matugen_source_index: int = typer.Option(None, "--matugen-source-index", help="Source color index (0-3)"),
):
```

### Task 5: Add tests for MatugenConfig validation
**File:** `tests/test_matugen_config.py`
**Effort:** 20 min

Test cases:
- Default values
- Valid scheme names
- Invalid scheme raises ValueError
- Valid mode (light/dark)
- Invalid mode raises ValueError
- Valid prefer values
- Invalid prefer raises ValueError
- source_color_index 0-3 valid, 4 invalid
- contrast range -1 to 1

### Task 6: Add tests for _build_matugen_cmd
**File:** `tests/test_matugen_cmd.py`
**Effort:** 20 min

Test cases:
- Default config produces correct cmd
- All flags wired correctly
- Optional flags omitted when None
- contrast=0.0 omitted
- extra_flags appended
- source_color_index conditional

### Task 7: Add tests for set_wallpaper with matugen
**File:** `tests/test_orchestrator_matugen.py`
**Effort:** 15 min

Test cases:
- set_wallpaper calls matugen with correct cmd
- matugen failure logs warning but doesn't raise
- _build_matugen_cmd called with cfg.matugen

### Task 8: Update config schema docs
**File:** `docs/config.md` or README
**Effort:** 10 min

Document new MatugenConfig options with examples.

---

## Execution Order

1. Task 1 (model) → Task 5 (model tests)
2. Task 2 (cmd builder) → Task 6 (cmd tests)
3. Task 3 (wire set_wallpaper) → Task 7 (orchestrator tests)
4. Task 4 (CLI flags)
5. Task 8 (docs)

Each task is **one file, one concern**. Agents can't get lost.

---

## Verification Checklist

After each task:
- [ ] `ruff check src/ tests/` passes
- [ ] `mypy src/` passes
- [ ] `pytest tests/ -x -q` passes
- [ ] No regressions in existing tests

After all tasks:
- [ ] Manual test: `wpick set --help` shows new flags
- [ ] Manual test: `wpick set --matugen-scheme scheme-vibrant <wallpaper>` works
- [ ] Manual test: daemon mode doesn't hang on multi-color images
