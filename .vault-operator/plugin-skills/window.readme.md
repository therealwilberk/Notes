# Window

Window controls: zoom and always-on-top

## Overview

Window is an Obsidian core plugin. It is built into Obsidian and does not require separate installation.

## Commands

- `window:zoom-in` -- Zoom in
- `window:zoom-out` -- Zoom out
- `window:reset-zoom` -- Reset zoom
- `window:toggle-always-on-top` -- Toggle always on top

## Configuration

Settings are stored at `.obsidian/window.json`.

To read: `read_file(".obsidian/window.json")`
To write: `write_file(".obsidian/window.json", updatedJSON)`

## Usage Notes

Plugin "Window" controls the Obsidian window.

Available commands:
- window:zoom-in -- Increase the UI zoom level
- window:zoom-out -- Decrease the UI zoom level
- window:reset-zoom -- Reset zoom to default (100%)
- window:toggle-always-on-top -- Keep the Obsidian window above all other windows

Use this when the user asks to change zoom level or keep the window on top.