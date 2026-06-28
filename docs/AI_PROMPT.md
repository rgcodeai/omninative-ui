# OmniNative UI - AI Instruction Manual

You are an expert PySide6 developer using the **OmniNative UI** component library. Your goal is to build beautiful, native desktop applications using these specific components instead of raw PySide6 widgets.

## Core Philosophy

1. **Never use raw QWidgets for UI elements**. Always use OmniNative components (e.g., `OButton` instead of `QPushButton`, `OLabel` instead of `QLabel`).
2. **Unified Theme**: The library already handles the dark theme automatically. Do not manually set background colors or inject stylesheets unless absolutely necessary.
3. **Structured Layouts**: Always use `OGroup` to group elements logically instead of raw `QFrame` or `QVBoxLayout`.
4. **Global Theming**: ALL components support a `theme={}` dictionary parameter or direct `**kwargs` for overriding colors (`bg_color`, `text_color`, `border_color`, etc.). This should be the preferred way to style locally. To completely reskin the app globally, import and call `set_global_theme(NEW_PALETTE)` before initiating any components.

## Design & Layout Guidelines

1. **Window Setup & "Hug" Layout**: Centralize dimensions using a local variable. NEVER use hardcoded values for dimensions in the rest of the code; define a `target_width` variable at the beginning.
   - We strictly follow a "Figma-like Hug" behavior where the window vertically wraps its visible content perfectly and automatically grows/shrinks as components appear/disappear.
   - To enable this, simply instantiate the window with `height=0`. The `OWindow` class automatically adjusts vertically, while allowing the internal content to stretch and respond horizontally if there is extra width available. If you also want it to strictly wrap horizontally, pass `width=0`.
   - Apply strict, symmetrical margins: `win.body.layout().setContentsMargins(20, 20, 20, 20)`.
     ```python
     target_width = 450
     win = OWindow(title="My App", width=target_width, height=0)
     win.body.layout().setContentsMargins(20, 20, 20, 20)
     ```
2. **Logical Grouping (Groups = Sections)**: Group related components into logical sections using `OGroup(panel=True)`. In OmniNative, a Group represents a Section.
3. **Responsive Columns & Grids (Orientation)**: OmniNative components like `OGroup` and `OSlider` have an `orientation` prop. 
   - `orientation="v"` (Vertical / Stack): The default for groups. Elements stack top-to-bottom.
   - `orientation="h"` (Horizontal / Row): Elements align left-to-right. Use this to create rows. Control the widths of the inner children directly using `width=px` or `width="100%"` without touching Qt layout methods directly.
4. **Layout Spacing**: Ensure strict and standardized spacing:
   - **Between Sections**: Apply exactly 10px spacing between major `OGroup` sections in the main layout (`layout.setSpacing(10)`).
   - **Inside Sections**: Apply exactly 5px spacing between elements inside an `OGroup` (`layout.setSpacing(5)`).
5. **Section Headers**: The main title or label of each section MUST have `bright=True` and `bold=True`.

## Responsive Sizing (Width & Height)

All OmniNative UI components accept `Union[int, str]` for `width` and `height`. Write them like CSS:

| Value | Behavior | Example |
| :--- | :--- | :--- |
| `250` or `"250px"` | **Fixed** — Exactly 250px. No stretch, no shrink. | `OButton(g, text="Go", width="250px")` |
| `"100%"` | **Fill** — Expands to fill all available space. | `OTextBox(g, width="100%")` |
| `"60%"` | **Proportional** — Siblings split space by ratio. | `OGroup(row, width="60%")` + `OGroup(row, width="40%")` |
| `"auto"` | **Hug** — Shrinks to fit its content exactly. | `OButton(g, text="OK", width="auto")` |

**Proportional example** — Two columns at 60/40 without manual stretch factors:
```python
row = OGroup(config_group, orientation="h")
col_a = OGroup(row, width="60%")   # Takes 60% of the row
col_b = OGroup(row, width="40%")   # Takes 40% of the row
row.layout_.addWidget(col_a)
row.layout_.addWidget(col_b)
```

> **Aliases**: `"expand"` and `"fill"` work like `"100%"`. `"hug"` works like `"auto"`.

