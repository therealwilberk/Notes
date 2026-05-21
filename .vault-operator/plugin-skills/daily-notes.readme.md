# Daily Notes

Create and navigate daily journal notes

## Overview

Daily Notes is an Obsidian core plugin. It is built into Obsidian and does not require separate installation.

## Commands

- `daily-notes:open` -- Open today's daily note
- `daily-notes:goto-next` -- Open next daily note
- `daily-notes:goto-prev` -- Open previous daily note

## Configuration

Settings are stored at `.obsidian/daily-notes.json`.

To read: `read_file(".obsidian/daily-notes.json")`
To write: `write_file(".obsidian/daily-notes.json", updatedJSON)`

## Usage Notes

Plugin "Daily Notes" provides date-based note creation and navigation.

Available commands:
- daily-notes:open -- Open or create today's daily note
- daily-notes:goto-next -- Navigate to the next daily note
- daily-notes:goto-prev -- Navigate to the previous daily note

Use this skill when the user asks about daily notes, journals, today's note, or date-based note navigation. The daily note format and folder are configured in Obsidian settings.