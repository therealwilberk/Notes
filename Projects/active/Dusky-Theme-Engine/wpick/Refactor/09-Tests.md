---
type: project
tags: [project, wpick]
created: 2026-05-24
status: in-progress
---

# 09 — Tests

## Current State
- Test files exist for every module: `test_assigner.py`, `test_clusterer.py`, `test_db.py`, `test_extractor.py`, `test_oklab.py`, `test_picker.py`, `test_orchestrator.py`, `test_cli.py`, `test_config.py`, `test_integration.py`, `test_pure.py`, `test_infra.py`
- `conftest.py` and `fixtures/` directory exist
- Unknown: what's actually in these files — they may be stubs, incomplete, or testing old interfaces

**Assumption:** treat all test files as needing review and likely rewrite against the new module interfaces defined in subdocs 02–08.

---

## Test surfaces

Three distinct surfaces — each needs a different strategy:

| Surface     | What                                                                 | Tools                            |
| ----------- | -------------------------------------------------------------------- | -------------------------------- |
| Pure logic  | Oklab math, cosine similarity, cluster naming, centroid computation  | pytest, no fixtures              |
| Integration | DB operations, pipeline stage I/O against real SQLite                | pytest, tmp_path fixture         |
| Contract    | auto-palette output parser, rofi entry format, swww/matugen CLI args | pytest, captured subprocess mock |

---

## Tasks

### Task 1 — `conftest.py` fixtures

Define these shared fixtures. All other test files import from here — no fixture duplication:

```python
@pytest.fixture
def jpeg_factory(tmp_path: Path):
    """Generate test JPEG images programmatically. No binary fixtures committed."""
    def _make(name: str, color: tuple[int, int, int] = (128, 64, 32), size: tuple[int, int] = (10, 10)) -> Path:
        p = tmp_path / name
        Image.new("RGB", size, color).save(p, "JPEG")
        return p
    return _make

@pytest.fixture
def tmp_db(tmp_path: Path) -> WallpaperDB:
    """Fresh in-memory WallpaperDB with schema applied."""
    db_path = tmp_path / "test.db"
    db = WallpaperDB(db_path)
    db.connect()
    init_schema(db_path)
    yield db
    db.close()

@pytest.fixture
def sample_feature() -> FeatureRow:
    """Deterministic FeatureRow for use across tests."""
    return FeatureRow(
        image_id="abc123",
        path="/tmp/test.jpg",
        oklab_vector=[0.5, 0.1, -0.1, 0.3, 0.2, 0.0],
        color_count=2,
        extracted_at="2024-01-01T00:00:00",
    )

@pytest.fixture
def sample_cluster() -> ClusterRow:
    return ClusterRow(
        cluster_id=0,
        label="dark-warm",
        centroid=[0.5, 0.1, -0.1],
        member_count=5,
        run_id="run-001",
    )

@pytest.fixture
def mock_auto_palette(monkeypatch: pytest.MonkeyPatch) -> None:
    """Patch subprocess.run to return a valid auto-palette JSON response."""
    fake_output = json.dumps([
        {"L": 0.5, "a": 0.1, "b": -0.1},
        {"L": 0.3, "a": 0.2, "b": 0.0},
    ])
    monkeypatch.setattr(
        "wpick.extractor.subprocess.run",
        lambda *a, **kw: SimpleNamespace(returncode=0, stdout=fake_output, stderr=""),
    )
```

### Task 2 — `test_pure.py` and `test_oklab.py`

Pure math — no DB, no filesystem, no subprocess. These must run in under 100ms total.

**`test_oklab.py`:**
- `test_rgb_to_oklab_known_values` — verify against pre-computed reference values for black, white, red, green, blue
- `test_oklab_roundtrip` — convert RGB → Oklab → RGB, assert within float tolerance
- `test_zero_saturation_handled` — pure grey input does not raise

**`test_pure.py`:**
- `test_cosine_similarity_identical` — same vector returns 1.0
- `test_cosine_similarity_orthogonal` — orthogonal vectors return 0.0
- `test_cosine_similarity_zero_vector` — returns 0.0, does not raise
- `test_cluster_naming_dark_warm` — centroid with low L, positive a → label contains "dark"
- `test_cluster_naming_light_cool` — high L, negative a → label contains "light"
- `test_cluster_naming_misc` — cluster_id -1 always returns "misc" regardless of centroid

### Task 3 — `test_db.py`

All tests use `tmp_db` fixture. Test every public `WallpaperDB` method:

- `test_upsert_image_idempotent` — insert same image twice, assert one row
- `test_upsert_features_updates_existing` — insert features twice with different vector, assert latest wins
- `test_get_unextracted_images` — insert images with and without features, assert correct subset returned
- `test_get_unassigned_images` — insert images with and without cluster assignment, assert correct subset
- `test_log_history_and_retrieve` — log 3 entries, assert `get_latest_history(1)` returns most recent
- `test_transaction_rollback` — force a SQL error mid-transaction, assert DB state unchanged and `DatabaseError` raised
- `test_schema_version_applied` — after `init_schema`, assert `schema_migrations` has correct version row
- `test_get_stats_empty_db` — `get_stats()` on empty DB returns zeros, does not raise

