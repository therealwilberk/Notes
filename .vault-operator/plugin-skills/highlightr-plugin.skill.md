---
id: highlightr-plugin
name: Highlightr
source: vault-native
plugin-type: community
status: disabled
class: FULL
description: "A minimal and aesthetically pleasing highlighting menu that makes color-coded highlighting much easier with a configurable assortment of highlight colors 🎨."
has-settings: false
needs-setup: true
commands:
  - id: "highlightr-plugin:highlighter-plugin-menu"
    name: "Highlightr: Open Highlightr"
  - id: "highlightr-plugin:Pink"
    name: "Highlightr: Pink"
  - id: "highlightr-plugin:unhighlight"
    name: "Highlightr: Remove highlight"
  - id: "highlightr-plugin:Red"
    name: "Highlightr: Red"
  - id: "highlightr-plugin:Orange"
    name: "Highlightr: Orange"
  - id: "highlightr-plugin:Yellow"
    name: "Highlightr: Yellow"
  - id: "highlightr-plugin:Green"
    name: "Highlightr: Green"
  - id: "highlightr-plugin:Cyan"
    name: "Highlightr: Cyan"
  - id: "highlightr-plugin:Blue"
    name: "Highlightr: Blue"
  - id: "highlightr-plugin:Purple"
    name: "Highlightr: Purple"
  - id: "highlightr-plugin:Grey"
    name: "Highlightr: Grey"
---

# Highlightr

**Description:** A minimal and aesthetically pleasing highlighting menu that makes color-coded highlighting much easier with a configurable assortment of highlight colors 🎨.
**Status:** Disabled
**Plugin ID:** highlightr-plugin

## Setup Required

Plugin is disabled. Use enable_plugin to activate it first.
Guide the user to configure this plugin via Obsidian Settings if needed.

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `highlightr-plugin:highlighter-plugin-menu` -- Highlightr: Open Highlightr
- `highlightr-plugin:Pink` -- Highlightr: Pink
- `highlightr-plugin:unhighlight` -- Highlightr: Remove highlight
- `highlightr-plugin:Red` -- Highlightr: Red
- `highlightr-plugin:Orange` -- Highlightr: Orange
- `highlightr-plugin:Yellow` -- Highlightr: Yellow
- `highlightr-plugin:Green` -- Highlightr: Green
- `highlightr-plugin:Cyan` -- Highlightr: Cyan
- `highlightr-plugin:Blue` -- Highlightr: Blue
- `highlightr-plugin:Purple` -- Highlightr: Purple
- `highlightr-plugin:Grey` -- Highlightr: Grey

## Configuration File

Settings path: `.obsidian/plugins/highlightr-plugin/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/highlightr-plugin/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/highlightr-plugin/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/plugin-skills/highlightr-plugin.readme.md")

## Usage

This plugin is currently disabled. Use enable_plugin("highlightr-plugin") to activate it first.
After enabling, the plugin's commands will become available for execute_command.
