# Open with Default App

Open files in the system default app or file manager

## Overview

Open with Default App is an Obsidian core plugin. It is built into Obsidian and does not require separate installation.

## Commands

- `open-with-default-app:open` -- Open in default app
- `open-with-default-app:show` -- Show in system explorer

## Configuration

Settings are stored at `.obsidian/open-with-default-app.json`.

To read: `read_file(".obsidian/open-with-default-app.json")`
To write: `write_file(".obsidian/open-with-default-app.json", updatedJSON)`

## Usage Notes

Plugin "Open with Default App" opens files outside Obsidian.

Available commands:
- open-with-default-app:open -- Open the active file with the system's default app (e.g., Preview for PDF, browser for HTML)
- open-with-default-app:show -- Reveal the active file in Finder/Explorer

Use this when the user wants to view a file in an external application or locate it in the file system.