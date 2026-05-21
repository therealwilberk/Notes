# Slides

Present notes as slideshows using --- separators

## Overview

Slides is an Obsidian core plugin. It is built into Obsidian and does not require separate installation.

## Commands

- `slides:start` -- Start presentation

## Configuration

Settings are stored at `.obsidian/slides.json`.

To read: `read_file(".obsidian/slides.json")`
To write: `write_file(".obsidian/slides.json", updatedJSON)`

## Usage Notes

Plugin "Slides" turns notes into presentations.

Available commands:
- slides:start -- Start a slideshow presentation of the current note

Notes are split into slides by horizontal rules (---). Use this when the user wants to present a note as a slideshow.