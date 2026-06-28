# omninative_ui/inputs.py
from typing import Optional, Callable, Any, Union
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QSlider,
    QProgressBar,
    QSizePolicy,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from .tokens import (
    OMNINATIVE,
    _FONT_FAMILY,
    _FONT_SIZE_SM,
    _CORNER,
    _PAD,
)
from ._utils import apply_layout_dimensions, o_theme_val


# ---------------------------------------------------------------------------
# OLineEdit
# ---------------------------------------------------------------------------
class OLineEdit(QLineEdit):
    def __init__(
        self,
        master: Optional[QWidget] = None,
        placeholder: str = "",
        width: Union[int, str] = "100%",
        height: Union[int, str] = 22,
        command: Optional[Callable[[str], None]] = None,
        password: bool = False,
        read_only: bool = False,
        bg_color: Optional[str] = None,
        bg_focus_color: Optional[str] = None,
        text_color: Optional[str] = None,
        border_color: Optional[str] = None,
        border_focus_color: Optional[str] = None,
        border_width: int = 1,
        border_radius: Optional[int] = None,
        font_size: Optional[int] = None,
        theme: Optional[dict] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master)
        self.setPlaceholderText(placeholder)
        apply_layout_dimensions(self, width, height)
        self._command = command
        
        if password:
            self.setEchoMode(QLineEdit.Password)
        if read_only:
            self.setReadOnly(True)
            
        _bg = o_theme_val(theme, "bg_color", bg_color, OMNINATIVE["surface"])
        _bg_foc = o_theme_val(theme, "bg_focus_color", bg_focus_color, _bg)
        _txt = o_theme_val(theme, "text_color", text_color, OMNINATIVE["fg"])
        _bc = o_theme_val(theme, "border_color", border_color, OMNINATIVE["border"])
        _bc_foc = o_theme_val(theme, "border_focus_color", border_focus_color, OMNINATIVE["accent"])
        _bw = o_theme_val(theme, "border_width", border_width, 1)
        _br = o_theme_val(theme, "border_radius", border_radius, _CORNER)
        _sz = o_theme_val(theme, "font_size", font_size, _FONT_SIZE_SM)

        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {_bg};
                color: {_txt};
                border: {_bw}px solid {_bc};
                border-radius: {_br}px;
                padding: 2px 4px;
                font-family: "{_FONT_FAMILY}";
                font-size: {_sz}pt;
            }}
            QLineEdit:focus {{
                border: {_bw}px solid {_bc_foc};
                background-color: {_bg_foc};
            }}
            QLineEdit[readOnly="true"] {{
                color: {OMNINATIVE["fg_muted"]};
                background-color: transparent;
                border: {_bw}px solid {OMNINATIVE["border"]};
            }}
            QLineEdit[readOnly="true"]:focus {{
                border: {_bw}px solid {OMNINATIVE["accent"]};
            }}
        """)
            
        self.textChanged.connect(self._on_text_changed)
        
    def _on_text_changed(self, text: str) -> None:
        if self._command:
            self._command(text)
            
    def get(self) -> str:
        return self.text()
        
    def set(self, val: Any) -> None:
        self.setText(str(val))
        self.setCursorPosition(0)
        
    def bind(self, event: Any, callback: Any, **kwargs: Any) -> None:
        # Dummy for tkinter compatibility
        pass
        
    def pack(self, **kwargs: Any) -> None: pass

# ---------------------------------------------------------------------------
# OHotkeyInput
# ---------------------------------------------------------------------------
class OHotkeyInput(OLineEdit):
    """
    A special line edit that captures keystrokes and formats them as hotkeys
    (e.g., 'ctrl+shift+r') instead of allowing normal typing. Shows live feedback.
    """
    def __init__(
        self, 
        master: Optional[QWidget] = None, 
        bg_color: Optional[str] = None,
        text_color: Optional[str] = None,
        text_recording_color: Optional[str] = None,
        border_color: Optional[str] = None,
        border_focus_color: Optional[str] = None,
        border_width: int = 1,
        border_radius: Optional[int] = None,
        font_size: Optional[int] = None,
        theme: Optional[dict] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(
            master, 
            bg_color=bg_color,
            text_color=text_color,
            border_color=border_color,
            border_focus_color=border_focus_color,
            border_width=border_width,
            border_radius=border_radius,
            font_size=font_size,
            theme=theme,
            **kwargs
        )
        self.setObjectName("OHotkeyInput")
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setCursor(Qt.PointingHandCursor)
        self.setPlaceholderText("Click here and press a shortcut...")
        self._recording_state = False
        self.setProperty("recording", False)
        
        _bg = o_theme_val(theme, "bg_color", bg_color, OMNINATIVE["surface"])
        _txt = o_theme_val(theme, "text_color", text_color, OMNINATIVE["fg_muted"])
        _txt_rec = o_theme_val(theme, "text_recording_color", text_recording_color, OMNINATIVE["fg"])
        _bc = o_theme_val(theme, "border_color", border_color, OMNINATIVE["border"])
        _bc_foc = o_theme_val(theme, "border_focus_color", border_focus_color, OMNINATIVE["accent"])
        _bw = o_theme_val(theme, "border_width", border_width, 1)
        _br = o_theme_val(theme, "border_radius", border_radius, _CORNER)
        _sz = o_theme_val(theme, "font_size", font_size, _FONT_SIZE_SM)

        self.setStyleSheet(f"""
            #OHotkeyInput {{
                background-color: {_bg};
                color: {_txt};
                border: {_bw}px solid {_bc};
                border-radius: {_br}px;
                padding: 2px 4px;
                font-family: "{_FONT_FAMILY}";
                font-size: {_sz}pt;
            }}
            #OHotkeyInput:focus {{
                border: {_bw}px solid {_bc_foc};
            }}
            #OHotkeyInput[recording="true"] {{
                color: {_txt_rec};
            }}
        """)
        
    @property
    def _recording(self) -> bool:
        return self._recording_state
        
    @_recording.setter
    def _recording(self, value: bool) -> None:
        if self._recording_state != value:
            self._recording_state = value
            self.setProperty("recording", value)
            self.style().unpolish(self)
            self.style().polish(self)
        
    def _on_text_changed(self, text: str) -> None:
        # Override OLineEdit's behavior: do not fire command automatically
        # when text changes, because we manually fire it on finalized hotkeys.
        pass
        
    def mousePressEvent(self, event: Any) -> None:
        self._recording = True
        super().mousePressEvent(event)
        
    def focusInEvent(self, event: Any) -> None:
        super().focusInEvent(event)
        
    def focusOutEvent(self, event: Any) -> None:
        self._recording = False
        if self.text().endswith("..."):
            self.set("")
        super().focusOutEvent(event)
        
    def keyPressEvent(self, event: Any) -> None:
        key = event.key()
        modifiers = event.modifiers()
        
        if key == Qt.Key_unknown:
            return
            
        # Allow backspace to clear the hotkey
        if key in (Qt.Key_Backspace, Qt.Key_Delete):
            self.set("")
            if self._command:
                self._command("")
            self._recording = True
            event.accept()
            return
            
        self._recording = True
            
        parts = []
        if modifiers & Qt.ControlModifier or key == Qt.Key_Control:
            parts.append("ctrl")
        if modifiers & Qt.ShiftModifier or key == Qt.Key_Shift:
            parts.append("shift")
        if modifiers & Qt.AltModifier or key == Qt.Key_Alt:
            parts.append("alt")
            
        is_modifier = key in (Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt, Qt.Key_Meta)
        
        if is_modifier:
            if parts:
                self.setText("+".join(parts) + "+...")
        else:
            from PySide6.QtGui import QKeySequence
            key_name = QKeySequence(key).toString().lower()
            if key_name:
                parts.append(key_name)
                hotkey_str = "+".join(parts)
                self.set(hotkey_str)
                if self._command:
                    self._command(hotkey_str)
                self._recording = False
                
        event.accept()

    def keyReleaseEvent(self, event: Any) -> None:
        if not self._recording:
            super().keyReleaseEvent(event)
            return
            
        key = event.key()
        modifiers = event.modifiers()
        
        parts = []
        ctrl = bool(modifiers & Qt.ControlModifier)
        shift = bool(modifiers & Qt.ShiftModifier)
        alt = bool(modifiers & Qt.AltModifier)
        
        if key == Qt.Key_Control: ctrl = False
        if key == Qt.Key_Shift: shift = False
        if key == Qt.Key_Alt: alt = False
        
        if ctrl: parts.append("ctrl")
        if shift: parts.append("shift")
        if alt: parts.append("alt")
        
        if parts:
            self.setText("+".join(parts) + "+...")
        else:
            self.setText("")
            
        event.accept()

# ---------------------------------------------------------------------------
# OTextBox
# ---------------------------------------------------------------------------
class OTextBox(QTextEdit):
    def __init__(
        self,
        master: Optional[QWidget] = None,
        placeholder: str = "",
        width: Union[int, str] = "100%",
        height: Union[int, str] = 40,
        command: Optional[Callable[[str], None]] = None,
        on_enter: Optional[Callable[['OTextBox', str, str], None]] = None,
        bg_color: Optional[str] = None,
        bg_focus_color: Optional[str] = None,
        text_color: Optional[str] = None,
        border_color: Optional[str] = None,
        border_focus_color: Optional[str] = None,
        border_width: int = 1,
        border_radius: Optional[int] = None,
        font_size: Optional[int] = None,
        theme: Optional[dict] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master)
        self.setPlaceholderText(placeholder)
        apply_layout_dimensions(self, width, height)
        self._command = command
        self._on_enter_callback = on_enter
        
        _bg = o_theme_val(theme, "bg_color", bg_color, OMNINATIVE["surface"])
        _bg_foc = o_theme_val(theme, "bg_focus_color", bg_focus_color, _bg)
        _txt = o_theme_val(theme, "text_color", text_color, OMNINATIVE["fg"])
        _bc = o_theme_val(theme, "border_color", border_color, OMNINATIVE["border"])
        _bc_foc = o_theme_val(theme, "border_focus_color", border_focus_color, OMNINATIVE["accent"])
        _bw = o_theme_val(theme, "border_width", border_width, 1)
        _br = o_theme_val(theme, "border_radius", border_radius, _CORNER)
        _sz = o_theme_val(theme, "font_size", font_size, _FONT_SIZE_SM)

        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {_bg};
                color: {_txt};
                border: {_bw}px solid {_bc};
                border-radius: {_br}px;
                padding: 2px 4px;
                font-family: "{_FONT_FAMILY}";
                font-size: {_sz}pt;
            }}
            QTextEdit:focus {{
                border: {_bw}px solid {_bc_foc};
                background-color: {_bg_foc};
            }}
            QTextEdit[readOnly="true"] {{
                color: {OMNINATIVE["fg_muted"]};
                background-color: transparent;
                border: {_bw}px solid {OMNINATIVE["border"]};
            }}
            QTextEdit[readOnly="true"]:focus {{
                border: {_bw}px solid {OMNINATIVE["accent"]};
            }}
        """)
        
        self.textChanged.connect(self._on_text_changed)
        
    def _on_text_changed(self) -> None:
        if self._command:
            self._command(self.toPlainText())
            
    def wheelEvent(self, event: Any) -> None:
        if self.hasFocus():
            super().wheelEvent(event)
            event.accept()
        else:
            event.ignore()
            
    def keyPressEvent(self, event: Any) -> None:
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if not (event.modifiers() & Qt.ShiftModifier):
                if self._on_enter_callback:
                    content = self.toPlainText()
                    cursor = self.textCursor()
                    pos = cursor.position()
                    text_before = content[:pos]
                    text_after = content[pos:]
                    self._on_enter_callback(self, text_before, text_after)
                return
        super().keyPressEvent(event)
        
    def get(self, start: str = "1.0", end: str = "end-1c") -> str:
        return self.toPlainText()
        
    def set(self, val: Any) -> None:
        self.setPlainText(str(val))
        
    def focus_set_at_start(self) -> None:
        self.setFocus()
        cursor = self.textCursor()
        cursor.setPosition(0)
        self.setTextCursor(cursor)
        
    def pack(self, **kwargs: Any) -> None: pass
    def configure(self, **kwargs: Any) -> None:
        if "state" in kwargs:
            self.setReadOnly(kwargs["state"] == "disabled")

