---
id: obsidian-excalidraw-plugin
name: Excalidraw
source: vault-native
plugin-type: community
status: enabled
class: FULL
description: "Sketch Your Mind. Edit and view Excalidraw drawings. Enter the world of 4D Visual PKM."
has-settings: true
commands:
  - id: "obsidian-excalidraw-plugin:excalidraw-convert-image-from-url-to-local-file"
    name: "Excalidraw: Save image from URL to local file"
  - id: "obsidian-excalidraw-plugin:excalidraw-unzip-file"
    name: "Excalidraw: Decompress current Excalidraw file"
  - id: "obsidian-excalidraw-plugin:excalidraw-publish-svg-check"
    name: "Excalidraw: Obsidian Publish: Find SVG and PNG exports that are out of date"
  - id: "obsidian-excalidraw-plugin:excalidraw-embeddable-poroperties"
    name: "Excalidraw: Embeddable Properties"
  - id: "obsidian-excalidraw-plugin:excalidraw-embeddables-relative-scale"
    name: "Excalidraw: Scale selected embeddable elements to 100% relative to the current canvas zoom"
  - id: "obsidian-excalidraw-plugin:open-image-excalidraw-source"
    name: "Excalidraw: Open Excalidraw drawing"
  - id: "obsidian-excalidraw-plugin:excalidraw-disable-autosave"
    name: "Excalidraw: Disable autosave until next time Obsidian starts (only set this if you know what you are doing)"
  - id: "obsidian-excalidraw-plugin:excalidraw-enable-autosave"
    name: "Excalidraw: Enable autosave"
  - id: "obsidian-excalidraw-plugin:excalidraw-toggle-session-view-mode"
    name: "Excalidraw: Toggle view mode for all Excalidraw drawings until Obsidian restarts"
  - id: "obsidian-excalidraw-plugin:excalidraw-download-lib"
    name: "Excalidraw: Export stencil library as an *.excalidrawlib file"
  - id: "obsidian-excalidraw-plugin:excalidraw-open-sidepanel"
    name: "Excalidraw: Open Excalidraw Sidepanel"
  - id: "obsidian-excalidraw-plugin:excalidraw-open"
    name: "Excalidraw: Open existing drawing - IN A NEW PANE"
  - id: "obsidian-excalidraw-plugin:excalidraw-open-on-current"
    name: "Excalidraw: Open existing drawing - IN THE CURRENT ACTIVE PANE"
  - id: "obsidian-excalidraw-plugin:excalidraw-insert-transclusion"
    name: "Excalidraw: Embed a drawing"
  - id: "obsidian-excalidraw-plugin:excalidraw-insert-last-active-transclusion"
    name: "Excalidraw: Embed the most recently edited drawing"
  - id: "obsidian-excalidraw-plugin:excalidraw-autocreate"
    name: "Excalidraw: Create new drawing - IN AN ADJACENT WINDOW"
  - id: "obsidian-excalidraw-plugin:excalidraw-autocreate-newtab"
    name: "Excalidraw: Create new drawing - IN A NEW TAB"
  - id: "obsidian-excalidraw-plugin:excalidraw-autocreate-on-current"
    name: "Excalidraw: Create new drawing - IN THE CURRENT ACTIVE WINDOW"
  - id: "obsidian-excalidraw-plugin:excalidraw-autocreate-popout"
    name: "Excalidraw: Create new drawing - IN A POPOUT WINDOW"
  - id: "obsidian-excalidraw-plugin:excalidraw-autocreate-and-embed"
    name: "Excalidraw: Create new drawing - IN AN ADJACENT WINDOW - and embed into active document"
  - id: "obsidian-excalidraw-plugin:excalidraw-autocreate-and-embed-new-tab"
    name: "Excalidraw: Create new drawing - IN A NEW TAB - and embed into active document"
  - id: "obsidian-excalidraw-plugin:excalidraw-autocreate-and-embed-on-current"
    name: "Excalidraw: Create new drawing - IN THE CURRENT ACTIVE WINDOW - and embed into active document"
  - id: "obsidian-excalidraw-plugin:excalidraw-autocreate-and-embed-popout"
    name: "Excalidraw: Create new drawing - IN A POPOUT WINDOW - and embed into active document"
  - id: "obsidian-excalidraw-plugin:run-ocr"
    name: "Excalidraw: OCR full drawing: Grab text from freedraw + images to clipboard and doc.props"
  - id: "obsidian-excalidraw-plugin:rerun-ocr"
    name: "Excalidraw: OCR full drawing re-run: Grab text from freedraw + images to clipboard and doc.props"
  - id: "obsidian-excalidraw-plugin:run-ocr-selectedelements"
    name: "Excalidraw: OCR selected elements: Grab text from freedraw + images to clipboard"
  - id: "obsidian-excalidraw-plugin:search-text"
    name: "Excalidraw: Search for text in drawing"
  - id: "obsidian-excalidraw-plugin:fullscreen"
    name: "Excalidraw: Toggle fullscreen mode"
  - id: "obsidian-excalidraw-plugin:disable-binding"
    name: "Excalidraw: Toggle to invert default binding behavior"
  - id: "obsidian-excalidraw-plugin:disable-framerendering"
    name: "Excalidraw: Toggle frame rendering"
  - id: "obsidian-excalidraw-plugin:frame-settings"
    name: "Excalidraw: Frame Settings"
  - id: "obsidian-excalidraw-plugin:copy-link-to-drawing"
    name: "Excalidraw: Copy ![[embed link]] for this drawing"
  - id: "obsidian-excalidraw-plugin:disable-frameclipping"
    name: "Excalidraw: Toggle frame clipping"
  - id: "obsidian-excalidraw-plugin:export-image"
    name: "Excalidraw: Export Image"
  - id: "obsidian-excalidraw-plugin:save"
    name: "Excalidraw: Save (will also update transclusions)"
  - id: "obsidian-excalidraw-plugin:toggle-lock"
    name: "Excalidraw: Toggle Text Element between edit RAW and PREVIEW"
  - id: "obsidian-excalidraw-plugin:scriptengine-store"
    name: "Excalidraw: Install or update Excalidraw Scripts"
  - id: "obsidian-excalidraw-plugin:delete-file"
    name: "Excalidraw: Delete selected image or Markdown file from Obsidian Vault"
  - id: "obsidian-excalidraw-plugin:convert-text2MD"
    name: "Excalidraw: Convert to file..."
  - id: "obsidian-excalidraw-plugin:insert-link"
    name: "Excalidraw: Insert link to file"
  - id: "obsidian-excalidraw-plugin:insert-command"
    name: "Excalidraw: Insert Obsidian Command as a link"
  - id: "obsidian-excalidraw-plugin:insert-link-to-element"
    name: "Excalidraw: Copy [[link]] for selected element to clipboard."
  - id: "obsidian-excalidraw-plugin:insert-link-to-element-group"
    name: "Excalidraw: Copy 'group=' ![[link]] for selected element to clipboard."
  - id: "obsidian-excalidraw-plugin:insert-link-to-element-frame"
    name: "Excalidraw: Copy 'frame=' ![[link]] for selected element to clipboard."
  - id: "obsidian-excalidraw-plugin:insert-link-to-element-frame-clipped"
    name: "Excalidraw: Copy 'clippedframe=' ![[link]] for selected element to clipboard."
  - id: "obsidian-excalidraw-plugin:insert-link-to-element-area"
    name: "Excalidraw: Copy 'area=' ![[link]] for selected element to clipboard."
  - id: "obsidian-excalidraw-plugin:toggle-lefthanded-mode"
    name: "Excalidraw: Toggle left-handed mode"
  - id: "obsidian-excalidraw-plugin:toggle-enable-context-menu"
    name: "Excalidraw: Toggle enable context menu (helpful on Mobile devices)"
  - id: "obsidian-excalidraw-plugin:flip-image"
    name: "Excalidraw: Open the back-of-the-note for the selected image in a popout window (flip the card)"
  - id: "obsidian-excalidraw-plugin:duplicate-image"
    name: "Excalidraw: Duplicate selected image with a different image ID"
  - id: "obsidian-excalidraw-plugin:reset-image-to-100"
    name: "Excalidraw: Set selected image element size to 100% of original"
  - id: "obsidian-excalidraw-plugin:reset-image-ar"
    name: "Excalidraw: Reset selected image element aspect ratio"
  - id: "obsidian-excalidraw-plugin:open-link-props"
    name: "Excalidraw: Open the image-link or LaTeX-formula editor"
  - id: "obsidian-excalidraw-plugin:convert-card-to-file"
    name: "Excalidraw: Move back-of-note card to File"
  - id: "obsidian-excalidraw-plugin:insert-active-pdfpage"
    name: "Excalidraw: Insert active PDF page as image"
  - id: "obsidian-excalidraw-plugin:crop-image"
    name: "Excalidraw: Crop and mask image"
  - id: "obsidian-excalidraw-plugin:annotate-image"
    name: "Excalidraw: Annotate image in Excalidraw"
  - id: "obsidian-excalidraw-plugin:insert-image"
    name: "Excalidraw: Insert image or Excalidraw drawing from your vault"
  - id: "obsidian-excalidraw-plugin:import-svg"
    name: "Excalidraw: Import an SVG file as Excalidraw strokes (limited SVG support, TEXT currently not supported)"
  - id: "obsidian-excalidraw-plugin:release-notes"
    name: "Excalidraw: Read latest release notes"
  - id: "obsidian-excalidraw-plugin:tray-mode"
    name: "Excalidraw: Toggle UI-mode"
  - id: "obsidian-excalidraw-plugin:insert-md"
    name: "Excalidraw: Insert markdown file from vault"
  - id: "obsidian-excalidraw-plugin:insert-pdf"
    name: "Excalidraw: Insert last active PDF page as image"
  - id: "obsidian-excalidraw-plugin:universal-add-file"
    name: "Excalidraw: Insert ANY file"
  - id: "obsidian-excalidraw-plugin:universal-card"
    name: "Excalidraw: Add back-of-note card"
  - id: "obsidian-excalidraw-plugin:insert-LaTeX-symbol"
    name: "Excalidraw: Insert LaTeX formula (e.g. \binom{n}{k} = \frac{n!}{k!(n-k)!})."
  - id: "obsidian-excalidraw-plugin:toggle-excalidraw-view"
    name: "Excalidraw: Toggle between Excalidraw and Markdown mode"
  - id: "obsidian-excalidraw-plugin:convert-to-excalidraw"
    name: "Excalidraw: Convert markdown note to Excalidraw Drawing"
  - id: "obsidian-excalidraw-plugin:convert-excalidraw"
    name: "Excalidraw: Convert *.excalidraw to *.md files"
