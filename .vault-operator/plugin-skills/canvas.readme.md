# Canvas

Visual canvas with cards, links, and spatial notes

## Overview

Canvas is an Obsidian core plugin. It is built into Obsidian and does not require separate installation.

## Commands

- `canvas:new-file` -- Create new canvas
- `canvas:export-as-image` -- Export canvas as image
- `canvas:convert-to-file` -- Convert to file

## Configuration

Settings are stored at `.obsidian/canvas.json`.

To read: `read_file(".obsidian/canvas.json")`
To write: `write_file(".obsidian/canvas.json", updatedJSON)`

## Usage Notes

Plugin "Canvas" provides visual thinking boards with cards and connections.

Available commands:
- canvas:new-file -- Create a new empty canvas file (.canvas)
- canvas:export-as-image -- Export the current canvas as an image
- canvas:convert-to-file -- Convert a canvas card to a standalone note file

Use this skill when the user wants to create visual boards, mind maps, or spatial note arrangements. Note: For programmatic canvas creation with nodes and edges, prefer the generate_canvas tool instead.