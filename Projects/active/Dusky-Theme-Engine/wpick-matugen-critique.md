# wpick Matugen Integration Plan — Critique

**Date:** 2026-05-25
**Reviewer:** Critical analysis against codebase
**Verdict:** 7 blocking issues, 6 significant gaps, 5 minor concerns

---

## BLOCKING ISSUES

### B1. The `set` command doesn't exist — Task 4 is broken

Task 4 says: "Add to the `set` command" with `@cli.command() def set(...)`.

**Problem:** The CLI (`cli.py`) has NO `set` command. The available commands are:
- `init`, `scan`, `cluster`, `assign`, `pick`, `next`, `prev`, `watch`, `restore`, `stats`

Wallpapers are currently set via:
1. `pick` → rofi picker → `set_wallpaper()`
2. `next` / `prev` → cycle → `set_wallpaper()`
3. `restore` → re-apply last → `set_wallpaper()`

None of these accept matugen CLI flags. Task 4 as written is impossible — there's no `set` command to add flags to.

**Fix:** Either:
- (a) Create a new `wpick set <path>` command with the matugen flags
- (b) Add matugen flags to `pick`, `next`, `prev`, and `restore` individually
- (c) Make the flags global (on `@app.callback()`) so they apply to all commands

Option (c) is cleanest — add the flags to the callback so every wallpaper-setting command gets them.

### B2. Shallow config merge destroys nested sections

`config.py` line 57: `raw.update(user_raw)` — this is a **shallow** dict merge.

If a user's `~/.config/wpick/config.toml` has:
```toml
[matugen]
scheme = "scheme-vibrant"
```

Then `user_raw` = `{"matugen": {"scheme": "scheme-vibrant"}}` and `raw.update(user_raw)` **replaces** the entire `matugen` dict. The defaults `enabled = true` and `extra_flags = []` are lost.

With the new 7 fields, this gets worse. A user setting just `scheme` loses ALL other matugen defaults.

**Fix:** Implement a recursive/deep merge utility:
```python
def _deep_merge(base: dict, override: dict) -> dict:
    result = base.copy()
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result
```

This is a **pre-existing bug** that becomes a **data loss bug** with the new fields. Must fix in Task 1 or before.

### B3. No CLI flags for lightness_dark and lightness_light

Task 1 adds `lightness_dark` and `lightness_light` to the model. Task 4 adds CLI flags for scheme, mode, prefer, contrast, and source_index — but **NOT** for lightness_dark and lightness_light.

Users can only set these via config file, not via CLI. This is inconsistent — every other matugen option gets a CLI flag.

**Fix:** Add `--matugen-lightness-dark` and `--matugen-lightness-light` to Task 4.

### B4. `enabled = false` is never checked

The `MatugenConfig` model has `enabled: bool = True`, but `set_wallpaper()` in `orchestrator.py` **always** calls matugen. The plan's Task 3 doesn't add an `if cfg.matugen.enabled:` guard.

**Fix:** Add to `_build_matugen_cmd` or `set_wallpaper`:
```python
if not cfg.matugen.enabled:
    return  # skip matugen entirely
```

### B5. `extra_flags` can conflict with structured fields

If a user has `extra_flags = ["--type", "scheme-vibrant"]` AND `scheme = "scheme-tonal-spot"`, the generated command will be:
```
matugen image path --type scheme-tonal-spot ... --type scheme-vibrant
```

Two `--type` flags. Matugen's behavior with duplicate flags is undefined (likely last-wins, but untested).

**Fix:** Either:
- (a) Filter `extra_flags` to exclude keys that conflict with structured fields
- (b) Log a warning if `extra_flags` contains known flags
- (c) Document that `extra_flags` should not overlap with structured fields

Option (b) is pragmatic.

### B6. `prefer = "closest-to-fallback"` requires `--fallback-color` but it's not exposed

The research shows `closest-to-fallback` is a valid `--prefer` value. But it **requires** `--fallback-color <hex>` to work. The plan's validator allows `closest-to-fallback` as a prefer value but provides no way to set `--fallback-color`.

If a user sets `prefer = "closest-to-fallback"` without a fallback color, matugen will either error or behave unexpectedly.

**Fix:** Either:
- (a) Remove `closest-to-fallback` from allowed values (simplest)
- (b) Add a `fallback_color: str | None = None` field with a cross-validator that requires it when prefer is `closest-to-fallback`

### B7. No timeout on matugen subprocess

`orchestrator.py` line 84-88: `subprocess.run(...)` has no `timeout=` parameter. The plan fixes the interactive prompt bug (via `--prefer`), but if matugen hangs for ANY other reason (broken image, filesystem issue, GPU driver crash), the daemon hangs forever.

