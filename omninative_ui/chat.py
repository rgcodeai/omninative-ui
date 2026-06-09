# omninative_ui/chat.py
import time
from typing import Optional, List, Any

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QLineEdit,
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, Signal, QTimer, QSize, QPoint

from .tokens import OMNINATIVE, _FONT_FAMILY, _FONT_SIZE_SM, _CORNER
from .icons import _get_cached_plus, _get_cached_arrow, _get_cached_chevron
from .containers import OScrollArea


# ---------------------------------------------------------------------------
# OChatMessage
# ---------------------------------------------------------------------------
class OChatMessage(QFrame):
    def __init__(self, role: str, content: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.role = role
        self.content = content
        
        self.setObjectName("chat_msg")
        
        self.layout_ = QHBoxLayout(self)
        self.layout_.setContentsMargins(12, 12, 12, 12)
        self.layout_.setSpacing(12)
        
        self.text_lbl = QLabel(content)
        self.text_lbl.setFont(QFont(_FONT_FAMILY, _FONT_SIZE_SM))
        self.text_lbl.setWordWrap(True)
        self.text_lbl.setTextFormat(Qt.MarkdownText)
        self.text_lbl.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.text_lbl.setOpenExternalLinks(True)
        
        if role == "user":
            self.setStyleSheet(f"#chat_msg {{ background-color: {OMNINATIVE['dark']}; border-radius: {_CORNER}px; }}")
            self.text_lbl.setStyleSheet(f"color: {OMNINATIVE['bright']}; background: transparent; border: none;")
            self.layout_.addWidget(self.text_lbl)
        else:
            self.setStyleSheet(f"#chat_msg {{ background: transparent; border: none; }}")
            self.text_lbl.setStyleSheet(f"color: {OMNINATIVE['bright']}; background: transparent; border: none;")
            self.layout_.addWidget(self.text_lbl)
            
    def append_text(self, text: str) -> None:
        self.content += text
        self.text_lbl.setText(self.content)

# ---------------------------------------------------------------------------
# OChatView
# ---------------------------------------------------------------------------
class OChatView(OScrollArea):
    def __init__(self, master: Optional[QWidget], **kwargs: Any) -> None:
        super().__init__(master, **kwargs)
        
        # Remove the outer border while preserving any scrollbar styles
        self.setStyleSheet(self.styleSheet() + " QScrollArea { border: none; background: transparent; }")
        
        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignTop)
        self.container_layout.setContentsMargins(10, 10, 10, 10)
        self.container_layout.setSpacing(15)
        
        self.setWidget(self.container)
        self.setWidgetResizable(True)
        
        self.messages: List[OChatMessage] = []
        self._last_assistant_msg: Optional[OChatMessage] = None
        
    def add_message(self, role: str, content: str) -> None:
        msg = OChatMessage(role, content)
        self.container_layout.addWidget(msg)
        self.messages.append(msg)
        if role == "assistant":
            self._last_assistant_msg = msg
        self._scroll_to_bottom()
        
    def append_chunk(self, text: str) -> None:
        if self._last_assistant_msg:
            self._last_assistant_msg.append_text(text)
            self._scroll_to_bottom()
            
    def clear_chat(self) -> None:
        for i in reversed(range(self.container_layout.count())):
            widget = self.container_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
        self.messages.clear()
        self._last_assistant_msg = None
        
    def _scroll_to_bottom(self) -> None:
        # Allow layout to compute sizes before scrolling
        QTimer.singleShot(10, self._do_scroll)
        
    def _do_scroll(self) -> None:
        sb = self.verticalScrollBar()
        sb.setValue(sb.maximum())
        
    def pack(self, **kwargs: Any) -> None: pass

# ---------------------------------------------------------------------------
# OChatInput
# ---------------------------------------------------------------------------
class OChatInput(QFrame):
    submitted = Signal(str)
    add_clicked = Signal()
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("chat_input")
        self.setFixedHeight(50)
        self.setStyleSheet(f"#chat_input {{ background-color: {OMNINATIVE['dark']}; border-radius: 25px; }}")
        
        self.layout_ = QHBoxLayout(self)
        self.layout_.setContentsMargins(15, 0, 10, 0)
        self.layout_.setSpacing(10)
        
        # Add button (+)
        self.btn_add = QPushButton()
        self.btn_add.setFixedSize(30, 30)
        self.btn_add.setIcon(QIcon(_get_cached_plus(size=24, color=OMNINATIVE['accent'], weight=1.5)))
        self.btn_add.setIconSize(QSize(24, 24))
        self.btn_add.setStyleSheet(f"background: transparent; border: none;")
        self.btn_add.setCursor(Qt.PointingHandCursor)
        
        def _add_enter(event: Any) -> None:
            self.btn_add.setIcon(QIcon(_get_cached_plus(size=24, color=OMNINATIVE['bright'], weight=1.5)))
            QPushButton.enterEvent(self.btn_add, event)
            
        def _add_leave(event: Any) -> None:
            self.btn_add.setIcon(QIcon(_get_cached_plus(size=24, color=OMNINATIVE['accent'], weight=1.5)))
            QPushButton.leaveEvent(self.btn_add, event)
            
        self.btn_add.enterEvent = _add_enter
        self.btn_add.leaveEvent = _add_leave
        
        self.btn_add.clicked.connect(self.add_clicked.emit)
        
        # Input Field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Pregunta lo que quieras")
        self.input_field.setFont(QFont(_FONT_FAMILY, 10))
        self.input_field.setStyleSheet(f"color: {OMNINATIVE['bright']}; background: transparent; border: none;")
        self.input_field.returnPressed.connect(self._submit)
        
        # Action button (Arrow)
        self.btn_action = QPushButton()
        self.btn_action.setFixedSize(34, 34)
        self.btn_action.setIcon(QIcon(_get_cached_arrow(size=24, color=OMNINATIVE['gray'], direction="up", weight=2.0)))
        self.btn_action.setIconSize(QSize(20, 20))
        self.btn_action.setStyleSheet(f"QPushButton {{ background-color: {OMNINATIVE['bright']}; border-radius: 17px; border: none; }}")
        self.btn_action.setCursor(Qt.PointingHandCursor)
        
        def _action_enter(event: Any) -> None:
            self.btn_action.setIcon(QIcon(_get_cached_arrow(size=24, color=OMNINATIVE['background'], direction="up", weight=2.0)))
            QPushButton.enterEvent(self.btn_action, event)
            
        def _action_leave(event: Any) -> None:
            self.btn_action.setIcon(QIcon(_get_cached_arrow(size=24, color=OMNINATIVE['gray'], direction="up", weight=2.0)))
            QPushButton.leaveEvent(self.btn_action, event)
            
        self.btn_action.enterEvent = _action_enter
        self.btn_action.leaveEvent = _action_leave
        
        self.btn_action.clicked.connect(self._on_action_clicked)
        
        self.layout_.addWidget(self.btn_add)
        self.layout_.addWidget(self.input_field)
        self.layout_.addWidget(self.btn_action)
        
    def _on_action_clicked(self) -> None:
        self._submit()
            
    def _submit(self) -> None:
        text = self.input_field.text().strip()
        if text:
            self.submitted.emit(text)
            self.input_field.clear()
            
    def clear(self) -> None:
        self.input_field.clear()
        
    def text(self) -> str:
        return self.input_field.text()

