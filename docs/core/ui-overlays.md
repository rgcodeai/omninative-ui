# UI Overlays

This document outlines the API reference for the Overlay components of `omninative-ui`, which are designed as floating, frameless, and often globally triggerable widgets.

---

### `OHotkeyOverlay`

Path: `omninative_ui/overlays.py`

Type: Component (Base Class)

Description: Base class for a floating, frameless overlay that can be toggled by a global hotkey. It operates as an independent top-level window (to prevent un-minimizing the main app) but manages its own cleanup. Uses the `keyboard` library to listen for hotkeys globally across the OS.

Key Exports:
| Name | Type | Description |
| :--- | :--- | :--- |
| `set_hotkey(hotkey_str: str)` | `Method` | Binds a global hotkey (e.g. `'ctrl+shift+a'`) to toggle the overlay. |
| `show_overlay()` | `Method` | Shows the overlay. |
| `hide_overlay()` | `Method` | Hides the overlay. |
| `toggle()` | `Method` | Toggles the visibility of the overlay. |
| `on_show()` | `Method` | Hook method called when the overlay is shown. |
| `on_hide()` | `Method` | Hook method called when the overlay is hidden. |

---

### `OSpinner`

Path: `omninative_ui/overlays.py`

Type: Component

Description: A minimal spinning loading icon.

Key Exports:
| Name | Type | Description |
| :--- | :--- | :--- |
| `__init__(size: int, color: str)` | `Constructor` | Creates the spinner. |

**Theming:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `spinner_color` | `Optional[str]` | `None` | Spinner stroke color (defaults to `dark`). |
| `theme` | `Optional[dict]` | `None` | Dictionary for global theming. |

---

### `OAudioRecorderOverlay`

Path: `omninative_ui/overlays.py`

Type: Component

Description: A pill-shaped frameless overlay for recording audio. It features a realtime dynamic waveform and a status message while transcribing. Audio is recorded using `sounddevice` and saved using `soundfile`. Supports traditional file saving and real-time chunk streaming.

Key Exports:
| Name | Type | Description |
| :--- | :--- | :--- |
| `__init__(chunk_ms: int, transcribing_text: str, enable_processing_state: bool)` | `Constructor` | `chunk_ms` sets audio chunk size. `transcribing_text` sets the text. `enable_processing_state` defaults to `False`; if `True`, toggling off enters a 'Working' state instead of closing immediately. |
| `toggle()` | `Method` | Cycles the overlay states: Show/Record -> Transcribing -> Reset/Hide. |
| `set_transcribing_state(text: str = None)` | `Method` | Stops recording, hides waveform, and shows the transcription label. Optionally updates the text. |
| `reset_ui()` | `Method` | Hides the transcription label and shows the waveform again. |
| `recording_finished` | `Signal(str)` | Emits the absolute file path to the saved `.wav` file when recording stops. |
| `audio_chunk_recorded` | `Signal(object)` | Emits `numpy.ndarray` chunks of raw audio data in real-time as they are recorded. |
| `position_on_screen()` | `Method` | Positions the overlay dynamically based on the mouse position. Incluye soporte nativo DPI scaling multiscreen para Windows. |
| `set_hotkey(hotkey_str: str)` | `Method` | Inherited. Sets the global hotkey to show/hide the recorder. |

**Theming:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `bg_color` | `Optional[str]` | `None` | Pill background color (defaults to `bright`). |
| `text_color` | `Optional[str]` | `None` | Transcribing text color and internal spinner (defaults to `dark`). |
| `theme` | `Optional[dict]` | `None` | Dictionary for global theming passed to waveform and spinner. |

---

### `OTooltip`

Path: `omninative_ui/overlays.py`

Type: Component

Description: A customized floating tooltip. Natively bypasses OS windows and applies `Qt.ToolTip` so it appears above all elements without un-minimizing the main app. Supports native width adjustments.

Key Exports:
| Name | Type | Description |
| :--- | :--- | :--- |
| `__init__(text: str, width: Union[int, str])` | `Constructor` | Creates the tooltip with the given text and optional fixed or proportional width. |

**Theming:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `bg_color` | `Optional[str]` | `None` | Tooltip background color (defaults to `dark`). |
| `text_color` | `Optional[str]` | `None` | Tooltip text color (defaults to `accent`). |
| `border_color` | `Optional[str]` | `None` | Tooltip border color (defaults to `bright`). |
| `border_radius` | `Optional[int]` | `None` | Border radius (defaults to `_CORNER`). |
| `font_size` | `Optional[int]` | `None` | Font size (defaults to `_FONT_SIZE_SM`). |
| `pad` | `Optional[int]` | `None` | Padding (defaults to `_PAD`). |
| `theme` | `Optional[dict]` | `None` | Dictionary for global theming. |

---

### `OInfoIcon`

Path: `omninative_ui/overlays.py`

Type: Component

Description: An information icon that displays an `OTooltip` with custom text on hover.

Key Exports:
| Name | Type | Description |
| :--- | :--- | :--- |
| `__init__(parent, tooltip_text: str, size: int, position: str, tooltip_width: Union[int, str])` | `Constructor` | Creates the info icon. `position` can be `"auto"`, `"left"`, or `"right"`. `tooltip_width` adjusts the native width of the generated tooltip. |

**Theming:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `icon_color` | `Optional[str]` | `None` | Default info icon color. |
| `icon_hover_color` | `Optional[str]` | `None` | Hover state icon color (defaults to `primary`). |
| `theme` | `Optional[dict]` | `None` | Dictionary for global theming. Passed to tooltip. |
