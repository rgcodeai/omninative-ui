# Component Development Guide

This guide outlines the protocol for building and integrating new UI components into the `omninative-ui` package.

## 1. File Structure & Location

All visual components reside inside the `omninative_ui` package.
- Determine the nature of your component. Is it a core building block? Place it in `core.py`.
- Is it a data input field? Place it in `inputs.py`.
- Is it a list or container? Place it in `containers.py`.
- If the component belongs to an entirely new category (e.g., `dialogs`), create a new `.py` file and register it in the system.

## 2. Design & Implementation Rules

When creating a component, inherit from the appropriate PySide6 class (`QWidget`, `QPushButton`, etc.) and follow these strict rules:

### Naming Convention
All custom components must be prefixed with `O` (e.g., `ONewButton`, `OCustomSlider`) to denote they are part of the OmniNative system.

### Styling & Tokens
- **NEVER use hardcoded colors.** Use the tokens defined in `omninative_ui/tokens.py`.
- The `OMNINATIVE` dictionary contains the palette (`OMNINATIVE["primary"]`, `OMNINATIVE["dark"]`, `OMNINATIVE["border"]`, etc.).
- Try to rely on the global stylesheet (`_utils.py`) for baseline aesthetics.
- If dynamic or specific styling is required, use inline `.setStyleSheet()` or override `paintEvent`, but always construct the style strings using the `OMNINATIVE` tokens, `_PAD`, and `_CORNER` constants.

### Component Skeleton Example

```python
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from .tokens import OMNINATIVE, _PAD, _CORNER

class OCustomCard(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        
        # 1. Layout Setup
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(_PAD, _PAD, _PAD, _PAD)
        
        # 2. Child Elements
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(f"color: {OMNINATIVE['text']}; font-weight: bold;")
        self.layout.addWidget(self.title_label)
        
        # 3. Component Styling
        self.setStyleSheet(f"""
            OCustomCard {{
                background-color: {OMNINATIVE['bg']};
                border-radius: {_CORNER}px;
                border: 1px solid {OMNINATIVE['border']};
            }}
        """)
```

## 3. Integration & Synchronization

After the component is fully functional, you MUST perform the following steps to synchronize the project state:

1. **Exports:** Add the new component to the `__all__` list in `omninative_ui/__init__.py` and import it there, exposing it to the public API.
2. **Demonstration:** Instantiate the new component in `examples/demo.py` so developers can see it in action.
3. **Documentation (CRITICAL):**
   - Update the relevant API reference document (e.g., `docs/core/ui-core.md`) with the new component's description, props, and exports.
   - If a new domain document or source file was created, update the project tree in `docs/DOC_TRACKER.md`.
