Now I have the full picture. Three things need to change.

---

The card visual — `image / name` — is **not a rofi text element**. It's a single composite PNG baked by ImageMagick, used as the icon. The rasi itself has `element-text { enabled: false; }`. Rofi is just showing a grid of images.

Your script already attempts this card composite, but the split is flat (`+append`). Hyde's split is **diagonal**. Also, the rasi needs a three-layer color setup (Hyde's actual pattern) rather than hardcoded colors.

---

## Fix 1 — Three-layer rofi color setup

| Wilber Here: We need this to use a different border scheme than default rofi which is designed to be no border -- remember this

Hyde separates colors from layout. You need a shared color file that matugen regenerates on wallpaper change, and the selector rasi files just import it.

**Create `~/.config/rofi/theme.rasi`** (this is what matugen should write to):

```rasi
* {
    main-bg:        #11111be6;
    main-fg:        #cdd6f4ff;
    main-br:        #cba6f7ff;
    main-ex:        #f5e0dcff;
    select-bg:      #b4befe80;
    select-fg:      #11111bff;
    border-color:   transparent;
    separatorcolor: transparent;
}
```

Point matugen at this file as its rofi output target. After that, every rofi session auto-picks up the current wallpaper's colors without touching your selector rasi files.

---

## Fix 2 — Updated rasi files (import colors, no hardcoding)

**`theme-selector.rasi`:**

```rasi
@theme "~/.config/rofi/theme.rasi"

configuration {
    show-icons: true;
    font: "JetBrainsMono Nerd Font 11";
}

window {
    transparency:       "real";
    background-color:   @main-bg;
    fullscreen:         true;
    cursor:             "default";
}

mainbox {
    background-color:   transparent;
    padding:            24% 5%;
    children:           [ "listview" ];
}

listview {
    layout:             horizontal;
    spacing:            20px;
    padding:            20px;
    background-color:   transparent;
    fixed-height:       false;
    dynamic:            true;
    scrollbar:          false;
}

element {
    orientation:        vertical;
    cursor:             pointer;
    background-color:   transparent;
    border-radius:      14px;
    padding:            6px;
}

element selected {
    background-color:   @select-bg;
}

element-icon {
    size:               20em;
    border-radius:      12px;
    cursor:             inherit;
}

element-text {
    enabled:            false;   /* name is baked into the card image */
}
```

**`wallpaper-grid.rasi`:**

```rasi
@theme "~/.config/rofi/theme.rasi"

configuration {
    show-icons: true;
    font: "JetBrainsMono Nerd Font 11";
}

window {
    transparency:       "real";
    background-color:   @main-bg;
    fullscreen:         true;
    cursor:             "default";
}

mainbox {
    background-color:   transparent;
    padding:            18% 5%;
    spacing:            14px;
    children:           [ "message", "listview" ];
    orientation:        vertical;
}

message {
    background-color:   transparent;
}

textbox {
    background-color:   transparent;
    text-color:         @main-fg;
    horizontal-align:   0.5;
}

listview {
    layout:             horizontal;
    spacing:            16px;
    padding:            20px;
    background-color:   transparent;
    fixed-height:       false;
    dynamic:            true;
    scrollbar:          false;
}

element {
    orientation:        vertical;
    cursor:             pointer;
    background-color:   transparent;
    border-radius:      14px;
    padding:            6px;
    spacing:            8px;
}

element selected {
    background-color:   @select-bg;
    border-radius:      14px;
}

element-icon {
    size:               12em;
    border-radius:      12px;
    cursor:             inherit;
}

element-text {
    enabled:            true;
    vertical-align:     0.5;
    horizontal-align:   0.5;
    text-color:         @main-fg;
    cursor:             inherit;
    padding:            2px 0;
}
```

---

## Fix 3 — Diagonal card composite (the actual `Image / name` split)

In `ensure_theme_thumbnails`, replace the card generation block (the `magick ... +append` section) with this:

```bash
local card_file="${thumb_dir}/${name}.card.png"
local dominant
dominant=$(magick "$thumb_file" -resize 1x1 -format '%[pixel:p{0,0}]' info: 2>/dev/null || echo "#2a2a3e")

# Card: 600x300 landscape
# Diagonal mask: wallpaper on left, color+name on right
# Polygon cuts from (360,0) to (240,300) — ~20° angle
nice -n 19 magick \
    \( "$thumb_file" -resize 600x300^ -gravity center -extent 600x300 \) \
    \( -size 600x300 "xc:${dominant}" \
       -font JetBrainsMono-NF-Regular -pointsize 20 \
       -fill white -gravity East -annotate +40+0 "$name" \) \
    \( -size 600x300 xc:black -fill white \
       -draw "polygon 0,0 360,0 240,300 0,300" \) \
    -composite \
    "$card_file" 2>/dev/null || true
```

The polygon `0,0 → 360,0 → 240,300 → 0,300` is the diagonal mask. It means:

- Top of card: wallpaper covers left 60%
- Bottom of card: wallpaper covers left 40%
- The angled cut creates the `/` slash effect

Adjust those X values to change the angle — wider gap = steeper slash.

---

## Fix 4 — Hash bug (still needed, from before)

In `show_wallpaper_grid`, line 422:

```bash
# Change this:
digest=$(printf "%s" "$(basename "$file")" | sha256sum | cut -d" " -f1)

# To this:
digest=$(printf "%s" "$file" | sha256sum | cut -d" " -f1)
```

---

## After all changes

```bash
# Force regenerate everything
theme-selector.sh --prune-cache

# Test the card looks right before launching
ls ~/.cache/theme-selector/theme-thumbs/Dark/
# Should see both *.png (plain thumb) and *.card.png (composite)
```

The `run_rofi -config /dev/null` in your script already matches Hyde's pattern — it ignores system rofi defaults and relies entirely on whatever `-theme` you pass in. The `@theme` import in the rasi files is what hooks into that shared color layer.