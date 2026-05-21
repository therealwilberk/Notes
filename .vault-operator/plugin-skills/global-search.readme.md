# Search

Full-text search across the vault

## Overview

Search is an Obsidian core plugin. It is built into Obsidian and does not require separate installation.

## Commands

- `global-search:open` -- Open search

## Configuration

Settings are stored at `.obsidian/global-search.json`.

To read: `read_file(".obsidian/global-search.json")`
To write: `write_file(".obsidian/global-search.json", updatedJSON)`

## Usage Notes

Plugin "Search" provides full-text search across all vault notes.

Available commands:
- global-search:open -- Open the search pane

Use this skill only when the user explicitly wants to open the search UI. For programmatic searching, prefer the search_files or semantic_search tools.