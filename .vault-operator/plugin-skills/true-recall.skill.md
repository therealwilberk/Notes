---
id: true-recall
name: True Recall
source: vault-native
plugin-type: community
status: disabled
class: FULL
description: "Review flashcards with FSRS spaced repetition. Supports Anki import/export, projects, and detailed statistics."
has-settings: false
needs-setup: true
commands:
  - id: "true-recall:insert-project-dashboard"
    name: "True Recall: Insert project dashboard"
  - id: "true-recall:create-master-dashboard"
    name: "True Recall: Create master dashboard note"
  - id: "true-recall:open-flashcard-panel"
    name: "True Recall: Open flashcard panel"
  - id: "true-recall:review-current-note"
    name: "True Recall: Review flashcards from current note"
  - id: "true-recall:review-todays-cards"
    name: "True Recall: Review today's new cards"
  - id: "true-recall:open-dashboard"
    name: "True Recall: Open dashboard"
  - id: "true-recall:open-card-browser"
    name: "True Recall: Open card browser"
  - id: "true-recall:open-fsrs-simulator"
    name: "True Recall: Open FSRS simulator"
  - id: "true-recall:open-stats"
    name: "True Recall: Open statistics"
  - id: "true-recall:manage-note-types"
    name: "True Recall: Manage note types"
  - id: "true-recall:add-flashcards"
    name: "True Recall: Import flashcards"
  - id: "true-recall:create-image-occlusion-card"
    name: "True Recall: Create image occlusion card"
  - id: "true-recall:create-backup"
    name: "True Recall: Create database backup"
  - id: "true-recall:add-flashcard-uid"
    name: "True Recall: Add flashcard uid to current note"
  - id: "true-recall:toggle-note-review"
    name: "True Recall: Toggle note review"
  - id: "true-recall:undo-flashcard-action"
    name: "True Recall: Undo last flashcard action"
  - id: "true-recall:redo-flashcard-action"
    name: "True Recall: Redo last undone action"
  - id: "true-recall:export-csv"
    name: "True Recall: Export as CSV/TSV"
  - id: "true-recall:set-fsrs-preset"
    name: "True Recall: Set FSRS preset for current note"
  - id: "true-recall:archive-current-note"
    name: "True Recall: Archive current note"
  - id: "true-recall:unarchive-current-note"
    name: "True Recall: Unarchive current note"
  - id: "true-recall:open-knowledge-chat"
    name: "True Recall: Chat with knowledge base"
  - id: "true-recall:generate-flashcards-from-selection"
    name: "True Recall: Generate flashcards from selection"
  - id: "true-recall:quick-add-flashcard-from-selection"
    name: "True Recall: Quick add flashcard from selection"
  - id: "true-recall:edit-selection-as-flashcard"
    name: "True Recall: Edit selection as flashcard"
  - id: "true-recall:global-generate-flashcards-from-selection"
    name: "True Recall: Generate flashcards from selection (any view)"
  - id: "true-recall:global-quick-add-flashcard-from-selection"
    name: "True Recall: Quick add flashcard from selection (any view)"
  - id: "true-recall:global-edit-selection-as-flashcard"
    name: "True Recall: Edit selection as flashcard (any view)"
---

# True Recall

**Description:** Review flashcards with FSRS spaced repetition. Supports Anki import/export, projects, and detailed statistics.
**Status:** Disabled
**Plugin ID:** true-recall

## Setup Required

Plugin is disabled. Use enable_plugin to activate it first.
Guide the user to configure this plugin via Obsidian Settings if needed.

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `true-recall:insert-project-dashboard` -- True Recall: Insert project dashboard
- `true-recall:create-master-dashboard` -- True Recall: Create master dashboard note
- `true-recall:open-flashcard-panel` -- True Recall: Open flashcard panel
- `true-recall:review-current-note` -- True Recall: Review flashcards from current note
- `true-recall:review-todays-cards` -- True Recall: Review today's new cards
- `true-recall:open-dashboard` -- True Recall: Open dashboard
- `true-recall:open-card-browser` -- True Recall: Open card browser
- `true-recall:open-fsrs-simulator` -- True Recall: Open FSRS simulator
- `true-recall:open-stats` -- True Recall: Open statistics
- `true-recall:manage-note-types` -- True Recall: Manage note types
- `true-recall:add-flashcards` -- True Recall: Import flashcards
- `true-recall:create-image-occlusion-card` -- True Recall: Create image occlusion card
- `true-recall:create-backup` -- True Recall: Create database backup
- `true-recall:add-flashcard-uid` -- True Recall: Add flashcard uid to current note
- `true-recall:toggle-note-review` -- True Recall: Toggle note review
- `true-recall:undo-flashcard-action` -- True Recall: Undo last flashcard action
- `true-recall:redo-flashcard-action` -- True Recall: Redo last undone action
- `true-recall:export-csv` -- True Recall: Export as CSV/TSV
- `true-recall:set-fsrs-preset` -- True Recall: Set FSRS preset for current note
- `true-recall:archive-current-note` -- True Recall: Archive current note
- `true-recall:unarchive-current-note` -- True Recall: Unarchive current note
- `true-recall:open-knowledge-chat` -- True Recall: Chat with knowledge base
- `true-recall:generate-flashcards-from-selection` -- True Recall: Generate flashcards from selection
- `true-recall:quick-add-flashcard-from-selection` -- True Recall: Quick add flashcard from selection
- `true-recall:edit-selection-as-flashcard` -- True Recall: Edit selection as flashcard
- `true-recall:global-generate-flashcards-from-selection` -- True Recall: Generate flashcards from selection (any view)
- `true-recall:global-quick-add-flashcard-from-selection` -- True Recall: Quick add flashcard from selection (any view)
- `true-recall:global-edit-selection-as-flashcard` -- True Recall: Edit selection as flashcard (any view)

## Configuration File

Settings path: `.obsidian/plugins/true-recall/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/true-recall/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/true-recall/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/plugin-skills/true-recall.readme.md")

## Usage

This plugin is currently disabled. Use enable_plugin("true-recall") to activate it first.
After enabling, the plugin's commands will become available for execute_command.