# ---------------------------------------------------------------------------
# OSpinBox
# ---------------------------------------------------------------------------
class OSpinBox(QWidget):
    def __init__(
        self,
        master: Optional[QWidget] = None,
        from_: int = 0,
        to: int = 100,
        value: int = 0,
        step: int = 1,
        command: Optional[Callable[[int], None]] = None,
        width: Union[int, str] = 120,
        height: Union[int, str] = 22,
        pad: int = 0,
        spacing: int = 2,
        button_width: int = 24,
        show_buttons: bool = True,
        bg_color: Optional[str] = None,
        bg_focus_color: Optional[str] = None,
        text_color: Optional[str] = None,
        border_color: Optional[str] = None,
        border_focus_color: Optional[str] = None,
        border_width: int = 1,
        border_radius: Optional[int] = None,
        font_size: Optional[int] = None,
        theme: Optional[dict] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master)
        self.layout_ = QHBoxLayout(self)
        self.layout_.setContentsMargins(pad, pad, pad, pad)
        self.layout_.setSpacing(spacing)
        
        apply_layout_dimensions(self, width, height)
            
        self._min = from_
        self._max = to
        self._step = step
        self._command = command
        self._value = value
        
        _btn_bg = o_theme_val(theme, "bg_color", bg_color, OMNINATIVE['surface'])
        _btn_txt = o_theme_val(theme, "text_color", text_color, OMNINATIVE['fg_muted'])
        _bc = o_theme_val(theme, "border_color", border_color, OMNINATIVE['border'])
        _bc_foc = o_theme_val(theme, "border_focus_color", border_focus_color, OMNINATIVE['accent'])
        _br = o_theme_val(theme, "border_radius", border_radius, _CORNER)

        btn_style = f"""
            QPushButton {{
                background: {_btn_bg};
                color: {_btn_txt};
                border: 1px solid {_bc};
                border-radius: {_br}px;
                text-align: center;
                padding-bottom: 2px;
            }}
            QPushButton:hover {{
                color: {OMNINATIVE['accent']};
                border: 1px solid {_bc_foc};
            }}
        """
        
        self.btn_minus = QPushButton("−")
        self.btn_minus.setFixedSize(button_width, height)
        self.btn_minus.clicked.connect(self._decrement)
        self.btn_minus.setStyleSheet(btn_style)
        
        entry_w = "100%" if isinstance(width, str) and width in ("100%", "expand", "fill") else (width - button_width * 2 - (spacing * 2) if isinstance(width, int) and width > 0 else "100%")
        self.entry = OLineEdit(
            self, 
            width=entry_w, 
            height=height,
            bg_color=bg_color,
            bg_focus_color=bg_focus_color,
            text_color=text_color,
            border_color=border_color,
            border_focus_color=border_focus_color,
            border_width=border_width,
            border_radius=border_radius,
            font_size=font_size,
            theme=theme
        )
        self.entry.setAlignment(Qt.AlignCenter)
        self.entry.set(str(value))
        
        self.btn_plus = QPushButton("+")
        self.btn_plus.setFixedSize(button_width, height)
        self.btn_plus.clicked.connect(self._increment)
        self.btn_plus.setStyleSheet(btn_style)
        
        if not show_buttons:
            self.btn_minus.hide()
            self.btn_plus.hide()
            
        self.layout_.addWidget(self.btn_minus)
        self.layout_.addWidget(self.entry, 1)
        self.layout_.addWidget(self.btn_plus)
        
    def get(self) -> int:
        try:
            return int(self.entry.get())
        except ValueError:
            return self._value
            
    def set(self, val: int) -> None:
        val = max(self._min, min(self._max, val))
        self._value = val
        self.entry.set(str(val))
        
    def _increment(self) -> None:
        self.set(self.get() + self._step)
        if self._command: self._command(self.get())
        
    def _decrement(self) -> None:
        self.set(self.get() - self._step)
        if self._command: self._command(self.get())
        
    def pack(self, **kwargs: Any) -> None: pass

