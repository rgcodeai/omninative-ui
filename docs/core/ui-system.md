# UI System (AI Prompt Guide & API Reference)

Visual components domain and base design system for the project, inspired by the native OmniNative interface. The system is packaged as the installable library `omninative-ui`.

> **AI ATTENTION (CRITICAL):** This document is the gateway to the design API. If you are requested to create or modify a visual interface, you must STRICTLY use the components listed here and obey the rules below. NEVER hallucinate or assume *props* that are not documented in the component files.

## 1. Core Rules (Strict Directives)

1. **Imports:** All components are imported from the top-level: `from omninative_ui import OWindow, OButton, OLineEdit...`. Do not try to import from internal sub-modules unless strictly necessary.
2. **No Hardcoded Colors:** NEVER use hexadecimal strings or color names (e.g., `"red"`, `"#FF0000"`) in the application code. If you need direct colors, import `OMNINATIVE` from `omninative_ui` and index the design palette (`OMNINATIVE["primary"]`, `OMNINATIVE["danger"]`, `OMNINATIVE["dark"]`, etc).
3. **Native Dialogs (QMessageBox, QFileDialog):** To prevent the global stylesheet from overriding the operating system's native interface (by inheritance), all invocations to OS dialogs must be instantiated by passing `None` as `parent` or invoking their static methods without a linked parent.
4. **Packaging:** Always use PySide6's layout system (`QVBoxLayout`, `QHBoxLayout`) to arrange elements, or take advantage of the layouts generated in containers if indicated.
5. **Global Theming (`theme={}` & `set_global_theme`):** ALL components support overriding their specific style properties (like `bg_color`, `text_color`, `border_color`, etc.) via direct `**kwargs` or by passing a `theme={}` dictionary containing those properties. This allows centralizing style overrides locally. To override the default palette for the **entire application**, use `set_global_theme(YOUR_PALETTE)` immediately after importing the module.

## 2. API Reference by Modules

The precise documentation of the *props* (constructor parameters), methods, and signals of each component has been segmented to avoid overloading the context.

**Before instantiating a component, READ its specific documentation by clicking on the following links:**

- 📚 [**Component Development** (`component-development.md`)](component-development.md): Guide for creating new UI components
- 📚 [**UI Core** (`ui-core.md`)](ui-core.md): `OWindow`, `OGroup`, `OButton`, `OComboBox`, `ORadioButton`, `OCheckBox`, `OLabel`, `OElidedLabel`, `OStatusBar`, `OOptionRow`
- 📚 [**UI Inputs** (`ui-inputs.md`)](ui-inputs.md): `OLineEdit`, `OTextBox`, `OSpinBox`, `OSlider`, `OProgressBar`
- 📚 [**UI Containers** (`ui-containers.md`)](ui-containers.md): `OScrollArea`, `OTreeWidget`, `OTabs`, `OVirtualTable`
- 📚 [**UI Media** (`ui-media.md`)](ui-media.md): `OAudioPlayer`, `OAudioWaveform`, `OImageViewer`
- 📚 [**UI Chat** (`ui-chat.md`)](ui-chat.md): `OChatView`, `OChatInput`, `OActionMenu`

---

## 3. Internal Utility Modules

These modules operate behind the scenes but can be imported in advanced cases:

### `tokens` (`omninative_ui/tokens.py`)
Central dictionary of colors and base design variables.
*Key Exports:* `OMNINATIVE`, `_FONT_FAMILY`, `_FONT_SIZE_SM`, `_CORNER`, `_PAD`, `set_global_theme`

### `icons` (`omninative_ui/icons.py`)
Vector icon generator by code using `QPainter` with a caching system.
*Key Exports:* `_get_cached_checkbox`, `_get_cached_chevron`, `_get_cached_audio_icon`

### `_utils` (`omninative_ui/_utils.py`)
Dynamic generator of the global stylesheet based on tokens.
*Key Exports:* `get_global_stylesheet`
