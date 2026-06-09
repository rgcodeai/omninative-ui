# omninative_ui/core.py
import os
import time
from typing import Optional, List, Dict, Any, Union, Callable

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QSizePolicy,
    QScrollArea, QRadioButton
)
from PySide6.QtGui import (
    QColor, QFont, QPixmap, QPainter, QPainterPath, QPen, QIcon,
    QCursor, QBrush, QFontMetrics
)
from PySide6.QtCore import (
    Qt, Signal, QTimer, QSize, QPoint, QRect
)

from .tokens import OMNINATIVE, _FONT_FAMILY, _FONT_SIZE_SM, _FONT_SIZE_LG, _CORNER, _PAD
from .icons import _get_cached_checkbox, _get_cached_chevron
from ._utils import get_global_stylesheet


# ---------------------------------------------------------------------------
# OWindow — Top-level window
# ---------------------------------------------------------------------------
class OWindow(QMainWindow):
    def __init__(self, title: str = "OmniNative Plugin", width: int = 480, height: int = 620, resizable: bool = False, icon_path: Optional[str] = None) -> None:
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.Window)

        self._resizable = resizable

        if icon_path and os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            from .icons import _get_cached_app_icon
            self.setWindowIcon(_get_cached_app_icon())

        if height > 0:
            self.resize(width, height)
        else:
            self.setMinimumSize(width, 200)

        if not resizable:
            self.setFixedSize(self.size())

        self.setStyleSheet(get_global_stylesheet())

        # Root structure
        self.central_widget = QWidget()
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self._root_layout = QVBoxLayout(self.central_widget)
        self._root_layout.setContentsMargins(0, 0, 0, 0)
        self._root_layout.setSpacing(0)

        # Content area without global margins (margins must be applied inside scrollable areas)
        content_wrapper = QWidget()
        content_wrapper.setObjectName("content_wrapper")
        content_wrapper.setStyleSheet("#content_wrapper { background: transparent; }")
        self.main_layout = QVBoxLayout(content_wrapper)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self._root_layout.addWidget(content_wrapper, 1)

        self._body = QWidget()
        self._body_layout = QVBoxLayout(self._body)
        self._body_layout.setContentsMargins(0, 0, 0, 0)
        self._body_layout.setSpacing(0)
        self.main_layout.addWidget(self._body)

        self.setWindowOpacity(0.0)

    @property
    def body(self) -> QWidget:
        return self._body

    def omninativeui_reveal_when_ready(self, alpha: float = 1.0) -> None:
        self.setWindowOpacity(alpha)


# ---------------------------------------------------------------------------
# OGroup — Layout container
# ---------------------------------------------------------------------------
class OGroup(QFrame):
    def __init__(self, master: Optional[QWidget], orientation: str = "v", pad: int = _PAD, panel: bool = False, **kwargs: Any) -> None:
        super().__init__(master)
        self._pad = pad
        self._orient = orientation
        
        if orientation == "v":
            self.layout_ = QVBoxLayout(self)
        else:
            self.layout_ = QHBoxLayout(self)
            
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(pad)
        
        if panel:
            self.setStyleSheet(f"""
                OGroup {{
                    background-color: {OMNINATIVE["background"]};
                    border: 1px solid {OMNINATIVE["dark"]};
                    border-radius: {_CORNER}px;
                }}
            """)
        else:
            self.setStyleSheet("OGroup { border: none; background-color: transparent; }")

    def add(self, widget: QWidget, expand: bool = False, fill: str = "none", padx: int = 0, pady: int = 0) -> None:
        # Compatibility layer for CTk .pack() params
        pass # Not used directly if we patch gui.py to use addWidget

    def pack(self, **kwargs: Any) -> None:
        # Shim to make gui.py conversion easier if we still call .pack() on the object
        # but in PySide, we should add it to the parent layout.
        # We will override this by adapting gui.py directly to PySide layouts.
        pass

