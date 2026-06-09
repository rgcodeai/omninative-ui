# omninative_ui/_utils.py
from typing import TYPE_CHECKING
from PySide6.QtCore import QByteArray, QBuffer, QIODevice

if TYPE_CHECKING:
    from PySide6.QtGui import QPixmap

from .tokens import OMNINATIVE, _FONT_FAMILY, _FONT_SIZE_SM, _CORNER


def _pixmap_to_data_url(pixmap: 'QPixmap') -> str:
    byte_array = QByteArray()
    buffer = QBuffer(byte_array)
    buffer.open(QIODevice.WriteOnly)
    pixmap.save(buffer, "PNG")
    return f"data:image/png;base64,{byte_array.toBase64().data().decode()}"

def get_global_stylesheet() -> str:
    bg_color = OMNINATIVE["background"]
    widget_bg = OMNINATIVE["background"]
    scroll_bg = OMNINATIVE["background"]
    return f"""
        QWidget {{
            background-color: transparent;
            color: {OMNINATIVE["bright"]};
            font-family: "{_FONT_FAMILY}";
            font-size: {_FONT_SIZE_SM}pt;
        }}
        QWidget#content_wrapper {{
            background-color: transparent;
        }}
        QWidget#central_widget {{
            background-color: {OMNINATIVE["background"]};
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
            background: {OMNINATIVE["accent"]};
            min-height: 20px;
            margin-left: 3px;
            margin-right: 4px;
            margin-top: 2px;
            margin-bottom: 2px;
            border-radius: 0px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {OMNINATIVE["accent"]};
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
            background-color: {OMNINATIVE["background"]};
            color: {OMNINATIVE["bright"]};
            border: 1px solid {OMNINATIVE["gray"]};
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
            background-color: {OMNINATIVE["background"]};
            color: {OMNINATIVE["accent"]};
            border: 1px solid {OMNINATIVE["gray"]};
            selection-background-color: {OMNINATIVE["dark"]};
            selection-color: {OMNINATIVE["bright"]};
        }}
        QLineEdit, QTextEdit, #RInput {{
            background-color: {OMNINATIVE["dark"]};
            color: {OMNINATIVE["bright"]};
            border: 1px solid {OMNINATIVE["gray"]};
            border-radius: {_CORNER}px;
            padding: 2px 4px;
        }}
        QLineEdit:focus, QTextEdit:focus, #RInput:focus {{
            border: 1px solid {OMNINATIVE["primary"]};
        }}
        QLineEdit[readOnly="true"], QTextEdit[readOnly="true"] {{
            color: {OMNINATIVE["accent"]};
            background-color: transparent;
            border: 1px dashed {OMNINATIVE["gray"]};
        }}
        QSpinBox {{
            background-color: {OMNINATIVE["dark"]};
            color: {OMNINATIVE["bright"]};
            border: 1px solid {OMNINATIVE["gray"]};
            border-radius: {_CORNER}px;
        }}
    """

