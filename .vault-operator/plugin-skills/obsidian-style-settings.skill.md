---
id: obsidian-style-settings
name: Style Settings
source: vault-native
plugin-type: community
status: enabled
class: PARTIAL
description: "Offers controls for adjusting theme, plugin, and snippet CSS variables."
has-settings: true
commands:
  - id: "obsidian-style-settings:show-style-settings-leaf"
    name: "Style Settings: Show style settings view"
---

# Style Settings

**Description:** Offers controls for adjusting theme, plugin, and snippet CSS variables.
**Status:** Enabled
**Plugin ID:** obsidian-style-settings

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `obsidian-style-settings:show-style-settings-leaf` -- Style Settings: Show style settings view

## Configuration File

Settings path: `.obsidian/plugins/obsidian-style-settings/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/obsidian-style-settings/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/obsidian-style-settings/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Current Configuration

These are the plugin's current settings (sensitive values redacted):

```
anuppuccin-theme-settings@@anp-header-color-toggle: true
anuppuccin-theme-settings@@anp-decoration-toggle: true
anuppuccin-theme-settings@@anp-active-line: anp-current-line-border-only
anuppuccin-theme-settings@@anp-callout-select: anp-callout-sleek
anuppuccin-theme-settings@@anp-callout-color-toggle: true
anuppuccin-theme-settings@@anp-custom-checkboxes: true
anuppuccin-theme-settings@@anp-speech-bubble: true
anuppuccin-theme-settings@@anp-codeblock-numbers: true
anuppuccin-theme-settings@@anp-list-toggle: true
anuppuccin-theme-settings@@anp-table-toggle: true
anuppuccin-theme-settings@@anp-table-width: true
anuppuccin-theme-settings@@anp-table-auto: true
anuppuccin-theme-settings@@anp-table-th-highlight: true
anuppuccin-theme-settings@@anp-toggle-preview: true
anuppuccin-theme-settings@@anp-autohide-titlebar: true
anuppuccin-theme-settings@@anp-header-margin-toggle: true
anuppuccin-theme-settings@@anp-header-divider-color-toggle: true
anuppuccin-theme-settings@@anp-canvas-dark-bg: true
anuppuccin-theme-settings@@anp-colorful-frame: false
anuppuccin-theme-settings@@anp-custom-vault-toggle: true
anuppuccin-theme-settings@@anp-file-icons: true
anuppuccin-theme-settings@@anp-floating-header: true
anuppuccin-theme-settings@@anp-collapse-folders: true
anuppuccin-theme-settings@@anp-pdf-blend-toggle-dark: true
anuppuccin-theme-settings@@anp-alt-rainbow-style: anp-simple-rainbow-color-toggle
anuppuccin-theme-settings@@anp-rainbow-file-toggle: false
anuppuccin-theme-settings@@anp-full-rainbow-text-color-toggle-light: false
anuppuccin-theme-settings@@anp-full-rainbow-text-color-toggle-dark: false
anuppuccin-theme-settings@@anp-simple-rainbow-title-toggle: false
anuppuccin-theme-settings@@anp-simple-rainbow-collapse-icon-toggle: true
anuppuccin-theme-settings@@anp-simple-rainbow-icon-toggle: true
anuppuccin-theme-settings@@anp-rainbow-subfolder-color-toggle: true
anuppuccin-theme-settings@@anp-status-bar-select: anp-floating-status-bar
anuppuccin-theme-settings@@anp-alt-tab-style: anp-alternate-tab-toggle
anuppuccin-theme-settings@@anp-safari-tab-animated: false
anuppuccin-theme-settings@@anp-hide-borders: true
anuppuccin-theme-settings@@anuppuccin-theme-light: ctp-latte
anuppuccin-theme-settings@@anuppuccin-theme-dark: ctp-mocha-old
anuppuccin-theme-settings@@anuppuccin-theme-accents: ctp-accent-sky
anuppuccin-theme-settings@@anp-color-transition-toggle: true
anuppuccin-theme-settings@@anp-toggle-scrollbars: true
anuppuccin-theme-settings@@anp-hide-status-bar: true
anuppuccin-theme-settings@@anp-tooltip-toggle: true
anuppuccin-theme-settings@@anp-toggle-metadata: true
anuppuccin-theme-settings@@hide-comment-indicators: true
anuppuccin-theme-settings@@hide-comments: false
anuppuccin-theme-settings@@anp-layout-select: anp-card-layout
anuppuccin-theme-settings@@anp-card-layout-padding: 8
anuppuccin-theme-settings@@anp-card-shadows: false
anuppuccin-theme-settings@@anp-card-layout-actions: true
anuppuccin-theme-settings@@anp-card-layout-filebrowser: false
anuppuccin-theme-settings@@anuppuccin-light-theme-accents: ctp-accent-light-rosewater
anuppuccin-theme-settings@@anuppuccin-accent-toggle: true
anuppuccin-theme-settings@@embed-corner-radius: 1
anuppuccin-theme-settings@@anp-bg-fix: false
anuppuccin-theme-settings@@anp-card-radius: 1
anuppuccin-theme-settings@@anp-card-header-left-padding: 15
```

For full settings, read: `.obsidian/plugins/obsidian-style-settings/data.json`

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/plugin-skills/obsidian-style-settings.readme.md")

## Usage

When the user asks for functionality related to Style Settings:
1. Read the plugin documentation (.readme.md) to understand capabilities and dependencies
2. Read the config file (.obsidian/plugins/obsidian-style-settings/data.json). If it does not exist, that is normal -- create it with the required settings
3. Configure the plugin by writing data.json with the values needed for the task
4. Execute the task using the appropriate tool:
   - For Obsidian-native commands (including file export): use execute_command
   - For CLI-based conversion needing Pandoc/LaTeX: use execute_recipe
   - For data queries: use call_plugin_api
5. If a command opens a UI dialog, tell the user what to click.

CRITICAL RULES:
- Prefer native Obsidian commands over external tools when both can accomplish the task.
- NEVER create fake output files. If the user asks for a PDF/DOCX/image export, use execute_recipe -- do NOT write content to a .pdf file yourself.
- If a dependency is missing (e.g. Pandoc), tell the user what to install.
IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