# ---------------------------------------------------------------------------
# OLabel
# ---------------------------------------------------------------------------
class OLabel(QLabel):
    def __init__(self, master: Optional[QWidget], text: str = "", bold: bool = False, bright: bool = False, size: Optional[int] = None, width: int = 0, anchor: str = "w", **kwargs: Any) -> None:
        super().__init__(master)
        self.setText(text)
        
        sz = size or _FONT_SIZE_SM
        weight = QFont.Bold if bold else QFont.Normal
        color = OMNINATIVE["accent"]
        if bright: color = OMNINATIVE["bright"]
        
        font = QFont(_FONT_FAMILY, sz, weight)
        self.setFont(font)
        self.setStyleSheet(f"color: {color}; background: transparent;")
        
        if width > 0:
            self.setFixedWidth(width)
            
        align = Qt.AlignLeft | Qt.AlignVCenter
        if anchor == "center":
            align = Qt.AlignCenter
        elif anchor == "e":
            align = Qt.AlignRight | Qt.AlignVCenter
        self.setAlignment(align)

    def pack(self, **kwargs: Any) -> None:
        pass

# ---------------------------------------------------------------------------
# OElidedLabel
# ---------------------------------------------------------------------------
class OElidedLabel(QLabel):
    def __init__(self, text: str = "", parent: Optional[QWidget] = None, **kwargs: Any) -> None:
        super().__init__(text, parent)
        self._full_text = text
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        self.setMinimumWidth(1)

    def setText(self, text: str) -> None:
        self._full_text = text
        self._elide_text()

    def resizeEvent(self, event: Any) -> None:
        super().resizeEvent(event)
        self._elide_text()

    def _elide_text(self) -> None:
        fm = self.fontMetrics()
        elided = fm.elidedText(self._full_text, Qt.ElideRight, self.width())
        super().setText(elided)

    def fullText(self) -> str:
        return self._full_text

# -----------------------------------------------------------------------------------------------------------
# OSectionHeader
# ---------------------------------------------------------------------------
class OSectionHeader(QWidget):
    def __init__(self, master: Optional[QWidget], text: str = "", **kwargs: Any) -> None:
        super().__init__(master)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        lbl = OLabel(
            self,
            text=text,
            bright=True,
            size=_FONT_SIZE_LG,
        )
        layout.addWidget(lbl)
        layout.addStretch()

    def pack(self, **kwargs: Any) -> None:
        pass

# ---------------------------------------------------------------------------
# OSeparator
# ---------------------------------------------------------------------------
class OSeparator(QFrame):
    def __init__(self, master: Optional[QWidget], **kwargs: Any) -> None:
        super().__init__(master)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Plain)
        self.setFixedHeight(1)
        self.setStyleSheet(f"color: {OMNINATIVE['gray']}; background-color: {OMNINATIVE['gray']}; border: none;")

    def pack(self, **kwargs: Any) -> None:
        pass

