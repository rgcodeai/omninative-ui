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

### `OAudioRecorderOverlay`

Path: `omninative_ui/overlays.py`

Type: Component

Description: A pill-shaped frameless overlay for recording audio. It features a realtime dynamic waveform and a stop button. Audio is recorded using `sounddevice` and saved using `soundfile`. Supports traditional file saving and real-time chunk streaming.

Key Exports:
| Name | Type | Description |
| :--- | :--- | :--- |
| `__init__(chunk_ms: int)` | `Constructor` | `chunk_ms` configures the size of emitted audio chunks in milliseconds. Default `0` means low-latency blocks provided by the OS. |
| `recording_finished` | `Signal(str)` | Emits the absolute file path to the saved `.wav` file when recording stops. |
| `audio_chunk_recorded` | `Signal(object)` | Emits `numpy.ndarray` chunks of raw audio data in real-time as they are recorded. |
| `position_on_screen()` | `Method` | Positions the overlay dynamically based estrictamente en la posición del mouse, ignorando la ventana parent por completo. Incluye soporte nativo DPI scaling multiscreen para Windows. |
| `set_hotkey(hotkey_str: str)` | `Method` | Inherited. Sets the global hotkey to show/hide the recorder. |
