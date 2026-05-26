---
type: project
tags: [project, wpick]
created: 2026-05-24
status: in-progress
---

# 03 — Extraction

## Current State
- `extractor.py` calls `auto-palette` (Rust binary) via subprocess
- Output written to `features.jsonl` — this is currently read back as canonical state (wrong)
- `oklab.py` handles color space conversion
- No validation that `auto-palette` binary exists before pipeline starts
- Subprocess failures likely uncaught or raising raw `subprocess.SubprocessError`
- Feature data shape is not formally typed

---

## Target
- `scan_and_extract` returns `list[FeatureRow]` and writes directly to DB via `WallpaperDB`
- `features.jsonl` may still be written as a debug artifact but is never read back
- `auto-palette` binary absence raises `ExtractorError` at startup, not mid-scan
- All subprocess calls wrapped with timeout and typed error handling

---

## Tasks

### Task 1 — Define extraction types in `models.py`

Add if not already present:

```python
@dataclass
class OklabColor:
    L: float
    a: float
    b: float

@dataclass
class FeatureRow:
    image_id: str        # SHA-256 of absolute path, hex string
    path: str            # absolute path as string
    oklab_vector: list[float]   # flattened: [L0,a0,b0, L1,a1,b1, ...]
    color_count: int
    extracted_at: str    # ISO 8601
```

`oklab_vector` is the canonical feature representation. Max length = `max_colors * 3`.

### Task 2 — Validate binary at startup

In `extractor.py`, add:

```python
def check_auto_palette_available() -> None:
    """Raise ExtractorError if auto-palette binary is not on PATH."""
    ...
```

Use `shutil.which("auto-palette")`. Raise `ExtractorError` with a clear message including install instructions if not found.

Call this from `scan_and_extract` before processing any images. Do not call it on every image — once per scan run.

### Task 3 — Harden `auto-palette` subprocess call

Current pattern is likely `subprocess.run(...)` with no timeout or structured error handling. Replace with:

```python
def _run_auto_palette(image_path: Path, max_colors: int) -> list[OklabColor]:
    """
    Invoke auto-palette and return parsed Oklab colors.
    Raises ExtractorError on binary failure, timeout, or bad output.
    """
    result = subprocess.run(
        ["auto-palette", "--format", "json", "--colors", str(max_colors), str(image_path)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise ExtractorError(
            f"auto-palette failed on {image_path.name}: {result.stderr.strip()}"
        )
    return _parse_palette_output(result.stdout)
```

`_parse_palette_output` does the JSON parse + validation. If the output shape is unexpected, raise `ExtractorError`, not `ValueError` or `KeyError`.

Timeout: 30s per image is generous. Adjust based on observed runtime but always set one.

### Task 4 — `oklab.py` type annotations

`oklab.py` handles RGB → Oklab conversion. Audit and ensure:
- All functions have explicit parameter and return type annotations
- No implicit `float | int` confusion — inputs are `float`, outputs are `float`
- `basedpyright` passes with zero errors on this file

No logic changes needed unless there are correctness bugs. Type annotations only.

### Task 5 — Rewrite `scan_and_extract`

Signature:

```python
def scan_and_extract(
    root: Path,
    db: WallpaperDB,
    *,
    force: bool = False,
    on_progress: Callable[[int, int, Path], None] | None = None,
) -> ScanResult:
```

Where:

```python
@dataclass
class ScanResult:
    total: int
    extracted: int
    skipped: int
    errors: int
```

Logic:
1. Walk `root` recursively, filter by `config.extensions`
2. For each image: compute `image_id` (SHA-256 of absolute path)
3. If `force=False` and `db.get_features(image_id)` returns a result → skip
4. Call `_run_auto_palette`, convert to `FeatureRow`, call `db.upsert_features(...)`
5. On `ExtractorError`: log `WARNING`, increment `errors`, continue — do not abort scan
6. Call `on_progress` after each image if provided

`features.jsonl` write is optional — controlled by a debug flag in config, off by default.

### Task 6 — Remove `features.jsonl` as input

Audit the entire codebase:
```bash
grep -r "features.jsonl\|jsonl" src/wpick/ --include="*.py"
```

Any read of `features.jsonl` is a violation. The file may be written (debug only) but must never be read as a pipeline input. Remove all read paths.

---

## Constraints
- `auto-palette` is an external binary — always validate presence before use
- Subprocess calls always have `timeout` set — no hanging scans
- `ExtractorError(WpickError)` is the only exception that escapes `extractor.py`
- `oklab.py` must pass basedpyright with zero errors after annotation pass
- `scan_and_extract` must accept a `WallpaperDB` instance — no internal config loading inside extractor
