---
id: code-styler
name: Code Styler
source: vault-native
plugin-type: community
status: disabled
class: FULL
description: "Style and customize codeblocks and inline code in both editing mode and reading mode."
has-settings: false
needs-setup: true
commands:
  - id: "code-styler:fold-all"
    name: "Code Styler: Fold all codeblocks"
  - id: "code-styler:unfold-all"
    name: "Code Styler: Unfold all codeblocks"
  - id: "code-styler:reset-all"
    name: "Code Styler: Reset fold state for all codeblocks"
  - id: "code-styler:update-references-vault"
    name: "Code Styler: Update all external references in vault"
  - id: "code-styler:update-references-page"
    name: "Code Styler: Update all external references in note"
  - id: "code-styler:clean-references"
    name: "Code Styler: Remove all unneeded external references"
---

# Code Styler

**Description:** Style and customize codeblocks and inline code in both editing mode and reading mode.
**Status:** Disabled
**Plugin ID:** code-styler

## Setup Required

Plugin is disabled. Use enable_plugin to activate it first.
Guide the user to configure this plugin via Obsidian Settings if needed.

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `code-styler:fold-all` -- Code Styler: Fold all codeblocks
- `code-styler:unfold-all` -- Code Styler: Unfold all codeblocks
- `code-styler:reset-all` -- Code Styler: Reset fold state for all codeblocks
- `code-styler:update-references-vault` -- Code Styler: Update all external references in vault
- `code-styler:update-references-page` -- Code Styler: Update all external references in note
- `code-styler:clean-references` -- Code Styler: Remove all unneeded external references

## Configuration File

Settings path: `.obsidian/plugins/code-styler/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/code-styler/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/code-styler/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/plugin-skills/code-styler.readme.md")

## Usage

This plugin is currently disabled. Use enable_plugin("code-styler") to activate it first.
After enabling, the plugin's commands will become available for execute_command.
