# Templates

Insert predefined note templates

## Overview

Templates is an Obsidian core plugin. It is built into Obsidian and does not require separate installation.

## Commands

- `templates:insert-template` -- Insert template

## Configuration

Settings are stored at `.obsidian/templates.json`.

To read: `read_file(".obsidian/templates.json")`
To write: `write_file(".obsidian/templates.json", updatedJSON)`

## Usage Notes

Plugin "Templates" inserts template content into the current note.

Available commands:
- templates:insert-template -- Opens a picker to insert a template from the configured templates folder

Use this skill when the user asks to apply a template to a note. The template folder is configured in Obsidian settings. Note: If Templater is installed, prefer that for dynamic templates.