# ---------------------------------------------------------------------------
# OSlider
# ---------------------------------------------------------------------------
class _WheelIgnoredSlider(QSlider):
    def wheelEvent(self, event: Any) -> None:
        event.ignore()

class OSlider(QWidget):
    def __init__(
        self,
        master: Optional[QWidget] = None,
        orientation: str = "h",
        from_: int = 0,
        to: int = 100,
        value: int = 0,
        command: Optional[Callable[[int], None]] = None,
        width: Union[int, str] = "100%",
        pad: int = 0,
        spacing: int = 6,
        entry_width: int = 40,
        show_entry: bool = True,
        bg_color: Optional[str] = None,
        primary_color: Optional[str] = None,
        text_color: Optional[str] = None,
        border_color: Optional[str] = None,
        font_size: Optional[int] = None,
        theme: Optional[dict] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master)
        self.layout_ = QHBoxLayout(self)
        self.layout_.setContentsMargins(pad, pad, pad, pad)
        self.layout_.setSpacing(spacing)
        
        apply_layout_dimensions(self, width, 22)
            
        ori = Qt.Horizontal if orientation == "h" else Qt.Vertical
        self._slider = _WheelIgnoredSlider(ori, self)
        self._slider.setMinimum(from_)
        self._slider.setMaximum(to)
        self._slider.setValue(value)
        self._slider.setCursor(Qt.PointingHandCursor)
        
        self._entry = OLineEdit(
            self, 
            width=entry_width,
            bg_color=bg_color,
            text_color=text_color,
            border_color=border_color,
            font_size=font_size,
            theme=theme
        )
        self._entry.setAlignment(Qt.AlignCenter)
        self._entry.set(str(value))
        
        if not show_entry:
            self._entry.hide()
            
        self.layout_.addWidget(self._slider)
        self.layout_.addWidget(self._entry)
        
        self._command = command
        
        self._slider.valueChanged.connect(self._on_slider_changed)
        self._entry.textChanged.connect(self._on_entry_changed)
        
        _bg = o_theme_val(theme, "bg_color", bg_color, OMNINATIVE['surface'])
        _primary = o_theme_val(theme, "primary_color", primary_color, OMNINATIVE['accent'])
        _accent = o_theme_val(theme, "accent_color", None, OMNINATIVE['fg_muted'])
        _bright = o_theme_val(theme, "bright_color", None, OMNINATIVE['fg'])

        self._slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                border: none;
                height: 3px;
                background: {_bg};
                border-radius: 1px;
            }}
            QSlider::handle:horizontal {{
                background: {_accent};
                border: none;
                width: 8px;
                margin: -2px 0px -3px 0px;
                border-radius: 4px;
            }}
            QSlider::handle:horizontal:hover {{
                background: {_bright};
            }}
            QSlider::sub-page:horizontal {{
                background: {_primary};
                border-radius: 1px;
            }}
            QSlider::groove:vertical {{
                border: none;
                width: 3px;
                background: {_bg};
                border-radius: 1px;
            }}
            QSlider::handle:vertical {{
                background: {_accent};
                border: none;
                height: 8px;
                margin: 0px -3px 0px -2px;
                border-radius: 4px;
            }}
            QSlider::handle:vertical:hover {{
                background: {_bright};
            }}
            QSlider::add-page:vertical {{
                background: {_primary};
                border-radius: 1px;
            }}
        """)
        
    def _on_slider_changed(self, val: int) -> None:
        self._entry.blockSignals(True)
        self._entry.set(str(val))
        self._entry.blockSignals(False)
        if self._command:
            self._command(val)
            
    def _on_entry_changed(self, text: str) -> None:
        try:
            val = int(text)
            val = max(self._slider.minimum(), min(self._slider.maximum(), val))
            self._slider.blockSignals(True)
            self._slider.setValue(val)
            self._slider.blockSignals(False)
            if self._command:
                self._command(val)
        except ValueError:
            pass

    def get(self) -> int:
        return self._slider.value()
        
    def set(self, val: int) -> None:
        self._slider.setValue(val)
        
    def pack(self, **kwargs: Any) -> None: pass

# ---------------------------------------------------------------------------
# OProgressBar
# ---------------------------------------------------------------------------
class OProgressBar(QProgressBar):
    def __init__(
        self,
        master: Optional[QWidget] = None,
        from_: int = 0,
        to: int = 100,
        value: int = 0,
        width: Union[int, str] = "100%",
        height: Union[int, str] = 3,
        bg_color: Optional[str] = None,
        primary_color: Optional[str] = None,
        theme: Optional[dict] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master)
        self.setRange(from_, to)
        self.setValue(value)
        self.setTextVisible(False)
        
        apply_layout_dimensions(self, width, height)
            
        h = int(height) if isinstance(height, int) else 3
        cr = h // 2
        if cr < 1:
            cr = 1
            
        _bg = o_theme_val(theme, "bg_color", bg_color, OMNINATIVE['surface'])
        _primary = o_theme_val(theme, "primary_color", primary_color, OMNINATIVE['accent'])

        self.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                background-color: {_bg};
                border-radius: {cr}px;
            }}
            QProgressBar::chunk {{
                background-color: {_primary};
                border-radius: {cr}px;
            }}
        """)
        
    def get(self) -> int:
        return self.value()
        
    def set(self, val: int) -> None:
        self.setValue(val)
        
    def set_indeterminate(self, active: bool = True) -> None:
        if active:
            self.setRange(0, 0)
        else:
            self.setRange(0, 100)
            self.setValue(0)
            
    def pack(self, **kwargs: Any) -> None:
        pass
