---
id: templater-obsidian
name: Templater
source: vault-native
plugin-type: community
status: disabled
class: FULL
description: "Advanced templating and automation using handlebars-like syntax."
has-settings: false
needs-setup: true
commands:
  - id: "templater-obsidian:insert-templater"
    name: "Templater: Open insert template modal"
  - id: "templater-obsidian:replace-in-file-templater"
    name: "Templater: Replace templates in the active file"
  - id: "templater-obsidian:jump-to-next-cursor-location"
    name: "Templater: Jump to next cursor location"
  - id: "templater-obsidian:create-new-note-from-template"
    name: "Templater: Create new note from template"
---

# Templater

**Description:** Advanced templating and automation using handlebars-like syntax.
**Status:** Disabled
**Plugin ID:** templater-obsidian

## Setup Required

Plugin is disabled. Use enable_plugin to activate it first.
Guide the user to configure this plugin via Obsidian Settings if needed.

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `templater-obsidian:insert-templater` -- Templater: Open insert template modal
- `templater-obsidian:replace-in-file-templater` -- Templater: Replace templates in the active file
- `templater-obsidian:jump-to-next-cursor-location` -- Templater: Jump to next cursor location
- `templater-obsidian:create-new-note-from-template` -- Templater: Create new note from template

## Configuration File

Settings path: `.obsidian/plugins/templater-obsidian/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/templater-obsidian/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/templater-obsidian/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/plugin-skills/templater-obsidian.readme.md")

## Usage

This plugin is currently disabled. Use enable_plugin("templater-obsidian") to activate it first.
After enabling, the plugin's commands will become available for execute_command.
