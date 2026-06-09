# OmniNative UI - AI Instruction Manual

You are an expert PySide6 developer using the **OmniNative UI** component library. Your goal is to build beautiful, native desktop applications using these specific components instead of raw PySide6 widgets.

## Core Philosophy

1. **Never use raw QWidgets for UI elements**. Always use OmniNative components (e.g., `OButton` instead of `QPushButton`, `OLabel` instead of `QLabel`).
2. **Unified Theme**: The library already handles the dark theme automatically. Do not manually set background colors or inject stylesheets unless absolutely necessary.
3. **Structured Layouts**: Always use `OGroup` to group elements logically instead of raw `QFrame` or `QVBoxLayout`.

## Design & Layout Guidelines

1. **Window Setup & "Hug" Layout**: Centralize dimensions using a local variable. NEVER use hardcoded values for dimensions in the rest of the code; define a `target_width` variable at the beginning.
   - We strictly follow a "Figma-like Hug" behavior where the window vertically wraps its visible content perfectly and automatically grows/shrinks as components appear/disappear, without allowing manual vertical resizing.
   - To enable this, simply instantiate the window with `height=0`. The `OWindow` class automatically handles layout constraints and strict width dummies natively. If you also want it to wrap horizontally, pass `width=0`.
   - Apply strict, symmetrical margins: `win.body.layout().setContentsMargins(20, 20, 20, 20)`.
     ```python
     target_width = 450
     win = OWindow(title="My App", width=target_width, height=0)
     win.body.layout().setContentsMargins(20, 20, 20, 20)
     ```
2. **Logical Grouping**: Group related components into logical sections using `OGroup(panel=True)` to create an outline/container native effect.
3. **Section Spacing**: Ensure strict and standardized spacing between sections or groups. Apply exactly 10px spacing between all major components: `layout.setSpacing(10)`.
4. **Section Headers**: The main title or label of each section MUST have `bright=True` and `bold=True`.

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
target_width = 450
win = OWindow(title="My App", width=target_width, height=0) # height=0 auto-enables native hug mode

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

- **Supports**: Grouping UI elements logically with vertical or horizontal layout. Can have a panel background.
- **Implementation**:

```python
# Create a logical section
config_group = OGroup(win.body, orientation="v", panel=True)
config_group.layout_.setContentsMargins(15, 15, 15, 15)
config_group.layout_.setSpacing(10)

# Always add the group to the parent's layout
win.body.layout().addWidget(config_group)
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

- **Supports**: Standard, primary (highlighted), and secondary actions. Triggers callbacks.
- **Implementation**:

```python
btn_submit = OButton(config_group, text="Submit", primary=True, command=lambda: print("Submitted!"))
config_group.layout_.addWidget(btn_submit)
```

---

### Inputs

#### `OLineEdit` & `OTextBox`

- **Supports**: Single-line text input (with optional password masking) and multi-line text blocks.
- **Implementation**:

```python
# Single Line
username_input = OLineEdit(config_group, placeholder="Enter username...")
config_group.layout_.addWidget(username_input)

# Multi-line
bio_input = OTextBox(config_group)
bio_input.set("Initial text...")
config_group.layout_.addWidget(bio_input)

# Get value later: val = username_input.get()
```

#### `OSpinBox` & `OSlider`

- **Supports**: Numeric inputs with increment arrows and horizontal sliding scales.
- **Implementation**:

```python
# Numeric input
age_spinner = OSpinBox(config_group, from_=0, to=120)
config_group.layout_.addWidget(age_spinner)

# Slider
volume_slider = OSlider(config_group, orientation="h")
config_group.layout_.addWidget(volume_slider)
```

#### `OProgressBar`

- **Supports**: Tracking completion (0-100) or indeterminate mode for continuous "thinking" animations.
- **Implementation**:

```python
prog = OProgressBar(config_group)
config_group.layout_.addWidget(prog)

# For dynamic updates:
prog.set(45) # 45%

# For AI thinking (infinite animation):
prog.set_indeterminate(True)
```

---

### AI & Media Features

#### `OFileItem`

- **Supports**: Visual card for a generated file or attachment, with built-in "Open" and "Save" buttons.
- **Implementation**:

```python
fitem = OFileItem(config_group, filepath="/path/to/result.csv", filesize_str="1.2 KB")
fitem.open_requested.connect(lambda p: print(f"Opening: {p}"))
config_group.layout_.addWidget(fitem)
```

#### `OChatView` & `OChatInput`

- **Supports**: Full chat interface. Native streaming for AI responses, user messages, and a dedicated chat input box.
- **Implementation**:

```python
chat_view = OChatView(config_group)
config_group.layout_.addWidget(chat_view)

chat_input = OChatInput()
config_group.layout_.addWidget(chat_input)

# Add user message
chat_view.add_message("user", "Hello AI!")

# Stream AI message
chat_view.add_message("assistant", "")
chat_view.append_chunk("Hello! ")
chat_view.append_chunk("How can I help?")
```