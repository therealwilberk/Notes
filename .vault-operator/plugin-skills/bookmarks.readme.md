# Bookmarks

Bookmark and organize favorite notes

## Overview

Bookmarks is an Obsidian core plugin. It is built into Obsidian and does not require separate installation.

## Commands

- `bookmarks:bookmark-current-view` -- Bookmark current view
- `bookmarks:unbookmark-current-view` -- Remove current bookmark

## Configuration

Settings are stored at `.obsidian/bookmarks.json`.

To read: `read_file(".obsidian/bookmarks.json")`
To write: `write_file(".obsidian/bookmarks.json", updatedJSON)`

## Usage Notes

Plugin "Bookmarks" (formerly Starred) manages favorite notes.

Available commands:
- bookmarks:bookmark-current-view -- Add the current note or view to bookmarks
- bookmarks:unbookmark-current-view -- Remove the current note from bookmarks

Use this skill when the user wants to bookmark or unbookmark notes.