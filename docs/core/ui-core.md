# UI Core Components

This module contains the structural and fundamental components for building the interface. All components must be instantiated natively without hardcoding colors, respecting the inheritance of the PySide6 visual hierarchy.

> **Import:** `from omninative_ui import OWindow, OGroup, OButton, OLabel, ...`

---

### `OWindow`

Path: `omninative_ui/core.py`
Type: Component (QMainWindow)
Description: Main application window. Automatically injects the base global theme through OmniNative styles and supports smooth appearance to avoid flickering. Also supports vertical responsive "Hug" mode natively when instantiated with `height=0`.

#### Initialization (Props)
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `title` | `str` | `"OmniNative Plugin"` | Window title. |
| `width` | `int` | `480` | Initial window width. Si se pasa `0` junto con `height=0`, la ventana se adaptará a su contenido en ambos ejes (Hug mode total). |
| `height` | `int` | `620` | Initial window height. Si se pasa `0`, habilita el modo "Hug": el ancho se vuelve estricto y la altura crece/se encoge nativamente según su contenido. |
| `resizable` | `bool` | `False` | If `True`, the window allows resizing. |
| `icon_path` | `Optional[str]` | `None` | Path to a custom `.png` or `.ico` to be used as window icon. If not provided, a default vector OmniNative logo is generated. |

#### Key Methods & Properties
| Name | Type | Description |
| :--- | :--- | :--- |
| `body` | Property | Returns the main `QWidget` where all internal content should be packed. |
| `omninativeui_reveal_when_ready(alpha: float = 1.0)` | Method | Restores window opacity. Call at the end of UI initialization to reveal smoothly. |

---

### `OGroup`

Path: `omninative_ui/core.py`
Type: Component (QFrame)
Description: Semantic container. Can be rendered transparent or darkened (`panel=True`) with rounded corners to visually group other elements.

#### Initialization (Props)
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |
| `orientation` | `str` | `"v"` | Internal layout direction: `"v"` (Vertical) or `"h"` (Horizontal). |
| `pad` | `int` | `_PAD` (8) | Spacing between elements and margins. |
| `panel` | `bool` | `False` | If `True`, the container draws a dark background and border (`#1E1E22`). |

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `add(widget: QWidget, expand: bool=False, fill: str="none", padx: int=0, pady: int=0)` | Method | **(Legacy)** Compatibility method `pack`-like. It is preferable to interact directly with `self.layout()`. |

---

### `OButton`

Path: `omninative_ui/core.py`
Type: Component (QPushButton)
Description: General-purpose actionable button. Supports visual variants (primary, danger, neutral).

#### Initialization (Props)
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |
| `text` | `str` | `""` | Button text. |
| `command` | `Optional[Callable[[], None]]` | `None` | Callback executed on click event. |
| `primary` | `bool` | `False` | Main style with blue background (`#528BFF`). |
| `danger` | `bool` | `False` | Danger style with red/alert background. |
| `small` | `bool` | `False` | Reduces padding and height to fit in compact bars. |
| `width` | `int` | `0` | Force a fixed width (if > 0). |

---

### `OLabel` & `OElidedLabel`

Path: `omninative_ui/core.py`
Type: Component (QLabel)
Description: Descriptive texts. `OLabel` provides base typographic hierarchy. `OElidedLabel` automatically truncates text adding `...` at the end if it doesn't fit in the available width.

#### Initialization (Props for OLabel)
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |
| `text` | `str` | `""` | Initial content. |
| `bold` | `bool` | `False` | Forces bold typography (useful for titles). |
| `bright` | `bool` | `False` | Forces bright white color (`#FFFFFF`) instead of default dimmed text. |
| `size` | `Optional[int]` | `None` | Force a specific font size in points (pt). |
| `anchor` | `str` | `"w"` | Alignment: `"w"` (Left), `"e"` (Right), `"center"`. |

---

### `OComboBox`

Path: `omninative_ui/core.py`
Type: Component (custom QFrame)
Description: Highly customized dropdown selector (Combo Box) with translucent popup. Does not use native `QComboBox` to allow rendering a specific custom UI.

#### Initialization (Props)
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |
| `values` | `Optional[List[Any]]` | `None` | List of initial values to display. |
| `command` | `Optional[Callable[[Any], None]]`| `None` | Callback executed when a new value is selected. Passes the selected value as an argument. |
| `width` | `int` | `0` | Force fixed width. |
| `transparent` | `bool` | `False` | If `True`, removes background and border from inactive state. |

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `get() -> str` | Method | Returns the currently selected textual value. |
| `set(val: Any)` | Method | Programmatically selects a value without invoking the `command`. |
| `configure(values: List[Any])` | Method | Dynamically replaces the list of possible options. |
| `set_enabled(enabled: bool)` | Method | Deactivates and visually changes to inactive mode if `False`. |

---

### `ORadioButton` & `OCheckBox`

Path: `omninative_ui/core.py`
Type: Component
Description: Mutually exclusive (Radio) or independent (Check) boolean state controls.

#### Initialization (Props)
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |
| `text` | `str` | `""` | Text adjacent to the control. |
| `command` | `Optional[Callable[[int], None]]`| `None` | Change callback. Returns `1` or `0`. |

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `get() -> int` | Method | Returns `1` if checked, or `0` if not. |
| `set(val: Any)` | Method | Forces checked state (use `True`/`False` or `1`/`0`). |

---

### `OStatusBar`

Path: `omninative_ui/core.py`
Type: Component (QLabel)
Description: Small text label specialized in notifying the current system status to the end user, usually arranged at the bottom of the window.

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `set(msg: str, level: str = "info")` | Method | Changes the message. The `level` alters the color. Options: `"info"` (gray), `"success"` (green), `"error"` (red), `"bright"` (white). |

---

### `OOptionRow`

Path: `omninative_ui/core.py`
Type: Component (QWidget)
Description: Utility layout in horizontal format that displays a Label on the left and reserves space on the right to attach the respective input/control.

#### Initialization (Props)
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |
| `label_text` | `str` | `""` | Static text of the property to modify. |
| `label_width` | `int` | `100` | Width of the text area. Useful for aligning multiple rows. |

#### Key Properties
| Name | Type | Description |
| :--- | :--- | :--- |
| `widget_area` | Property | Returns `self` (the QWidget). For native use: call `row.layout().addWidget(...)` to insert the associated control (e.g. OComboBox) on the right side of the row. |
