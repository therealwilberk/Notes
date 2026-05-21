# Note Composer

Split, merge, and extract content between notes

## Overview

Note Composer is an Obsidian core plugin. It is built into Obsidian and does not require separate installation.

## Commands

- `note-composer:merge-file` -- Merge current file with another file
- `note-composer:split-file` -- Extract selection to new note
- `note-composer:extract-heading` -- Extract heading to new note

## Configuration

Settings are stored at `.obsidian/note-composer.json`.

To read: `read_file(".obsidian/note-composer.json")`
To write: `write_file(".obsidian/note-composer.json", updatedJSON)`

## Usage Notes

Plugin "Note Composer" restructures content across notes.

Available commands:
- note-composer:merge-file -- Merge the current note with another note
- note-composer:split-file -- Extract the selected text into a new note
- note-composer:extract-heading -- Extract a heading and its content into a new note

Use this skill when the user wants to reorganize notes: splitting long notes, merging related notes, or extracting sections. These commands operate on the currently open note in the editor.