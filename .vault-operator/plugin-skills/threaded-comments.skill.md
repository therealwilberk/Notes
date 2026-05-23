---
id: threaded-comments
name: Threaded Comments
source: vault-native
plugin-type: community
status: enabled
class: PARTIAL
description: "Notion-style inline comments with highlights, speech bubbles, and threaded replies."
has-settings: true
commands:
  - id: "threaded-comments:add-comment"
    name: "Threaded Comments: Add comment at selection"
  - id: "threaded-comments:toggle-comments"
    name: "Threaded Comments: Toggle comment highlights"
---

# Threaded Comments

**Description:** Notion-style inline comments with highlights, speech bubbles, and threaded replies.
**Status:** Enabled
**Plugin ID:** threaded-comments

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

## Current Configuration

These are the plugin's current settings (sensitive values redacted):

```
authorName: user
highlightColor: rgba(249, 226, 175, 0.25)
showBubbles: true
showResolved: false
```

For full settings, read: `.obsidian/plugins/threaded-comments/data.json`

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/plugin-skills/threaded-comments.readme.md")

## Usage

When the user asks for functionality related to Threaded Comments:
1. Read the plugin documentation (.readme.md) to understand capabilities and dependencies
2. Read the config file (.obsidian/plugins/threaded-comments/data.json). If it does not exist, that is normal -- create it with the required settings
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
