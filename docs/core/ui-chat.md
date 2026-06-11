# UI Chat Components

This module provides specialized interfaces for conversational applications, autonomous agents, and chat-like assistants.

> **Import:** `from omninative_ui import OChatView, OChatInput, OActionMenu`

---

### `OChatView`

Path: `omninative_ui/chat.py`
Type: Component (QScrollArea)
Description: Message history in bubble format (Chat). Renders the visual distinction between "User" (bubble floating to the right, primary color) and "Assistant" (bubble to the left, gray color).

#### Initialization (Props)
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | `None` | Parent container. |

**Layout & Dimensions:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `"100%"` | Fixed width in px or CSS percentage. `"100%"` = Expanding. |
| `height` | `Union[int, str]` | `"auto"` | Fixed height in px. `"auto"` = Hug. |
| `pad` | `int` | `10` | Internal padding inside the scroll area. |
| `spacing` | `int` | `15` | Spacing between messages. |

#### Usage Examples
```python
# Default
chat_view = OChatView(config_group)

# Customized
chat_view = OChatView(config_group, width=400, pad=15, spacing=20)
```

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `add_message(sender: str, text: str, html: bool=False, msg_type: str="text")` | Method | Injects a message. `sender` can be `"user"` or another (e.g., `"ai"`, `"assistant"`). If `html` is `True`, basic Markdown or HTML is parsed for links and bold text. `msg_type` determines the internal rendering (e.g., simple text vs special widget if the library is extended). |
| `clear()` | Method | Clears the entire message history. |
| `set_loading(is_loading: bool)` | Method | If `True`, shows a "typing..." animation at the bottom of the chat. If `False`, destroys it. |

---

### `OChatInput`

Path: `omninative_ui/chat.py`
Type: Component (QFrame)
Description: Multi-line text box anchored at the bottom of the chat, with an integrated button to attach files (optional) and another to send (`Send`). Supports automatic vertical expansion.

#### Initialization (Props)
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `parent` | `Optional[QWidget]` | `None` | Parent container. |
| `placeholder_text`| `str` | `"Pregunta lo que quieras"`| Dimmed background text. |

**Layout & Dimensions:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `"100%"` | Fixed width in px or CSS percentage. `"100%"` = Expanding. |
| `height` | `Union[int, str]` | `50` | Fixed height in px. `"auto"` = Hug. |
| `pad_left` | `int` | `15` | Left padding. |
| `pad_right` | `int` | `10` | Right padding. |
| `pad_y` | `int` | `0` | Vertical padding. |
| `spacing` | `int` | `10` | Spacing between add button, input, and action button. |
| `button_size` | `int` | `30` | Width/height of the add button. |
| `action_button_size` | `int` | `34` | Width/height of the action button. |
| `icon_size` | `int` | `24` | Size of icons. |
| `action_icon_size` | `int` | `20` | Size of the action button icon. |

**Visibility:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `show_add` | `bool` | `True` | Show/hide the "+" add button. |
| `show_action`| `bool` | `True` | Show/hide the action (arrow) button. |

#### Usage Examples
```python
# Default
chat_input = OChatInput(config_group)
chat_input.submitted.connect(lambda text: print(text))

# Custom placeholder without add button
chat_input = OChatInput(config_group, placeholder_text="Type a message...", show_add=False, height=60)
```

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `get() -> str` | Method | Gets the text currently in the box. |
| `clear()` | Method | Clears the text content (e.g., after sending). |
| `set_focus()` | Method | Immediately sets keyboard focus on the input box. |

---

### `OActionMenu`

Path: `omninative_ui/chat.py`
Type: Component (QWidget)
Description: Compact grid of buttons or suggested actions. Commonly used above `OChatInput` to provide quick options like "Prompt Starters".

#### Initialization (Props)
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `parent` | `Optional[QWidget]` | `None` | Parent container. |

**Layout & Dimensions:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `280` | Fixed width in px or CSS percentage. `"100%"` = Expanding. |
| `height` | `Union[int, str]` | `"auto"` | Fixed height in px. `"auto"` = Hug. |
| `pad` | `int` | `6` | Internal padding. |
| `spacing` | `int` | `2` | Spacing between menu items. |

#### Usage Examples
```python
# Default
menu = OActionMenu(parent_widget)
menu.add_action("Option 1")

# Compact
menu = OActionMenu(parent_widget, width=200, pad=4, spacing=0)
```

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `add_action(label: str, callback: Callable[[], None], icon: Optional[str] = None)` | Method | Adds a secondary button to the menu with the provided text and its bound function. Automatically handles horizontal wrapping. |