---

# Excalidraw

**Description:** Sketch Your Mind. Edit and view Excalidraw drawings. Enter the world of 4D Visual PKM.
**Status:** Enabled
**Plugin ID:** obsidian-excalidraw-plugin

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `obsidian-excalidraw-plugin:excalidraw-convert-image-from-url-to-local-file` -- Excalidraw: Save image from URL to local file
- `obsidian-excalidraw-plugin:excalidraw-unzip-file` -- Excalidraw: Decompress current Excalidraw file
- `obsidian-excalidraw-plugin:excalidraw-publish-svg-check` -- Excalidraw: Obsidian Publish: Find SVG and PNG exports that are out of date
- `obsidian-excalidraw-plugin:excalidraw-embeddable-poroperties` -- Excalidraw: Embeddable Properties
- `obsidian-excalidraw-plugin:excalidraw-embeddables-relative-scale` -- Excalidraw: Scale selected embeddable elements to 100% relative to the current canvas zoom
- `obsidian-excalidraw-plugin:open-image-excalidraw-source` -- Excalidraw: Open Excalidraw drawing
- `obsidian-excalidraw-plugin:excalidraw-disable-autosave` -- Excalidraw: Disable autosave until next time Obsidian starts (only set this if you know what you are doing)
- `obsidian-excalidraw-plugin:excalidraw-enable-autosave` -- Excalidraw: Enable autosave
- `obsidian-excalidraw-plugin:excalidraw-toggle-session-view-mode` -- Excalidraw: Toggle view mode for all Excalidraw drawings until Obsidian restarts
- `obsidian-excalidraw-plugin:excalidraw-download-lib` -- Excalidraw: Export stencil library as an *.excalidrawlib file
- `obsidian-excalidraw-plugin:excalidraw-open-sidepanel` -- Excalidraw: Open Excalidraw Sidepanel
- `obsidian-excalidraw-plugin:excalidraw-open` -- Excalidraw: Open existing drawing - IN A NEW PANE
- `obsidian-excalidraw-plugin:excalidraw-open-on-current` -- Excalidraw: Open existing drawing - IN THE CURRENT ACTIVE PANE
- `obsidian-excalidraw-plugin:excalidraw-insert-transclusion` -- Excalidraw: Embed a drawing
- `obsidian-excalidraw-plugin:excalidraw-insert-last-active-transclusion` -- Excalidraw: Embed the most recently edited drawing
- `obsidian-excalidraw-plugin:excalidraw-autocreate` -- Excalidraw: Create new drawing - IN AN ADJACENT WINDOW
- `obsidian-excalidraw-plugin:excalidraw-autocreate-newtab` -- Excalidraw: Create new drawing - IN A NEW TAB
- `obsidian-excalidraw-plugin:excalidraw-autocreate-on-current` -- Excalidraw: Create new drawing - IN THE CURRENT ACTIVE WINDOW
- `obsidian-excalidraw-plugin:excalidraw-autocreate-popout` -- Excalidraw: Create new drawing - IN A POPOUT WINDOW
- `obsidian-excalidraw-plugin:excalidraw-autocreate-and-embed` -- Excalidraw: Create new drawing - IN AN ADJACENT WINDOW - and embed into active document
- `obsidian-excalidraw-plugin:excalidraw-autocreate-and-embed-new-tab` -- Excalidraw: Create new drawing - IN A NEW TAB - and embed into active document
- `obsidian-excalidraw-plugin:excalidraw-autocreate-and-embed-on-current` -- Excalidraw: Create new drawing - IN THE CURRENT ACTIVE WINDOW - and embed into active document
- `obsidian-excalidraw-plugin:excalidraw-autocreate-and-embed-popout` -- Excalidraw: Create new drawing - IN A POPOUT WINDOW - and embed into active document
- `obsidian-excalidraw-plugin:run-ocr` -- Excalidraw: OCR full drawing: Grab text from freedraw + images to clipboard and doc.props
- `obsidian-excalidraw-plugin:rerun-ocr` -- Excalidraw: OCR full drawing re-run: Grab text from freedraw + images to clipboard and doc.props
- `obsidian-excalidraw-plugin:run-ocr-selectedelements` -- Excalidraw: OCR selected elements: Grab text from freedraw + images to clipboard
- `obsidian-excalidraw-plugin:search-text` -- Excalidraw: Search for text in drawing
- `obsidian-excalidraw-plugin:fullscreen` -- Excalidraw: Toggle fullscreen mode
- `obsidian-excalidraw-plugin:disable-binding` -- Excalidraw: Toggle to invert default binding behavior
- `obsidian-excalidraw-plugin:disable-framerendering` -- Excalidraw: Toggle frame rendering
- `obsidian-excalidraw-plugin:frame-settings` -- Excalidraw: Frame Settings
- `obsidian-excalidraw-plugin:copy-link-to-drawing` -- Excalidraw: Copy ![[embed link]] for this drawing
- `obsidian-excalidraw-plugin:disable-frameclipping` -- Excalidraw: Toggle frame clipping
- `obsidian-excalidraw-plugin:export-image` -- Excalidraw: Export Image
- `obsidian-excalidraw-plugin:save` -- Excalidraw: Save (will also update transclusions)
- `obsidian-excalidraw-plugin:toggle-lock` -- Excalidraw: Toggle Text Element between edit RAW and PREVIEW
- `obsidian-excalidraw-plugin:scriptengine-store` -- Excalidraw: Install or update Excalidraw Scripts
- `obsidian-excalidraw-plugin:delete-file` -- Excalidraw: Delete selected image or Markdown file from Obsidian Vault
- `obsidian-excalidraw-plugin:convert-text2MD` -- Excalidraw: Convert to file...
- `obsidian-excalidraw-plugin:insert-link` -- Excalidraw: Insert link to file
- `obsidian-excalidraw-plugin:insert-command` -- Excalidraw: Insert Obsidian Command as a link
- `obsidian-excalidraw-plugin:insert-link-to-element` -- Excalidraw: Copy [[link]] for selected element to clipboard.
- `obsidian-excalidraw-plugin:insert-link-to-element-group` -- Excalidraw: Copy 'group=' ![[link]] for selected element to clipboard.
- `obsidian-excalidraw-plugin:insert-link-to-element-frame` -- Excalidraw: Copy 'frame=' ![[link]] for selected element to clipboard.
- `obsidian-excalidraw-plugin:insert-link-to-element-frame-clipped` -- Excalidraw: Copy 'clippedframe=' ![[link]] for selected element to clipboard.
- `obsidian-excalidraw-plugin:insert-link-to-element-area` -- Excalidraw: Copy 'area=' ![[link]] for selected element to clipboard.
- `obsidian-excalidraw-plugin:toggle-lefthanded-mode` -- Excalidraw: Toggle left-handed mode
- `obsidian-excalidraw-plugin:toggle-enable-context-menu` -- Excalidraw: Toggle enable context menu (helpful on Mobile devices)
- `obsidian-excalidraw-plugin:flip-image` -- Excalidraw: Open the back-of-the-note for the selected image in a popout window (flip the card)
- `obsidian-excalidraw-plugin:duplicate-image` -- Excalidraw: Duplicate selected image with a different image ID
- `obsidian-excalidraw-plugin:reset-image-to-100` -- Excalidraw: Set selected image element size to 100% of original
- `obsidian-excalidraw-plugin:reset-image-ar` -- Excalidraw: Reset selected image element aspect ratio
- `obsidian-excalidraw-plugin:open-link-props` -- Excalidraw: Open the image-link or LaTeX-formula editor
- `obsidian-excalidraw-plugin:convert-card-to-file` -- Excalidraw: Move back-of-note card to File
- `obsidian-excalidraw-plugin:insert-active-pdfpage` -- Excalidraw: Insert active PDF page as image
- `obsidian-excalidraw-plugin:crop-image` -- Excalidraw: Crop and mask image
- `obsidian-excalidraw-plugin:annotate-image` -- Excalidraw: Annotate image in Excalidraw
- `obsidian-excalidraw-plugin:insert-image` -- Excalidraw: Insert image or Excalidraw drawing from your vault
- `obsidian-excalidraw-plugin:import-svg` -- Excalidraw: Import an SVG file as Excalidraw strokes (limited SVG support, TEXT currently not supported)
- `obsidian-excalidraw-plugin:release-notes` -- Excalidraw: Read latest release notes
- `obsidian-excalidraw-plugin:tray-mode` -- Excalidraw: Toggle UI-mode
- `obsidian-excalidraw-plugin:insert-md` -- Excalidraw: Insert markdown file from vault
- `obsidian-excalidraw-plugin:insert-pdf` -- Excalidraw: Insert last active PDF page as image
- `obsidian-excalidraw-plugin:universal-add-file` -- Excalidraw: Insert ANY file
- `obsidian-excalidraw-plugin:universal-card` -- Excalidraw: Add back-of-note card
- `obsidian-excalidraw-plugin:insert-LaTeX-symbol` -- Excalidraw: Insert LaTeX formula (e.g. \binom{n}{k} = \frac{n!}{k!(n-k)!}).
- `obsidian-excalidraw-plugin:toggle-excalidraw-view` -- Excalidraw: Toggle between Excalidraw and Markdown mode
- `obsidian-excalidraw-plugin:convert-to-excalidraw` -- Excalidraw: Convert markdown note to Excalidraw Drawing
- `obsidian-excalidraw-plugin:convert-excalidraw` -- Excalidraw: Convert *.excalidraw to *.md files

