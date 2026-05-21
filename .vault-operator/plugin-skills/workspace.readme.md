# Workspace

Native workspace operations: PDF export, tab/pane management, file paths

## Overview

Workspace is an Obsidian core plugin. It is built into Obsidian and does not require separate installation.

## Commands

- `workspace:export-pdf` -- Export current note to PDF
- `workspace:close` -- Close current tab
- `workspace:split-horizontal` -- Split horizontally
- `workspace:split-vertical` -- Split vertically
- `workspace:new-tab` -- New tab
- `workspace:copy-path` -- Copy file path
- `workspace:copy-url` -- Copy Obsidian URL
- `workspace:edit-file-title` -- Rename file
- `workspace:toggle-pin` -- Toggle pin

## Configuration

Settings are stored at `.obsidian/workspace.json`.

To read: `read_file(".obsidian/workspace.json")`
To write: `write_file(".obsidian/workspace.json", updatedJSON)`

## Usage Notes

Plugin "Workspace" provides core Obsidian workspace operations.

Available commands:
- workspace:export-pdf -- Export the currently open note to PDF using Obsidian's built-in renderer
- workspace:close -- Close the currently active tab
- workspace:split-horizontal -- Split the current pane horizontally
- workspace:split-vertical -- Split the current pane vertically
- workspace:new-tab -- Open a new empty tab
- workspace:copy-path -- Copy the active file's vault-relative path to clipboard
- workspace:copy-url -- Copy an obsidian:// URL for the active file
- workspace:edit-file-title -- Rename the active file inline
- workspace:toggle-pin -- Pin or unpin the active tab (pinned tabs stay open)

workspace:export-pdf is a native Obsidian command -- zero external dependencies, always available.
It renders the note exactly as Obsidian displays it (theme, CSS, plugins applied).
Note: Opens an export dialog. The user must confirm settings and save location.

Use workspace:export-pdf for quick PDF exports. For advanced conversion (custom LaTeX templates, bibliography, DOCX): use execute_recipe with Pandoc instead.