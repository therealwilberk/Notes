---
tags:
  - project
  - wpick
  - deployment
  - systemd
parent: "[[wpick]]"
created: 2026-05-23
---

# wpick — Deployment

## First-time Setup

```bash
cd ~/.config/wpick

# 1. Install deps
uv sync

# 2. Install CLI globally
uv tool install .

# 3. Init DB and directories
wpick init

# 4. Set wallpaper path in config
cp config.default.toml config.toml
$EDITOR config.toml   # set paths.wallpapers

# 5. First scan (may take several minutes for 1500 images)
wpick scan

# 6. Cluster
wpick cluster

# 7. Check results
wpick stats

# 8. Test the picker
wpick pick

# 9. Enable watcher service
systemctl --user enable --now wpick-watch.service
```

## systemd User Service

```ini
[Unit]
Description=wpick wallpaper watcher
After=graphical-session.target
PartOf=graphical-session.target

[Service]
Type=simple
ExecStart=%h/.local/bin/wpick watch
Restart=on-failure
RestartSec=5
Environment=HOME=%h
Environment=XDG_RUNTIME_DIR=/run/user/%U

StandardOutput=journal
StandardError=journal
SyslogIdentifier=wpick

[Install]
WantedBy=graphical-session.target
```

## Install Service

```bash
mkdir -p ~/.config/systemd/user/
cp ~/.config/wpick/systemd/wpick-watch.service ~/.config/systemd/user/

systemctl --user daemon-reload
systemctl --user enable --now wpick-watch.service
systemctl --user status wpick-watch.service
journalctl --user -u wpick-watch.service -f
```

## Hyprland Keybinds

```ini
# ~/.config/hypr/hyprland.conf

# Wallpaper picker
bind = $mainMod, W, exec, wpick pick

# Cycle wallpapers in current cluster
bind = $mainMod SHIFT, W, exec, wpick next
bind = $mainMod CTRL, W, exec, wpick prev

# Restore wallpaper on login
exec-once = swww-daemon
exec-once = wpick restore
```

## When to Recluster

```bash
# After bulk wallpaper import
wpick scan && wpick cluster

# Cluster quality degraded (misc > 20%)
wpick stats
wpick cluster

# After tuning min_cluster_size
wpick cluster
```

## Pre-sharing Checklist

- [ ] `features.jsonl` and `storage/` in `.gitignore`
- [ ] `config.toml` in `.gitignore`; only `config.default.toml` committed
- [ ] `uv.lock` committed
- [ ] `wpick --help` reads cleanly
- [ ] All tests pass: `uv run pytest`
- [ ] No hardcoded paths in source
- [ ] `README.md` covers: install, first-time setup, keybind
- [ ] `schema.sql` committed
- [ ] Tested on fresh venv: `uv sync --frozen && wpick init`

## See Also

- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/08-CLI]] — Available commands
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/06-Orchestrator]] — Watcher and matugen integration
- [[Projects/active/Dusky-Theme-Engine/wpick/Refactor/07-Picker]] — rofi UI setup