# ---------------------------------------------------------------------------
# OButton
# ---------------------------------------------------------------------------
class OButton(QPushButton):
    def __init__(
        self,
        master: Optional[QWidget],
        text: str = "",
        command: Optional[Callable[[], None]] = None,
        primary: bool = False,
        danger: bool = False,
        small: bool = False,
        width: int = 0,
        **kwargs: Any,
    ) -> None:
        super().__init__(text, master)

        if command:
            self.clicked.connect(command)

        fg = "transparent"
        hover = "transparent"
        txt = OMNINATIVE["accent"]
        bw = 1
        bc = OMNINATIVE["accent"]
        h = 24 if small else 22
        self.setFixedHeight(h)
        if width > 0:
            self.setFixedWidth(width)
        cr = h // 2

        if primary:
            fg = "transparent"
            hover = "transparent"
            txt = OMNINATIVE["bright"]
            bc = OMNINATIVE["bright"]

        sz = _FONT_SIZE_SM

        enter_color = OMNINATIVE["danger"] if danger else OMNINATIVE["bright"]

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {fg};
                color: {txt};
                border: {bw}px solid {bc};
                border-radius: {cr}px;
                font-family: '{_FONT_FAMILY}';
                font-size: {sz}pt;
                padding: 0px 15px 2px 15px;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: {hover};
                color: {enter_color if not primary else txt};
                border-color: {enter_color if not primary else bc};
            }}
            QPushButton:disabled {{
                color: {OMNINATIVE["dark"]};
                border-color: {OMNINATIVE["dark"]};
            }}
        """)
        self.setCursor(Qt.PointingHandCursor)

    def pack(self, **kwargs: Any) -> None:
        pass

# ---------------------------------------------------------------------------
# OOptionButton
# ---------------------------------------------------------------------------
class OOptionButton(QPushButton):
    hovered = Signal(str)
    unhovered = Signal()

    def __init__(
        self,
        val: Any,
        text: str,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(text, parent)
        self.val = val
        self.setCursor(Qt.PointingHandCursor)

    def enterEvent(self, event: Any) -> None:
        self.hovered.emit(self.val)
        super().enterEvent(event)

    def leaveEvent(self, event: Any) -> None:
        self.unhovered.emit()
        super().leaveEvent(event)


# ---------------------------------------------------------------------------
# OComboBox — OmniNative-styled dropdown (floating overlay menu)
# ---------------------------------------------------------------------------
class OComboBox(QFrame):
    def __init__(
        self,
        master: Optional[QWidget],
        values: Optional[List[Any]] = None,
        command: Optional[Callable[[Any], None]] = None,
        width: int = 0,
        height: int = 22,
        anchor: str = "w",
        transparent: bool = False,
        **kwargs: Any,
    ) -> None:
        self._transparent = transparent
        super().__init__(master)

        if height > 0:
            self.setFixedHeight(height)
        if width > 0:
            self.setFixedWidth(width)

        self.values = values or []
        self._command = command
        self.enabled = True
        self._popup = None
        self._current_value = self.values[0] if self.values else ""
        self._last_close_time = 0

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(8, 0, 3, 0)
        self._layout.setSpacing(4)

        self._lbl_text = QLabel(self._current_value, self)
        self._lbl_text.setFont(
            QFont(
                _FONT_FAMILY,
                _FONT_SIZE_SM,
            )
        )
        self._lbl_text.setStyleSheet(
            """
            background: transparent;
            padding: 0px;
            margin: 0px;
            """
        )

        align = Qt.AlignLeft | Qt.AlignVCenter
        if anchor == "center":
            align = Qt.AlignCenter
        elif anchor == "e":
            align = Qt.AlignRight | Qt.AlignVCenter

        self._lbl_text.setAlignment(align)
        self._lbl_text.setFixedHeight(20)
        self._layout.addWidget(
            self._lbl_text,
            1,
            Qt.AlignVCenter,
        )

        self._chevron_pix = _get_cached_chevron(
            size=20,
            color=OMNINATIVE["accent"],
        )
        self._lbl_chevron = QLabel(self)
        self._lbl_chevron.setPixmap(self._chevron_pix)
        self._lbl_chevron.setFixedSize(20, 20)
        self._lbl_chevron.setAlignment(Qt.AlignCenter)
        self._lbl_chevron.setStyleSheet(
            """
            background: transparent;
            padding: 0px;
            margin: 0px;
            """
        )
        self._layout.addWidget(
            self._lbl_chevron,
            0,
            Qt.AlignVCenter,
        )

        self.setCursor(Qt.PointingHandCursor)
        self.update_styles()

    def update_styles(self, is_hover: bool = False) -> None:
        if self._transparent:
            bg_color = "transparent"
            border_str = "border: none;"
            btn_bg = "transparent"
        else:
            bg_color = OMNINATIVE["dark"]
            border_str = f"border: 1px solid {OMNINATIVE['gray']};"
            btn_bg = OMNINATIVE["dark"]

        text_color = OMNINATIVE["bright"]
        if not self.enabled:
            text_color = OMNINATIVE["accent"]
        elif self._current_value == "---":
            text_color = OMNINATIVE["accent"]

        border_radius = _CORNER if not self._transparent else 0

        self.setStyleSheet(
            f"""
            OComboBox {{
                background-color: {btn_bg if is_hover else bg_color};
                {border_str}
                border-radius: {border_radius}px;
            }}
            """
        )
        self._lbl_text.setStyleSheet(
            f"""
            color: {text_color};
            background: transparent;
            padding-top: 0px;
            padding-bottom: 1px;
            margin: 0px;
            """
        )

    def enterEvent(self, event: Any) -> None:
        if self.enabled:
            self.update_styles(is_hover=True)
        super().enterEvent(event)

    def leaveEvent(self, event: Any) -> None:
        if self.enabled:
            self.update_styles(is_hover=False)
        super().leaveEvent(event)

    def mousePressEvent(self, event: Any) -> None:
        if self.enabled and event.button() == Qt.LeftButton:
            self._toggle()
        super().mousePressEvent(event)

    def get(self) -> str:
        return self._current_value

    def set(self, val: Any) -> None:
        self._current_value = str(val)
        self._lbl_text.setText(self._current_value)
        self.update_styles()

    def configure(self, values: Optional[List[Any]] = None, **kwargs: Any) -> None:
        if values is not None:
            self.values = values
            if self._current_value not in self.values:
                self.set(self.values[0] if self.values else "")
            else:
                self.update_styles()

    def set_enabled(self, enabled: bool = True) -> None:
        self.enabled = enabled
        self.setCursor(
            Qt.PointingHandCursor if enabled else Qt.ArrowCursor
        )
        self.update_styles()

    def count(self) -> int:
        return len(self.values)

    def itemText(self, index: int) -> str:
        if 0 <= index < len(self.values):
            return str(self.values[index])
        return ""

    def _popup_geometry(self) -> tuple[int, int, int, int]:
        global_pos = self.mapToGlobal(QPoint(0, 0))
        x = global_pos.x()
        y = global_pos.y() + self.height() - 1
        w = self.width()

        item_h = 24
        max_items = 10

        items_a_mostrar = min(len(self.values), max_items)
        if items_a_mostrar == 0:
            items_a_mostrar = 1

        h = (items_a_mostrar * item_h) + 2
        return x, y, w, h

    def _toggle(self) -> None:
        if not self.enabled:
            return
        if time.time() - self._last_close_time < 0.15:
            return
        if self._popup and self._popup.isVisible():
            self._close()
        else:
            self._open()

    def _open(self) -> None:
        self._popup = QWidget(
            self,
            Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint,
        )
        self._popup.setAttribute(Qt.WA_TranslucentBackground, True)

        # Hook hideEvent dynamically to update _last_close_time on focus loss or closing
        original_hide = self._popup.hideEvent
        def custom_hide(event: Any) -> None:
            self._last_close_time = time.time()
            if original_hide:
                original_hide(event)
        self._popup.hideEvent = custom_hide

        x, y, w, h = self._popup_geometry()
        self._popup.setGeometry(x, y, w, h)

        base_frame = QFrame(self._popup)
        base_frame.setObjectName("BaseFrame")
        base_frame.setStyleSheet(
            f"""
            QFrame#BaseFrame {{
                background-color: {OMNINATIVE["gray"]};
                border: none;
                border-radius: 3px;
            }}
            """
        )
        base_layout = QVBoxLayout(base_frame)
        base_layout.setContentsMargins(1, 1, 1, 1)
        base_layout.setSpacing(0)

        usar_scroll = len(self.values) > 10

        if usar_scroll:
            container = QScrollArea(base_frame)
            container.setWidgetResizable(True)
            container.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            container.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            container.setStyleSheet(
                f"""
                QScrollArea {{
                    border: none;
                    background-color: {OMNINATIVE["background"]};
                    border-radius: 2px;
                }}
                QScrollBar:vertical {{
                    border: none;
                    background: {OMNINATIVE["background"]};
                    width: 6px;
                }}
                QScrollBar::handle:vertical {{
                    background: {OMNINATIVE["accent"]};
                    min-height: 20px;
                    border-radius: 3px;
                }}
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                    border: none;
                    background: none;
                }}
                """
            )

            scroll_content = QWidget()
            scroll_content.setStyleSheet(
                f"background-color: {OMNINATIVE['background']};"
            )
            scroll_layout = QVBoxLayout(scroll_content)
            scroll_layout.setContentsMargins(0, 0, 0, 0)
            scroll_layout.setSpacing(0)

            container.setWidget(scroll_content)
            base_layout.addWidget(container)
            parent_layout = scroll_layout
        else:
            container = QFrame(base_frame)
            container.setStyleSheet(
                f"""
                QFrame {{
                    background-color: {OMNINATIVE["background"]};
                    border: none;
                    border-radius: 2px;
                }}
                """
            )
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setSpacing(0)
            base_layout.addWidget(container)
            parent_layout = container_layout

        self.botones_opciones = {}

        def actualizar_resaltado(val_hover: str = "___NONE___") -> None:
            for val, btn in self.botones_opciones.items():
                if val_hover != "___NONE___":
                    debe_resaltar = val == val_hover
                else:
                    debe_resaltar = val == self._current_value
                bg = OMNINATIVE["dark"] if debe_resaltar else OMNINATIVE["background"]
                tc = OMNINATIVE["bright"] if debe_resaltar else OMNINATIVE["accent"]
                btn.setStyleSheet(
                    f"""
                    QPushButton {{
                        background-color: {bg};
                        color: {tc};
                        border: none;
                        padding-left: 10px;
                        text-align: left;
                        font-family: '{_FONT_FAMILY}';
                        font-size: {_FONT_SIZE_SM}pt;
                    }}
                    """
                )

        for val in self.values:
            texto_str = str(val)
            display_text = texto_str

            metrics = QFontMetrics(
                QFont(
                    _FONT_FAMILY,
                    _FONT_SIZE_SM,
                )
            )
            max_text_width = w - (30 if usar_scroll else 15)
            if (
                metrics.horizontalAdvance(f"  {display_text}")
                > max_text_width
            ):
                display_text = metrics.elidedText(
                    display_text,
                    Qt.ElideRight,
                    max_text_width,
                )

            btn = OOptionButton(
                val,
                f"  {display_text}",
                self._popup,
            )
            btn.setFixedHeight(24)
            btn.clicked.connect(
                lambda checked=False, v=val: self._select(v)
            )
            btn.hovered.connect(actualizar_resaltado)
            btn.unhovered.connect(
                lambda: actualizar_resaltado("___NONE___")
            )

            parent_layout.addWidget(btn)
            self.botones_opciones[val] = btn

        actualizar_resaltado("___NONE___")

        popup_layout = QVBoxLayout(self._popup)
        popup_layout.setContentsMargins(0, 0, 0, 0)
        popup_layout.addWidget(base_frame)

        self._popup.show()

    def _close(self) -> None:
        if self._popup:
            self._popup.close()
            self._popup.deleteLater()
            self._popup = None
            self._last_close_time = time.time()

    def _select(self, val: Any) -> None:
        self.set(val)
        self._close()
        if self._command and callable(self._command):
            self._command(val)

    def pack(self, **kwargs: Any) -> None:
        pass

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ORadioButton
# ---------------------------------------------------------------------------
class ORadioButton(QRadioButton):
    def __init__(self, master: Optional[QWidget], text: str = "", command: Optional[Callable[[int], None]] = None, icon_position: str = "left", **kwargs: Any) -> None:
        super().__init__(text, master)
        self.setFont(QFont(_FONT_FAMILY, _FONT_SIZE_SM))
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self._command = command
        
        if icon_position == "right":
            self.setLayoutDirection(Qt.RightToLeft)
        else:
            self.setLayoutDirection(Qt.LeftToRight)
            
        if command:
            self.toggled.connect(lambda checked: command(1 if checked else 0))
            
        self.setStyleSheet(f"""
            QRadioButton {{
                color: {OMNINATIVE['accent']};
                spacing: 8px;
            }}
            QRadioButton:disabled {{
                color: {OMNINATIVE['dark']};
            }}
            QRadioButton::indicator {{
                width: 12px;
                height: 12px;
                border: 1px solid {OMNINATIVE['bright']};
                border-radius: 7px;
                background: {OMNINATIVE['dark']};
            }}
            QRadioButton::indicator:checked {{
                border: 1px solid {OMNINATIVE['primary']};
                background: qradialgradient(cx:0.5, cy:0.5, radius: 0.5, fx:0.5, fy:0.5, stop:0 {OMNINATIVE['primary']}, stop:0.45 {OMNINATIVE['primary']}, stop:0.55 {OMNINATIVE['dark']}, stop:1 {OMNINATIVE['dark']});
            }}
            QRadioButton::indicator:hover {{
                border: 1px solid {OMNINATIVE['primary']};
            }}
        """)
        
    def get(self) -> int:
        return 1 if self.isChecked() else 0
        
    def set(self, val: Any) -> None:
        self.setChecked(val == 1 or val is True or val == "1" or val == "True")
        
    def pack(self, **kwargs: Any) -> None: pass

# ---------------------------------------------------------------------------
# OCheckBox / OTableCheckBox
# ---------------------------------------------------------------------------
class OCheckBoxBase(QWidget):
    def __init__(self, master: Optional[QWidget], text: str = "", command: Optional[Callable[[int], None]] = None, size: int = 20, corner_radius: int = 3, **kwargs: Any) -> None:
        super().__init__(master)
        self.layout_ = QHBoxLayout(self)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(6)
        
        self._command = command
        self._state = False
        self._enabled = True
        
        self.icon_lbl = QLabel()
        self.icon_lbl.setFixedSize(size, size)
        self.icon_lbl.setCursor(Qt.PointingHandCursor)
        self.layout_.addWidget(self.icon_lbl)
        
        if text:
            self.text_lbl = QLabel(text)
            self.text_lbl.setCursor(Qt.PointingHandCursor)
            self.text_lbl.setStyleSheet(f"color: {OMNINATIVE['accent']}; font-size: {_FONT_SIZE_SM}pt;")
            self.layout_.addWidget(self.text_lbl)
            self.text_lbl.mousePressEvent = self._on_click
        else:
            self.text_lbl = None
            
        self.layout_.addStretch()
        self.icon_lbl.mousePressEvent = self._on_click
        
        self._size = size
        self._corner_radius = corner_radius
        self._update_ui()
        
    def _on_click(self, event: Any) -> None:
        if not self._enabled: return
        self.toggle()
        if self._command:
            self._command(self.get())
            
    def toggle(self) -> None:
        self._state = not self._state
        self._update_ui()
        
    def set(self, val: Any) -> None:
        self._state = (val == 1 or val is True or val == "1" or val == "True")
        self._update_ui()
        
    def get(self) -> int:
        return 1 if self._state else 0
        
    def set_enabled(self, enabled: bool = True) -> None:
        self._enabled = enabled
        self.icon_lbl.setCursor(Qt.PointingHandCursor if enabled else Qt.ArrowCursor)
        if self.text_lbl:
            self.text_lbl.setCursor(Qt.PointingHandCursor if enabled else Qt.ArrowCursor)
            self.text_lbl.setStyleSheet(f"color: {OMNINATIVE['accent'] if enabled else OMNINATIVE['dark']}; font-size: {_FONT_SIZE_SM}pt;")
            
    def _update_ui(self) -> None:
        pixmap = _get_cached_checkbox(size=self._size, checked=self._state, corner_radius=self._corner_radius)
        self.icon_lbl.setPixmap(pixmap)
        
    def pack(self, **kwargs: Any) -> None: pass

class OCheckBox(OCheckBoxBase):
    pass

class OTableCheckBox(OCheckBoxBase):
    def __init__(self, master: Optional[QWidget], text: str = "", command: Optional[Callable[[int], None]] = None, **kwargs: Any) -> None:
        super().__init__(master, text=text, command=command, **kwargs)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        if self.text_lbl: self.text_lbl.hide()
        self.layout_.setAlignment(self.icon_lbl, Qt.AlignCenter)

# ---------------------------------------------------------------------------
# OStatusBar
# ---------------------------------------------------------------------------
class OStatusBar(QLabel):
    def __init__(self, master: Optional[QWidget], **kwargs: Any) -> None:
        super().__init__(master)
        self.setText("Ready")
        self.setFont(QFont(_FONT_FAMILY, _FONT_SIZE_SM))
        self.setStyleSheet(f"color: {OMNINATIVE['accent']}; background: transparent;")
        
    def set(self, msg: str, level: str = "info") -> None:
        colors = {
            "info": OMNINATIVE["accent"],
            "success": OMNINATIVE["success"],
            "error": OMNINATIVE["primary"],
            "bright": OMNINATIVE["bright"],
        }
        self.setText(msg)
        color = colors.get(level, OMNINATIVE["accent"])
        self.setStyleSheet(f"color: {color}; background: transparent;")
        
    def pack(self, **kwargs: Any) -> None: pass

# ---------------------------------------------------------------------------
# OOptionRow
# ---------------------------------------------------------------------------
class OOptionRow(QWidget):
    def __init__(self, master: Optional[QWidget], label_text: str = "", label_width: int = 100, **kwargs: Any) -> None:
        super().__init__(master)
        self.layout_ = QHBoxLayout(self)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(0)
        
        self.layout_.addStretch()
        
        self.label = QLabel(label_text)
        self.label.setFixedWidth(label_width)
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label.setFont(QFont(_FONT_FAMILY, _FONT_SIZE_SM))
        self.label.setStyleSheet(f"color: {OMNINATIVE['accent']}; padding-right: 12px;")
        
        self.layout_.addWidget(self.label)
        
    @property
    def widget_area(self) -> QWidget:
        return self
        
    def pack(self, **kwargs: Any) -> None: pass
