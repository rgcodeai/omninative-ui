# omninative_ui/overlays.py
import os
import time
import threading
from typing import Optional, Any, Callable
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen, QBrush, QIcon, QPixmap
from PySide6.QtCore import Qt, Signal, QTimer, QRect, QPoint, QSize
from .tokens import OMNINATIVE, _FONT_FAMILY, _FONT_SIZE_SM, _CORNER, _PAD
from ._utils import apply_layout_dimensions
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
        # Qt.ToolTip flag is crucial here: it prevents the OS from un-minimizing the main window
        self.setWindowFlags(
            Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        self._hotkey = None
        self._is_visible = False
        self._keyboard_hook = None
        
        self.hide()
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
import math
import math
import math
class ORealtimeWaveform(QWidget):
    """A controlled aesthetic audio visualizer for recording."""
    def __init__(self, parent=None) -> None:
        from PySide6.QtWidgets import QWidget
        super().__init__(parent)
        self.setMinimumWidth(90)
        self.setFixedHeight(41)
        self._is_talking = False
        self._intensity = 0.0
        self._time = 0.0
        
        # Shorter pattern to fit 125px width. Around 17 bars.
        self._pattern = [
            0.15, 0.2, 0.4, 0.8, 0.4, 0.2, 0.3, 1.0, 0.5, 
            1.0, 0.3, 0.2, 0.4, 0.8, 0.4, 0.2, 0.15
        ]
        self._current_scales = [0.15 for _ in self._pattern]
        
    def set_intensity(self, intensity: float) -> None:
        """Update whether dialogue is detected based on volume threshold."""
        self._is_talking = intensity > 0.05
        self._intensity = intensity
        self.update()
        
    def paintEvent(self, event) -> None:
        from PySide6.QtGui import QPainter, QColor, QBrush, QPen
        from PySide6.QtCore import Qt, QRectF
        from .tokens import OMNINATIVE
        painter = QPainter()
        if painter.begin(self):
            try:
                painter.setRenderHint(QPainter.Antialiasing)
                
                w = self.width()
                h = self.height()
                
                bar_w = 2.0
                bar_spacing = 3.0
                
                color = QColor(OMNINATIVE["dark"])
                
                total_bars_width = len(self._pattern) * (bar_w + bar_spacing) - bar_spacing
                start_x = (w - total_bars_width) / 2.0
                
                if self._is_talking:
                    # Much faster and more fluid movement
                    self._time += 0.8
                    # Hyper-reactive aggression based on sound
                    aggression = 0.3 + (self._intensity * 2.5)
                    
                    target_scales = []
                    for i, base_h in enumerate(self._pattern):
                        # Faster complex wave for rapid fluid vibration
                        wave1 = math.sin(self._time * 1.8 + i * 0.4) 
                        wave2 = math.cos(self._time * 1.2 - i * 0.2)
                        combined_wave = (wave1 * 0.6 + wave2 * 0.4) * aggression
                        scale = max(0.15, min(1.0, base_h + combined_wave))
                        target_scales.append(scale)
                else:
                    # Shrink to minimum dots when not talking
                    target_scales = [0.15 for _ in self._pattern]
                    
                for i in range(len(self._pattern)):
                    # Extremely fast but mathematically smooth interpolation
                    self._current_scales[i] += (target_scales[i] - self._current_scales[i]) * 0.6
                    
                    bar_x = start_x + i * (bar_w + bar_spacing)
                    # Use 45% of height for max amplitude to look more elegant and less aggressive
                    max_bar_h = h * 0.45
                    bar_h = max(2.0, max_bar_h * self._current_scales[i])
                    
                    # Perfect mathematical center using floats
                    y_top = (h - bar_h) / 2.0
                    
                    painter.setBrush(QBrush(color))
                    painter.setPen(Qt.NoPen)
                    painter.drawRoundedRect(QRectF(bar_x, y_top, bar_w, bar_h), 1, 1)
            finally:
                painter.end()

class OSpinner(QWidget):
    """A minimal spinning loading icon."""
    def __init__(self, parent=None, size=16, color=None) -> None:
        from PySide6.QtCore import QTimer
        from .tokens import OMNINATIVE
        super().__init__(parent)
        self.setFixedSize(size, size)
        self._color = color or OMNINATIVE["dark"]
        self._angle = 0
        self._timer = QTimer(self)
        self._timer.setInterval(20)
        self._timer.timeout.connect(self._rotate)
        self._timer.start()

    def _rotate(self) -> None:
        self._angle = (self._angle + 12) % 360
        self.update()

    def paintEvent(self, event) -> None:
        from PySide6.QtGui import QPainter, QPen, QColor
        from PySide6.QtCore import Qt, QRectF
        painter = QPainter()
        if painter.begin(self):
            try:
                painter.setRenderHint(QPainter.Antialiasing)
                
                # Setup Pen
                pen = QPen(QColor(self._color))
                pen.setWidth(2)
                pen.setCapStyle(Qt.RoundCap)
                painter.setPen(pen)
                
                # Create bounding rect slightly smaller than widget to avoid clipping
                rect = QRectF(2, 2, self.width() - 4, self.height() - 4)
                
                # Arc sweeps 270 degrees
                start_angle = -self._angle * 16
                span_angle = 270 * 16
                
                painter.drawArc(rect, start_angle, span_angle)
            finally:
                painter.end()
class OAudioRecorderOverlay(OHotkeyOverlay):
    """
    A pill-shaped overlay for recording audio.
    Shows an animated waveform and transcription status.
    """
    recording_finished = Signal(str)  # Emits the path to the saved wav file
    audio_chunk_recorded = Signal(object)  # Emits numpy ndarray chunks in real-time
    
    def __init__(self, master=None, auto_start: bool = True, chunk_ms: int = 0, transcribing_text: str = "Working", enable_processing_state: bool = False) -> None:
        from PySide6.QtWidgets import QHBoxLayout, QLabel
        from PySide6.QtCore import Qt, QTimer
        from .tokens import OMNINATIVE, _FONT_FAMILY
        super().__init__(master)
        self.auto_start = auto_start
        self.chunk_ms = chunk_ms
        self.enable_processing_state = enable_processing_state
        
        self.setFixedSize(125, 41)
        
        from PySide6.QtWidgets import QGraphicsOpacityEffect
        from PySide6.QtCore import QVariantAnimation, QEasingCurve
        
        self.content_container = QWidget(self)
        self.content_container.setFixedSize(125, 41)
        
        self.opacity_effect = QGraphicsOpacityEffect(self.content_container)
        self.opacity_effect.setOpacity(0.01)
        self.content_container.setGraphicsEffect(self.opacity_effect)
        
        self._entrance_anim = QVariantAnimation(self)
        self._entrance_anim.setDuration(400)
        self._entrance_anim.setStartValue(0.0)
        self._entrance_anim.setEndValue(1.0)
        self._entrance_anim.setEasingCurve(QEasingCurve.OutExpo)
        self._entrance_anim.valueChanged.connect(self._on_anim_step)
        self._entrance_anim.finished.connect(self._on_anim_finished)
        self._anim_progress = 0.0
        self._is_closing = False
        
        # Main layout inside the container
        self.layout_ = QHBoxLayout(self.content_container)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(0)
        
        # Realtime Waveform
        self.waveform = ORealtimeWaveform(self.content_container)
        self.layout_.addWidget(self.waveform, 1, Qt.AlignCenter)
        
        # Transcribing Container
        self.transcribing_widget = QWidget(self.content_container)
        self.transcribing_widget.setFixedSize(125, 41)
        
        self.transcribing_spinner = OSpinner(self.transcribing_widget, size=14, color=OMNINATIVE["dark"])
        
        self.transcribing_text = transcribing_text
        self.transcribing_label = QLabel(transcribing_text + "...", self.transcribing_widget)
        self.transcribing_label.setStyleSheet(f"color: {OMNINATIVE['dark']}; font-family: {_FONT_FAMILY}; font-size: 13px; font-weight: bold; padding-bottom: 2px; margin: 0px;")
        self.transcribing_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.transcribing_label.adjustSize()
        self.transcribing_label.setText(transcribing_text)
        
        # We will position these manually in _on_anim_step
        
        self.transcribing_widget.hide()
        self.layout_.addWidget(self.transcribing_widget, 1, Qt.AlignCenter)
        
        # Audio Recording State
        self._stream = None
        self._is_recording = False
        self._audio_data = []
        self._sample_rate = 44100
        self._temp_filepath = ""
        
        # UI Update Timers
        self._ui_timer = QTimer(self)
        self._ui_timer.setInterval(33)
        self._ui_timer.timeout.connect(self._update_ui)
        self._current_volume = 0.0
        
        self._dots_timer = QTimer(self)
        self._dots_timer.setInterval(400)
        self._dots_timer.timeout.connect(self._update_dots)
        self._dots_count = 0
        
    def _update_dots(self) -> None:
        self._dots_count = (self._dots_count + 1) % 4
        self.transcribing_label.setText(self.transcribing_text + "." * self._dots_count)
        
    def _on_anim_step(self, val: float) -> None:
        from PySide6.QtCore import QVariantAnimation
        self._anim_progress = val
        
        if self._is_closing:
            # Fade out slightly faster during close (reaches 0.01 when val is 0.4)
            opacity = max(0.01, min(1.0, (val - 0.4) * 1.66))
        else:
            # Fade in normally during open
            opacity = max(0.01, min(1.0, (val - 0.2) * 1.5))
            
        self.opacity_effect.setOpacity(opacity)
        
        # Manually position spinner and text so they slide to center
        sw = self.transcribing_spinner.width()
        lw = self.transcribing_label.width()
        total_w = sw + lw
        
        center_x = 125 / 2.0
        center_y = 41 / 2.0
        
        # Normal positions (val = 1.0)
        normal_sx = center_x - total_w / 2.0
        normal_lx = normal_sx + sw
        
        # Contracted positions (val = 0.0) - both centered
        contract_sx = center_x - sw / 2.0
        contract_lx = center_x - lw / 2.0
        
        sx = contract_sx + (normal_sx - contract_sx) * val
        lx = contract_lx + (normal_lx - contract_lx) * val
        
        self.transcribing_spinner.move(int(sx), int(center_y - self.transcribing_spinner.height() / 2.0))
        self.transcribing_label.move(int(lx), int(center_y - self.transcribing_label.height() / 2.0))
        
        self.update()

    def toggle(self) -> None:
        if self._is_visible and not getattr(self, '_is_closing', False):
            if self._is_recording:
                if self.enable_processing_state:
                    self.set_transcribing_state()
                else:
                    self.hide_overlay()
            else:
                self.hide_overlay()
        else:
            self.reset_ui()
            self.show_overlay()
            
    def set_transcribing_state(self, text: str = None) -> None:
        if text:
            self.transcribing_text = text
            self.transcribing_label.setText(text + "...")
            self.transcribing_label.adjustSize()
            self.transcribing_label.setText(text)
        self._stop_recording()
        self.waveform.hide()
        
        self._dots_count = 0
        self._dots_timer.start()
        self.transcribing_widget.show()
        
    def reset_ui(self) -> None:
        self._dots_timer.stop()
        self.transcribing_widget.hide()
        self.waveform.show()
    def paintEvent(self, event) -> None:
        """Draw the pill-shaped background."""
        from PySide6.QtGui import QPainter, QPainterPath, QColor, QBrush
        from PySide6.QtCore import Qt, QRectF
        from .tokens import OMNINATIVE
        painter = QPainter()
        if painter.begin(self):
            try:
                painter.setRenderHint(QPainter.Antialiasing)
                
                rect = self.rect()
                h = rect.height()
                target_w = rect.width()
                start_w = h  # 41 (circle)
                
                # Prevent any mathematical artifacts from floating point over/under shoot
                current_progress = max(0.0, min(1.0, getattr(self, '_anim_progress', 1.0)))
                
                current_w = start_w + (target_w - start_w) * current_progress
                x = (target_w - current_w) / 2.0
                
                path = QPainterPath()
                radius = h / 2.0
                path.addRoundedRect(QRectF(x, 0, current_w, h), radius, radius)
                
                # Slightly translucent bright background (Cross-OS compatible)
                bg_color = QColor(OMNINATIVE["bright"])
                
                if getattr(self, '_is_closing', False):
                    # Fades out as it shrinks, reaching 0 opacity just as it becomes a circle
                    # Using a slight power curve makes it fade beautifully at the end
                    bg_alpha = int(225 * (current_progress ** 1.5))
                else:
                    # Fades in very quickly at the start to keep the entrance punchy and solid
                    bg_alpha = int(225 * min(1.0, current_progress * 5.0))
                    
                # Clamp alpha just in case to avoid ValueError in QColor
                bg_color.setAlpha(max(0, min(255, bg_alpha)))
                
                painter.setBrush(QBrush(bg_color))
                painter.setPen(Qt.NoPen)
                painter.drawPath(path)
            finally:
                painter.end()
        
    def position_on_screen(self) -> None:
        """Positions the overlay at the bottom center of the active screen (mouse position), ignoring parent geometry."""
        from PySide6.QtGui import QGuiApplication, QCursor
        
        # 1. Get the global cursor position to determine which screen to use (Important for multi-screen setups)
        cursor_pos = QCursor.pos()
        target_screen = QGuiApplication.primaryScreen()
        
        # 2. Find the screen that contains the cursor (or fallback to primary)
        for s in QGuiApplication.screens():
            if s.geometry().contains(cursor_pos):
                target_screen = s
                break
                
        geom = target_screen.geometry()
        
        # 3. Move the window to the target screen (Important for multi-screen setups)
        window_handle = self.windowHandle()
        if window_handle:
            window_handle.setScreen(target_screen)
            
        # 4. Calculate the exact center on the active screen (Ignoring the parent window)
        x = geom.x() + (geom.width() - self.width()) // 2
        y = geom.bottom() - 100
        
        self.move(x, y)
    def show_overlay(self) -> None:
        from PySide6.QtCore import QVariantAnimation, QEasingCurve
        self.position_on_screen()
        # Set initial visual state BEFORE showing the window to prevent flashing the old state
        self._anim_progress = 0.0
        self._is_closing = False
        self.opacity_effect.setOpacity(0.01)
        self.update()
        
        super().show_overlay()
        
        self._entrance_anim.stop()
        self._entrance_anim.setDirection(QVariantAnimation.Forward)
        self._entrance_anim.setStartValue(0.0)
        self._entrance_anim.setEndValue(1.0)
        self._entrance_anim.setEasingCurve(QEasingCurve.OutExpo)
        self._entrance_anim.start()
        
        if self.auto_start:
            self._start_recording()

    def hide_overlay(self) -> None:
        from PySide6.QtCore import QVariantAnimation, QEasingCurve
        self._dots_timer.stop()
        if self._is_recording:
            self._stop_recording()
            
        self._is_closing = True
        self._entrance_anim.stop()
        # Always run Forward to keep OutExpo soft-landing behavior, but animate from 1.0 down to 0.0
        current_val = getattr(self, '_anim_progress', 1.0)
        self._entrance_anim.setDirection(QVariantAnimation.Forward)
        self._entrance_anim.setStartValue(current_val)
        self._entrance_anim.setEndValue(0.0)
        self._entrance_anim.setEasingCurve(QEasingCurve.OutExpo)
        self._entrance_anim.start()

    def _on_anim_finished(self) -> None:
        if self._is_closing:
            super().hide_overlay()

    def on_show(self) -> None:
        pass
        
    def on_hide(self) -> None:
        pass
            
    def _audio_callback(self, indata, frames: int, time_info, status) -> None:
        import numpy as np
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
            exaggerated_vol = (vol * 40.0)
            self._current_volume = min(1.0, exaggerated_vol)
    def _start_recording(self) -> None:
        if not HAS_AUDIO:
            print("Audio libraries not found. Cannot record.")
            return
            
        import tempfile
        import time
        import sounddevice as sd
        self._temp_filepath = os.path.join(tempfile.gettempdir(), f"omninative_record_{int(time.time())}.wav")
        self._audio_data = []
        self._is_recording = True
        self.waveform._is_talking = False
        
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
            import numpy as np
            import soundfile as sf
            try:
                audio_np = np.concatenate(self._audio_data, axis=0)
                sf.write(self._temp_filepath, audio_np, self._sample_rate)
                self.recording_finished.emit(self._temp_filepath)
            except Exception as e:
                print(f"Failed to save audio: {e}")
    def _update_ui(self) -> None:
        """Called periodically by QTimer to update the waveform."""
        if self._is_recording:
            self.waveform.set_intensity(self._current_volume)
            # Add some decay to the volume so it doesn't freeze high
            # Faster decay (0.5 instead of 0.8) makes it react quicker when sound stops
            self._current_volume *= 0.5
        else:
            self.waveform.set_intensity(0.0)

class OTooltip(QWidget):
    def __init__(self, text: str, width: Any = "auto"):
        super().__init__()
        from PySide6.QtWidgets import QLabel, QVBoxLayout
        from PySide6.QtCore import Qt
        
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.label = QLabel(text)
        self.label.setWordWrap(True)
        apply_layout_dimensions(self.label, width, "auto")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        
        self.label.setStyleSheet(f"""
            QLabel {{
                background-color: {OMNINATIVE['dark']};
                color: {OMNINATIVE['accent']};
                border: 1px solid {OMNINATIVE['bright']};
                border-radius: {_CORNER}px;
                padding: {_PAD}px;
                font-family: {_FONT_FAMILY};
                font-size: {_FONT_SIZE_SM}pt;
            }}
        """)

class OInfoIcon(QLabel):
    """An info icon that shows a custom tooltip on hover."""
    def __init__(self, parent=None, tooltip_text: str = "", size: int = 20, position: str = "auto", tooltip_width: Any = "auto") -> None:
        from PySide6.QtCore import Qt
        from .icons import _get_cached_info_icon
        super().__init__(parent)
        self.tooltip_text = tooltip_text
        self.tooltip_width = tooltip_width
        self.position = position
        self.icon_size = size
        self.setPixmap(_get_cached_info_icon(size=self.icon_size))
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignCenter)
        self.custom_tooltip = None

    def enterEvent(self, event) -> None:
        from .icons import _get_cached_info_icon
        from .tokens import OMNINATIVE
        
        self.setPixmap(_get_cached_info_icon(size=self.icon_size, color=OMNINATIVE["primary"]))
        
        if not self.custom_tooltip and self.tooltip_text:
            self.custom_tooltip = OTooltip(self.tooltip_text, width=self.tooltip_width)
            
        if self.custom_tooltip:
            self.custom_tooltip.adjustSize()
            tooltip_w = self.custom_tooltip.width()
            tooltip_h = self.custom_tooltip.height()
            
            icon_center = self.mapToGlobal(self.rect().center())
            icon_right = self.mapToGlobal(self.rect().topRight())
            icon_left = self.mapToGlobal(self.rect().topLeft())
            
            y = icon_left.y() # Aligns the top of the tooltip with the top of the icon
            x = icon_right.x() + 5 # default right
            
            screen_geom = self.screen().availableGeometry()
            if self.position == "left" or (self.position == "auto" and x + tooltip_w > screen_geom.right()):
                x = icon_left.x() - 5 - tooltip_w
            elif self.position == "right":
                x = icon_right.x() + 5
                
            self.custom_tooltip.move(x, y)
            self.custom_tooltip.show()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        from .icons import _get_cached_info_icon
        
        self.setPixmap(_get_cached_info_icon(size=self.icon_size))
        
        if self.custom_tooltip:
            self.custom_tooltip.hide()
            self.custom_tooltip.deleteLater()
            self.custom_tooltip = None
        super().leaveEvent(event)