# omninative_ui/media.py
import os
import time
from typing import Optional, List, Dict, Any

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QSizePolicy, QScrollArea, QDialog
)
from PySide6.QtGui import (
    QColor, QFont, QPixmap, QPainter, QPainterPath, QPen, QIcon,
    QBrush
)
from PySide6.QtCore import (
    Qt, Signal, QTimer, QSize, QPoint, QRect, QRectF, QPointF
)

from .tokens import OMNINATIVE, _FONT_FAMILY, _FONT_SIZE_SM, _CORNER, _PAD
from .icons import _get_cached_audio_icon
from .core import OButton, OElidedLabel
from .inputs import _WheelIgnoredSlider


# ---------------------------------------------------------------------------
# OAudioButton
# ---------------------------------------------------------------------------
class OAudioButton(QPushButton):
    def __init__(self, master: Optional[QWidget], icon_type: str, size: int = 24, **kwargs: Any) -> None:
        super().__init__(master)
        self.icon_type = icon_type
        self.size_val = size
        self.is_active = False
        
        self.setFixedSize(size, size)
        self.setCursor(Qt.PointingHandCursor)
        
        self.setMouseTracking(True)
        self._hovered = False
        
        self.update_icon()
        
    def set_active(self, active: bool) -> None:
        self.is_active = active
        self.update_icon()
        
    def enterEvent(self, event: Any) -> None:
        self._hovered = True
        self.update_icon()
        super().enterEvent(event)
        
    def leaveEvent(self, event: Any) -> None:
        self._hovered = False
        self.update_icon()
        super().leaveEvent(event)
        
    def update_icon(self) -> None:
        if self.is_active:
            if self.icon_type == "mic":
                color = OMNINATIVE["danger"]
            else:
                color = OMNINATIVE["primary"]
        elif self._hovered:
            color = OMNINATIVE["primary"]
        else:
            color = OMNINATIVE["accent"]
            
        pix = _get_cached_audio_icon(self.icon_type, size=self.size_val, color=color)
        self.setIcon(QIcon(pix))
        self.setIconSize(QSize(self.size_val, self.size_val))
        
        bg = OMNINATIVE["dark"]
        border_color = OMNINATIVE["accent"]
        if self._hovered:
            border_color = OMNINATIVE["primary"]
            
        cr = self.size_val // 2
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                border: 1px solid {border_color};
                border-radius: {cr}px;
                padding: 0px;
                margin: 0px;
            }}
            QPushButton:pressed {{
                background-color: {OMNINATIVE["gray"]};
            }}
        """)

# ---------------------------------------------------------------------------
# OAudioWaveform
# ---------------------------------------------------------------------------
class OAudioWaveform(QWidget):
    seek_requested = Signal(float)  # Emits playback ratio (0.0 to 1.0)
    
    def __init__(self, master: Optional[QWidget] = None, **kwargs: Any) -> None:
        super().__init__(master)
        self.setMinimumHeight(60)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.playback_ratio = 0.0
        self.peaks = []
        
        self.hover_x = -1
        self.is_hovered = False
        self.is_dragging = False
        
        self.setMouseTracking(True)
        
    def generate_dummy_peaks(self, num_peaks: int = 120) -> None:
        import random
        import math
        random.seed(42)  # Consistent dummy peaks
        self.peaks = []
        for i in range(num_peaks):
            val1 = math.sin(i * 0.15) * 0.4
            val2 = math.cos(i * 0.05) * 0.3
            noise = random.uniform(-0.15, 0.15)
            x = i / float(num_peaks)
            env = math.sin(x * math.pi)  # Envelope shape (bell curve)
            amp = abs(val1 + val2 + noise) * env
            amp = max(0.05, min(0.95, amp))
            self.peaks.append(amp)
        self.update()
        
    def load_audio_file(self, filepath: str) -> bool:
        """Loads peak data from a WAV audio file using standard library wave module."""
        try:
            import wave
            import struct
            with wave.open(filepath, 'rb') as w:
                nchannels = w.getnchannels()
                sampwidth = w.getsampwidth()
                framerate = w.getframerate()
                nframes = w.getnframes()
                
                # Limit samples to read
                max_samples = 150
                step = max(1, nframes // max_samples)
                
                new_peaks = []
                # Read frames in chunks
                for i in range(max_samples):
                    w.setpos(min(nframes - 1, i * step))
                    frame_data = w.readframes(1)
                    if not frame_data:
                        break
                    # Parse sample
                    if sampwidth == 2:
                        val = struct.unpack("<h", frame_data[:2])[0]
                        amp = abs(val) / 32768.0
                    elif sampwidth == 1:
                        val = struct.unpack("<B", frame_data[:1])[0]
                        amp = abs(val - 128) / 128.0
                    else:
                        amp = 0.5
                    new_peaks.append(max(0.05, min(0.95, amp)))
                
                if new_peaks:
                    self.peaks = new_peaks
                    self.update()
                    return True
        except Exception as e:
            print(f"Error loading audio file: {e}")
        return False
        
    def set_playback_ratio(self, ratio: float) -> None:
        self.playback_ratio = max(0.0, min(1.0, ratio))
        self.update()
        
    def paintEvent(self, event: Any) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        w = self.width()
        h = self.height()
        
        # Draw background container
        bg_rect = QRect(0, 0, w, h)
        painter.fillRect(bg_rect, QColor(OMNINATIVE["dark"]))
        
        # Draw horizontal center line
        painter.setRenderHint(QPainter.Antialiasing, False)
        painter.setPen(QPen(QColor(OMNINATIVE["gray"]), 1))
        painter.drawLine(0, h // 2, w, h // 2)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        if not self.peaks:
            painter.end()
            return
            
        bar_w = 2
        bar_spacing = 1
        max_bars = max(1, w // (bar_w + bar_spacing))
        
        display_peaks = self.peaks
        is_recording = getattr(self.parent(), 'is_recording', False)
        
        if is_recording:
            if len(self.peaks) > max_bars:
                display_peaks = self.peaks[-max_bars:]
        else:
            if len(self.peaks) > 0:
                display_peaks = []
                for i in range(max_bars):
                    exact_idx = i * (len(self.peaks) - 1) / max(1, max_bars - 1)
                    idx1 = int(exact_idx)
                    idx2 = min(len(self.peaks) - 1, idx1 + 1)
                    frac = exact_idx - idx1
                    val = self.peaks[idx1] * (1.0 - frac) + self.peaks[idx2] * frac
                    display_peaks.append(val)
                    
        num_bars = len(display_peaks)
        actual_content_w = (bar_w * num_bars) + (bar_spacing * max(0, num_bars - 1))
        
        start_x = 0
        if not is_recording and actual_content_w < w:
            start_x = (w - actual_content_w) / 2.0
        
        # Colors
        played_color = QColor(OMNINATIVE["primary"])
        unplayed_color = QColor(OMNINATIVE["accent"])
        
        for i, peak in enumerate(display_peaks):
            bar_x = start_x + i * (bar_w + bar_spacing)
            bar_center_x = bar_x + bar_w / 2.0
            
            # Determine if this bar is in the played portion
            ratio_at_bar = bar_center_x / float(w)
            is_played = ratio_at_bar <= self.playback_ratio
            
            color = played_color if is_played else unplayed_color
            
            # Draw vertical bar symmetric to center
            bar_h = max(3, int(h * 0.8 * peak))
            y_top = (h - bar_h) // 2
            
            # Draw with rounded corners
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(QRect(int(bar_x), int(y_top), max(1, int(bar_w)), int(bar_h)), 1, 1)
            
        # Draw playhead line
        playhead_x = int(self.playback_ratio * w)
        painter.setPen(QPen(QColor(OMNINATIVE["primary"]), 2))
        painter.drawLine(playhead_x, 0, playhead_x, h)
        
        # Draw playhead top handle
        handle_path = QPainterPath()
        handle_path.moveTo(playhead_x - 5, 0)
        handle_path.lineTo(playhead_x + 5, 0)
        handle_path.lineTo(playhead_x, 6)
        handle_path.closeSubpath()
        painter.setBrush(QBrush(QColor(OMNINATIVE["primary"])))
        painter.setPen(Qt.NoPen)
        painter.drawPath(handle_path)
        
        # Draw hover guide line if hovered
        if self.is_hovered and 0 <= self.hover_x <= w:
            painter.setPen(QPen(QColor(OMNINATIVE["accent"]), 1, Qt.DashLine))
            painter.drawLine(self.hover_x, 0, self.hover_x, h)
            
        painter.end()
        
    def mousePressEvent(self, event: Any) -> None:
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            ratio = event.position().x() / float(self.width())
            self.seek_requested.emit(ratio)
            
    def mouseMoveEvent(self, event: Any) -> None:
        self.hover_x = event.position().x()
        if self.is_dragging:
            ratio = self.hover_x / float(self.width())
            self.seek_requested.emit(ratio)
        self.update()
        
    def mouseReleaseEvent(self, event: Any) -> None:
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            
    def enterEvent(self, event: Any) -> None:
        self.is_hovered = True
        self.update()
        
    def leaveEvent(self, event: Any) -> None:
        self.is_hovered = False
        self.hover_x = -1
        self.update()

# ---------------------------------------------------------------------------
# OAudioPlayer
# ---------------------------------------------------------------------------
class OAudioPlayer(QWidget):
    file_loaded = Signal(str)  # Emits absolute filepath when an audio is loaded

    def __init__(self, master: Optional[QWidget] = None, **kwargs: Any) -> None:
        super().__init__(master)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        # Main layout
        self.layout_ = QVBoxLayout(self)
        self.layout_.setContentsMargins(8, 8, 8, 8)
        self.layout_.setSpacing(6)
        
        # State
        self.current_filepath = None
        self.duration = 0.0  # Duration in seconds
        self.position = 0.0  # Position in seconds
        self.is_playing = False
        self.is_looping = False
        
        # Native media player support (QtMultimedia)
        self.media_player = None
        self.audio_output = None
        self.capture_session = None
        self.audio_input = None
        self.media_recorder = None
        self.is_recording = False
        self.record_filepath = None
        try:
            from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaCaptureSession, QMediaRecorder, QAudioInput
            self.media_player = QMediaPlayer()
            self.audio_output = QAudioOutput()
            self.media_player.setAudioOutput(self.audio_output)
            
            self.capture_session = QMediaCaptureSession()
            self.audio_input = QAudioInput()
            self.capture_session.setAudioInput(self.audio_input)
            self.media_recorder = QMediaRecorder()
            self.capture_session.setRecorder(self.media_recorder)
            
            # Connect signals
            self.media_player.positionChanged.connect(self._on_media_position_changed)
            self.media_player.durationChanged.connect(self._on_media_duration_changed)
            self.media_player.playbackStateChanged.connect(self._on_media_state_changed)
            self.media_recorder.recorderStateChanged.connect(self._on_recorder_state_changed)
        except Exception as e:
            print(f"QtMultimedia not fully loaded: {e}. Simulation mode enabled.")
            
        # Simulation Timer
        self.sim_timer = QTimer(self)
        self.sim_timer.setInterval(16)  # ~60 fps
        self.sim_timer.timeout.connect(self._on_sim_timeout)
        self.last_tick_time = 0.0
        
        # Top Bar
        self.top_bar = QWidget()
        self.top_layout = QHBoxLayout(self.top_bar)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setSpacing(8)
        
        self.title_lbl = OElidedLabel("No Audio Loaded")
        self.title_lbl.setFont(QFont(_FONT_FAMILY, _FONT_SIZE_SM, QFont.Bold))
        self.title_lbl.setStyleSheet(f"color: {OMNINATIVE['bright']};")
        
        self.load_btn = OButton(self.top_bar, text="Load File", command=self._open_file_dialog)
        
        self.top_layout.addWidget(self.title_lbl, 1)
        self.top_layout.addWidget(self.load_btn)
        self.layout_.addWidget(self.top_bar)
        
        # Middle Waveform
        self.waveform = OAudioWaveform(self)
        self.waveform.seek_requested.connect(self.seek_to_ratio)
        self.layout_.addWidget(self.waveform)
        
        # Bottom Controls
        self.controls_bar = QWidget()
        self.controls_layout = QHBoxLayout(self.controls_bar)
        self.controls_layout.setContentsMargins(0, 0, 0, 0)
        self.controls_layout.setSpacing(10)
        
        self.record_btn = OAudioButton(self.controls_bar, "mic", size=24)
        self.record_btn.clicked.connect(self.toggle_record)
        
        self.play_btn = OAudioButton(self.controls_bar, "play", size=24)
        self.play_btn.clicked.connect(self.toggle_play)
        
        self.stop_btn = OAudioButton(self.controls_bar, "stop", size=24)
        self.stop_btn.clicked.connect(self.stop)
        
        self.time_lbl = QLabel("00:00 / 00:00")
        self.time_lbl.setFont(QFont(_FONT_FAMILY, _FONT_SIZE_SM))
        self.time_lbl.setStyleSheet(f"color: {OMNINATIVE['accent']};")
        
        self.vol_icon = QLabel()
        self.vol_icon.setFixedSize(20, 20)
        self.vol_icon.setAlignment(Qt.AlignCenter)
        self.vol_icon.setStyleSheet("background: transparent;")
        
        self.vol_slider = _WheelIgnoredSlider(Qt.Horizontal)
        self.vol_slider.setRange(0, 100)
        self.vol_slider.setValue(80)
        self.vol_slider.setFixedWidth(70)
        self.vol_slider.setCursor(Qt.PointingHandCursor)
        self.vol_slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                height: 4px;
                background: {OMNINATIVE['dark']};
                border-radius: 2px;
            }}
            QSlider::sub-page:horizontal {{
                background: {OMNINATIVE['primary']};
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: {OMNINATIVE['bright']};
                width: 10px;
                height: 10px;
                margin: -3px 0;
                border-radius: 5px;
            }}
            QSlider::handle:horizontal:hover {{
                background: {OMNINATIVE['primary']};
            }}
        """)
        self.vol_slider.valueChanged.connect(self.set_volume)
        self.controls_layout.addWidget(self.play_btn)
        self.controls_layout.addWidget(self.record_btn)
        self.controls_layout.addWidget(self.stop_btn)
        self.controls_layout.addWidget(self.time_lbl)
        self.controls_layout.addStretch(1)
        self.controls_layout.addWidget(self.vol_icon)
        self.controls_layout.addWidget(self.vol_slider)
        
        self.layout_.addWidget(self.controls_bar)
        
        # Initial updates
        self.update_time_label()
        self.set_volume(80)
        
    def _open_file_dialog(self) -> None:
        from PySide6.QtWidgets import QFileDialog
        filepath, _ = QFileDialog.getOpenFileName(None, "Open Audio File", "", "Audio Files (*.wav *.mp3 *.ogg *.m4a)")
        if filepath:
            self.current_filepath = filepath
            filename = os.path.basename(filepath)
            self.title_lbl.setText(filename)
            
            is_loaded_peaks = False
            if filepath.lower().endswith(".wav"):
                is_loaded_peaks = self.waveform.load_audio_file(filepath)
                
            if not is_loaded_peaks:
                self.waveform.generate_dummy_peaks(num_peaks=120)
                
            self.position = 0.0
            if self.media_player:
                from PySide6.QtCore import QUrl
                self.media_player.stop()
                self.media_player.setSource(QUrl.fromLocalFile(filepath))
                self.media_player.setPosition(0)
            else:
                self.sim_timer.stop()
                self.duration = 30.0
                
            self.is_playing = False
            self.play_btn.icon_type = "play"
            self.play_btn.set_active(False)
            self.update_playback()
            self.file_loaded.emit(filepath)
                
    def toggle_play(self) -> None:
        if not self.current_filepath:
            return
        if self.is_playing:
            self.pause()
        else:
            self.play()
            
    def play(self) -> None:
        if not self.current_filepath:
            return
        self.is_playing = True
        self.play_btn.icon_type = "pause"
        self.play_btn.set_active(True)
        
        self.last_tick_time = time.time()
        self.sim_timer.start()
        
        if self.media_player and self.media_player.source().isValid():
            self.media_player.play()
            
    def pause(self) -> None:
        if not self.current_filepath:
            return
        self.is_playing = False
        self.play_btn.icon_type = "play"
        self.play_btn.set_active(False)
        self.sim_timer.stop()
        
        if self.media_player and self.media_player.source().isValid():
            self.media_player.pause()
            
    def stop(self) -> None:
        if not self.current_filepath:
            return
        self.is_playing = False
        self.play_btn.icon_type = "play"
        self.play_btn.set_active(False)
        self.position = 0.0
        self.sim_timer.stop()
        
        if self.media_player and self.media_player.source().isValid():
            self.media_player.stop()
        self.update_playback()
            
    def set_volume(self, value: int) -> None:
        if self.media_player and self.audio_output:
            self.audio_output.setVolume(value / 100.0)
            
        # Determine icon type
        if value == 0:
            icon_type = "volume_mute"
        elif value < 40:
            icon_type = "volume_low"
        elif value < 80:
            icon_type = "volume_med"
        else:
            icon_type = "volume_high"
            
        pix = _get_cached_audio_icon(icon_type, size=20, color=OMNINATIVE["accent"])
        self.vol_icon.setPixmap(pix)
            
    def seek_to_ratio(self, ratio: float) -> None:
        if not self.current_filepath:
            return
        self.position = ratio * self.duration
        if self.media_player and self.media_player.source().isValid() and self.duration > 0:
            ms_pos = int(ratio * self.media_player.duration())
            self.media_player.setPosition(ms_pos)
        else:
            self.update_playback()
            if self.is_playing:
                self.last_tick_time = time.time()
        self._last_seek_time = time.time()
                
    def _on_sim_timeout(self) -> None:
        now = time.time()
        dt = now - self.last_tick_time
        self.last_tick_time = now
        
        if self.is_recording:
            amp = 0.05
            has_real_data = False
            if getattr(self, 'audio_io', None) and getattr(self, 'audio_fmt', None):
                try:
                    data = self.audio_io.readAll().data()
                    if data:
                        has_real_data = True
                        import struct
                        sf_str = str(self.audio_fmt.sampleFormat())
                        max_amp = 0.0
                        if 'Int16' in sf_str:
                            count = len(data) // 2
                            if count > 0:
                                samples = struct.unpack(f"<{count}h", data)
                                max_amp = max(abs(s) for s in samples) / 32768.0
                        elif 'Float' in sf_str:
                            count = len(data) // 4
                            if count > 0:
                                samples = struct.unpack(f"<{count}f", data)
                                max_amp = max(abs(s) for s in samples)
                        elif 'Int32' in sf_str:
                            count = len(data) // 4
                            if count > 0:
                                samples = struct.unpack(f"<{count}i", data)
                                max_amp = max(abs(s) for s in samples) / 2147483648.0
                        elif 'UInt8' in sf_str:
                            count = len(data)
                            if count > 0:
                                samples = struct.unpack(f"<{count}B", data)
                                max_amp = max(abs(s - 128) for s in samples) / 128.0
                        
                        amp = max(0.05, min(0.95, max_amp * 2.5))
                except Exception:
                    pass
            
            if not has_real_data:
                import math, random
                t = time.time() * 3.0
                envelope = abs(math.sin(t) * math.sin(t * 0.3) * math.cos(t * 0.8))
                noise = random.uniform(0.7, 1.0)
                amp = max(0.05, min(0.95, envelope * noise * 1.8))
                
            self.waveform.peaks.append(amp)
            self.waveform.playback_ratio = 1.0
            self.waveform.update()
            
            self.position += dt
            self.duration = self.position
            self.update_time_label()
            return
            
        if getattr(self, 'is_playing', False):
            if self.media_player and self.media_player.source().isValid():
                actual_pos = self.media_player.position() / 1000.0
                if time.time() - getattr(self, '_last_seek_time', 0.0) > 0.3:
                    if abs(self.position - actual_pos) > 0.5:
                        self.position = actual_pos
                    else:
                        self.position += dt
                        self.position = self.position * 0.9 + actual_pos * 0.1
                else:
                    self.position += dt
            else:
                self.position += dt
                
            if self.position >= self.duration and self.duration > 0:
                if getattr(self, 'is_looping', False):
                    self.position = 0.0
                else:
                    self.position = self.duration
                    self.stop()
                    return
            self.update_playback()
        
    def update_playback(self) -> None:
        ratio = 0.0
        if self.duration > 0:
            ratio = self.position / self.duration
        self.waveform.set_playback_ratio(ratio)
        self.update_time_label()
        
    def update_time_label(self) -> None:
        pos_min = int(self.position) // 60
        pos_sec = int(self.position) % 60
        dur_min = int(self.duration) // 60
        dur_sec = int(self.duration) % 60
        self.time_lbl.setText(f"{pos_min:02d}:{pos_sec:02d} / {dur_min:02d}:{dur_sec:02d}")
        
    def _on_media_position_changed(self, pos_ms: int) -> None:
        if self.media_player and self.media_player.duration() > 0:
            if not getattr(self, 'is_playing', False):
                self.position = pos_ms / 1000.0
                self.update_playback()
            
    def _on_media_duration_changed(self, dur_ms: int) -> None:
        self.duration = dur_ms / 1000.0
        self.update_playback()
        
    def _on_media_state_changed(self, state: Any) -> None:
        from PySide6.QtMultimedia import QMediaPlayer
        if state == QMediaPlayer.PlayingState:
            self.is_playing = True
            self.play_btn.icon_type = "pause"
            self.play_btn.set_active(True)
        else:
            self.is_playing = False
            self.play_btn.icon_type = "play"
            self.play_btn.set_active(False)
            
    def toggle_record(self) -> None:
        if not self.media_recorder:
            print("Recording not supported (QtMultimedia missing).")
            return
            
        if self.is_recording:
            self.media_recorder.stop()
        else:
            if self.is_playing:
                self.stop()
            import tempfile
            import os
            self.record_filepath = os.path.join(tempfile.gettempdir(), f"record_{int(time.time())}.m4a")
            from PySide6.QtCore import QUrl
            self.media_recorder.setOutputLocation(QUrl.fromLocalFile(self.record_filepath))
            self.media_recorder.record()
            self.is_recording = True
            self.record_btn.set_active(True)
            self.title_lbl.setText("Recording...")
            
            # Start QAudioSource for visual levels
            self.audio_source = None
            self.audio_io = None
            try:
                from PySide6.QtMultimedia import QAudioSource, QAudioFormat, QMediaDevices
                device = QMediaDevices.defaultAudioInput()
                fmt = device.preferredFormat()
                self.audio_fmt = fmt
                self.audio_source = QAudioSource(device, fmt, self)
                self.audio_io = self.audio_source.start()
            except Exception as e:
                print(f"Failed to start audio level source: {e}")
            
            self.waveform.peaks = []
            self.duration = 0.0
            self.position = 0.0
            self.last_tick_time = time.time()
            self.sim_timer.start()

    def _on_recorder_state_changed(self, state: Any) -> None:
        try:
            from PySide6.QtMultimedia import QMediaRecorder
        except ImportError:
            return
            
        if state == QMediaRecorder.StoppedState:
            self.sim_timer.stop()
            if getattr(self, 'audio_source', None):
                self.audio_source.stop()
                self.audio_source = None
                self.audio_io = None
                
            self.is_recording = False
            self.record_btn.set_active(False)
            
            import os
            if self.record_filepath and os.path.exists(self.record_filepath):
                self.current_filepath = self.record_filepath
                filename = os.path.basename(self.record_filepath)
                self.title_lbl.setText(filename)
                self.waveform.generate_dummy_peaks(num_peaks=120)
                self.position = 0.0
                if self.media_player:
                    from PySide6.QtCore import QUrl
                    self.media_player.setSource(QUrl.fromLocalFile(self.record_filepath))
                    self.media_player.setPosition(0)
                self.is_playing = False
                self.play_btn.icon_type = "play"
                self.play_btn.set_active(False)
                self.update_playback()
                self.file_loaded.emit(self.record_filepath)
            
    def get(self) -> Optional[str]:
        return self.current_filepath

    def pack(self, **kwargs: Any) -> None: pass

        


