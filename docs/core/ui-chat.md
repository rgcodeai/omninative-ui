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
| `master` | `Optional[QWidget]` | | Parent container. |
| `send_command` | `Callable[[str], None]` | | Mandatory callback triggered by pressing the Send button or pressing the `Enter` key (without shift). Returns the content of the input. |
| `attach_command`| `Optional[Callable[[], None]]`| `None` | If provided, the clip button to attach multimedia appears, which executes this callback. |
| `placeholder` | `str` | `"Type a message..."`| Dimmed background text. |

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
| `master` | `Optional[QWidget]` | | Parent container. |

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `add_action(label: str, callback: Callable[[], None], icon: Optional[str] = None)` | Method | Adds a secondary button to the menu with the provided text and its bound function. Automatically handles horizontal wrapping. |
