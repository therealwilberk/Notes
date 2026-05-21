# File Explorer

File explorer: create, move, and reveal files

## Overview

File Explorer is an Obsidian core plugin. It is built into Obsidian and does not require separate installation.

## Commands

- `file-explorer:new-file` -- Create new note
- `file-explorer:move-file` -- Move file to another folder
- `file-explorer:reveal-active-file` -- Reveal active file in navigation

## Configuration

Settings are stored at `.obsidian/file-explorer.json`.

To read: `read_file(".obsidian/file-explorer.json")`
To write: `write_file(".obsidian/file-explorer.json", updatedJSON)`

## Usage Notes

Plugin "File Explorer" provides file management commands.

Available commands:
- file-explorer:new-file -- Create a new note (opens an untitled note in the editor)
- file-explorer:move-file -- Move the active file to a different folder (opens folder picker)
- file-explorer:reveal-active-file -- Scroll the file explorer to reveal and highlight the active file

Note: For programmatic file creation, prefer write_file. For moving files, prefer the move_file tool. Use file-explorer commands when the user wants the native UI interaction.