**Fix:** Add `timeout=30` (or configurable) to the matugen subprocess call. Catch `subprocess.TimeoutExpired` and log a warning.

---

## SIGNIFICANT GAPS

### S1. source_color_index may fail for single-color images

The research notes: "Some images only yield 1 color; complex images yield up to 4." If a user sets `source_color_index = 3` and the image only has 1 dominant color, matugen will likely error.

The plan validates the range (0-3) but doesn't handle the runtime case where the image doesn't have enough colors.

**Fix:** Either catch the matugen error gracefully (already partially handled since failures log warnings) or document this limitation.

### S2. No validation of prefer + source_color_index interaction

When both `prefer` and `source_color_index` are set, both flags are passed to matugen. What does matugen do? The research doesn't test this interaction. Likely:
- `--source-color-index` picks which of the 4 extracted colors to use
- `--prefer` picks which color to select when there are candidates
- Both together: undefined/conflicting behavior?

**Fix:** Test this interaction. If conflicting, add a cross-validator that raises if both are set (or document which takes precedence).

### S3. lightness_dark and lightness_light have no range validators

The research shows:
- `lightness-dark`: range `-∞ to 1`
- `lightness-light`: range `-1 to +∞`

But the plan doesn't add `Field(...)` constraints. Only `float | None = None` — no `le=1.0` on lightness_dark, no `ge=-1.0` on lightness_light.

**Fix:**
```python
lightness_dark: float | None = Field(default=None, le=1.0)
lightness_light: float | None = Field(default=None, ge=-1.0)
```

### S4. Config default TOML not updated

Task 1 adds 7 new fields to `MatugenConfig`, but `config.default.toml` still only has:
```toml
[matugen]
enabled = true
extra_flags = []
```

New users won't see the new options. The TOML file is the primary documentation for the config schema.

**Fix:** Add to Task 8 (docs) or Task 1: update `config.default.toml` with all new fields and comments.

### S5. No test for the full CLI → config → orchestrator flow

Tasks 5-7 test the model, cmd builder, and orchestrator in isolation. But there's no test for:
1. User sets `--matugen-scheme scheme-vibrant` on CLI
2. That flows through to the config
3. `_build_matugen_cmd` produces the right command
4. `set_wallpaper` calls it correctly

The CLI flags (Task 4) are only added to a non-existent `set` command, so there's no integration path to test.

**Fix:** After fixing B1, add an integration test that exercises the full path.

### S6. Existing tests will break

`test_orchestrator.py` line 34: `test_calls_swww_and_matugen` mocks `subprocess.run` and asserts `call_count == 2`. After the refactor, `set_wallpaper` will call `_build_matugen_cmd` first, then `subprocess.run`. The mock count is still 2, so this test should pass — BUT the second call's arguments will change from `["matugen", "image", str(path)]` to include `--type`, `--mode`, `--prefer` flags. If any assertion checks the exact args, it will fail.

The test only checks `call_count` and that `"swww"` is in the first call, so it should survive. But `test_swww_failure_raises` might be affected if the error path changes.

**Fix:** Review and update existing tests in Task 3.

---

## MINOR CONCERNS

### M1. Typo in _cycle_wallpaper (pre-existing)

`cli.py` lines 226-230: The `target = ...` assignment is inside the `except StopIteration` block due to indentation. It should be at the same level as the `try/except`. This means `next`/`prev` only work when the current wallpaper is NOT in the database (StopIteration case). This is a pre-existing bug, not introduced by the plan, but worth noting.

### M2. No check that matugen is installed

If matugen is not installed, `subprocess.run(["matugen", ...])` raises `FileNotFoundError`. The plan doesn't add a preflight check. The current code doesn't have one either, so this is pre-existing — but with more complex flag building, a clear error message would help.

**Suggestion:** Add a `_check_matugen_available()` function or catch `FileNotFoundError` in `set_wallpaper`.

### M3. Contrast=0.0 is silently omitted

The plan omits `--contrast` when `cfg.contrast != 0.0`. This means users can't explicitly set contrast to 0.0 via CLI (it's the same as not setting it). This is fine functionally, but could confuse users who want to be explicit.

### M4. No `from __future__ import annotations` in code snippets

The codebase consistently uses `from __future__ import annotations`. The plan's code snippets don't include it. Minor style inconsistency.

### M5. Float serialization edge case

TOML stores floats as IEEE 754. A user writing `contrast = 0.1` in TOML gets `0.1` exactly in Python. But `contrast = 0.3` might serialize slightly differently. Not a real problem in practice, but worth noting for the `contrast != 0.0` check.

---

## TASK DECOMPOSITION ISSUES

### D1. Task dependencies are correct but incomplete

