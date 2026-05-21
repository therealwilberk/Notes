---
id: quickadd
name: QuickAdd
source: vault-native
plugin-type: community
status: enabled
class: FULL
description: "Quickly add new pages or content to your vault."
has-settings: true
commands:
  - id: "quickadd:runQuickAdd"
    name: "QuickAdd: Run"
  - id: "quickadd:reloadQuickAdd"
    name: "QuickAdd: Reload (dev)"
  - id: "quickadd:testQuickAdd"
    name: "QuickAdd: Test (dev)"
---

# QuickAdd

**Description:** Quickly add new pages or content to your vault.
**Status:** Enabled
**Plugin ID:** quickadd

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `quickadd:runQuickAdd` -- QuickAdd: Run
- `quickadd:reloadQuickAdd` -- QuickAdd: Reload (dev)
- `quickadd:testQuickAdd` -- QuickAdd: Test (dev)

## Plugin API

This plugin exposes a JavaScript API. Use call_plugin_api to call these methods:
- `hasOwnProperty` -- call via call_plugin_api("quickadd", "hasOwnProperty", [args])
- `isPrototypeOf` -- call via call_plugin_api("quickadd", "isPrototypeOf", [args])
- `propertyIsEnumerable` -- call via call_plugin_api("quickadd", "propertyIsEnumerable", [args])
- `toString` -- call via call_plugin_api("quickadd", "toString", [args])
- `valueOf` -- call via call_plugin_api("quickadd", "valueOf", [args])
- `toLocaleString` -- call via call_plugin_api("quickadd", "toLocaleString", [args])

Note: Dynamically discovered methods require user approval for each call unless marked as safe in settings.

## Configuration File

Settings path: `.obsidian/plugins/quickadd/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/quickadd/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/quickadd/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Current Configuration

These are the plugin's current settings (sensitive values redacted):

```
inputPrompt: single-line
persistInputPromptDrafts: true
useSelectionAsCaptureValue: true
devMode: false
announceUpdates: major
onePageInputEnabled: false
disableOnlineFeatures: true
enableRibbonIcon: false
showCaptureNotification: true
showInputCancellationNotification: false
enableTemplatePropertyTypes: false
dateAliases:
  t: today
  tm: tomorrow
  yd: yesterday
  nw: next week
  nm: next month
  ny: next year
  lw: last week
  lm: last month
  ly: last year
ai:
  defaultModel: Ask me
  defaultSystemPrompt: [string, 731 chars]
  showAssistant: true
  providers: [2 items: {...}, {...}...]
migrations:
  migrateToMacroIDFromEmbeddedMacro: true
  useQuickAddTemplateFolder: true
  incrementFileNameSettingMoveToDefaultBehavior: true
  consolidateFileExistsBehavior: true
  mutualExclusionInsertAfterAndWriteToBottomOfFile: true
  setVersionAfterUpdateModalRelease: true
  addDefaultAIProviders: true
  removeMacroIndirection: true
  migrateFileOpeningSettings: true
  backfillFileOpeningDefaults: true
  setProviderModelDiscoveryMode: true
```
(1 sensitive field(s) redacted)

For full settings, read: `.obsidian/plugins/quickadd/data.json`

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/plugin-skills/quickadd.readme.md")

## Usage

When the user asks for functionality related to QuickAdd:
1. Read the plugin documentation (.readme.md) to understand capabilities and dependencies
2. Read the config file (.obsidian/plugins/quickadd/data.json). If it does not exist, that is normal -- create it with the required settings
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
