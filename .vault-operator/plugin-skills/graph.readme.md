# Graph View

Visualize note connections as a graph

## Overview

Graph View is an Obsidian core plugin. It is built into Obsidian and does not require separate installation.

## Commands

- `graph:open` -- Open graph view
- `graph:open-local` -- Open local graph

## Configuration

Settings are stored at `.obsidian/graph.json`.

To read: `read_file(".obsidian/graph.json")`
To write: `write_file(".obsidian/graph.json", updatedJSON)`

## Usage Notes

Plugin "Graph View" visualizes connections between notes.

Available commands:
- graph:open -- Open the full vault graph view
- graph:open-local -- Open a local graph showing connections of the active note

Use this when the user wants to visualize note relationships or explore the knowledge graph.