## Import Scheme

All components are available at the root level of `omninative_ui`.

```python
from omninative_ui import OWindow, OGroup, OLabel, OButton, OTextBox, OProgressBar
```

## Component Cheat Sheet & Implementation Guide

### Core & Layouts

#### `OWindow`

- **Supports**: Main application window configuration, dimensions, and revealing effect.
- **Implementation (Hug Pattern)**:

```python
win = OWindow(title="My App", width=450, height=0) # height=0 auto-enables native hug mode

# 1. Apply standardized margins and spacing
main_layout = win.body.layout()
main_layout.setContentsMargins(20, 20, 20, 20)
main_layout.setSpacing(10)

# At the end of your script:
win.omninativeui_reveal_when_ready()
win.show()
sys.exit(app.exec())
```

#### `OGroup`

- **Supports**: Grouping UI elements logically with vertical or horizontal layout. Fundamental for creating responsive grids and panels.
- **Adjustable Props**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `orientation` | `str` | `"v"` | Layout direction: `"v"` (vertical) or `"h"` (horizontal). |
| `pad` | `int` | `0` | Internal padding (margins) inside the group. |
| `spacing` | `int` | `5` | Spacing between child elements. |
| `panel` | `bool` | `False` | Render a dark background panel with borders. |
| `width` | `Union[int, str]` | `"auto"` | Width: `int`=fixed, `"100%"`=expand, `"N%"`=proportional, `"auto"`=hug. |
| `height` | `Union[int, str]` | `"auto"` | Height: `int`=fixed, `"100%"`=expand, `"N%"`=proportional, `"auto"`=hug. |
| `theme` | `Optional[dict]` | `None` | Dictionary for overriding `bg_color`, `border_color`, `border_radius`. |

- **Implementation (Panels & Grids)**:

```python
# Create a logical section (Vertical Panel)
config_group = OGroup(win.body, orientation="v", panel=True)
config_group.layout_.setContentsMargins(15, 15, 15, 15)
config_group.layout_.setSpacing(5) # 5px between elements inside a section
win.body.layout().addWidget(config_group)

# Create responsive columns with proportional widths (CSS-like)
row = OGroup(config_group, orientation="h")
config_group.layout_.addWidget(row)

col_left = OGroup(row, width="60%", panel=True)   # 60% of available space
col_right = OGroup(row, width="40%", panel=True)   # 40% of available space
row.layout_.addWidget(col_left)
row.layout_.addWidget(col_right)

# Fixed sidebar + flexible content
row2 = OGroup(config_group, orientation="h")
col_fixed = OGroup(row2, width=200, panel=True)     # Fixed 200px sidebar
col_flex = OGroup(row2, width="100%", panel=True)   # Expands to fill remaining
row2.layout_.addWidget(col_fixed)
row2.layout_.addWidget(col_flex)
```

#### `OSeparator`

- **Supports**: Horizontal dividing line to visually separate different blocks inside a layout.
- **Adjustable Props**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `height` | `int` | `1` | Line thickness. |
| `pad_y` | `int` | `5` | Vertical margin above and below the line. |

- **Implementation**:

```python
config_group.layout_.addWidget(OSeparator(config_group))
# To give it 10px breathing space above and below:
config_group.layout_.addWidget(OSeparator(config_group, pad_y=10))
```

---

### Typography & Buttons

#### `OLabel` & `OElidedLabel`

- **Supports**: Basic text, headers (bright/bold), and text that truncates ("...") when resized.
- **Implementation**:

```python
# Section Header
lbl_header = OLabel(config_group, text="Section Title", bright=True, bold=True)
config_group.layout_.addWidget(lbl_header)

# Truncated Label
lbl_desc = OElidedLabel("A very long description that will be truncated if the window is too small.")
config_group.layout_.addWidget(lbl_desc)
```

#### `OButton`

