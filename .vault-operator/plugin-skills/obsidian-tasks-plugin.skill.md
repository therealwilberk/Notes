---
id: obsidian-tasks-plugin
name: Tasks
source: vault-native
plugin-type: community
status: disabled
class: PARTIAL
description: "Track tasks across your vault. Supports due dates, recurring tasks, done dates, sub-set of checklist items, and filtering."
has-settings: false
needs-setup: true
---

# Tasks

**Description:** Track tasks across your vault. Supports due dates, recurring tasks, done dates, sub-set of checklist items, and filtering.
**Status:** Disabled
**Plugin ID:** obsidian-tasks-plugin

## Setup Required

Plugin is disabled. Use enable_plugin to activate it first.
Guide the user to configure this plugin via Obsidian Settings if needed.

## Configuration File

Settings path: `.obsidian/plugins/obsidian-tasks-plugin/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/obsidian-tasks-plugin/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/obsidian-tasks-plugin/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/plugin-skills/obsidian-tasks-plugin.readme.md")

## Usage

This plugin is currently disabled. Use enable_plugin("obsidian-tasks-plugin") to activate it first.
After enabling, the plugin's commands will become available for execute_command.