## Configuration File

Settings path: `.obsidian/plugins/obsidian-excalidraw-plugin/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/obsidian-excalidraw-plugin/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/obsidian-excalidraw-plugin/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Current Configuration

These are the plugin's current settings (sensitive values redacted):

```
copyLinkToElemenetAnchorTo100: false
copyFrameLinkByName: false
disableDoubleClickTextEditing: false
phoneFooterSafeAreaPadding: false
folder: Excalidraw
embedUseExcalidrawFolder: false
templateFilePath: Excalidraw/Template.excalidraw
scriptFolderPath: Excalidraw/Scripts
fontAssetsPath: Excalidraw/CJK Fonts
loadChineseFonts: false
loadJapaneseFonts: false
loadKoreanFonts: false
compress: true
decompressForMDView: false
autosave: true
autosaveIntervalDesktop: 60000
autosaveIntervalMobile: 30000
drawingFilenamePrefix: Drawing 
drawingEmbedPrefixWithFilename: true
drawingFilnameEmbedPostfix:  
drawingFilenameDateTime: YYYY-MM-DD HH.mm.ss
useExcalidrawExtension: true
cropPrefix: cropped_
annotatePrefix: annotated_
annotatePreserveSize: false
displaySVGInPreview: false
previewImageType: SVG
renderingConcurrency: 3
imageCacheRetentionDays: 30
allowImageCache: true
allowImageCacheInScene: true
displayExportedImageIfAvailable: false
previewMatchObsidianTheme: false
width: 400
overrideObsidianFontSize: false
dynamicStyling: colorful
isLeftHanded: false
desktopUIMode: tray
tabletUIMode: compact
phoneUIMode: mobile
iframeMatchExcalidrawTheme: true
matchTheme: false
matchThemeAlways: false
matchThemeTrigger: false
defaultMode: normal
defaultPenMode: never
penModeDoubleTapEraser: true
penModeSingleFingerPanning: true
penModeCrosshairVisible: true
panWithRightMouseButton: false
renderImageInMarkdownReadingMode: false
renderImageInHoverPreviewForMDNotes: false
renderImageInMarkdownToPDF: false
allowPinchZoom: false
allowWheelZoom: false
zoomToFitOnOpen: true
zoomToFitOnResize: false
zoomToFitMaxLevel: 2
zoomStep: 0.05
zoomMin: 0.1
zoomMax: 30
linkPrefix: 📍
urlPrefix: 🌐
parseTODO: false
todo: ☐
done: 🗹
hoverPreviewWithoutCTRL: false
linkOpacity: 1
openInAdjacentPane: true
showSecondOrderLinks: true
focusOnFileTab: true
openInMainWorkspace: true
showLinkBrackets: false
syncElementLinkWithText: false
allowCtrlClick: true
forceWrap: false
pageTransclusionCharLimit: 200
wordWrappingDefault: 0
removeTransclusionQuoteSigns: true
oEmbedAllowed: false
pngExportScale: 1
exportWithTheme: true
exportWithBackground: true
exportPaddingSVG: 10
exportEmbedScene: false
keepInSync: false
autoexportSVG: false
autoexportPNG: false
autoExportLightAndDark: false
autoexportExcalidraw: false
embedType: excalidraw
embedMarkdownCommentLinks: true
embedWikiLink: true
embedPlaceholderImage: true
syncExcalidraw: false
experimentalFileType: false
experimentalFileTag: ✏️
experimentalLivePreview: true
fadeOutExcalidrawMarkup: false
loadPropertySuggestions: false
experimentalEnableFourthFont: false
experimantalFourthFont: Virgil
addDummyTextElement: false
zoteroCompatibility: false
fieldSuggester: true
enableOnloadScripts: false
enableCommandLinks: false
compatibilityMode: false
drawingOpenCount: 0
library: deprecated
library2:
  type: excalidrawlib
  source: https://github.com/zsviczian/obsidian-excalidraw-plugin/releases/tag2.23.6