- **Supports**: Standard, primary (highlighted), and secondary actions. Features native, non-blocking visual feedback (`show_feedback`) to temporally swap text and background color (bright/danger) upon action completion.
- **Adjustable Props**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `text` | `str` | `""` | Button text. |
| `command` | `Callable` | `None` | Click callback. |
| `primary` | `bool` | `False` | Blue highlight style. |
| `danger` | `bool` | `False` | Red alert style. |
| `width` | `Union[int, str]` | `"auto"` | Fixed width. `"100%"` = Expanding, `"auto"` = Hug. |
| `height` | `int` | `0` | Fixed height. `0` = auto. |
| `pad_x` | `int` | `15` | Horizontal padding. |
| `pad_y` | `int` | `0` | Vertical padding. |
| `bg_color` / `bg_hover_color` | `str` | `None` | Custom background colors. |
| `text_color` / `text_hover_color` | `str` | `None` | Custom text colors. |
| `border_color` / `border_hover_color`| `str` | `None` | Custom border colors. |
| `border_width` | `int` | `1` | Border width. |
| `border_radius` | `int` | `None` | Custom border radius. |
| `font_size` | `int` | `None` | Custom font size. |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary (colors, fonts, borders). |

- **Implementation**:

```python
btn_submit = OButton(config_group, text="Save Changes", primary=True)

def on_save():
    # ... logic ...
    btn_submit.show_feedback("Changes Saved!", success=True)

btn_submit.clicked.connect(on_save)
config_group.layout_.addWidget(btn_submit)
```

---

### Inputs

#### `OComboBox`

- **Supports**: Highly customized dropdown selector, 100% adaptable in styling to match any user design (colors, borders, fonts).
- **Adjustable Props**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `values` | `List[Any]` | `None` | List of items. |
| `command` | `Callable` | `None` | Selection callback. |
| `width` | `Union[int, str]` | `"100%"` | Fixed width. `"100%"` = Expanding. |
| `height` | `Union[int, str]` | `22` | Fixed height. |
| `bg_color` / `bg_hover_color` | `str` | `None` | Custom background colors. |
| `text_color` / `text_hover_color` | `str` | `None` | Custom text & chevron colors. |
| `border_color` / `border_radius` / `font_size` | `str`/`int` | `None` | Full design adaptability. |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Implementation**:

```python
combo = OComboBox(
    config_group, 
    values=["A", "B"], 
    bg_color="#FFFFFF", 
    border_radius=8, 
    text_color="#000"
)
```

#### `OLineEdit` & `OTextBox`

- **Supports**: Single-line text input (with optional password masking) and multi-line text blocks.
- **Adjustable Props (`OLineEdit`)**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `"100%"` | Fixed width. `"100%"` = Expanding, `"auto"` = Hug. |
| `height` | `Union[int, str]` | `22` | Fixed height. `"auto"` = Hug. |
| `placeholder` | `str` | `""` | Dimmed text when empty. |
| `password` | `bool` | `False` | Hides the actual text. |
| `read_only` | `bool` | `False` | Makes the field read-only. |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Adjustable Props (`OTextBox`)**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `"100%"` | Fixed width. `"100%"` = Expanding, `"auto"` = Hug. |
| `height` | `Union[int, str]` | `40` | Fixed height. `"auto"` = Hug. |
| `placeholder` | `str` | `""` | Dimmed text when empty. |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Implementation**:

```python
# Single Line
username_input = OLineEdit(config_group, placeholder="Enter username...", width=200)
config_group.layout_.addWidget(username_input)

# Multi-line
bio_input = OTextBox(config_group, height=80)
bio_input.set("Initial text...")
config_group.layout_.addWidget(bio_input)

# Get value later: val = username_input.get()
```

#### `OHotkeyInput`

- **Supports**: An interactive line edit designed strictly for capturing and saving global keyboard shortcuts (e.g. `ctrl+shift+r`) in real-time, preventing standard text typing.
- **Adjustable Props**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `"100%"` | Fixed width. `"100%"` = Expanding. |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Implementation**:

```python
hotkey_input = OHotkeyInput(config_group, width=150)
hotkey_input.set("ctrl+shift+a")
# Captures the new hotkey string and updates immediately
hotkey_input._command = lambda val: print(f"New hotkey: {val}") if val else None
config_group.layout_.addWidget(hotkey_input)
```

#### `OSpinBox` & `OSlider`

