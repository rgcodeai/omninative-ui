# UI Containers Components

This module contains advanced structural containers for grouping other widgets, enabling scrollable views, and handling massive data lists efficiently.

> **Import:** `from omninative_ui import OScrollArea, OTreeWidget, OTabs, OVirtualTable`

---

### `OScrollArea`

Path: `omninative_ui/containers.py`
Type: Component (QScrollArea)
Description: Dynamic scrolling area. It will grow vertically as internal content requires, and disable horizontal scrolling, injecting clean margins and thin OmniNative-like scrollbars.

#### Initialization (Props)

**Layout & Dimensions:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | `None` | Parent container. |
| `width` | `Union[int, str]` | `"100%"` | Fixed width. `"100%"` = Expanding, `"auto"` = Hug. |
| `height` | `Union[int, str]` | `"auto"` | Fixed height. `"auto"` = Hug. |
| `bg_color` | `Optional[str]` | `None` | Background color. |
| `border_color` | `Optional[str]` | `None` | Border color. |
| `border_width` | `int` | `1` | Border width in px. |
| `border_radius` | `Optional[int]` | `None` | Custom border radius. |
| `theme` | `Optional[dict]` | `None` | Theme dictionary. |

#### Key Methods & Properties
| Name | Type | Description |
| :--- | :--- | :--- |
| `view` | Property | Returns the internal `QWidget`. Use `scroll.view.layout().addWidget(...)` in PySide6 to add elements. |
| `add(widget: QWidget, ...)` | Method | Optional helper method to add a widget to the vertical stack. |

#### Usage Examples

```python
# Default (fills parent width, auto height)
scroll = OScrollArea(config_group)
config_group.layout_.addWidget(scroll)

# Fixed dimensions
scroll = OScrollArea(config_group, width=300, height=400)
```

---

### `OTreeWidget`

Path: `omninative_ui/containers.py`
Type: Component (QWidget)
Description: Collapsible tree node with a chevron icon header and indented content area. Supports expand/collapse toggle with animated chevron direction. Use nested OTreeWidget instances for hierarchical structures.

#### Initialization (Props)

**Layout & Dimensions:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | `None` | Parent container. |
| `text` | `str` | `"Label"` | Header text. |
| `expanded` | `bool` | `True` | Initial expand/collapse state. |
| `width` | `Union[int, str]` | `"100%"` | Fixed width. `"100%"` = Expanding. |
| `height` | `Union[int, str]` | `"auto"` | Fixed height. `"auto"` = Hug. |
| `header_height` | `int` | `24` | Height of the clickable header row. |
| `icon_width` | `int` | `14` | Width of the chevron icon area. |
| `icon_height` | `int` | `20` | Height of the chevron icon (also used for text label height). |
| `header_spacing` | `int` | `8` | Spacing between icon and text in header. |
| `indent` | `int` | `20` | Left indentation of nested content. |
| `content_spacing` | `int` | `5` | Spacing between child widgets in the content area. |
| `text_color` | `Optional[str]` | `None` | Text color. |
| `icon_color` | `Optional[str]` | `None` | Chevron icon color. |
| `icon_hover_color` | `Optional[str]` | `None` | Chevron icon color when hovered. |
| `font_size` | `Optional[int]` | `None` | Font size in pt. |
| `theme` | `Optional[dict]` | `None` | Theme dictionary. |

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `toggle(event)` | Method | Toggles expand/collapse state. |
| `add_widget(widget: QWidget)` | Method | Adds a widget to the content area. |

#### Usage Examples

```python
# Default tree node
tree = OTreeWidget(config_group, text="Section A")
tree.add_widget(OLabel(tree.content, text="Item 1"))
tree.add_widget(OLabel(tree.content, text="Item 2"))
config_group.layout_.addWidget(tree)

# Compact tree (smaller indent, collapsed by default)
tree = OTreeWidget(config_group, text="Advanced", expanded=False, indent=12, header_height=20)

# Large header with wide spacing
tree = OTreeWidget(config_group, text="Root Node", header_height=32, icon_height=24, header_spacing=12)
```

---

### `OTabs`

Path: `omninative_ui/containers.py`
Type: Component (QWidget)
Description: Tabbed container with a pill-style header bar and stacked content pages. Supports lazy loading via `on_first_activate` callbacks.

#### Initialization (Props)

