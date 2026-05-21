# Theme

Switch between light and dark mode or change themes

## Overview

Theme is an Obsidian core plugin. It is built into Obsidian and does not require separate installation.

## Commands

- `theme:switch` -- Switch theme
- `theme:use-dark` -- Use dark mode
- `theme:use-light` -- Use light mode

## Configuration

Settings are stored at `.obsidian/theme.json`.

To read: `read_file(".obsidian/theme.json")`
To write: `write_file(".obsidian/theme.json", updatedJSON)`

## Usage Notes

Plugin "Theme" controls the visual appearance.

Available commands:
- theme:switch -- Open the theme picker to change the active theme
- theme:use-dark -- Switch to dark color scheme
- theme:use-light -- Switch to light color scheme

Use this when the user asks to change the theme or switch between dark and light mode.