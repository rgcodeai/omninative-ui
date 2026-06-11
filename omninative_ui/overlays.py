# omninative_ui/overlays.py
import os
import time
import threading
from typing import Optional, Any, Callable

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen, QBrush, QIcon, QPixmap
from PySide6.QtCore import Qt, Signal, QTimer, QRect, QPoint, QSize

from .tokens import OMNINATIVE, _FONT_FAMILY, _FONT_SIZE_SM, _CORNER

# Optional dependencies for audio and hotkeys
try:
    import keyboard
    HAS_KEYBOARD = True
except ImportError:
    HAS_KEYBOARD = False

try:
    import sounddevice as sd
    import soundfile as sf
    import numpy as np
    HAS_AUDIO = True
except ImportError:
    HAS_AUDIO = False


class OHotkeyOverlay(QWidget):
    """
    Base class for a floating, frameless overlay that can be toggled by a global hotkey.
    """
    _hotkey_signal = Signal()

    def __init__(self, master: Optional[QWidget] = None) -> None:
        super().__init__(master)
        # Configure as a frameless floating tool window that stays on top
        self.setWindowFlags(
            Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        self._hotkey = None
        self._is_visible = False
        self._keyboard_hook = None
        
        self._hotkey_signal.connect(self.toggle)
        
    def set_hotkey(self, hotkey_str: str) -> None:
        """
        Sets a global hotkey (e.g., 'ctrl+shift+a') to toggle this overlay.
        Requires the 'keyboard' library.
        """
        if not HAS_KEYBOARD:
            print("Warning: 'keyboard' library not found. Global hotkeys are disabled.")
            return
            
        if self._keyboard_hook:
            try:
                keyboard.remove_hotkey(self._keyboard_hook)
            except Exception as e:
                print(f"Notice: Could not remove previous hotkey hook: {e}")
            
        self._hotkey = hotkey_str
        try:
            self._keyboard_hook = keyboard.add_hotkey(self._hotkey, self._on_hotkey_pressed)
        except Exception as e:
            print(f"Error registering hotkey '{self._hotkey}': {e}")
            self._keyboard_hook = None
        
    def mousePressEvent(self, event: Any) -> None:
        """Starts window dragging if clicked."""
        if event.button() == Qt.LeftButton:
            # globalPosition() returns a QPointF, so we convert it to QPoint
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: Any) -> None:
        """Handles window dragging."""
        if event.buttons() & Qt.LeftButton:
            if hasattr(self, '_drag_pos'):
                self.move(event.globalPosition().toPoint() - self._drag_pos)
                event.accept()
                
    def _on_hotkey_pressed(self) -> None:
        """Called from a background thread by the keyboard library."""
        self._hotkey_signal.emit()
        
    def toggle(self) -> None:
        if self._is_visible:
            self.hide_overlay()
        else:
            self.show_overlay()
            
    def show_overlay(self) -> None:
        self.show()
        self._is_visible = True
        self.on_show()
        
    def hide_overlay(self) -> None:
        self.hide()
        self._is_visible = False
        self.on_hide()
        
    def on_show(self) -> None:
        """Override to implement behavior when shown."""
        pass
        
    def on_hide(self) -> None:
        """Override to implement behavior when hidden."""
        pass


class ORealtimeWaveform(QWidget):
    """A real-time audio visualizer for recording."""
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setMinimumWidth(100)
        self.setFixedHeight(30)
        self.peaks = []
        self._max_bars = 40
        
    def add_peak(self, volume: float) -> None:
        self.peaks.append(volume)
        if len(self.peaks) > self._max_bars:
            self.peaks = self.peaks[-self._max_bars:]
        self.update()
        
    def paintEvent(self, event: Any) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w = self.width()
        h = self.height()
        
        bar_w = 3
        bar_spacing = 2
        
        played_color = QColor(OMNINATIVE["primary"])
        
        start_x = w - (len(self.peaks) * (bar_w + bar_spacing))
        
        for i, peak in enumerate(self.peaks):
            bar_x = start_x + i * (bar_w + bar_spacing)
            bar_h = max(2, int(h * peak))
            y_top = (h - bar_h) // 2
            
            painter.setBrush(QBrush(played_color))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(int(bar_x), int(y_top), bar_w, int(bar_h), 1, 1)