**Layout & Dimensions:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | `None` | Parent container. |
| `eager` | `bool` | `True` | Whether to eagerly load all tabs. |
| `width` | `Union[int, str]` | `"100%"` | Fixed width. `"100%"` = Expanding. |
| `height` | `Union[int, str]` | `"auto"` | Fixed height. `"auto"` = Hug. |
| `header_height` | `int` | `28` | Height of the tab header bar. |
| `header_pad` | `int` | `3` | Internal padding of the header bar. |
| `header_spacing` | `int` | `4` | Spacing between tab buttons. |
| `tab_button_height` | `int` | `20` | Height of individual tab buttons. |
| `content_gap` | `int` | `10` | Spacing between header bar and content area (section-level gap). |
| `bg_color` | `Optional[str]` | `None` | Background color for the header container. |
| `border_color` | `Optional[str]` | `None` | Border color for the header container. |
| `tab_bg_color` | `Optional[str]` | `None` | Background color for inactive tabs. |
| `tab_text_color` | `Optional[str]` | `None` | Text color for inactive tabs. |
| `tab_active_bg_color` | `Optional[str]` | `None` | Background color for active tab. |
| `tab_active_text_color` | `Optional[str]` | `None` | Text color for active tab. |
| `tab_hover_text_color` | `Optional[str]` | `None` | Text color when hovering over an inactive tab. |
| `border_radius` | `Optional[int]` | `None` | Custom border radius for the header container. |
| `font_size` | `Optional[int]` | `None` | Font size for tab labels. |
| `theme` | `Optional[dict]` | `None` | Theme dictionary. |

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `add(name: str, on_first_activate: Callable) -> QWidget` | Method | Creates a new tab and returns its page widget. |
| `set_active(name: str)` | Method | Programmatically switches to the named tab. |
| `preload(name: str)` | Method | Triggers lazy-load callback without switching to the tab. |

#### Usage Examples

```python
# Default tabs
tabs = OTabs(config_group)
page1 = tabs.add("General")
page2 = tabs.add("Advanced")
config_group.layout_.addWidget(tabs)

# Compact tabs (smaller header)
tabs = OTabs(config_group, header_height=22, tab_button_height=16, header_pad=2, content_gap=5)

# Tabs with lazy loading
def load_settings(page):
    page.layout().addWidget(OLabel(page, text="Settings loaded!"))
tabs.add("Settings", on_first_activate=load_settings)
```

---

### `OVirtualTable`

Path: `omninative_ui/containers.py`
Type: Component (QTableView)
Description: Native table based on the Model/View (MVC) pattern and virtualization (`_RNativeTableModel` + `OTableItemDelegate`). Can handle 100,000+ rows and render native embedded controls (real Buttons and CheckBoxes by intercepting clicks on cells).

#### Initialization (Props)

**Layout & Dimensions:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | `None` | Parent container. |
| `columns` | `Tuple[str, ...]` | `("Column 1",)` | Column header names. |
| `column_widgets` | `Optional[List[Dict]]` | `None` | Per-column widget configuration (class, kwargs, weight). |
| `hug` | `bool` | `True` | If `True`, table height auto-hugs the row count (no scrollbar). |
| `visible_rows` | `Optional[int]` | `None` | Number of visible rows when `hug=False`. Defaults to 8. |
| `row_height` | `int` | `24` | Height of each row. |
| `header_height` | `int` | `28` | Height of the column header. |
| `flexible_height` | `bool` | `False` | If `True`, rows stretch to fill available height. |
| `bg_color` | `Optional[str]` | `None` | Background color for rows. |
| `alt_bg_color` | `Optional[str]` | `None` | Background color for alternate rows. |
| `text_color` | `Optional[str]` | `None` | Text color for cells. |
| `border_color` | `Optional[str]` | `None` | Border color for grid and table. |
| `header_bg_color` | `Optional[str]` | `None` | Background color for the header. |
| `header_text_color` | `Optional[str]` | `None` | Text color for the header. |
| `primary_color` | `Optional[str]` | `None` | Primary color for internal focus. |
| `border_radius` | `Optional[int]` | `None` | Custom border radius for the table. |
| `font_size` | `Optional[int]` | `None` | Font size for header and rows. |
| `theme` | `Optional[dict]` | `None` | Theme dictionary. |

#### Internal Cell Types (Delegates)
To draw native controls inside cells, `column_widgets` uses the `class` key:
- `"QLabel"` → Painted as a traditional Label (default).
- `"OComboBox"` → Persistent combo editor.
- `"OTextBox"` → Multi-line text editor.

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `update_data(data: List[Tuple])` | Method | Replaces all row data and refreshes the view. |
| `scroll_to_index(index: int)` | Method | Scrolls to the specified row index. |
| `focus_row(row, col, cursor_pos)` | Method | Activates editing on a specific cell. |

#### Usage Examples

```python
# Basic table
table = OVirtualTable(
    config_group,
    columns=("ID", "Name", "Status"),
    row_height=28,
)
table.update_data([(1, "Item A", "Active"), (2, "Item B", "Inactive")])
config_group.layout_.addWidget(table)

# Table with custom header height
table = OVirtualTable(config_group, columns=("A", "B"), header_height=32, row_height=30)

# Non-hug scrollable table
table = OVirtualTable(config_group, columns=("Log",), hug=False, visible_rows=10)
```
