---
tags:
  - project
  - wpick
  - cli
parent: "[[wpick]]"
created: 2026-05-23
---

# wpick — CLI

## Entry Points

```python
"""CLI entry points via Typer."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

app = typer.Typer(name="wpick", help="Wallpaper clustering and smart picker.")


@app.command()
def init():
    """Initialize database schema and cache directories."""
    from wpick import db, config
    db.init_schema()
    cfg = config.get()
    for key in ("cache", "storage"):
        Path(cfg["paths"][key]).mkdir(parents=True, exist_ok=True)
    typer.echo("✓ wpick initialized")


@app.command()
def scan(
    force: bool = typer.Option(False, "--force", help="Re-extract already-extracted images"),
    quiet: bool = typer.Option(False, "--quiet", "-q"),
):
    """Scan wallpaper directory and extract features from all images."""
    from wpick import config
    from wpick.extractor import scan_and_extract

    cfg = config.get()
    root = Path(cfg["paths"]["wallpapers"])

    if not root.exists():
        typer.echo(f"Error: wallpapers directory not found: {root}", err=True)
        raise typer.Exit(1)

    def progress(current, total, path):
        if not quiet:
            typer.echo(f"\r[{current}/{total}] {path.name}", nl=False)

    total, extracted, errors = scan_and_extract(root, force=force, on_progress=progress)
    if not quiet:
        typer.echo()
    typer.echo(f"Scan complete: {extracted}/{total} extracted, {errors} errors")


@app.command()
def cluster():
    """Run HDBSCAN clustering on extracted features."""
    from wpick.clusterer import run_clustering, ClusteringError

    try:
        summary = run_clustering()
    except ClusteringError as e:
        typer.echo(f"Clustering failed: {e}", err=True)
        raise typer.Exit(1)

    typer.echo(
        f"✓ {summary['clusters']} clusters  |  "
        f"{summary['noise_images']} noise → misc  |  "
        f"run: {summary['run_id']}"
    )


@app.command()
def assign(
    path: Optional[Path] = typer.Argument(None, help="Specific image to assign"),
):
    """Assign new image(s) to existing clusters without reclustering."""
    from wpick import config
    from wpick.assigner import assign_image, assign_all_unassigned

    cfg = config.get()
    root = Path(cfg["paths"]["wallpapers"])

    if path:
        result = assign_image(path, root)
        if result:
            typer.echo(f"Assigned {path.name} → {result}")
        else:
            typer.echo(f"Could not assign {path.name}")
    else:
        assigned, failed = assign_all_unassigned(root)
        typer.echo(f"Assigned: {assigned}, failed: {failed}")


@app.command()
def pick():
    """Launch rofi wallpaper picker."""
    from wpick.picker import launch_picker
    launch_picker()


@app.command()
def next():
    """Cycle to next wallpaper in current cluster."""
    from wpick.orchestrator import cycle_wallpaper
    cycle_wallpaper("next")


@app.command()
def prev():
    """Cycle to previous wallpaper in current cluster."""
    from wpick.orchestrator import cycle_wallpaper
    cycle_wallpaper("prev")


@app.command()
def watch():
    """Start filesystem watcher daemon."""
    from wpick.orchestrator import start_watcher, WallpaperError
    try:
        start_watcher()
    except WallpaperError as e:
        typer.echo(f"Watcher error: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def restore():
    """Re-apply the most recently set wallpaper."""
    from wpick import db
    from wpick.orchestrator import set_wallpaper, WallpaperError
    with db.connection() as conn:
        row = conn.execute("""
            SELECT i.path FROM history h
            JOIN images i ON h.image_id = i.id
            ORDER BY h.set_at DESC LIMIT 1
        """).fetchone()
    if not row:
        typer.echo("No wallpaper history found.")
        return
    try:
        set_wallpaper(Path(row["path"]), log=False)
    except WallpaperError as e:
        typer.echo(f"Restore failed: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def stats():
    """Show cluster statistics."""
    from wpick import db
    with db.connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM images").fetchone()[0]
        extracted = conn.execute(
            "SELECT COUNT(*) FROM images WHERE extracted_at IS NOT NULL"
        ).fetchone()[0]
        clusters = conn.execute(
            "SELECT id, name, member_count FROM clusters ORDER BY member_count DESC"
        ).fetchall()

    typer.echo(f"Images: {total} total, {extracted} extracted")
    typer.echo(f"Clusters: {len(clusters)}")
    typer.echo()
    for c in clusters:
        bar = "█" * min(40, c["member_count"] // 2)
        name = c["name"] or c["id"]
        typer.echo(f"  {name:20s}  {c['member_count']:4d}  {bar}")


if __name__ == "__main__":
    app()
```

## Commands Summary

| Command | Description |
|---|---|
| `wpick init` | Initialize DB and directories |
| `wpick scan` | Scan wallpapers, extract features |
| `wpick scan --force` | Re-extract all images |
| `wpick cluster` | Run HDBSCAN clustering |
| `wpick assign` | Assign all unassigned images |
| `wpick assign <path>` | Assign specific image |
| `wpick pick` | Launch rofi picker |
| `wpick next` | Next wallpaper in cluster |
| `wpick prev` | Previous wallpaper in cluster |
| `wpick watch` | Start filesystem watcher |
| `wpick restore` | Restore last wallpaper |
| `wpick stats` | Show cluster statistics |

## See Also

- [[10-Deployment]] — Keybinds and systemd setup
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/07-Picker]] — rofi UI details