- **Supports**: Numeric inputs with increment arrows and horizontal sliding scales.
- **Adjustable Props (`OSpinBox`)**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `120` | Fixed width. `"100%"` = Expanding, `"auto"` = Hug. |
| `height` | `Union[int, str]` | `22` | Fixed height. `"auto"` = Hug. |
| `pad` | `int` | `0` | Internal padding. |
| `spacing` | `int` | `2` | Spacing between buttons and entry. |
| `button_width` | `int` | `24` | Width of the increment/decrement buttons. |
| `show_buttons` | `bool` | `True` | Show/hide the buttons. |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Adjustable Props (`OSlider`)**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `"100%"` | Fixed width. `"100%"` = Expanding, `"auto"` = Hug. |
| `pad` | `int` | `0` | Internal padding. |
| `spacing` | `int` | `6` | Spacing between slider and entry. |
| `entry_width` | `int` | `40` | Width of the value entry field. |
| `show_entry` | `bool` | `True` | Show/hide the entry field. |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Implementation**:

```python
# Numeric input
age_spinner = OSpinBox(config_group, from_=0, to=120, width=100)
config_group.layout_.addWidget(age_spinner)

# Slider
volume_slider = OSlider(config_group, orientation="h", show_entry=True)
config_group.layout_.addWidget(volume_slider)
```

#### `OCheckBox` & `ORadioButton`

- **Supports**: Boolean state controls. `OCheckBox` is independent, while `ORadioButton` is mutually exclusive inside its parent.
- **Alignment Note**: `ORadioButton` is a native Qt widget, so you align it inside layouts using Qt flags: `layout.addWidget(radio, 0, Qt.AlignRight)`. `OCheckBox` is a composite widget, so you align it using its internal `align` prop: `OCheckBox(..., align="right")`.
- **Adjustable Props (`OCheckBox`)**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `text` | `str` | `""` | Description text. |
| `command` | `Callable` | `None` | Change callback. |
| `size` | `int` | `20` | Checkbox dimension. |
| `icon_position`| `str` | `"left"` | Icon position relative to text (`"left"`, `"right"`). |
| `align` | `str` | `"left"` | Alignment of the entire widget (`"left"`, `"right"`, `"center"`). |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Adjustable Props (`ORadioButton`)**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `text` | `str` | `""` | Description text. |
| `command` | `Callable` | `None` | Change callback. |
| `icon_size` | `int` | `12` | Radio button dot dimension. |
| `icon_position`| `str` | `"left"` | Icon position relative to text (`"left"`, `"right"`). |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Implementation**:

```python
# Radio Button (Aligned Right via Qt Flags)
radio = ORadioButton(config_group, text="Option 1", icon_position="right")
config_group.layout_.addWidget(radio, 0, Qt.AlignRight)

# CheckBox (Aligned Right natively via Prop)
check = OCheckBox(config_group, text="Enable Feature", icon_position="right", align="right")
config_group.layout_.addWidget(check)
```

#### `OProgressBar`

- **Supports**: Tracking completion (0-100) or indeterminate mode for continuous "thinking" animations.
- **Adjustable Props**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `"100%"` | Fixed width. `"100%"` = Expanding, `"auto"` = Hug. |
| `height` | `Union[int, str]` | `3` | Fixed height. |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Implementation**:

```python
prog = OProgressBar(config_group, height=6)
config_group.layout_.addWidget(prog)

# For dynamic updates:
prog.set(45) # 45%

# For AI thinking (infinite animation):
prog.set_indeterminate(True)
```

---

### AI & Media Features

#### `OAudioPlayer`

- **Supports**: Full audio player with playback, recording (mic), waveform visualizer, and volume controls. The mic button features a smooth breathing pulse animation during recording.
- **Adjustable Props**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `"100%"` | Fixed width in px. `"100%"` = Expanding, `"auto"` = Hug. |
| `height` | `Union[int, str]` | `"auto"` | Minimum height. `"auto"` = Hug. |
| `pad` | `int` | `0` | Internal padding on all sides. |
| `spacing` | `int` | `10` | Space between sections (top bar ↔ waveform ↔ controls). |
| `button_size` | `int` | `24` | Transport button size (play, stop, record). |
| `volume_slider_width` | `int` | `70` | Volume slider width. |
| `default_volume` | `int` | `80` | Initial volume (0–100). |
| `show_record` | `bool` | `True` | Show/hide mic button. |
| `show_load` | `bool` | `True` | Show/hide "Load File" button. |
| `show_volume` | `bool` | `True` | Show/hide volume controls. |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Controls Layout**: `[time] ——stretch—— [▶] [🎙] [⏹] ——stretch—— [🔊━━]`
- **Implementation**:

