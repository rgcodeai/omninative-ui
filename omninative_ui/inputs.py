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
from ._utils import apply_layout_dimensions


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
        **kwargs: Any,
    ) -> None:
        super().__init__(master)
        self.setPlaceholderText(placeholder)
        apply_layout_dimensions(self, width, height)
        self._command = command
        self._on_enter_callback = on_enter
        
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
        
        btn_style = f"""
            QPushButton {{
                background: {OMNINATIVE['dark']};
                color: {OMNINATIVE['accent']};
                border: 1px solid {OMNINATIVE['gray']};
                border-radius: {_CORNER}px;
                text-align: center;
                padding-bottom: 2px;
            }}
            QPushButton:hover {{
                color: {OMNINATIVE['primary']};
                border: 1px solid {OMNINATIVE['primary']};
            }}
        """
        
        self.btn_minus = QPushButton("−")
        self.btn_minus.setFixedSize(button_width, height)
        self.btn_minus.clicked.connect(self._decrement)
        self.btn_minus.setStyleSheet(btn_style)
        
        entry_w = "100%" if isinstance(width, str) and width in ("100%", "expand", "fill") else (width - button_width * 2 - (spacing * 2) if isinstance(width, int) and width > 0 else "100%")
        self.entry = OLineEdit(self, width=entry_w, height=height)
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
        
        self._entry = OLineEdit(self, width=entry_width)
        self._entry.setAlignment(Qt.AlignCenter)
        self._entry.set(str(value))
        
        if not show_entry:
            self._entry.hide()
            
        self.layout_.addWidget(self._slider)
        self.layout_.addWidget(self._entry)
        
        self._command = command
        
        self._slider.valueChanged.connect(self._on_slider_changed)
        self._entry.textChanged.connect(self._on_entry_changed)
        
        self._slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                border: none;
                height: 3px;
                background: {OMNINATIVE['dark']};
                border-radius: 1px;
            }}
            QSlider::handle:horizontal {{
                background: {OMNINATIVE['accent']};
                border: none;
                width: 8px;
                margin: -2px 0px -3px 0px;
                border-radius: 4px;
            }}
            QSlider::handle:horizontal:hover {{
                background: {OMNINATIVE['bright']};
            }}
            QSlider::sub-page:horizontal {{
                background: {OMNINATIVE['primary']};
                border-radius: 1px;
            }}
            QSlider::groove:vertical {{
                border: none;
                width: 3px;
                background: {OMNINATIVE['dark']};
                border-radius: 1px;
            }}
            QSlider::handle:vertical {{
                background: {OMNINATIVE['accent']};
                border: none;
                height: 8px;
                margin: 0px -3px 0px -2px;
                border-radius: 4px;
            }}
            QSlider::handle:vertical:hover {{
                background: {OMNINATIVE['bright']};
            }}
            QSlider::add-page:vertical {{
                background: {OMNINATIVE['primary']};
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
            
        self.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                background-color: {OMNINATIVE['dark']};
                border-radius: {cr}px;
            }}
            QProgressBar::chunk {{
                background-color: {OMNINATIVE['primary']};
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
