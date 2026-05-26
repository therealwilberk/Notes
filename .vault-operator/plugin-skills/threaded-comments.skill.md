---
id: threaded-comments
name: Threaded Comments
source: vault-native
plugin-type: community
status: disabled
class: PARTIAL
description: "Notion-style inline comments with highlights, speech bubbles, and threaded replies."
has-settings: false
needs-setup: true
commands:
  - id: "threaded-comments:add-comment"
    name: "Threaded Comments: Add comment at selection"
  - id: "threaded-comments:toggle-comments"
    name: "Threaded Comments: Toggle comment highlights"
---

# Threaded Comments

**Description:** Notion-style inline comments with highlights, speech bubbles, and threaded replies.
**Status:** Disabled
**Plugin ID:** threaded-comments

## Setup Required

Plugin is disabled. Use enable_plugin to activate it first.
Guide the user to configure this plugin via Obsidian Settings if needed.

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `threaded-comments:add-comment` -- Threaded Comments: Add comment at selection
- `threaded-comments:toggle-comments` -- Threaded Comments: Toggle comment highlights

## Configuration File

Settings path: `.obsidian/plugins/threaded-comments/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/threaded-comments/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/threaded-comments/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/plugin-skills/threaded-comments.readme.md")

## Usage

This plugin is currently disabled. Use enable_plugin("threaded-comments") to activate it first.
After enabling, the plugin's commands will become available for execute_command.
