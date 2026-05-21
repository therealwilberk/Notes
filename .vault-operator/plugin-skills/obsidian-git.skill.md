---
id: obsidian-git
name: Git
source: vault-native
plugin-type: community
status: enabled
class: FULL
description: "Integrate Git version control with automatic backup and other advanced features."
has-settings: false
needs-setup: true
commands:
  - id: "obsidian-git:edit-gitignore"
    name: "Git: Edit .gitignore"
  - id: "obsidian-git:open-git-view"
    name: "Git: Open source control view"
  - id: "obsidian-git:open-history-view"
    name: "Git: Open history view"
  - id: "obsidian-git:open-diff-view"
    name: "Git: Open diff view"
  - id: "obsidian-git:view-file-on-github"
    name: "Git: Open file on GitHub"
  - id: "obsidian-git:view-history-on-github"
    name: "Git: Open file history on GitHub"
  - id: "obsidian-git:pull"
    name: "Git: Pull"
  - id: "obsidian-git:fetch"
    name: "Git: Fetch"
  - id: "obsidian-git:switch-to-remote-branch"
    name: "Git: Switch to remote branch"
  - id: "obsidian-git:add-to-gitignore"
    name: "Git: Add file to .gitignore"
  - id: "obsidian-git:push"
    name: "Git: Commit-and-sync"
  - id: "obsidian-git:backup-and-close"
    name: "Git: Commit-and-sync and then close Obsidian"
  - id: "obsidian-git:commit-push-specified-message"
    name: "Git: Commit-and-sync with specific message"
  - id: "obsidian-git:commit"
    name: "Git: Commit all changes"
  - id: "obsidian-git:commit-specified-message"
    name: "Git: Commit all changes with specific message"
  - id: "obsidian-git:commit-smart"
    name: "Git: Commit"
  - id: "obsidian-git:commit-staged"
    name: "Git: Commit staged"
  - id: "obsidian-git:commit-amend-staged-specified-message"
    name: "Git: Amend staged"
  - id: "obsidian-git:commit-smart-specified-message"
    name: "Git: Commit with specific message"
  - id: "obsidian-git:commit-staged-specified-message"
    name: "Git: Commit staged with specific message"
  - id: "obsidian-git:push2"
    name: "Git: Push"
  - id: "obsidian-git:stage-current-file"
    name: "Git: Stage current file"
  - id: "obsidian-git:unstage-current-file"
    name: "Git: Unstage current file"
  - id: "obsidian-git:edit-remotes"
    name: "Git: Edit remotes"
  - id: "obsidian-git:remove-remote"
    name: "Git: Remove remote"
  - id: "obsidian-git:set-upstream-branch"
    name: "Git: Set upstream branch"
  - id: "obsidian-git:delete-repo"
    name: "Git: CAUTION: Delete repository"
  - id: "obsidian-git:init-repo"
    name: "Git: Initialize a new repo"
  - id: "obsidian-git:clone-repo"
    name: "Git: Clone an existing remote repo"
  - id: "obsidian-git:list-changed-files"
    name: "Git: List changed files"
  - id: "obsidian-git:switch-branch"
    name: "Git: Switch branch"
  - id: "obsidian-git:create-branch"
    name: "Git: Create new branch"
  - id: "obsidian-git:delete-branch"
    name: "Git: Delete branch"
  - id: "obsidian-git:discard-all"
    name: "Git: CAUTION: Discard all changes"
  - id: "obsidian-git:pause-automatic-routines"
    name: "Git: Pause/Resume automatic routines"
  - id: "obsidian-git:raw-command"
    name: "Git: Raw command"
  - id: "obsidian-git:toggle-line-author-info"
    name: "Git: Toggle line author information"
  - id: "obsidian-git:reset-hunk"
    name: "Git: Reset hunk"
  - id: "obsidian-git:stage-hunk"
    name: "Git: Stage hunk"
  - id: "obsidian-git:preview-hunk"
    name: "Git: Preview hunk"
  - id: "obsidian-git:next-hunk"
    name: "Git: Go to next hunk"
  - id: "obsidian-git:prev-hunk"
    name: "Git: Go to previous hunk"
