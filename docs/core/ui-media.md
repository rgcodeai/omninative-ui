# UI Media Components

This module groups components for visualizing and manipulating complex media, such as audio players, waveform drawing (real-time or static frequencies), visualizers, and image galleries.

> **Import:** `from omninative_ui import OAudioPlayer, OAudioWaveform, OImageViewer, OFullscreenViewer, OFileItem`

---

### `OAudioPlayer`

Path: `omninative_ui/media.py`
Type: Component (QWidget)
Description: Full audio player with native playback (via `QtMultimedia`), top name bar, waveform visualizer, and transport controls (Play, Stop, Record, Volume). The microphone button features a smooth breathing pulse animation (primary ↔ bright) during recording. Layout follows a section-based spacing model: 10px between sections, 5px within groups.

#### Initialization (Props)

**Layout & Dimensions:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | `None` | Parent container. |
| `width` | `Union[int, str]` | `"100%"` | Fixed width in px. `"100%"` = Expanding, `"auto"` = Hug (fills available space). |
| `height` | `Union[int, str]` | `"auto"` | Minimum height in px. `"auto"` = natural/preferred height. |
| `pad` | `int` | `0` | Internal padding (margins) on all 4 sides in px. |
| `spacing` | `int` | `10` | Vertical spacing between sections (top bar ↔ waveform ↔ controls) in px. |

**Controls:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `button_size` | `int` | `24` | Size of transport buttons (play, stop, record) in px. |
| `volume_slider_width` | `int` | `70` | Width of the volume slider in px. |
| `default_volume` | `int` | `80` | Initial volume level (0–100). |

**Visibility:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `show_record` | `bool` | `True` | Show/hide the microphone record button. |
| `show_load` | `bool` | `True` | Show/hide the "Load File" button. |
| `show_volume` | `bool` | `True` | Show/hide volume icon and slider. |

#### Controls Layout Order

```
[00:00 / 00:00] ——stretch—— [▶] [🎙] [⏹] ——stretch—— [🔊 ━━━━]
```

Time label at start, transport buttons centered, volume at end.

#### Signals
| Name | Type | Description |
| :--- | :--- | :--- |
| `file_loaded(str)` | Signal | Emitted when the user loads a file or finishes recording, passing the absolute filepath. |

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `play()` / `pause()` / `stop()` | Method | Programmatic playback controls. |
| `toggle_play()` | Method | Toggles between pause and play. |
| `toggle_record()` | Method | Starts or stops audio capture via microphone (QtMultimedia). |
| `set_volume(value: int)` | Method | Adjusts volume (0–100). |
| `get() -> Optional[str]` | Method | Gets the path of the currently loaded or recorded file. |

#### Usage Examples

```python
# Default player (no margins, expanding width)
player = OAudioPlayer(parent)

# Compact player: fixed width, no record, no volume
player = OAudioPlayer(parent, width=300, show_record=False, show_volume=False)

# Player with custom padding and bigger buttons
player = OAudioPlayer(parent, pad=12, button_size=32)
```

---

### `OAudioWaveform`

Path: `omninative_ui/media.py`
Type: Component (custom QWidget paint)
Description: Visual waveform component using native `QPainter`. Graphs audio peaks with configurable bar dimensions. Used internally by `OAudioPlayer` but can be instantiated independently for custom audio UIs.

#### Initialization (Props)

| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | `None` | Parent container. |
| `min_height` | `int` | `60` | Minimum height of the waveform area in px. |
| `bar_width` | `int` | `2` | Width of each waveform bar in px. |
| `bar_spacing` | `int` | `1` | Horizontal gap between bars in px. |
| `bar_corner_radius` | `int` | `1` | Corner radius of each bar in px. |
| `playhead_width` | `int` | `2` | Width of the playhead indicator line in px. |
| `height_ratio` | `float` | `0.8` | Proportion of widget height used for bar drawing (0.0–1.0). |

#### Signals
| Name | Type | Description |
| :--- | :--- | :--- |
| `seek_requested(float)` | Signal | Emitted on click/drag. Returns normalized position (0.0–1.0). |

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `load_audio_file(filepath: str) -> bool` | Method | Extracts peaks from a WAV file. Returns success/failure. |
| `generate_dummy_peaks(num_peaks=120)` | Method | Generates cosmetic random peaks. |
| `set_playback_ratio(ratio: float)` | Method | Sets playhead position and progress color (0.0–1.0). |

#### Usage Examples

```python
# Default waveform
waveform = OAudioWaveform(parent)

# Taller waveform with thicker bars
waveform = OAudioWaveform(parent, min_height=100, bar_width=4, bar_spacing=2)
```

---

### `OImageViewer`

Path: `omninative_ui/media.py`
Type: Component (QWidget)
Description: Embedded image viewer and gallery with thumbnail strip, fullscreen mode, and load/download actions. Supports both file-based and in-memory images (useful for AI-generated content).

#### Initialization (Props)