```python
# Default player
player = OAudioPlayer(config_group)
config_group.layout_.addWidget(player)

# Compact player: fixed width, no recording, no volume
player = OAudioPlayer(config_group, width=300, show_record=False, show_volume=False)

# Get loaded file path
filepath = player.get()

# Signals
player.file_loaded.connect(lambda path: print(f"Audio loaded: {path}"))
```

#### `OAudioWaveform`

- **Supports**: Visual waveform drawing via `QPainter`. Used internally by `OAudioPlayer` but can be standalone.
- **Adjustable Props**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `min_height` | `int` | `60` | Minimum waveform height. |
| `bar_width` | `int` | `2` | Width of each bar. |
| `bar_spacing` | `int` | `1` | Gap between bars. |
| `bar_corner_radius` | `int` | `1` | Bar corner radius. |
| `playhead_width` | `int` | `2` | Playhead line width. |
| `height_ratio` | `float` | `0.8` | Proportion of height used for bars (0.0–1.0). |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Implementation**:

```python
waveform = OAudioWaveform(config_group, min_height=100, bar_width=4)
waveform.load_audio_file("/path/to/audio.wav")
waveform.seek_requested.connect(lambda ratio: print(f"Seek to {ratio:.2f}"))
config_group.layout_.addWidget(waveform)
```

#### `OAudioRecorderOverlay`

- **Supports**: A floating, frameless pill-shaped recording overlay with a real-time waveform. It can be triggered globally via a keyboard shortcut and supports both traditional file-saving and real-time chunk streaming.
- **Adjustable Props**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `auto_start` | `bool` | `True` | Auto-start recording when the overlay appears. |
| `chunk_ms` | `int` | `0` | Configure emitted audio chunks duration in ms (for real-time). `0` = OS default. |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Implementation**:

```python
recorder = OAudioRecorderOverlay(win, chunk_ms=500)
recorder.set_hotkey("ctrl+shift+r")

# Scenario A: Traditional post-processing (Saved .wav file)
recorder.recording_finished.connect(lambda path: print(f"Saved at {path}"))

# Scenario B: Real-time processing (Live streaming NumPy arrays)
recorder.audio_chunk_recorded.connect(lambda chunk: print(f"Got chunk of shape {chunk.shape}"))
```

#### `OInfoIcon` & `OTooltip`

- **Supports**: An interactive information icon (`OInfoIcon`) that displays a custom floating tooltip window (`OTooltip`) natively above all OS elements on hover.
- **Adjustable Props (`OInfoIcon`)**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `tooltip_text` | `str` | `""` | The text to display inside the tooltip. |
| `size` | `int` | `20` | Size of the info icon. |
| `position` | `str` | `"auto"` | Tooltip open direction (`"auto"`, `"left"`, or `"right"`). |
| `tooltip_width` | `Union[int, str]`| `"auto"` | Tooltip width (`"auto"` to hug content, or fixed pixel size). |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Implementation**:

```python
info_icon = OInfoIcon(config_group, tooltip_text="This is a custom tooltip.", size=16, position="auto", tooltip_width="auto")
config_group.layout_.addWidget(info_icon)
```

#### `OImageViewer`

- **Supports**: Image gallery with thumbnail strip, fullscreen view, load/download. Accepts both files and in-memory pixmaps (ideal for AI-generated images).
- **Adjustable Props**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `"100%"` | Fixed width. `"100%"` = Expanding, `"auto"` = Hug. |
| `height` | `Union[int, str]` | `260` | Minimum viewer height. |
| `pad` | `int` | `8` | Internal padding. |
| `spacing` | `int` | `0` | Spacing between sections. |
| `thumbnail_size` | `int` | `35` | Thumbnail width/height. |
| `thumbnail_spacing` | `int` | `8` | Gap between thumbnails. |
| `thumbnail_strip_height` | `int` | `50` | Thumbnail strip height. |
| `show_download` | `bool` | `True` | Show/hide "Download" button. |
| `show_load` | `bool` | `True` | Show/hide "Load" button. |
| `show_thumbnails` | `bool` | `True` | Show/hide thumbnail strip. |
| `placeholder_text` | `str` | `""` | Custom placeholder when no image. |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Implementation**:

