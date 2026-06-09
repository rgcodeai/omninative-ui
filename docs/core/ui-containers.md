# UI Containers Components

This module contains advanced structural containers for grouping other widgets, enabling scrollable views, and handling massive data lists efficiently.

> **Import:** `from omninative_ui import OScrollArea, OTreeWidget, OTabs, OVirtualTable`

---

### `OScrollArea`

Path: `omninative_ui/containers.py`
Type: Component (QScrollArea)
Description: Dynamic scrolling area. It will grow vertically as internal content requires, and disable horizontal scrolling, injecting clean margins and thin OmniNative-like scrollbars.

#### Initialization (Props)
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |

#### Key Methods & Properties
| Name | Type | Description |
| :--- | :--- | :--- |
| `view` | Property | Returns the internal `QWidget`. It's fundamental to use `scroll.view.layout().addWidget(...)` in PySide6 to add elements to this container, or use its helper method `.add()`. |
| `add(widget: QWidget, ...)`| Method | Optional helper method to add a widget to the vertical stack. |

---

### `OTreeWidget`

Path: `omninative_ui/containers.py`
Type: Component (QTreeWidget)
Description: Hierarchical tree and list in table format, ideal for file explorers, grouped properties, and outline trees. Includes a custom transparent style for headers.

#### Initialization (Props)
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |
| `columns` | `int` | `1` | Number of columns (if headers are not passed). |
| `headers` | `Optional[List[str]]` | `None` | Header names. Implicitly sets the number of columns. |
| `height` | `int` | `200` | Minimum height of the widget. |

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `add_item(parent, texts, icon) -> QTreeWidgetItem` | Method | `parent` is the root or parent sub-node (`None` if top-level). `texts` is the list of strings for each column. `icon` can be the name of a cached QIcon. Returns the created node. |
| `clear()` | Method | Deletes all nodes from the tree. |
| `set_column_width(col: int, width: int)` | Method | Sets the width of a specific column. |

---

### `OTabs`

Path: `omninative_ui/containers.py`
Type: Component (QTabWidget)
Description: Tabbed container. Supports an elegant transition when switching panels and is styled to simulate modern dark tabs.

#### Initialization (Props)
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `add(name: str) -> QWidget` | Method | Creates and registers a new tab with the given name and returns the internal `QWidget` of that tab. The desired layout must be attached to this returned widget. |
| `set(name: str)` | Method | Programmatically switches to the tab that exactly matches the string `name`. |

---

### `OVirtualTable`

Path: `omninative_ui/containers.py`
Type: Component (QTableView)
Description: Native table based on the Model/View (MVC) pattern and virtualization (`_RNativeTableModel` + `OTableItemDelegate`). Unlike QTableWidget, it can handle 100,000+ rows and render native embedded controls (real Buttons and CheckBoxes by intercepting clicks on cells).

#### Initialization (Props)
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | | Parent container. |
| `headers` | `List[str]` | | Table columns (e.g., `["ID", "Name", "Active", "Action"]`). |
| `get_data_cb` | `Callable[[], List[Dict]]`| | Callback that returns the in-memory data. Dictionary example: `{"ID": 1, "Name": "A", "Active": {"type": "checkbox", "value": True}}` |
| `update_item_cb`| `Optional[Callable]` | `None` | `(row_idx, col_name, new_val) -> None`. Callback when the user changes a value or embedded checkbox. |
| `action_cb` | `Optional[Callable]` | `None` | `(action_name, row_idx) -> None`. Callback if an embedded button is drawn and clicked. |
| `height` | `int` | `300` | Recommended minimum height of the view. |

#### Internal Cell Types (Delegates)
To draw native controls inside cells, `get_data_cb` must return a dictionary in the column value instead of a primitive, using the following keywords:
- `{"type": "checkbox", "value": bool}` -> Paints a real and editable OTableCheckBox.
- `{"type": "button", "label": "Delete"}` -> Paints an OButton.
- Primitives (str, int) will be painted as a traditional Label.

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `refresh()` | Method | Requests repainting the view because the original internal data changed. |