# ---------------------------------------------------------------------------
# OActionMenu
# ---------------------------------------------------------------------------
class OActionMenuItem(QFrame):
    clicked = Signal(str)
    
    def __init__(self, text: str, icon_char: Optional[str] = None, has_chevron: bool = False, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.text_val = text
        self.setObjectName("action_item")
        self.setStyleSheet(f"#action_item {{ background-color: transparent; border-radius: 6px; }}")
        self.setFixedHeight(36)
        self.setCursor(Qt.PointingHandCursor)
        
        self.layout_ = QHBoxLayout(self)
        self.layout_.setContentsMargins(10, 0, 10, 0)
        self.layout_.setSpacing(12)
        
        # Icon
        if icon_char:
            self.icon_lbl = QLabel(icon_char)
            self.icon_lbl.setFont(QFont(_FONT_FAMILY, 14))
            self.icon_lbl.setStyleSheet(f"color: {OMNINATIVE['bright']}; background: transparent;")
            self.icon_lbl.setFixedWidth(24)
            self.icon_lbl.setAlignment(Qt.AlignCenter)
            self.layout_.addWidget(self.icon_lbl)
            
        # Text
        self.text_lbl = QLabel(text)
        self.text_lbl.setFont(QFont(_FONT_FAMILY, 10))
        self.text_lbl.setStyleSheet(f"color: {OMNINATIVE['bright']}; background: transparent;")
        self.layout_.addWidget(self.text_lbl)
        
        self.layout_.addStretch()
        
        # Chevron
        if has_chevron:
            self.chevron_lbl = QLabel()
            self.chevron_lbl.setPixmap(_get_cached_chevron(size=14, color=OMNINATIVE['bright'], direction="right"))
            self.chevron_lbl.setStyleSheet("background: transparent;")
            self.layout_.addWidget(self.chevron_lbl)
            
    def enterEvent(self, event: Any) -> None:
        self.setStyleSheet(f"#action_item {{ background-color: {OMNINATIVE['dark']}; border-radius: 6px; }}")
        super().enterEvent(event)
        
    def leaveEvent(self, event: Any) -> None:
        self.setStyleSheet(f"#action_item {{ background-color: transparent; border-radius: 6px; }}")
        super().leaveEvent(event)
        
    def mousePressEvent(self, event: Any) -> None:
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.text_val)
            # Find the popup and close it
            p = self.window()
            if isinstance(p, OActionMenu):
                p.close()
        super().mousePressEvent(event)

class OActionMenu(QWidget):
    action_triggered = Signal(str)
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._last_hide_time = 0.0
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.container = QFrame()
        self.container.setObjectName("menu_container")
        self.container.setStyleSheet(f"#menu_container {{ background-color: #2F2F2F; border-radius: 12px; border: 1px solid #3F3F3F; }}")
        self.main_layout.addWidget(self.container)
        
        self.layout_ = QVBoxLayout(self.container)
        self.layout_.setContentsMargins(6, 6, 6, 6)
        self.layout_.setSpacing(2)
        
        self.setFixedWidth(280)
        
    def add_action(self, text: str, icon_char: Optional[str] = None, has_chevron: bool = False) -> OActionMenuItem:
        item = OActionMenuItem(text, icon_char, has_chevron)
        item.clicked.connect(self.action_triggered.emit)
        self.layout_.addWidget(item)
        return item
        
    def add_separator(self) -> None:
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"background-color: {OMNINATIVE['dark']}; margin: 4px 10px;")
        self.layout_.addWidget(sep)
        
    def hideEvent(self, event: Any) -> None:
        self._last_hide_time = time.time()
        super().hideEvent(event)
        
    def show_above(self, widget: QWidget) -> None:
        # Prevent immediate reopening if it was just closed by a click on the toggle button
        if time.time() - self._last_hide_time < 0.15:
            return
            
        self.adjustSize()
        pos = widget.mapToGlobal(QPoint(0, 0))
        x = pos.x()
        y = pos.y() - self.height() - 10
        self.move(x, y)
        self.show()