imageElementNotice: true
mdSVGwidth: 500
mdSVGmaxHeight: 800
mdFont: Virgil
mdFontColor: Black
mdBorderColor: Black
previousRelease: 2.23.6
showReleaseNotes: true
excalidrawMasteryPromoCollapsed: false
compareManifestToPluginVersion: true
showNewVersionNotification: true
latexBoilerplate: \color{green}e=mc^2
latexPreambleLocation: preamble.sty
taskboneEnabled: false
customPens: [10 items: {...}, {...}, {...}...]
numberOfCustomPens: 0
pdfScale: 4
pdfBorderBox: true
pdfFrame: false
pdfGapSize: 20
pdfGroupPages: false
pdfLockAfterImport: true
pdfNumColumns: 1
pdfNumRows: 1
pdfDirection: right
pdfImportScale: 0.3
gridSettings:
  DYNAMIC_COLOR: true
  COLOR: #000000
  OPACITY: 50
  GRID_DIRECTION:
    horizontal: true
    vertical: true
laserSettings:
  DECAY_LENGTH: 50
  DECAY_TIME: 1000
  COLOR: #ff0000
embeddableMarkdownDefaults:
  useObsidianDefaults: false
  backgroundMatchCanvas: false
  backgroundMatchElement: true
  backgroundColor: #fff
  backgroundOpacity: 60
  borderMatchElement: true
  borderColor: #fff
  borderOpacity: 0
  filenameVisible: false