**Layout & Dimensions:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | `None` | Parent container. |
| `width` | `Union[int, str]` | `"100%"` | Fixed width in px. `"100%"` = Expanding, `"auto"` = Hug. |
| `height` | `Union[int, str]` | `260` | Minimum height of the viewer in px. |
| `pad` | `int` | `8` | Internal padding on all 4 sides in px. |
| `spacing` | `int` | `0` | Vertical spacing between sections in px. |

**Thumbnails:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `thumbnail_size` | `int` | `35` | Width/height of each thumbnail in px. |
| `thumbnail_spacing` | `int` | `8` | Horizontal spacing between thumbnails in px. |
| `thumbnail_strip_height` | `int` | `50` | Height of the thumbnail strip container in px. |

**Visibility:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `show_download` | `bool` | `True` | Show/hide the "Download" button. |
| `show_load` | `bool` | `True` | Show/hide the "Load" button. |
| `show_thumbnails` | `bool` | `True` | Show/hide thumbnail strip when >1 images. |
| `placeholder_text` | `str` | `""` | Custom placeholder text. Default: `"Click 'Load' to add images"`. |

#### Signals
| Name | Type | Description |
| :--- | :--- | :--- |
| `file_loaded(str)` | Signal | Emitted when loading images via the "Load" button. |

#### Key Methods
| Name | Type | Description |
| :--- | :--- | :--- |
| `load_file(filepath: str)` | Method | Loads an image from disk to the gallery. |
| `add_pixmap(pixmap, title)` | Method | Adds an in-memory image (e.g., AI-generated). |
| `set_pixmap(pixmap, title)` | Method | Clears gallery and sets a single image. |
| `clear()` | Method | Removes all images. |
| `download_current()` | Method | Opens native save dialog for the current image. |
| `show_fullscreen()` | Method | Opens the image in borderless fullscreen. Also triggered by clicking the image. |
| `get() -> Optional[str]` | Method | Gets the filepath of the current image (if disk-based). |

#### Usage Examples

```python
# Default viewer
viewer = OImageViewer(parent)

# Read-only viewer (no load/download buttons)
viewer = OImageViewer(parent, show_load=False, show_download=False)

# Viewer with larger thumbnails
viewer = OImageViewer(parent, thumbnail_size=50, thumbnail_strip_height=65)

# AI-generated image display (no file interaction)
viewer = OImageViewer(parent, show_load=False, show_download=True, placeholder_text="Waiting for AI...")
viewer.add_pixmap(generated_pixmap, "AI Result")
```

---

### `OFullscreenViewer`

Path: `omninative_ui/media.py`
Type: Component (QDialog)
Description: Borderless fullscreen image viewer (`Qt.WindowStaysOnTopHint`). Managed internally by `OImageViewer`. Supports left/right arrow navigation and Esc/click to close. Not typically instantiated directly.

---

### `OFileItem`

Path: `omninative_ui/media.py`
Type: Component (QFrame)
Description: Card component displaying a file's icon, name, and size with Open/Save action buttons. Long filenames are truncated in the middle (`ElideMiddle`) to always preserve the file extension.

#### Initialization (Props)

**Data:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `master` | `Optional[QWidget]` | `None` | Parent container. |
| `filepath` | `str` | | Absolute path of the file. |
| `filename` | `str` | `""` | Display name (auto-extracted from filepath if empty). |
| `filesize_str` | `str` | `""` | Optional size string (e.g. `"1.2 MB"`). |

**Layout & Dimensions:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `width` | `Union[int, str]` | `"100%"` | Fixed width in px. `"100%"` = Expanding, `"auto"` = Hug. |
| `height` | `Union[int, str]` | `50` | Fixed height of the card in px. |
| `pad` | `int` | `12` | Horizontal padding (left/right) in px. |
| `pad_y` | `int` | `8` | Vertical padding (top/bottom) in px. |
| `spacing` | `int` | `12` | Spacing between main elements (icon, text, buttons) in px. |
| `icon_size` | `int` | `24` | File icon size in px. |

**Buttons:**
| Prop | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `button_width` | `int` | `60` | Width of Open/Save buttons in px. |
| `button_height` | `int` | `24` | Height of Open/Save buttons in px. |
| `button_spacing` | `int` | `5` | Spacing between the Open and Save buttons in px. |
| `show_open` | `bool` | `True` | Show/hide the "Open" button. |
| `show_save` | `bool` | `True` | Show/hide the "Save" button. |

#### Signals
| Name | Type | Description |
| :--- | :--- | :--- |
| `open_requested(str)` | Signal | Emitted when clicking "Open", passing the filepath. |
| `save_requested(str)` | Signal | Emitted when clicking "Save", passing the filepath. |

#### Usage Examples

```python
# Default file card
fitem = OFileItem(parent, filepath="/path/to/report.pdf", filesize_str="2.4 MB")
fitem.open_requested.connect(lambda p: os.startfile(p))

# Save-only card (no Open button)
fitem = OFileItem(parent, filepath="/path/to/export.csv", show_open=False)

# Compact card
fitem = OFileItem(parent, filepath="/path/to/file.txt", height=40, pad=8, spacing=8)
```
