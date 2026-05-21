# App

Core app operations: navigation, delete, reload, sidebars

## Overview

App is an Obsidian core plugin. It is built into Obsidian and does not require separate installation.

## Commands

- `app:delete-file` -- Delete current file
- `app:go-back` -- Navigate back
- `app:go-forward` -- Navigate forward
- `app:reload` -- Reload app
- `app:open-vault` -- Open another vault
- `app:open-settings` -- Open settings
- `app:toggle-left-sidebar` -- Toggle left sidebar
- `app:toggle-right-sidebar` -- Toggle right sidebar

## Configuration

Settings are stored at `.obsidian/app.json`.

To read: `read_file(".obsidian/app.json")`
To write: `write_file(".obsidian/app.json", updatedJSON)`

## Usage Notes

Plugin "App" provides global Obsidian app commands.

Available commands:
- app:delete-file -- Delete the currently active file (moves to trash)
- app:go-back -- Navigate to the previous file in history
- app:go-forward -- Navigate to the next file in history
- app:reload -- Reload the Obsidian app
- app:open-vault -- Open a different vault
- app:open-settings -- Open the Obsidian settings dialog
- app:toggle-left-sidebar -- Show or hide the left sidebar
- app:toggle-right-sidebar -- Show or hide the right sidebar

Note: For programmatic file deletion, prefer the delete_file tool. Use app:delete-file only when the user explicitly wants the native Obsidian delete behavior (trash + UI confirmation).