markdownNodeOneClickEditing: false
canvasImmersiveEmbed: true
aiEnabled: true
aiVerboseLogging: false
aiProviderProfiles:
  OpenAI:
    provider: openai
    baseURL: https://api.openai.com/v1
  Anthropic:
    provider: anthropic
    baseURL: https://api.anthropic.com/v1
  Google Gemini:
    provider: google
    baseURL: https://generativelanguage.googleapis.com/v1beta
  xAI:
    provider: xai
    baseURL: https://api.x.ai/v1
  OpenAI-compatible:
    provider: openai-compatible
    baseURL: https://api.openai.com/v1
aiTextModelConfigs:
  gpt-5-mini:
    providerId: OpenAI
    model: gpt-5-mini
    multimodalSupport: true
  claude-sonnet-4-5:
    providerId: Anthropic
    model: claude-sonnet-4-5
    multimodalSupport: true
  gemini-2.5-pro:
    providerId: Google Gemini
    model: gemini-2.5-pro
    multimodalSupport: true
  grok-4-fast:
    providerId: xAI
    model: grok-4-fast
    multimodalSupport: true
aiImageModelConfigs:
  dall-e-2:
    providerId: OpenAI
    model: dall-e-2
    supportedSizes: [256x256, 512x512, 1024x1024]
    supportsPromptImageTransforms: true
    supportsMaskImageEdits: true
  dall-e-3:
    providerId: OpenAI
    model: dall-e-3
    supportedSizes: [1024x1024, 1792x1024, 1024x1792]
    supportsPromptImageTransforms: false
    supportsMaskImageEdits: false
  gpt-image-1:
    providerId: OpenAI
    model: gpt-image-1
    supportedSizes: [1024x1024, 1536x1024, 1024x1536]
    supportsPromptImageTransforms: true
    supportsMaskImageEdits: true
  gpt-image-1-mini:
    providerId: OpenAI
    model: gpt-image-1-mini
    supportedSizes: [1024x1024, 1536x1024, 1024x1536]
    supportsPromptImageTransforms: true
    supportsMaskImageEdits: true
  gpt-image-1.5:
    providerId: OpenAI
    model: gpt-image-1.5
    supportedSizes: [1024x1024, 1536x1024, 1024x1536]
    supportsPromptImageTransforms: true
    supportsMaskImageEdits: true
  gpt-image-2:
    providerId: OpenAI
    model: gpt-image-2
    supportedSizes: [1024x1024, 1536x1024, 1024x1536, 2048x2048]
    supportsPromptImageTransforms: true
    supportsMaskImageEdits: true
  gemini-2.5-flash-image:
    providerId: Google Gemini
    model: gemini-2.5-flash-image
    supportedSizes: [1024x1024]
    supportsPromptImageTransforms: true
    supportsMaskImageEdits: false
  gemini-3.1-flash-image-preview:
    providerId: Google Gemini
    model: gemini-3.1-flash-image-preview
    supportedSizes: [1024x1024]
    supportsPromptImageTransforms: true
    supportsMaskImageEdits: false
  gemini-3-pro-image-preview:
    providerId: Google Gemini
    model: gemini-3-pro-image-preview
    supportedSizes: [1024x1024]
    supportsPromptImageTransforms: true
    supportsMaskImageEdits: false
  grok-imagine-image-quality:
    providerId: xAI
    model: grok-imagine-image-quality
    supportedSizes: [1024x1024]
    supportsPromptImageTransforms: true
    supportsMaskImageEdits: false
  grok-imagine-image-pro:
    providerId: xAI
    model: grok-imagine-image-pro
    supportedSizes: [1024x1024]
    supportsPromptImageTransforms: true
    supportsMaskImageEdits: false