class OAudioRecorderOverlay(OHotkeyOverlay):
    """
    A pill-shaped overlay for recording audio.
    Shows a realtime waveform and a stop button.
    """
    recording_finished = Signal(str)  # Emits the path to the saved wav file
    audio_chunk_recorded = Signal(object)  # Emits numpy ndarray chunks in real-time
    
    def __init__(self, master: Optional[QWidget] = None, auto_start: bool = True, chunk_ms: int = 0) -> None:
        super().__init__(master)
        self.auto_start = auto_start
        self.chunk_ms = chunk_ms
        
        self.setFixedSize(220, 50)
        
        # Main layout inside the pill
        self.layout_ = QHBoxLayout(self)
        self.layout_.setContentsMargins(15, 5, 10, 5)
        self.layout_.setSpacing(10)
        
        # Realtime Waveform
        self.waveform = ORealtimeWaveform(self)
        self.layout_.addWidget(self.waveform, 1)
        
        # Stop Button (White circle with dark bars)
        self.stop_btn = QLabel()
        self.stop_btn.setFixedSize(30, 30)
        self.stop_btn.setCursor(Qt.PointingHandCursor)
        self.stop_btn.mousePressEvent = self._on_stop_clicked
        self._update_stop_btn_ui(is_hover=False)
        
        # Hover events for stop button
        self.stop_btn.enterEvent = lambda e: self._update_stop_btn_ui(is_hover=True)
        self.stop_btn.leaveEvent = lambda e: self._update_stop_btn_ui(is_hover=False)
        
        self.layout_.addWidget(self.stop_btn, 0)
        
        # Audio Recording State
        self._stream = None
        self._is_recording = False
        self._audio_data = []
        self._sample_rate = 44100
        self._temp_filepath = ""
        
        # UI Update Timer
        self._ui_timer = QTimer(self)
        self._ui_timer.setInterval(33)
        self._ui_timer.timeout.connect(self._update_ui)
        self._current_volume = 0.0

    def _update_stop_btn_ui(self, is_hover: bool) -> None:
        bg = OMNINATIVE["bright"] if not is_hover else OMNINATIVE["gray"]
        fg = OMNINATIVE["background"]
        self.stop_btn.setStyleSheet(f"""
            background-color: {bg};
            border-radius: 15px;
        """)
        
        from .icons import _get_cached_waveform_icon
        pix = _get_cached_waveform_icon(size=20, color=fg)
        
        # Center the 20x20 icon in a 30x30 pixmap
        container = QPixmap(30, 30)
        container.fill(Qt.transparent)
        painter = QPainter(container)
        painter.drawPixmap(5, 5, pix)
        painter.end()
        
        self.stop_btn.setPixmap(container)

    def paintEvent(self, event: Any) -> None:
        """Draw the pill-shaped background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = self.rect()
        path = QPainterPath()
        path.addRoundedRect(QRect(0, 0, rect.width(), rect.height()), 25, 25)
        
        # Semi-transparent dark background
        bg_color = QColor(OMNINATIVE["background"])
        bg_color.setAlpha(240)
        
        painter.setBrush(QBrush(bg_color))
        painter.setPen(QPen(QColor(OMNINATIVE["dark"]), 1))
        painter.drawPath(path)
        
    def position_on_screen(self) -> None:
        """Positions the overlay at the bottom center of the screen or parent window."""
        if self.parentWidget():
            parent_geom = self.parentWidget().geometry()
            x = parent_geom.center().x() - self.width() // 2
            y = parent_geom.bottom() - self.height() - 40  # 40px margin from bottom
            self.move(x, y)
        else:
            from PySide6.QtGui import QGuiApplication
            screen = QGuiApplication.primaryScreen().geometry()
            x = screen.center().x() - self.width() // 2
            y = screen.bottom() - 100  # 100px from bottom
            self.move(x, y)

    def on_show(self) -> None:
        """Starts recording when the overlay appears."""
        self.position_on_screen()
        if self.auto_start:
            self._start_recording()
        
    def on_hide(self) -> None:
        """Stops recording when hidden."""
        if self._is_recording:
            self._stop_recording()
            
    def _on_stop_clicked(self, event: Any) -> None:
        if event.button() == Qt.LeftButton:
            if self._is_recording:
                if self.auto_start:
                    self.hide_overlay()
                else:
                    self._stop_recording()
            else:
                self._start_recording()
            
    def _audio_callback(self, indata: Any, frames: int, time_info: Any, status: Any) -> None:
        if status:
            print(f"Audio status: {status}")
        if self._is_recording:
            chunk = indata.copy()
            self._audio_data.append(chunk)
            
            # Emit chunk for real-time streaming (Scenario B)
            self.audio_chunk_recorded.emit(chunk)
            
            # Calculate volume (RMS or peak)
            vol = np.linalg.norm(chunk) / np.sqrt(len(chunk))
            
            # Exaggerate the amplitude (multiplier from 10 to 40)
            # We also apply a small base to make it look alive even with low noise
            exaggerated_vol = (vol * 40.0)
            self._current_volume = min(1.0, exaggerated_vol)

    def _start_recording(self) -> None:
        if not HAS_AUDIO:
            print("Audio libraries not found. Cannot record.")
            return
            
        import tempfile
        self._temp_filepath = os.path.join(tempfile.gettempdir(), f"omninative_record_{int(time.time())}.wav")
        self._audio_data = []
        self._is_recording = True
        self.waveform.peaks = []
        
        try:
            blocksize = int((self.chunk_ms / 1000.0) * self._sample_rate) if self.chunk_ms > 0 else 0
            self._stream = sd.InputStream(
                samplerate=self._sample_rate,
                channels=1,
                blocksize=blocksize,
                callback=self._audio_callback
            )
            self._stream.start()
            self._ui_timer.start()
        except Exception as e:
            print(f"Failed to start audio stream: {e}")
            self._is_recording = False

    def _stop_recording(self) -> None:
        self._is_recording = False
        self._ui_timer.stop()
        
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
            
        if self._audio_data and HAS_AUDIO:
            try:
                audio_np = np.concatenate(self._audio_data, axis=0)
                sf.write(self._temp_filepath, audio_np, self._sample_rate)
                self.recording_finished.emit(self._temp_filepath)
            except Exception as e:
                print(f"Failed to save audio: {e}")

    def _update_ui(self) -> None:
        """Called periodically by QTimer to update the waveform."""
        if self._is_recording:
            # We add the last known peak to the waveform
            self.waveform.add_peak(self._current_volume)
            # Add some decay to the volume so it doesn't freeze high
            self._current_volume *= 0.5
