---
id: true-recall
name: True Recall
source: vault-native
plugin-type: community
status: enabled
class: FULL
description: "Review flashcards with FSRS spaced repetition. Supports Anki import/export, projects, and detailed statistics."
has-settings: true
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
**Status:** Enabled
**Plugin ID:** true-recall

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

## Current Configuration

These are the plugin's current settings (sensitive values redacted):

```
enableDeviceSync: false
providerType: openrouter
customBaseUrl: http://localhost:11434/v1
lmStudioBaseUrl: http://localhost:1234/v1
aiModel: google/gemini-2.5-flash
aiTier: byok
generationLanguage: auto
fsrsRequestRetention: 0.9
fsrsMaximumInterval: 36500
newCardsPerDay: 20
reviewsPerDay: 200
learningSteps: [1, 10]
relearningSteps: [10]
reviewMode: fullscreen
reviewContentWidth: default
showNextReviewTime: true
autoAdvance: false
showReviewHeader: true
showReviewHeaderStats: true
continuousCustomReviews: true
ignoreDailyLimitsForNoteStudy: true
reviewKeybindings:
  revealAndGood:  
  again: 1
  hard: 2
  easy: 4
removeFlashcardContentAfterCollect: false
newCardOrder: random
reviewOrder: due-date
newReviewMix: mix-with-reviews
dayStartHour: 4
autoBackupOnLoad: false
maxBackups: 10
periodicBackupEnabled: true
backupIntervalMinutes: 60
activityTriggeredBackup: false
reviewsBeforeBackup: 50
retentionPolicy:
  hourlyBackupsToKeep: 24
  dailyBackupsToKeep: 7
  weeklyBackupsToKeep: 4
copilotAutoContext: false
loadBalanceEnabled: false
loadBalanceTarget: 100
loadBalanceMaxDeviation: 20
loadBalanceMaxShiftDays: 3
loadBalanceBulkDays: 30
easyDaysMultiplier: 0.5
siblingMinInterval: 3
siblingDisperseEnabled: false
fsrsPresets: [1 items]
defaultPresetId: default
showLinkStatusIndicators: true
showDonutsInPanel: true
showDonutsInReview: true
showStatusBarWidget: true
defaultTypeInMode: off
noteReviewShowFrontmatter: false
editorToolbarButtons: [8 items]
globalToolbarButtons: [7 items]
imageToolbarButtons: [3 items]
enableLocalApi: false
apiPort: 27182
ragEnabled: false
ragEmbeddingModel: baai/bge-m3
ragExcludeFolders: [.true-recall, templates]
ragIndexFlashcards: true
ragAutoIndex: true
ragDailyNoteExcludeHeadings: [Thoughts, Journal, Reflections, Random]
ragChatConfig:
  presetId: default
  responseLength: medium
generationPresets: [2 items: {...}, {...}...]
defaultGenerationPresetId: builtin-basic-flashcards
deviceId: 9xe2ks70
lastSeenVersion: 1.9.4
archiveCascadeMigrated: true
```
(2 sensitive field(s) redacted)

For full settings, read: `.obsidian/plugins/true-recall/data.json`

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/plugin-skills/true-recall.readme.md")

## Usage

When the user asks for functionality related to True Recall:
1. Read the plugin documentation (.readme.md) to understand capabilities and dependencies
2. Read the config file (.obsidian/plugins/true-recall/data.json). If it does not exist, that is normal -- create it with the required settings
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