aiDefaultTextModel: gpt-5-mini
aiDefaultImageGenerationModel: gpt-image-1
modifierKeyConfig:
  Mac:
    LocalFileDragAction:
      defaultAction: image-import
      rules: [4 items]
    WebBrowserDragAction:
      defaultAction: image-url
      rules: [4 items]
    InternalDragAction:
      defaultAction: link
      rules: [4 items]
    LinkClickAction:
      defaultAction: new-tab
      rules: [5 items]
  Win:
    LocalFileDragAction:
      defaultAction: image-import
      rules: [4 items]
    WebBrowserDragAction:
      defaultAction: image-url
      rules: [4 items]
    InternalDragAction:
      defaultAction: link
      rules: [4 items]
    LinkClickAction:
      defaultAction: new-tab
      rules: [5 items]
slidingPanesSupport: false
areaZoomLimit: 1
longPressDesktop: 500
longPressMobile: 500
doubleClickLinkOpenViewMode: true
rank: Bronze
modifierKeyOverrides: [3 items]
showSplashscreen: true
pdfS
[...truncated -- full settings in data.json]
```
(8 sensitive field(s) redacted)

For full settings, read: `.obsidian/plugins/obsidian-excalidraw-plugin/data.json`

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/plugin-skills/obsidian-excalidraw-plugin.readme.md")

## Usage

When the user asks for functionality related to Excalidraw:
1. Read the plugin documentation (.readme.md) to understand capabilities and dependencies
2. Read the config file (.obsidian/plugins/obsidian-excalidraw-plugin/data.json). If it does not exist, that is normal -- create it with the required settings
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