### Task 4 — `test_extractor.py`

Uses `mock_auto_palette` fixture and `tmp_db`:

- `test_scan_and_extract_happy_path` — create 3 real small JPEG fixtures in `tmp_path`, run `scan_and_extract`, assert 3 features in DB
- `test_scan_skips_extracted_on_no_force` — pre-insert feature for one image, assert `scan_and_extract` skips it, `result.skipped == 1`
- `test_scan_force_reextracts` — same setup, `force=True`, assert all 3 extracted
- `test_scan_continues_on_single_failure` — patch `_run_auto_palette` to raise `ExtractorError` for one image, assert scan completes, `result.errors == 1`
- `test_check_auto_palette_missing` — monkeypatch `shutil.which` to return `None`, assert `ExtractorError` raised
- `test_parse_bad_output_raises` — feed malformed JSON to `_parse_palette_output`, assert `ExtractorError`

Small JPEG fixtures: generate programmatically in conftest using Pillow — 10×10 solid colour images. Do not commit binary fixtures.

### Task 5 — `test_clusterer.py`

Uses `tmp_db` and pre-inserted feature rows:

- `test_run_clustering_produces_clusters` — insert 20 features with varied vectors, run clustering, assert clusters in DB
- `test_all_images_assigned` — assert every image has a cluster_id after clustering (no noise/unsassigned)
- `test_run_clustering_insufficient_data_raises` — fewer features than `cluster_count * 2`, assert `ClusteringError`
- `test_cluster_run_recorded` — after clustering, assert one `cluster_runs` row with correct `image_count`
- `test_images_since_last_cluster` — insert features after clustering, assert count is correct

### Task 6 — `test_assigner.py`

- `test_assign_image_selects_nearest` — insert 2 clusters with known centroids, insert feature closer to cluster 0, assert assigned to 0
- `test_assign_image_no_features_raises` — call `assign_image` with image_id that has no features, assert `AssignerError`
- `test_assign_image_no_clusters_raises` — call with no clusters in DB, assert `AssignerError`
- `test_assign_all_unassigned_batch` — insert 5 unassigned images, run batch, assert `batch.assigned == 5`
- `test_assign_all_continues_on_failure` — one image has no features, assert `batch.failed == 1`, others assigned

### Task 7 — `test_orchestrator.py`

All subprocess calls monkeypatched — never invoke real swww or matugen:

- `test_set_wallpaper_calls_swww` — assert swww called with correct args for given config
- `test_set_wallpaper_skips_matugen_when_disabled` — `config.matugen.enabled = False`, assert matugen not called
- `test_set_wallpaper_missing_file_raises` — path does not exist, assert `WallpaperError` before subprocess
- `test_set_wallpaper_swww_failure_raises` — subprocess returns nonzero, assert `WallpaperError`
- `test_check_swww_missing` — `shutil.which` returns None, assert `WallpaperError`
- `test_pid_file_prevents_second_instance` — write PID file with current PID, call `_write_pid`, assert `WallpaperError`
- `test_stale_pid_file_overwritten` — write PID file with dead PID, call `_write_pid`, assert no error

### Task 8 — `test_picker.py`

- `test_generate_thumbnail_creates_file` — real 10×10 JPEG in tmp_path, assert thumb file created
- `test_generate_thumbnail_cache_hit` — call twice, assert `was_generated=False` on second call
- `test_generate_thumbnail_stale_cache` — set thumb mtime older than source, assert regenerated
- `test_build_rofi_entries_groups_by_cluster` — assert entries sorted cluster-first then filename
- `test_build_rofi_entries_excludes_no_thumb` — image with no thumbnail excluded from entries
- `test_launch_rofi_cancellation_returns_none` — mock subprocess exit code 1, assert returns `None`
- `test_launch_rofi_failure_raises` — mock exit code 2, assert `PickerError`

### Task 9 — `test_integration.py`

Full pipeline end-to-end using real SQLite and mocked external binaries. One test class:

```python
class TestFullPipeline:
    def test_scan_cluster_assign_pick(self, tmp_path, monkeypatch): ...
```

Steps: generate 20 small JPEG fixtures → `scan_and_extract` → `run_clustering` → `assign_all_unassigned` → assert DB state is consistent (all images assigned, cluster centroids present, history empty). Do not invoke rofi — stop before picker.

This test is the integration smoke test. It must pass before any release.

### Task 10 — Coverage gate

`pyproject.toml` already sets `fail_under = 70`. After all tests are written, run:

```bash
pytest --cov=wpick --cov-report=term-missing
```

Modules that must individually hit 80%+: `db.py`, `extractor.py`, `clusterer.py`, `assigner.py`. If any fall short, add targeted tests — do not lower the threshold.

---

## Constraints
- No test commits binary image fixtures — generate programmatically with Pillow
- No test invokes real swww, matugen, auto-palette, or rofi — all subprocess calls monkeypatched
- `tmp_db` fixture is the only way tests access SQLite — no hardcoded paths
- Tests must pass with `pytest -x` (stop on first failure) — no order dependencies
- basedpyright must pass on `tests/` directory — test functions are typed too