# ---------------------------------------------------------------------------
# OFullscreenViewer
# ---------------------------------------------------------------------------
class OFullscreenViewer(QDialog):
    def __init__(self, images_list: List[Dict[str, Any]], current_idx: int, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent, Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet(f"background-color: {OMNINATIVE['dark']};")
        self.layout_ = QVBoxLayout(self)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        
        self.images = images_list
        self.current_idx = current_idx
        
        self.image_lbl = QLabel()
        self.image_lbl.setAlignment(Qt.AlignCenter)
        self.layout_.addWidget(self.image_lbl)
        
        self.update_image()
        
    def update_image(self) -> None:
        if not self.images:
            return
        pixmap = self.images[self.current_idx]["pixmap"]
        screen_size = self.screen().size()
        scaled = pixmap.scaled(screen_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_lbl.setPixmap(scaled)
        
    def keyPressEvent(self, event: Any) -> None:
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Right:
            self.current_idx = (self.current_idx + 1) % len(self.images)
            self.update_image()
        elif event.key() == Qt.Key_Left:
            self.current_idx = (self.current_idx - 1) % len(self.images)
            self.update_image()
        else:
            super().keyPressEvent(event)
            
    def mousePressEvent(self, event: Any) -> None:
        if event.button() == Qt.LeftButton:
            self.close()

# ---------------------------------------------------------------------------
# OImageViewer
# ---------------------------------------------------------------------------
class OImageViewer(QWidget):
    file_loaded = Signal(str)

    def __init__(self, master: Optional[QWidget] = None, height: int = 260, **kwargs: Any) -> None:
        super().__init__(master)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.setMinimumHeight(height)
        
        self.images = []
        self.current_index = -1
        
        self.layout_ = QVBoxLayout(self)
        self.layout_.setContentsMargins(8, 8, 8, 8)
        self.layout_.setSpacing(0)
        
        # Top Bar
        self.top_bar = QWidget()
        self.top_layout = QHBoxLayout(self.top_bar)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setSpacing(8)
        
        self.title_lbl = OElidedLabel("No Image")
        self.title_lbl.setFont(QFont(_FONT_FAMILY, _FONT_SIZE_SM, QFont.Bold))
        self.title_lbl.setStyleSheet(f"color: {OMNINATIVE['bright']};")
        
        self.download_btn = OButton(self.top_bar, text="Download", command=self.download_current)
        self.load_btn = OButton(self.top_bar, text="Load", command=self._open_file_dialog)
        
        self.top_layout.addWidget(self.title_lbl, 1)
        self.top_layout.addWidget(self.download_btn)
        self.top_layout.addWidget(self.load_btn)
        self.layout_.addWidget(self.top_bar)
        
        # Image Area
        self.image_container = QFrame()
        self.image_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_container.setMinimumHeight(100)
        self.image_container.setStyleSheet(f"background-color: {OMNINATIVE['dark']}; border: 1px solid {OMNINATIVE['gray']}; border-radius: {_CORNER}px; margin-top: 7px; margin-bottom: 5px;")
        self.image_layout = QVBoxLayout(self.image_container)
        self.image_layout.setContentsMargins(4, 4, 4, 4)
        
        self.image_lbl = QLabel("Click to open Fullscreen")
        self.image_lbl.setAlignment(Qt.AlignCenter)
        self.image_lbl.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image_lbl.setStyleSheet("color: " + OMNINATIVE['accent'] + "; background: transparent; border: none;")
        self.image_lbl.setMouseTracking(True)
        self.image_lbl.mousePressEvent = self._on_image_click
        self.image_lbl.mouseMoveEvent = self._on_image_mouse_move
        self.image_layout.addWidget(self.image_lbl)
        
        self.layout_.addWidget(self.image_container, 1)
        
        self.thumbnails_container = QFrame()
        self.thumbnails_container.setFixedHeight(50)
        self.thumbnails_container.setStyleSheet(f"background-color: {OMNINATIVE['dark']}; border: 1px solid {OMNINATIVE['gray']}; border-radius: {_CORNER}px;")
        self.thumbnails_container_layout = QVBoxLayout(self.thumbnails_container)
        self.thumbnails_container_layout.setContentsMargins(0, 0, 0, 0)
        
        self.thumbnails_scroll = QScrollArea()
        self.thumbnails_scroll.setWidgetResizable(True)
        self.thumbnails_scroll.setStyleSheet("background: transparent; border: none;")
        self.thumbnails_container_layout.addWidget(self.thumbnails_scroll)
        
        self.thumbnails_widget = QWidget()
        self.thumbnails_widget.setStyleSheet("background: transparent;")
        self.thumbnails_layout = QHBoxLayout(self.thumbnails_widget)
        self.thumbnails_layout.setContentsMargins(4, 4, 4, 4)
        self.thumbnails_layout.setSpacing(8)
        self.thumbnails_layout.setAlignment(Qt.AlignLeft)
        self.thumbnails_scroll.setWidget(self.thumbnails_widget)
        self.layout_.addWidget(self.thumbnails_container)
        self.thumbnails_container.hide()
        
        self._update_controls()
        
    def _open_file_dialog(self) -> None:
        from PySide6.QtWidgets import QFileDialog
        from PySide6.QtCore import QStandardPaths
        desktop_path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        filepaths, _ = QFileDialog.getOpenFileNames(None, "Open Image(s)", desktop_path, "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif)")
        if filepaths:
            self.clear()
            for filepath in filepaths:
                self.load_file(filepath)
            
    def load_file(self, filepath: str) -> None:
        import os
        from PySide6.QtGui import QPixmap
        filename = os.path.basename(filepath)
        pixmap = QPixmap(filepath)
        if not pixmap.isNull():
            self.images.append({
                "pixmap": pixmap,
                "title": filename,
                "filepath": filepath
            })
            if self.current_index == -1:
                self.current_index = 0
            self._rebuild_thumbnails()
            self._update_image()
            self.file_loaded.emit(filepath)
            
    def add_pixmap(self, pixmap: QPixmap, title: str = "Generated Image") -> None:
        if pixmap and not pixmap.isNull():
            self.images.append({
                "pixmap": pixmap,
                "title": title,
                "filepath": None
            })
            if self.current_index == -1:
                self.current_index = 0
            self._rebuild_thumbnails()
            self._update_image()
            
    def set_pixmap(self, pixmap: QPixmap, title: str = "Generated Image") -> None:
        self.clear()
        self.add_pixmap(pixmap, title)
        
    def clear(self) -> None:
        self.images = []
        self.current_index = -1
        self._rebuild_thumbnails()
        self._update_image()
        
    def download_current(self) -> None:
        if self.current_index >= 0 and self.current_index < len(self.images):
            from PySide6.QtWidgets import QFileDialog
            from PySide6.QtCore import QStandardPaths
            import os
            
            img_data = self.images[self.current_index]
            desktop_path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
            default_path = os.path.join(desktop_path, img_data["title"])
            
            save_path, _ = QFileDialog.getSaveFileName(None, "Save Image", default_path, "Images (*.png *.jpg *.jpeg *.bmp)")
            if save_path:
                img_data["pixmap"].save(save_path)
                
    def _update_controls(self) -> None:
        has_images = len(self.images) > 0
        self.download_btn.setVisible(has_images)
        
    def _rebuild_thumbnails(self) -> None:
        while self.thumbnails_layout.count():
            item = self.thumbnails_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        if len(self.images) <= 1:
            self.thumbnails_container.hide()
            return
            
        self.thumbnails_container.show()
        for idx, img_data in enumerate(self.images):
            thumb_lbl = QLabel()
            thumb_lbl.setFixedSize(35, 35)
            thumb_lbl.setCursor(Qt.PointingHandCursor)
            
            pixmap = img_data["pixmap"]
            scaled = pixmap.scaled(35, 35, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            
            from PySide6.QtGui import QPainter, QPainterPath, QPixmap
            rounded = QPixmap(scaled.size())
            rounded.fill(Qt.transparent)
            painter = QPainter(rounded)
            painter.setRenderHint(QPainter.Antialiasing)
            path = QPainterPath()
            path.addRoundedRect(0, 0, scaled.width(), scaled.height(), 4, 4)
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, scaled)
            painter.end()
            
            thumb_lbl.setPixmap(rounded)
            
            if idx == self.current_index:
                thumb_lbl.setStyleSheet(f"border: 1px solid {OMNINATIVE['bright']}; border-radius: 4px;")
            else:
                thumb_lbl.setStyleSheet(f"border: 1px solid {OMNINATIVE['gray']}; border-radius: 4px;")
                
            thumb_lbl.mousePressEvent = lambda e, i=idx: self.set_current_index(i)
            self.thumbnails_layout.addWidget(thumb_lbl)

    def set_current_index(self, idx: int) -> None:
        if 0 <= idx < len(self.images):
            self.current_index = idx
            self._update_image()

    def _update_image(self) -> None:
        self._update_controls()
        
        # Update thumbnails selection
        for i in range(self.thumbnails_layout.count()):
            widget = self.thumbnails_layout.itemAt(i).widget()
            if widget:
                if i == self.current_index:
                    widget.setStyleSheet(f"border: 1px solid {OMNINATIVE['bright']}; border-radius: 4px;")
                else:
                    widget.setStyleSheet(f"border: 1px solid {OMNINATIVE['gray']}; border-radius: 4px;")
                    
        if self.current_index >= 0 and self.current_index < len(self.images):
            img_data = self.images[self.current_index]
            title = img_data["title"]
            if len(self.images) > 1:
                title = f"[{self.current_index + 1}/{len(self.images)}] {title}"
            self.title_lbl.setText(title)
            
            pixmap = img_data["pixmap"]
            size = self.image_lbl.size()
            scaled_pixmap = pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_lbl.setPixmap(scaled_pixmap)
        else:
            self.title_lbl.setText("No Image")
            self.image_lbl.clear()
            self.image_lbl.setText("Click 'Load' to add images")
            
    def resizeEvent(self, event: Any) -> None:
        super().resizeEvent(event)
        self._update_image()
        
    def _on_image_click(self, event: Any) -> None:
        if event.button() == Qt.LeftButton and self.images:
            if self.image_lbl.pixmap():
                pix_rect = self.image_lbl.pixmap().rect()
                pix_rect.moveCenter(self.image_lbl.rect().center())
                if not pix_rect.contains(event.position().toPoint() if hasattr(event, "position") else event.pos()):
                    return
            self.show_fullscreen()
            
    def _on_image_mouse_move(self, event: Any) -> None:
        if self.images and self.image_lbl.pixmap():
            pix_rect = self.image_lbl.pixmap().rect()
            pix_rect.moveCenter(self.image_lbl.rect().center())
            pos = event.position().toPoint() if hasattr(event, "position") else event.pos()
            if pix_rect.contains(pos):
                self.image_lbl.setCursor(Qt.PointingHandCursor)
            else:
                self.image_lbl.setCursor(Qt.ArrowCursor)
        else:
            self.image_lbl.setCursor(Qt.ArrowCursor)
            
    def show_fullscreen(self) -> None:
        if self.images:
            self.fs_viewer = OFullscreenViewer(self.images, self.current_index, self)
            self.fs_viewer.showFullScreen()
            self.fs_viewer.exec()
            
    def get(self) -> Optional[str]:
        if self.current_index >= 0 and self.current_index < len(self.images):
            return self.images[self.current_index]["filepath"]
        return None
        
    def pack(self, **kwargs: Any) -> None: pass
