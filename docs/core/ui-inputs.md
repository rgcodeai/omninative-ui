# UI Inputs Components

This module contains specialized components for data ingestion and modification directly by the user (text, numerical values, increments, percentages).

> **Import:** `from omninative_ui import OLineEdit, OTextBox, OSpinBox, OSlider, OProgressBar`

---

### `OLineEdit`

Path: `omninative_ui/inputs.py`
Type: Component (QLineEdit)
Description: Standardized single-line text field. Supports placeholder and password mode.

#### Initialization (Props)
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |
| `text` | `str` | `""` | Default initial text. |
| `placeholder` | `str` | `""` | Dimmed text shown when the field is empty. |
| `width` | `int` | `0` | Force fixed width. |
| `transparent` | `bool` | `False` | Removes the base background, useful when placing over existing panels. |
| `password` | `bool` | `False` | Hides the actual text using the standard password character (`*`). |

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `get() -> str` | Method | Extracts the text entered by the user. |
| `set(val: Any)` | Method | Overwrites the field's text. |

---

### `OTextBox`

Path: `omninative_ui/inputs.py`
Type: Component (QTextEdit)
Description: Rich / multi-line text input field.

#### Initialization (Props)
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |
| `text` | `str` | `""` | Initial text. |
| `height` | `int` | `60` | Minimum height of the multi-line container. |
| `placeholder` | `str` | `""` | Dimmed text when empty. |

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
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |
| `command` | `Optional[Callable]`| `None` | Callback executed when the value changes, receives the numeric value. |
| `from_` | `Union[int, float]` | `0` | Allowed lower limit. |
| `to` | `Union[int, float]` | `100` | Allowed upper limit. |
| `number_of_steps`| `Optional[int]` | `None` | Divisions between `from_` and `to`. If `None` is passed, the step is `1.0`. If the number of divisions requires decimals, it internally switches to `float` mode. |
| `state` | `str` | `"normal"` | If `"readonly"`, typing is ignored but arrows are allowed. For native use, it's preferable to call `.setEnabled(False)`. |
| `width` | `int` | `80` | Standard width. |

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
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |
| `command` | `Optional[Callable]`| `None` | Function triggered upon releasing the slider or changing its intermediate value. |
| `from_` | `Union[int, float]` | `0` | Lower limit. |
| `to` | `Union[int, float]` | `100` | Upper limit. |
| `number_of_steps`| `Optional[int]` | `None` | Modifies the granularity level. Internally, a `QSlider` always handles integers, so floating granularity is mapped to a larger range. |

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
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |
| `master` | `Optional[QWidget]` | | Parent container. |
| `width` | `int` | `0` | Optional fixed width. |

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `get() -> float` | Method | Returns the current value. |
| `set(val: Any)` | Method | Sets the progress bar value (0 to 100). |
| `set_indeterminate(active: bool)` | Method | Activates or deactivates the indeterminate animation mode. |
