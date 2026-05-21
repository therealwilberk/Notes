---
id: copilot
name: Copilot
source: vault-native
plugin-type: community
status: disabled
class: FULL
description: "Your AI Copilot: Chat with Your Second Brain, Learn Faster, Work Smarter."
has-settings: false
needs-setup: true
commands:
  - id: "copilot:count-word-and-tokens-selection"
    name: "Copilot: Count words and tokens in selection"
  - id: "copilot:count-total-vault-tokens"
    name: "Copilot: Count total tokens in your vault"
  - id: "copilot:chat-toggle-window"
    name: "Copilot: Toggle Copilot Chat Window"
  - id: "copilot:chat-open-window"
    name: "Copilot: Open Copilot Chat Window"
  - id: "copilot:new-chat"
    name: "Copilot: New Copilot Chat"
  - id: "copilot:trigger-quick-command"
    name: "Copilot: Trigger quick command"
  - id: "copilot:clear-local-copilot-index"
    name: "Copilot: Clear local Copilot index"
  - id: "copilot:garbage-collect-copilot-index"
    name: "Copilot: Garbage collect Copilot index (remove files that no longer exist in vault)"
  - id: "copilot:index-vault-to-copilot-index"
    name: "Copilot: Index (refresh) vault"
  - id: "copilot:force-reindex-vault-to-copilot-index"
    name: "Copilot: Force reindex vault"
  - id: "copilot:load-copilot-chat-conversation"
    name: "Copilot: Load Copilot chat conversation"
  - id: "copilot:copilot-list-indexed-files"
    name: "Copilot: List all indexed files (debug)"
  - id: "copilot:copilot-inspect-index-by-note-paths"
    name: "Copilot: Inspect Copilot index by note paths (debug)"
  - id: "copilot:clear-copilot-cache"
    name: "Copilot: Clear Copilot cache"
  - id: "copilot:open-log-file"
    name: "Copilot: Create log file"
  - id: "copilot:clear-log-file"
    name: "Copilot: Clear log file"
  - id: "copilot:add-selection-to-chat-context"
    name: "Copilot: Add selection to chat context"
  - id: "copilot:add-web-selection-to-chat-context"
    name: "Copilot: Add web selection to chat context"
  - id: "copilot:add-custom-command"
    name: "Copilot: Add new custom command"
  - id: "copilot:apply-custom-command"
    name: "Copilot: Apply custom command"
  - id: "copilot:download-youtube-script"
    name: "Copilot: Download YouTube Script (plus)"
  - id: "copilot:trigger-quick-ask"
    name: "Copilot: Quick Ask"
  - id: "copilot:clip%20web%20page"
    name: "Copilot: Clip Web Page"
---

# Copilot

**Description:** Your AI Copilot: Chat with Your Second Brain, Learn Faster, Work Smarter.
**Status:** Disabled
**Plugin ID:** copilot

## Setup Required

Plugin is disabled. Use enable_plugin to activate it first.
Guide the user to configure this plugin via Obsidian Settings if needed.

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `copilot:count-word-and-tokens-selection` -- Copilot: Count words and tokens in selection
- `copilot:count-total-vault-tokens` -- Copilot: Count total tokens in your vault
- `copilot:chat-toggle-window` -- Copilot: Toggle Copilot Chat Window
- `copilot:chat-open-window` -- Copilot: Open Copilot Chat Window
- `copilot:new-chat` -- Copilot: New Copilot Chat
- `copilot:trigger-quick-command` -- Copilot: Trigger quick command
- `copilot:clear-local-copilot-index` -- Copilot: Clear local Copilot index
- `copilot:garbage-collect-copilot-index` -- Copilot: Garbage collect Copilot index (remove files that no longer exist in vault)
- `copilot:index-vault-to-copilot-index` -- Copilot: Index (refresh) vault
- `copilot:force-reindex-vault-to-copilot-index` -- Copilot: Force reindex vault
- `copilot:load-copilot-chat-conversation` -- Copilot: Load Copilot chat conversation
- `copilot:copilot-list-indexed-files` -- Copilot: List all indexed files (debug)
- `copilot:copilot-inspect-index-by-note-paths` -- Copilot: Inspect Copilot index by note paths (debug)
- `copilot:clear-copilot-cache` -- Copilot: Clear Copilot cache
- `copilot:open-log-file` -- Copilot: Create log file
- `copilot:clear-log-file` -- Copilot: Clear log file
- `copilot:add-selection-to-chat-context` -- Copilot: Add selection to chat context
- `copilot:add-web-selection-to-chat-context` -- Copilot: Add web selection to chat context
- `copilot:add-custom-command` -- Copilot: Add new custom command
- `copilot:apply-custom-command` -- Copilot: Apply custom command
- `copilot:download-youtube-script` -- Copilot: Download YouTube Script (plus)
- `copilot:trigger-quick-ask` -- Copilot: Quick Ask
- `copilot:clip%20web%20page` -- Copilot: Clip Web Page

## Configuration File

Settings path: `.obsidian/plugins/copilot/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/copilot/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/copilot/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/plugin-skills/copilot.readme.md")

## Usage

This plugin is currently disabled. Use enable_plugin("copilot") to activate it first.
After enabling, the plugin's commands will become available for execute_command.