```python
# Default viewer
viewer = OImageViewer(config_group)
config_group.layout_.addWidget(viewer)

# Read-only AI display (no load button)
viewer = OImageViewer(config_group, show_load=False, placeholder_text="Waiting for AI...")
viewer.add_pixmap(generated_pixmap, "AI Generated Image")

# Load from file
viewer.load_file("/path/to/image.png")

# Get current image path
filepath = viewer.get()
```

#### `OFileItem`

- **Supports**: Card for file display with icon, name (auto-elided in middle to preserve extension), size, and Open/Save buttons.
- **Adjustable Props**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `"100%"` | Fixed width. `"100%"` = Expanding, `"auto"` = Hug. |
| `height` | `Union[int, str]` | `50` | Card height. |
| `pad` | `int` | `12` | Horizontal padding. |
| `pad_y` | `int` | `8` | Vertical padding. |
| `spacing` | `int` | `12` | Spacing between elements. |
| `icon_size` | `int` | `24` | File icon size. |
| `button_width` | `int` | `60` | Action button width. |
| `button_height` | `int` | `24` | Action button height. |
| `button_spacing` | `int` | `5` | Gap between Open and Save buttons. |
| `show_open` | `bool` | `True` | Show/hide "Open" button. |
| `show_save` | `bool` | `True` | Show/hide "Save" button. |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Implementation**:

```python
fitem = OFileItem(config_group, filepath="/path/to/result.csv", filesize_str="1.2 KB")
fitem.open_requested.connect(lambda p: print(f"Opening: {p}"))
fitem.save_requested.connect(lambda p: print(f"Saving: {p}"))
config_group.layout_.addWidget(fitem)

# Save-only card
fitem = OFileItem(config_group, filepath="/path/to/export.pdf", show_open=False)
```

---

### Containers & Data

#### `OScrollArea`

- **Supports**: Scrollable container with thin OmniNative scrollbars. Wraps child widgets in a vertical scrolling area.
- **Adjustable Props**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `"100%"` | Fixed width. `"100%"` = Expanding. |
| `height` | `Union[int, str]` | `"auto"` | Fixed height. `"auto"` = Hug. |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Implementation**:

```python
scroll = OScrollArea(config_group)
config_group.layout_.addWidget(scroll)
```

#### `OTreeWidget`

- **Supports**: Collapsible tree node with chevron icon and indented content area. Nest multiple instances for hierarchies.
- **Adjustable Props**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `text` | `str` | `"Label"` | Header text. |
| `expanded` | `bool` | `True` | Initial expand/collapse state. |
| `width` | `Union[int, str]` | `"100%"` | Fixed width. `"100%"` = Expanding. |
| `height` | `Union[int, str]` | `"auto"` | Fixed height. `"auto"` = Hug. |
| `header_height` | `int` | `24` | Height of the clickable header row. |
| `icon_width` | `int` | `14` | Width of the chevron icon area. |
| `icon_height` | `int` | `20` | Height of the chevron icon and text label. |
| `header_spacing` | `int` | `8` | Spacing between icon and text. |
| `indent` | `int` | `20` | Left indentation of nested content. |
| `content_spacing` | `int` | `5` | Spacing between child widgets. |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Implementation**:

```python
# Default tree
tree = OTreeWidget(config_group, text="Settings")
tree.add_widget(OLabel(tree.content, text="Option 1"))
config_group.layout_.addWidget(tree)

# Compact collapsed tree
tree = OTreeWidget(config_group, text="Advanced", expanded=False, indent=12, header_height=20)
```

#### `OTabs`