---

# Git

**Description:** Integrate Git version control with automatic backup and other advanced features.
**Status:** Enabled
**Plugin ID:** obsidian-git

## Setup Required

No settings file found (data.json). Plugin may need initial setup via Obsidian Settings.
Guide the user to configure this plugin via Obsidian Settings if needed.

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `obsidian-git:edit-gitignore` -- Git: Edit .gitignore
- `obsidian-git:open-git-view` -- Git: Open source control view
- `obsidian-git:open-history-view` -- Git: Open history view
- `obsidian-git:open-diff-view` -- Git: Open diff view
- `obsidian-git:view-file-on-github` -- Git: Open file on GitHub
- `obsidian-git:view-history-on-github` -- Git: Open file history on GitHub
- `obsidian-git:pull` -- Git: Pull
- `obsidian-git:fetch` -- Git: Fetch
- `obsidian-git:switch-to-remote-branch` -- Git: Switch to remote branch
- `obsidian-git:add-to-gitignore` -- Git: Add file to .gitignore
- `obsidian-git:push` -- Git: Commit-and-sync
- `obsidian-git:backup-and-close` -- Git: Commit-and-sync and then close Obsidian
- `obsidian-git:commit-push-specified-message` -- Git: Commit-and-sync with specific message
- `obsidian-git:commit` -- Git: Commit all changes
- `obsidian-git:commit-specified-message` -- Git: Commit all changes with specific message
- `obsidian-git:commit-smart` -- Git: Commit
- `obsidian-git:commit-staged` -- Git: Commit staged
- `obsidian-git:commit-amend-staged-specified-message` -- Git: Amend staged
- `obsidian-git:commit-smart-specified-message` -- Git: Commit with specific message
- `obsidian-git:commit-staged-specified-message` -- Git: Commit staged with specific message
- `obsidian-git:push2` -- Git: Push
- `obsidian-git:stage-current-file` -- Git: Stage current file
- `obsidian-git:unstage-current-file` -- Git: Unstage current file
- `obsidian-git:edit-remotes` -- Git: Edit remotes
- `obsidian-git:remove-remote` -- Git: Remove remote
- `obsidian-git:set-upstream-branch` -- Git: Set upstream branch
- `obsidian-git:delete-repo` -- Git: CAUTION: Delete repository
- `obsidian-git:init-repo` -- Git: Initialize a new repo
- `obsidian-git:clone-repo` -- Git: Clone an existing remote repo
- `obsidian-git:list-changed-files` -- Git: List changed files
- `obsidian-git:switch-branch` -- Git: Switch branch
- `obsidian-git:create-branch` -- Git: Create new branch
- `obsidian-git:delete-branch` -- Git: Delete branch
- `obsidian-git:discard-all` -- Git: CAUTION: Discard all changes
- `obsidian-git:pause-automatic-routines` -- Git: Pause/Resume automatic routines
- `obsidian-git:raw-command` -- Git: Raw command
- `obsidian-git:toggle-line-author-info` -- Git: Toggle line author information
- `obsidian-git:reset-hunk` -- Git: Reset hunk
- `obsidian-git:stage-hunk` -- Git: Stage hunk
- `obsidian-git:preview-hunk` -- Git: Preview hunk
- `obsidian-git:next-hunk` -- Git: Go to next hunk
- `obsidian-git:prev-hunk` -- Git: Go to previous hunk

## Configuration File

Settings path: `.obsidian/plugins/obsidian-git/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/obsidian-git/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/obsidian-git/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/plugin-skills/obsidian-git.readme.md")

## Usage

When the user asks for functionality related to Git:
1. Read the plugin documentation (.readme.md) to understand capabilities and dependencies
2. Read the config file (.obsidian/plugins/obsidian-git/data.json). If it does not exist, that is normal -- create it with the required settings
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
