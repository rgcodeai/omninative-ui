# UI Inputs Components

This module contains specialized components for data ingestion and modification directly by the user (text, numerical values, increments, percentages).

> **Import:** `from omninative_ui import OLineEdit, OTextBox, OSpinBox, OSlider, OProgressBar`

---

### `OLineEdit`

Path: `omninative_ui/inputs.py`
Type: Component (QLineEdit)
Description: Standardized single-line text field. Supports placeholder and password mode.

#### Initialization (Props)

**General:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |
| `placeholder` | `str` | `""` | Dimmed text shown when the field is empty. |
| `password` | `bool` | `False` | Hides the actual text using the standard password character (`*`). |
| `read_only` | `bool` | `False` | Makes the field read-only. |

**Layout & Dimensions:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `"100%"` | Fixed width in px. `"100%"` = Expanding, `"auto"` = Hug. |
| `height` | `Union[int, str]` | `22` | Fixed height in px. `"auto"` = Hug. |

#### Usage Examples

```python
# Default
entry = OLineEdit(group, placeholder="Search...")

# Compact / Customized
entry = OLineEdit(group, width=150, height=30, password=True)
```

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `get() -> str` | Method | Extracts the text entered by the user. |
| `set(val: Any)` | Method | Overwrites the field's text. |

---

### `OHotkeyInput`

Path: `omninative_ui/inputs.py`
Type: Component (OLineEdit)
Description: A special line edit that captures keystrokes and formats them as hotkeys (e.g., 'ctrl+shift+r') instead of allowing normal typing. Shows live feedback.

#### Initialization (Props)

**General:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |

#### Usage Examples

```python
hotkey_input = OHotkeyInput(group)
```

---

### `OTextBox`

Path: `omninative_ui/inputs.py`
Type: Component (QTextEdit)
Description: Rich / multi-line text input field.

#### Initialization (Props)

**General:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |
| `placeholder` | `str` | `""` | Dimmed text when empty. |
| `command` | `Optional[Callable]`| `None` | Callback for text changes. |

**Layout & Dimensions:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `"100%"` | Fixed width in px. `"100%"` = Expanding, `"auto"` = Hug. |
| `height` | `Union[int, str]` | `40` | Fixed height in px. `"auto"` = Hug. |

#### Usage Examples

```python
# Default
text_box = OTextBox(group)

# Customized
text_box = OTextBox(group, width=300, height=100)
```

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `get() -> str` | Method | Extracts the content as plain text. |
| `set(val: Any)` | Method | Replaces the text and moves the cursor to the beginning. |

---

### `OSpinBox`

Path: `omninative_ui/inputs.py`
Type: Component (QDoubleSpinBox)
Description: Numerical input field with integrated increment/decrement arrows. Automatically adjusts floating precision if limits or steps require it.

#### Initialization (Props)

**General:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |
| `from_` | `int` | `0` | Allowed lower limit. |
| `to` | `int` | `100` | Allowed upper limit. |
| `value` | `int` | `0` | Initial value. |
| `step` | `int` | `1` | Increment/decrement step. |
| `command` | `Optional[Callable]`| `None` | Callback executed when value changes. |

**Layout & Dimensions:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `120` | Fixed width in px. `"100%"` = Expanding, `"auto"` = Hug. |
| `height` | `Union[int, str]` | `22` | Fixed height in px. `"auto"` = Hug. |
| `pad` | `int` | `0` | Internal padding on all sides. |
| `spacing` | `int` | `2` | Spacing between buttons and entry. |
| `button_width` | `int` | `24` | Width of the +/- buttons. |

**Visibility:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `show_buttons` | `bool` | `True` | Show/hide the increment/decrement buttons. |

#### Usage Examples

```python
# Default
spinner = OSpinBox(group, from_=0, to=50)

# Customized dimensions and no buttons
spinner = OSpinBox(group, width=80, height=30, show_buttons=False)
```

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `get() -> float` | Method | Gets the current value. |
| `set(val: Any)` | Method | Adjusts the value internally and visually. |

---

### `OSlider`

Path: `omninative_ui/inputs.py`
Type: Component (Horizontal QSlider)
Description: Sliding bar (Slider) that doesn't steal mouse wheel focus by default, allowing smooth scrolling in option views without accidental value changes.

#### Initialization (Props)

**General:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |
| `orientation` | `str` | `"h"` | `"h"` for horizontal, `"v"` for vertical. |
| `from_` | `int` | `0` | Lower limit. |
| `to` | `int` | `100` | Upper limit. |
| `value` | `int` | `0` | Initial value. |
| `command` | `Optional[Callable]`| `None` | Callback for value changes. |

**Layout & Dimensions:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `"100%"` | Fixed width in px. `"100%"` = Expanding, `"auto"` = Hug. |
| `pad` | `int` | `0` | Internal padding. |
| `spacing` | `int` | `6` | Spacing between slider and entry. |
| `entry_width` | `int` | `40` | Width of the text entry. |

**Visibility:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `show_entry` | `bool` | `True` | Show/hide the value entry field. |

#### Usage Examples

```python
# Default
slider = OSlider(group)

# Customized
slider = OSlider(group, width=200, show_entry=False)
```

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `get() -> float` | Method | Gets the floating value adjusted according to `from_`, `to`, and *steps*. |
| `set(val: Any)` | Method | Sets the slided value programmatically. |

---

### `OProgressBar`

Path: `omninative_ui/inputs.py`
Type: Component (QProgressBar)
Description: Progress bar for long-running tasks. Can operate in determinate or indeterminate ("infinite marquee") mode.

#### Initialization (Props)

**General:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |
| `from_` | `int` | `0` | Lower limit. |
| `to` | `int` | `100` | Upper limit. |
| `value` | `int` | `0` | Initial value. |

**Layout & Dimensions:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `"100%"` | Fixed width in px. `"100%"` = Expanding, `"auto"` = Hug. |
| `height` | `Union[int, str]` | `3` | Fixed height in px. `"auto"` = Hug. |

#### Usage Examples

```python
# Default
prog = OProgressBar(group)

# Customized
prog = OProgressBar(group, width=300, height=8)
```

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `get() -> float` | Method | Returns the current value. |
| `set(val: Any)` | Method | Sets the progress bar value (0 to 100). |
| `set_indeterminate(active: bool)` | Method | Activates or deactivates the indeterminate animation mode. |
