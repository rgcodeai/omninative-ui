# omninative_ui/chat.py
import time
from typing import Optional, List, Any, Union

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QLineEdit,
    QSizePolicy,
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, Signal, QTimer, QSize, QPoint

from .tokens import OMNINATIVE, _FONT_FAMILY, _FONT_SIZE_SM, _CORNER
from .icons import _get_cached_plus, _get_cached_arrow, _get_cached_chevron
from .containers import OScrollArea
from ._utils import apply_layout_dimensions, o_theme_val


# ---------------------------------------------------------------------------
# OChatMessage
# ---------------------------------------------------------------------------
class OChatMessage(QFrame):
    def __init__(
        self,
        role: str,
        content: str,
        parent: Optional[QWidget] = None,
        width: Union[int, str] = "100%",
        height: Union[int, str] = "auto",
        pad: int = 12,
        spacing: int = 12,
        user_bg_color: Optional[str] = None,
        user_text_color: Optional[str] = None,
        assistant_bg_color: Optional[str] = None,
        assistant_text_color: Optional[str] = None,
        border_radius: Optional[int] = None,
        font_size: Optional[int] = None,
        theme: Optional[dict] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(parent)
        apply_layout_dimensions(self, width, height)

        self.role = role
        self.content = content
        
        self.setObjectName("chat_msg")
        
        self.layout_ = QHBoxLayout(self)
        self.layout_.setContentsMargins(pad, pad, pad, pad)
        self.layout_.setSpacing(spacing)
        
        self._user_bg = o_theme_val(theme, "user_bg_color", user_bg_color, OMNINATIVE["dark"])
        self._user_txt = o_theme_val(theme, "user_text_color", user_text_color, OMNINATIVE["bright"])
        self._ast_bg = o_theme_val(theme, "assistant_bg_color", assistant_bg_color, "transparent")
        self._ast_txt = o_theme_val(theme, "assistant_text_color", assistant_text_color, OMNINATIVE["bright"])
        self._br = o_theme_val(theme, "border_radius", border_radius, _CORNER)
        self._sz = o_theme_val(theme, "font_size", font_size, _FONT_SIZE_SM)

        self.text_lbl = QLabel(content)
        self.text_lbl.setFont(QFont(_FONT_FAMILY, self._sz))
        self.text_lbl.setWordWrap(True)
        self.text_lbl.setTextFormat(Qt.MarkdownText)
        self.text_lbl.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.text_lbl.setOpenExternalLinks(True)
        
        if role == "user":
            self.setStyleSheet(f"#chat_msg {{ background-color: {self._user_bg}; border-radius: {self._br}px; }}")
            self.text_lbl.setStyleSheet(f"color: {self._user_txt}; background: transparent; border: none;")
            self.layout_.addWidget(self.text_lbl)
        else:
            self.setStyleSheet(f"#chat_msg {{ background-color: {self._ast_bg}; border-radius: {self._br}px; border: none; }}")
            self.text_lbl.setStyleSheet(f"color: {self._ast_txt}; background: transparent; border: none;")
            self.layout_.addWidget(self.text_lbl)
            
    def append_text(self, text: str) -> None:
        self.content += text
        self.text_lbl.setText(self.content)

# ---------------------------------------------------------------------------
# OChatView
# ---------------------------------------------------------------------------
class OChatView(OScrollArea):
    def __init__(
        self,
        master: Optional[QWidget] = None,
        width: Union[int, str] = "100%",
        height: Union[int, str] = "auto",
        pad: int = 10,
        spacing: int = 15,
        theme: Optional[dict] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, width=width, height=height, theme=theme, **kwargs)
        self._theme = theme
        
        # Remove the outer border while preserving any scrollbar styles
        self.setStyleSheet(self.styleSheet() + " QScrollArea { border: none; background: transparent; }")
        
        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignTop)
        self.container_layout.setContentsMargins(pad, pad, pad, pad)
        self.container_layout.setSpacing(spacing)
        
        self.setWidget(self.container)
        self.setWidgetResizable(True)
        
        self.messages: List[OChatMessage] = []
        self._last_assistant_msg: Optional[OChatMessage] = None
        
    def add_message(self, role: str, content: str) -> None:
        msg = OChatMessage(role, content, theme=self._theme)
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
    
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        width: Union[int, str] = "100%",
        height: Union[int, str] = 50,
        pad_left: int = 15,
        pad_right: int = 10,
        pad_y: int = 0,
        spacing: int = 10,
        button_size: int = 30,
        action_button_size: int = 34,
        icon_size: int = 24,
        action_icon_size: int = 20,
        show_add: bool = True,
        show_action: bool = True,
        placeholder_text: str = "Pregunta lo que quieras",
        bg_color: Optional[str] = None,
        text_color: Optional[str] = None,
        icon_color: Optional[str] = None,
        icon_hover_color: Optional[str] = None,
        button_bg_color: Optional[str] = None,
        button_icon_color: Optional[str] = None,
        button_icon_hover_color: Optional[str] = None,
        theme: Optional[dict] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(parent)
        apply_layout_dimensions(self, width, height)

        self.setObjectName("chat_input")
        radius = height // 2 if height > 0 else 25

        self._bg = o_theme_val(theme, "bg_color", bg_color, OMNINATIVE["dark"])
        self._txt = o_theme_val(theme, "text_color", text_color, OMNINATIVE["bright"])
        self._icon = o_theme_val(theme, "icon_color", icon_color, OMNINATIVE["accent"])
        self._icon_hov = o_theme_val(theme, "icon_hover_color", icon_hover_color, OMNINATIVE["bright"])
        self._btn_bg = o_theme_val(theme, "button_bg_color", button_bg_color, OMNINATIVE["bright"])
        self._btn_icon = o_theme_val(theme, "button_icon_color", button_icon_color, OMNINATIVE["gray"])
        self._btn_icon_hov = o_theme_val(theme, "button_icon_hover_color", button_icon_hover_color, OMNINATIVE["background"])

        self.setStyleSheet(f"#chat_input {{ background-color: {self._bg}; border-radius: {radius}px; }}")
        
        self.layout_ = QHBoxLayout(self)
        self.layout_.setContentsMargins(pad_left, pad_y, pad_right, pad_y)
        self.layout_.setSpacing(spacing)
        
        self._icon_size = icon_size
        
        # Add button (+)
        self.btn_add = QPushButton()
        self.btn_add.setFixedSize(button_size, button_size)
        self.btn_add.setIcon(QIcon(_get_cached_plus(size=icon_size, color=self._icon, weight=1.5)))
        self.btn_add.setIconSize(QSize(icon_size, icon_size))
        self.btn_add.setStyleSheet(f"background: transparent; border: none;")
        self.btn_add.setCursor(Qt.PointingHandCursor)
        
        def _add_enter(event: Any) -> None:
            self.btn_add.setIcon(QIcon(_get_cached_plus(size=self._icon_size, color=self._icon_hov, weight=1.5)))
            QPushButton.enterEvent(self.btn_add, event)
            
        def _add_leave(event: Any) -> None:
            self.btn_add.setIcon(QIcon(_get_cached_plus(size=self._icon_size, color=self._icon, weight=1.5)))
            QPushButton.leaveEvent(self.btn_add, event)
            
        self.btn_add.enterEvent = _add_enter
        self.btn_add.leaveEvent = _add_leave
        
        self.btn_add.clicked.connect(self.add_clicked.emit)
        
        # Input Field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(placeholder_text)
        self.input_field.setFont(QFont(_FONT_FAMILY, 10))
        self.input_field.setStyleSheet(f"color: {self._txt}; background: transparent; border: none;")
        self.input_field.returnPressed.connect(self._submit)
        
        # Action button (Arrow)
        self.btn_action = QPushButton()
        self.btn_action.setFixedSize(action_button_size, action_button_size)
        self.btn_action.setIcon(QIcon(_get_cached_arrow(size=icon_size, color=self._btn_icon, direction="up", weight=2.0)))
        self.btn_action.setIconSize(QSize(action_icon_size, action_icon_size))
        action_radius = action_button_size // 2
        self.btn_action.setStyleSheet(f"QPushButton {{ background-color: {self._btn_bg}; border-radius: {action_radius}px; border: none; }}")
        self.btn_action.setCursor(Qt.PointingHandCursor)
        
        def _action_enter(event: Any) -> None:
            self.btn_action.setIcon(QIcon(_get_cached_arrow(size=self._icon_size, color=self._btn_icon_hov, direction="up", weight=2.0)))
            QPushButton.enterEvent(self.btn_action, event)
            
        def _action_leave(event: Any) -> None:
            self.btn_action.setIcon(QIcon(_get_cached_arrow(size=self._icon_size, color=self._btn_icon, direction="up", weight=2.0)))
            QPushButton.leaveEvent(self.btn_action, event)
            
        self.btn_action.enterEvent = _action_enter
        self.btn_action.leaveEvent = _action_leave
        
        self.btn_action.clicked.connect(self._on_action_clicked)
        
        self.layout_.addWidget(self.btn_add)
        self.layout_.addWidget(self.input_field)
        self.layout_.addWidget(self.btn_action)

        if not show_add:
            self.btn_add.hide()
        if not show_action:
            self.btn_action.hide()
        
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
    
    def __init__(
        self,
        text: str,
        icon_char: Optional[str] = None,
        has_chevron: bool = False,
        parent: Optional[QWidget] = None,
        width: Union[int, str] = "100%",
        height: Union[int, str] = 36,
        pad_x: int = 10,
        pad_y: int = 0,
        spacing: int = 12,
        icon_width: int = 24,
        chevron_size: int = 14,
        bg_hover_color: Optional[str] = None,
        text_color: Optional[str] = None,
        theme: Optional[dict] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(parent)
        apply_layout_dimensions(self, width, height)

        self.text_val = text
        self.setObjectName("action_item")

        self._bg_hov = o_theme_val(theme, "bg_hover_color", bg_hover_color, OMNINATIVE["dark"])
        self._txt = o_theme_val(theme, "text_color", text_color, OMNINATIVE["bright"])

        self.setStyleSheet(f"#action_item {{ background-color: transparent; border-radius: 6px; }}")
        self.setCursor(Qt.PointingHandCursor)
        
        self.layout_ = QHBoxLayout(self)
        self.layout_.setContentsMargins(pad_x, pad_y, pad_x, pad_y)
        self.layout_.setSpacing(spacing)
        
        # Icon
        if icon_char:
            self.icon_lbl = QLabel(icon_char)
            self.icon_lbl.setFont(QFont(_FONT_FAMILY, 14))
            self.icon_lbl.setStyleSheet(f"color: {self._txt}; background: transparent;")
            self.icon_lbl.setFixedWidth(icon_width)
            self.icon_lbl.setAlignment(Qt.AlignCenter)
            self.layout_.addWidget(self.icon_lbl)
            
        # Text
        self.text_lbl = QLabel(text)
        self.text_lbl.setFont(QFont(_FONT_FAMILY, 10))
        self.text_lbl.setStyleSheet(f"color: {self._txt}; background: transparent;")
        self.layout_.addWidget(self.text_lbl)
        
        self.layout_.addStretch()
        
        # Chevron
        if has_chevron:
            self.chevron_lbl = QLabel()
            self.chevron_lbl.setPixmap(_get_cached_chevron(size=chevron_size, color=self._txt, direction="right"))
            self.chevron_lbl.setStyleSheet("background: transparent;")
            self.layout_.addWidget(self.chevron_lbl)
            
    def enterEvent(self, event: Any) -> None:
        self.setStyleSheet(f"#action_item {{ background-color: {self._bg_hov}; border-radius: 6px; }}")
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
    
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        width: Union[int, str] = 280,
        height: Union[int, str] = "auto",
        pad: int = 6,
        spacing: int = 2,
        bg_color: Optional[str] = None,
        border_color: Optional[str] = None,
        separator_color: Optional[str] = None,
        theme: Optional[dict] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(parent)
        apply_layout_dimensions(self, width, height)

        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._last_hide_time = 0.0
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self._bg = o_theme_val(theme, "bg_color", bg_color, "#2F2F2F")
        self._bc = o_theme_val(theme, "border_color", border_color, "#3F3F3F")
        self._sep = o_theme_val(theme, "separator_color", separator_color, OMNINATIVE["dark"])
        self._theme = theme

        self.container = QFrame()
        self.container.setObjectName("menu_container")
        self.container.setStyleSheet(f"#menu_container {{ background-color: {self._bg}; border-radius: 12px; border: 1px solid {self._bc}; }}")
        self.main_layout.addWidget(self.container)
        
        self.layout_ = QVBoxLayout(self.container)
        self.layout_.setContentsMargins(pad, pad, pad, pad)
        self.layout_.setSpacing(spacing)
        
    def add_action(self, text: str, icon_char: Optional[str] = None, has_chevron: bool = False) -> OActionMenuItem:
        item = OActionMenuItem(text, icon_char, has_chevron, theme=self._theme)
        item.clicked.connect(self.action_triggered.emit)
        self.layout_.addWidget(item)
        return item
        
    def add_separator(self) -> None:
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"background-color: {self._sep}; margin: 4px 10px;")
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