The execution order is:
1. Task 1 (model) → Task 5 (model tests)
2. Task 2 (cmd builder) → Task 6 (cmd tests)
3. Task 3 (wire set_wallpaper) → Task 7 (orchestrator tests)
4. Task 4 (CLI flags)
5. Task 8 (docs)

Missing dependency: Task 4 depends on fixing B1 (the `set` command doesn't exist). Without a `set` command, Task 4 can't be implemented.

Also: Task 2 depends on Task 1 (needs `MatugenConfig` with new fields). This is implicit but should be explicit.

### D2. Effort estimates are optimistic

- Task 1: 15 min — reasonable
- Task 2: 20 min — reasonable
- Task 3: 10 min — reasonable
- Task 4: 20 min — **underestimated** if we need to create a new `set` command or refactor to global flags
- Task 5: 20 min — reasonable
- Task 6: 20 min — reasonable
- Task 7: 15 min — reasonable
- Task 8: 10 min — reasonable

Total should be ~3 hours with the fixes, not ~2 hours.

### D3. No task for fixing the shallow merge (B2)

The deep merge fix is a prerequisite for the new fields to work correctly with user config overrides. It should be Task 0 or part of Task 1.

---

## TEST COVERAGE GAPS

### T1. Missing test cases

The plan's test cases are:
- Task 5: Default values, valid/invalid scheme, mode, prefer, source_color_index, contrast range
- Task 6: Default cmd, all flags, optional flags omitted, contrast=0.0 omitted, extra_flags
- Task 7: set_wallpaper calls matugen, matugen failure doesn't raise

**Missing:**
- `enabled = false` skips matugen entirely
- `extra_flags` conflicting with structured fields
- `prefer = "closest-to-fallback"` without fallback_color
- `lightness_dark > 1.0` raises validation error
- `lightness_light < -1.0` raises validation error
- Config roundtrip: TOML → model → dict → model preserves values
- Deep merge preserves nested defaults
- CLI flag override takes precedence over config file
- Matugen subprocess timeout

### T2. No property-based testing

The validators have clear mathematical constraints (ranges, enums). Property-based testing with Hypothesis would catch edge cases:
```python
@given(st.floats(min_value=-1.0, max_value=1.0))
def test_contrast_range(v):
    cfg = MatugenConfig(contrast=v)
    assert cfg.contrast == v
```

Not strictly necessary but would catch float edge cases (NaN, inf).

---

## ARCHITECTURAL CONCERNS

### A1. The plan doesn't address the config merge architecture

The shallow merge in `config.py` is a systemic issue. The new matugen fields make it more visible, but the same problem exists for `[swww]`, `[paths]`, `[extraction]`, and `[watch]` sections. A user overriding any nested section loses all defaults in that section.

**Recommendation:** Fix the merge architecture as a prerequisite, not as part of this feature.

### A2. CLI flag proliferation

Adding 7 `--matugen-*` flags to the CLI is a lot. The naming convention (`--matugen-scheme`, `--matugen-mode`, etc.) is verbose. Alternatives:
- Use a single `--matugen-args` flag that accepts a string: `--matugen-args "--scheme scheme-vibrant --mode light"`
- Use subcommands: `wpick set --matugen.scheme scheme-vibrant`
- Use environment variables: `WPICK_MATUGEN_SCHEME=scheme-vibrant`

The current approach is fine for now but may not scale.

### A3. No validation that matugen version supports the flags

Different matugen versions may support different flags. If a user has an old matugen without `--contrast`, the command will fail. The plan doesn't check matugen version.

**Suggestion:** Document minimum matugen version requirement.

---

## SUMMARY OF REQUIRED FIXES

| Priority | Issue | Fix |
|----------|-------|-----|
| BLOCKING | B1: No `set` command | Create `wpick set <path>` or make flags global |
| BLOCKING | B2: Shallow merge | Implement deep merge in config.py |
| BLOCKING | B3: No lightness CLI flags | Add `--matugen-lightness-dark/light` |
| BLOCKING | B4: `enabled` flag ignored | Add guard in set_wallpaper |
| BLOCKING | B5: extra_flags conflict | Warn or filter conflicting flags |
| BLOCKING | B6: closest-to-fallback | Remove from allowed values or add fallback_color field |
| BLOCKING | B7: No subprocess timeout | Add timeout=30 to matugen call |
| SIGNIFICANT | S1: source_color_index + single-color images | Document or catch gracefully |
| SIGNIFICANT | S2: prefer + source_color_index interaction | Test and document |
| SIGNIFICANT | S3: No lightness range validators | Add Field constraints |
| SIGNIFICANT | S4: config.default.toml not updated | Update with new fields |
| SIGNIFICANT | S5: No integration test | Add full CLI→config→orchestrator test |
| SIGNIFICANT | S6: Existing tests may break | Review and update |

**Total estimated effort with fixes: ~3.5 hours** (up from ~2 hours).
