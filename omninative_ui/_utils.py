# omninative_ui/_utils.py
import re
from typing import TYPE_CHECKING, Union, Any

from PySide6.QtCore import QByteArray, QBuffer, QIODevice
from PySide6.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QVBoxLayout

if TYPE_CHECKING:
    from PySide6.QtGui import QPixmap

from .tokens import OMNINATIVE, _FONT_FAMILY, _FONT_SIZE_SM, _CORNER


def _pixmap_to_data_url(pixmap: 'QPixmap') -> str:
    byte_array = QByteArray()
    buffer = QBuffer(byte_array)
    buffer.open(QIODevice.WriteOnly)
    pixmap.save(buffer, "PNG")
    return f"data:image/png;base64,{byte_array.toBase64().data().decode()}"

_PCT_RE = re.compile(r'^(\d+(?:\.\d+)?)\s*%$')
_PX_RE = re.compile(r'^(\d+(?:\.\d+)?)\s*(?:px)?$')


def apply_layout_dimensions(widget: QWidget, width: Union[int, str], height: Union[int, str]) -> None:
    w_policy = widget.sizePolicy().horizontalPolicy()
    h_policy = widget.sizePolicy().verticalPolicy()

    if isinstance(width, int):
        widget.setFixedWidth(width)
        w_policy = QSizePolicy.Fixed
    elif isinstance(width, str):
        v = width.strip()
        m_pct = _PCT_RE.match(v)
        m_px = _PX_RE.match(v)
        if m_pct:
            pct = int(float(m_pct.group(1)))
            w_policy = QSizePolicy.Expanding
            widget._omni_stretch_w = pct
        elif m_px:
            px = int(float(m_px.group(1)))
            widget.setFixedWidth(px)
            w_policy = QSizePolicy.Fixed
        elif v.lower() in ("expand", "fill"):
            w_policy = QSizePolicy.Expanding
        elif v.lower() in ("auto", "hug"):
            w_policy = QSizePolicy.Minimum

    if isinstance(height, int):
        widget.setFixedHeight(height)
        h_policy = QSizePolicy.Fixed
    elif isinstance(height, str):
        v = height.strip()
        m_pct = _PCT_RE.match(v)
        m_px = _PX_RE.match(v)
        if m_pct:
            pct = int(float(m_pct.group(1)))
            h_policy = QSizePolicy.Expanding
            widget._omni_stretch_h = pct
        elif m_px:
            px = int(float(m_px.group(1)))
            widget.setFixedHeight(px)
            h_policy = QSizePolicy.Fixed
        elif v.lower() in ("expand", "fill"):
            h_policy = QSizePolicy.Expanding
        elif v.lower() in ("auto", "hug"):
            h_policy = QSizePolicy.Minimum

    widget.setSizePolicy(w_policy, h_policy)


class _StretchAwareHBoxLayout(QHBoxLayout):
    """Horizontal layout that auto-applies percentage-based stretch hints."""

    def addWidget(self, widget, stretch=0, alignment=None):
        if stretch == 0 and hasattr(widget, '_omni_stretch_w'):
            stretch = widget._omni_stretch_w
        if alignment is not None:
            super().addWidget(widget, stretch, alignment)
        else:
            super().addWidget(widget, stretch)


class _StretchAwareVBoxLayout(QVBoxLayout):
    """Vertical layout that auto-applies percentage-based stretch hints."""

    def addWidget(self, widget, stretch=0, alignment=None):
        if stretch == 0 and hasattr(widget, '_omni_stretch_h'):
            stretch = widget._omni_stretch_h
        if alignment is not None:
            super().addWidget(widget, stretch, alignment)
        else:
            super().addWidget(widget, stretch)

def get_global_stylesheet() -> str:
    bg_color = OMNINATIVE["bg"]
    widget_bg = OMNINATIVE["bg"]
    scroll_bg = OMNINATIVE["bg"]
    return f"""
        QWidget {{
            background-color: transparent;
            color: {OMNINATIVE["fg"]};
            font-family: "{_FONT_FAMILY}";
            font-size: {_FONT_SIZE_SM}pt;
        }}
        QWidget#content_wrapper {{
            background-color: transparent;
        }}
        QWidget#central_widget {{
            background-color: {OMNINATIVE["bg"]};
        }}
        QLabel {{
            background-color: transparent;
        }}
        QScrollArea {{
            background-color: transparent;
        }}
        QScrollArea > QWidget > QWidget {{
            background-color: transparent;
        }}
        QScrollBar:vertical {{
            border: none;
            background: transparent;
            width: 8px;
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background: {OMNINATIVE["fg_muted"]};
            min-height: 20px;
            margin-left: 3px;
            margin-right: 4px;
            margin-top: 2px;
            margin-bottom: 2px;
            border-radius: 0px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {OMNINATIVE["fg_muted"]};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
            height: 0px;
            width: 0px;
        }}
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
            background: none;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}
        QComboBox {{
            background-color: {OMNINATIVE["bg"]};
            color: {OMNINATIVE["fg"]};
            border: 1px solid {OMNINATIVE["border"]};
            border-radius: {_CORNER}px;
            padding: 2px 8px;
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left-width: 0px;
        }}
        QComboBox::down-arrow {{
            image: none;
        }}
        QComboBox QAbstractItemView {{
            background-color: {OMNINATIVE["bg"]};
            color: {OMNINATIVE["fg_muted"]};
            border: 1px solid {OMNINATIVE["border"]};
            selection-background-color: {OMNINATIVE["surface"]};
            selection-color: {OMNINATIVE["fg"]};
        }}
        QLineEdit, QTextEdit, #RInput {{
            background-color: {OMNINATIVE["surface"]};
            color: {OMNINATIVE["fg"]};
            border: 1px solid {OMNINATIVE["border"]};
            border-radius: {_CORNER}px;
            padding: 2px 4px;
        }}
        QLineEdit:focus, QTextEdit:focus, #RInput:focus {{
            border: 1px solid {OMNINATIVE["accent"]};
        }}
        QLineEdit[readOnly="true"], QTextEdit[readOnly="true"] {{
            color: {OMNINATIVE["fg_muted"]};
            background-color: transparent;
            border: 1px solid {OMNINATIVE["border"]};
        }}
        QLineEdit[readOnly="true"]:focus, QTextEdit[readOnly="true"]:focus {{
            border: 1px solid {OMNINATIVE["accent"]};
        }}
        #OHotkeyInput {{
            background-color: {OMNINATIVE["surface"]};
            color: {OMNINATIVE["fg_muted"]};
        }}
        #OHotkeyInput[recording="true"] {{
            color: {OMNINATIVE["fg"]};
        }}
        QSpinBox {{
            background-color: {OMNINATIVE["surface"]};
            color: {OMNINATIVE["fg"]};
            border: 1px solid {OMNINATIVE["border"]};
            border-radius: {_CORNER}px;
        }}
    """

def o_theme_val(theme: dict | None, key: str, explicit_val: Any, default_val: Any) -> Any:
    if explicit_val is not None:
        return explicit_val
    if theme and key in theme:
        return theme[key]
    return default_val
