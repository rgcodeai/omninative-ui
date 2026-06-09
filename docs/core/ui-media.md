# UI Media Components

This module groups components for visualizing and manipulating complex media, such as audio players, waveform drawing (real-time or static frequencies), visualizers, and image galleries.

> **Import:** `from omninative_ui import OAudioPlayer, OAudioWaveform, OImageViewer, OFullscreenViewer`

---

### `OAudioPlayer`

Path: `omninative_ui/media.py`
Type: Component (QWidget)
Description: Full audio player with support for native playback (via `QtMultimedia`), top name bar, internal waveform visualizer, and Play, Stop, Microphone (for local audio recording), and Volume controls.

#### Initialization (Props)
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | `None` | Parent container. |

#### Signals
| Name | Type | Description |
| :--- | :--- | :--- |
| `file_loaded(str)` | Signal | Emitted when the user successfully loads a file through the UI (or after recording audio), passing the absolute path of the file on disk. |

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `play()` / `pause()` / `stop()` | Method | Programmatic playback controls. |
| `toggle_play()` | Method | Toggles the state between pause and play. |
| `toggle_record()` | Method | Starts or stops audio capture through the microphone (QtMultimedia). |
| `set_volume(value: int)` | Method | Adjusts the volume (range 0 to 100). |
| `get() -> Optional[str]` | Method | Gets the path of the currently loaded (or temporarily recorded) file. |

---

### `OAudioWaveform`

Path: `omninative_ui/media.py`
Type: Component (custom QWidget paint)
Description: Visual component based on native `QPainter` drawing that graphs audio peaks in an optimized way. Used internally by `OAudioPlayer` but can be instantiated independently.

#### Initialization (Props)
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | `None` | Parent container. |

#### Signals
| Name | Type | Description |
| :--- | :--- | :--- |
| `seek_requested(float)` | Signal | Emitted when the user clicks on the waveform. Returns the normalized ratio (0.0 to 1.0) from the start to the end of the track. |

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `load_audio_file(filepath: str) -> bool` | Method | Physically extracts volume peaks from a WAV file synchronously. Returns success or failure. |
| `generate_dummy_peaks(num_peaks=120)`| Method | Generates cosmetic random peaks in case the audio cannot be scanned. |
| `set_playback_ratio(ratio: float)` | Method | Adjusts the playback indicator line and the progress color (0.0 to 1.0). |

---

### `OImageViewer`

Path: `omninative_ui/media.py`
Type: Component (QWidget)
Description: Embedded image viewer and gallery. Allows dragging, scaling, and inspecting images, as well as viewing a bottom thumbnail scroll bar if multiple images are loaded.

#### Initialization (Props)
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | `None` | Parent container. |
| `height` | `int` | `260` | Minimum height of the viewer to ensure visibility in dense interfaces. |

#### Signals
| Name | Type | Description |
| :--- | :--- | :--- |
| `file_loaded(str)` | Signal | Emitted when loading images through the UI "Load" button. |

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `load_file(filepath: str)` | Method | Loads and instantiates a physical image from disk to the gallery. |
| `add_pixmap(pixmap: QPixmap, title: str="Generated Image")` | Method | Adds an image from memory (useful after generating it via AI) and creates its thumbnail. |
| `set_pixmap(pixmap: QPixmap, title: str)` | Method | Clears the gallery and sets this single image. |
| `clear()` | Method | Removes all current images from the internal gallery. |
| `download_current()` | Method | Calls a native save dialog to export the current image. |
| `show_fullscreen()` | Method | Opens the active image in borderless full-screen mode using `OFullscreenViewer`. This event is automatically triggered by clicking the image area. |
| `get() -> Optional[str]` | Method | Gets the filepath of the displayed image (if it comes from disk). |

---

### `OFullscreenViewer`

Path: `omninative_ui/media.py`
Type: Component (QDialog)
Description: Full-screen and opaque viewer (`Qt.WindowStaysOnTopHint`), typically managed from `OImageViewer`. Not usually used explicitly.
