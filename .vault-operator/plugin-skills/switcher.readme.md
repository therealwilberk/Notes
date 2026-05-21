# Quick Switcher

Quickly navigate to any note by name

## Overview

Quick Switcher is an Obsidian core plugin. It is built into Obsidian and does not require separate installation.

## Commands

- `switcher:open` -- Open quick switcher

## Configuration

Settings are stored at `.obsidian/switcher.json`.

To read: `read_file(".obsidian/switcher.json")`
To write: `write_file(".obsidian/switcher.json", updatedJSON)`

## Usage Notes

Plugin "Quick Switcher" opens a fuzzy-search dialog to jump to any note.

Available commands:
- switcher:open -- Open the quick switcher dialog

Use this skill when the user wants to navigate to a specific note by name. For programmatic navigation, prefer the open_note tool.