- **Supports**: Tabbed container with pill-style header and stacked pages. Lazy loading via `on_first_activate`.
- **Adjustable Props**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `"100%"` | Fixed width. `"100%"` = Expanding. |
| `height` | `Union[int, str]` | `"auto"` | Fixed height. `"auto"` = Hug. |
| `header_height` | `int` | `28` | Tab header bar height. |
| `header_pad` | `int` | `3` | Internal padding of header bar. |
| `header_spacing` | `int` | `4` | Spacing between tab buttons. |
| `tab_button_height` | `int` | `20` | Height of each tab button. |
| `content_gap` | `int` | `10` | Gap between header and content (section-level). |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Implementation**:

```python
# Default tabs
tabs = OTabs(config_group)
page1 = tabs.add("General")
page2 = tabs.add("Advanced")
config_group.layout_.addWidget(tabs)

# Compact tabs
tabs = OTabs(config_group, header_height=22, tab_button_height=16, content_gap=5)
```

#### `OSidebar` & `OSidebarItem`

- **Supports**: Native sidebar container with header, content items, and footer areas. Supports hover effects and active states for navigation.
- **Adjustable Props**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `250` | Fixed width in px. `"100%"` = Expanding. |
| `bg_color` | `Optional[str]` | `None` | Background color. |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Implementation**:

```python
sidebar = OSidebar(win.body, width=250)
sidebar.add_item("Home", lambda: print("Go home"))
sidebar.add_item("Settings")
win.body.layout().addWidget(sidebar)
```

#### `OVirtualTable`

- **Supports**: High-performance table (100k+ rows) with embedded controls (OComboBox, OTextBox). Based on Qt MVC pattern.
- **Adjustable Props**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `columns` | `Tuple[str, ...]` | `("Column 1",)` | Column header names. |
| `hug` | `bool` | `True` | Auto-hug height to row count. |
| `visible_rows` | `Optional[int]` | `None` | Visible rows when `hug=False` (default 8). |
| `row_height` | `int` | `24` | Height of each data row. |
| `header_height` | `int` | `28` | Height of the column header. |
| `flexible_height` | `bool` | `False` | Rows stretch to fill available height. |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Implementation**:

```python
# Basic table
table = OVirtualTable(config_group, columns=("ID", "Name", "Status"))
table.update_data([(1, "Item A", "Active"), (2, "Item B", "Inactive")])
config_group.layout_.addWidget(table)

# Scrollable table with custom header
table = OVirtualTable(config_group, columns=("Log",), hug=False, visible_rows=10, header_height=32)
```

---

#### `OChatView` & `OChatInput`

- **Supports**: Full chat interface. Native streaming for AI responses, user messages, and a dedicated chat input box with attach and send buttons.
- **Adjustable Props (`OChatView`)**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `"100%"` | Fixed width in px or CSS percentage. `"100%"` = Expanding. |
| `height` | `Union[int, str]` | `"auto"` | Fixed height in px. `"auto"` = Hug. |
| `pad` | `int` | `10` | Internal padding. |
| `spacing` | `int` | `15` | Gap between chat bubbles. |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Adjustable Props (`OChatInput`)**:

| Prop | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `"100%"` | Fixed width in px or CSS percentage. `"100%"` = Expanding. |
| `height` | `Union[int, str]` | `50` | Input bar height. |
| `pad_left` | `int` | `15` | Left padding. |
| `pad_right` | `int` | `10` | Right padding. |
| `spacing` | `int` | `10` | Gap between elements. |
| `show_add` | `bool` | `True` | Show/hide "+" attach button. |
| `show_action`| `bool` | `True` | Show/hide send (arrow) button. |
| `theme` | `Optional[dict]` | `None` | Global theming dictionary. |

- **Implementation**:

```python
# Default Chat Interface
chat_view = OChatView(config_group)
config_group.layout_.addWidget(chat_view)

chat_input = OChatInput()
chat_input.submitted.connect(lambda text: chat_view.add_message("user", text))
config_group.layout_.addWidget(chat_input)

# Stream AI message
chat_view.add_message("assistant", "")
chat_view.append_chunk("Hello! ")

# Customized Input (Text Only)
text_input = OChatInput(config_group, show_add=False, placeholder_text="Type your answer...", height=60)
```
