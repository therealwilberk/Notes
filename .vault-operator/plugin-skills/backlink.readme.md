# Backlinks

View and navigate backlinks between notes

## Overview

Backlinks is an Obsidian core plugin. It is built into Obsidian and does not require separate installation.

## Commands

- `backlink:open` -- Open backlinks pane
- `backlink:open-backlinks` -- Open backlinks for current note
- `backlink:toggle-backlinks-in-document` -- Toggle backlinks in document

## Configuration

Settings are stored at `.obsidian/backlink.json`.

To read: `read_file(".obsidian/backlink.json")`
To write: `write_file(".obsidian/backlink.json", updatedJSON)`

## Usage Notes

Plugin "Backlinks" shows which notes link to the current note.

Available commands:
- backlink:open -- Open the backlinks pane in the sidebar
- backlink:open-backlinks -- Open backlinks for the current note
- backlink:toggle-backlinks-in-document -- Toggle inline backlinks at the bottom of the note

Use this skill when the user asks about connections between notes, what links to a specific note, or wants to see the backlink panel. For programmatic backlink analysis, prefer the get_linked_notes tool.