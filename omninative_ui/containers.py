# omninative_ui/containers.py
import re
from typing import Optional, List, Dict, Any, Tuple, Union, Callable

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTableView,
    QHeaderView,
    QAbstractItemView,
    QStyledItemDelegate,
    QComboBox as _QComboBox,
    QStackedWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QTextEdit,
)
from PySide6.QtGui import (
    QColor,
    QFont,
    QBrush,
    QPen,
    QFontMetrics,
)
from PySide6.QtCore import (
    Qt,
    Signal,
    QTimer,
    QSize,
    QPoint,
    QRect,
    QAbstractTableModel,
    QModelIndex,
)

from .tokens import OMNINATIVE, _FONT_FAMILY, _FONT_SIZE_SM, _CORNER, _PAD
from .icons import _get_cached_chevron
from .core import OComboBox
from .inputs import OTextBox
from ._utils import apply_layout_dimensions, o_theme_val


# -----------------------------------------------------------------------------------------------------------
# OScrollArea
# ---------------------------------------------------------------------------
class OScrollArea(QScrollArea):
    def __init__(
        self,
        master: Optional[QWidget] = None,
        width: Union[int, str] = "100%",
        height: Union[int, str] = "auto",
        bg_color: Optional[str] = None,
        border_color: Optional[str] = None,
        border_width: int = 1,
        border_radius: Optional[int] = None,
        theme: Optional[dict] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master)

        apply_layout_dimensions(self, width, height)

        self.setWidgetResizable(True)
        
        _bg = o_theme_val(theme, "bg_color", bg_color, "transparent")
        _bc = o_theme_val(theme, "border_color", border_color, OMNINATIVE['surface'])
        _bw = o_theme_val(theme, "border_width", border_width, 1)
        _br = o_theme_val(theme, "border_radius", border_radius, _CORNER)

        self.setStyleSheet(f"""
            QScrollArea {{
                border: {_bw}px solid {_bc};
                border-radius: {_br}px;
                background: {_bg};
            }}
            QScrollArea > QWidget > QWidget {{
                background: transparent;
            }}
        """)

    def pack(self, **kwargs: Any) -> None: pass

# ---------------------------------------------------------------------------
# OVirtualTable (QTableView Native Implementation)
# ---------------------------------------------------------------------------


class OTableTextEdit(QTextEdit):
    on_enter_pressed = Signal(str, str)
    on_backspace_pressed = Signal(str)

    def wheelEvent(self, event: Any) -> None:
        if self.hasFocus():
            delta = event.angleDelta().y()
            if delta != 0:
                step = 1 if delta < 0 else -1
                sb = self.verticalScrollBar()
                sb.setValue(sb.value() + step * sb.singleStep())
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, event: Any) -> None:
        if event.key() in (Qt.Key_Return, Qt.Key_Enter) and not (event.modifiers() & Qt.ShiftModifier):
            cursor = self.textCursor()
            pos = cursor.position()
            text = self.toPlainText()
            before = text[:pos]
            after = text[pos:]
            self.on_enter_pressed.emit(before, after)
            return
        elif event.key() == Qt.Key_Backspace:
            cursor = self.textCursor()
            if cursor.position() == 0 and not cursor.hasSelection():
                self.on_backspace_pressed.emit(self.toPlainText())
                return
        super().keyPressEvent(event)


class OTableItemDelegate(QStyledItemDelegate):
    def __init__(self, parent: Optional[QAbstractItemView] = None, col_config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(parent)
        self.col_config = col_config or {}

    def paint(self, painter: Any, option: Any, index: QModelIndex) -> None:
        painter.save()
        rect = option.rect

        table = self.parent()
        _bg = getattr(table, "_bg", OMNINATIVE["bg"])
        _alt_bg = getattr(table, "_alt_bg", OMNINATIVE["surface"])
        _txt = getattr(table, "_txt", OMNINATIVE["fg_muted"])
        _bc = getattr(table, "_bc", OMNINATIVE["border"])
        _br = getattr(table, "_br", _CORNER)

        # No selection highlight
        bg_color = QColor(_alt_bg) if index.row() % 2 else QColor(_bg)
        painter.fillRect(rect, bg_color)

        cls_name = self.col_config.get("class", "QLabel")
        if cls_name == "QLabel":
            cls_name = QLabel

        is_combo = (cls_name == OComboBox or cls_name == "OComboBox")
        is_textbox = (cls_name == OTextBox or cls_name == "OTextBox")

        text = str(index.data(Qt.DisplayRole))
        painter.setPen(QPen(QColor(_txt)))

        if is_combo:
            h = 22
            y_off = (rect.height() - h) // 2
            box_rect = QRect(rect.x() + 4, rect.y() + y_off, rect.width() - 8, h)
            painter.setBrush(QBrush(bg_color))
            painter.setPen(QPen(QColor(OMNINATIVE["border"])))
            painter.drawRoundedRect(box_rect, _CORNER, _CORNER)

        elif is_textbox:
            painter.setPen(QPen(QColor(_txt)))
            painter.drawText(
                rect.adjusted(8, 4, -8, -4),
                Qt.AlignLeft | Qt.AlignTop | Qt.TextWordWrap,
                text,
            )

        else:
            align_cfg = self.col_config.get("kwargs", {}).get("align", "vcenter")
            align_flag = Qt.AlignTop if align_cfg == "top" else Qt.AlignVCenter
            pad_y = 6 if align_cfg == "top" else 0
            
            txt_str = str(text)
            if "\n" in txt_str:
                draw_str = txt_str
            else:
                fm = painter.fontMetrics()
                draw_str = fm.elidedText(txt_str, Qt.ElideRight, rect.width() - 16)
                
            painter.drawText(
                rect.adjusted(8, pad_y, -8, -pad_y),
                Qt.AlignLeft | align_flag,
                draw_str,
            )

        painter.restore()

    def createEditor(self, parent: QWidget, option: Any, index: QModelIndex) -> QWidget:
        cls_name = self.col_config.get("class", "QLabel")
        if cls_name == "QLabel":
            cls_name = QLabel
        is_combo = (cls_name == OComboBox or cls_name == "OComboBox")

        kwargs = self.col_config.get("kwargs", {}).copy()

        if is_combo:
            editor = OComboBox(parent, transparent=True, height="auto")
            values = kwargs.get("values", [])
            editor.configure(values=values)
            
            original_select = editor._select
            def _new_select(val):
                original_select(val)
                if hasattr(editor, "_current_index"):
                    table = self.parent()
                    if table and table.model:
                        table.model.setData(editor._current_index, val, Qt.EditRole)
            editor._select = _new_select
            return editor
        else:
            editor = OTableTextEdit(parent)
            editor.document().setDocumentMargin(0)
            
            table = self.parent()
            _bg = getattr(table, "_bg", OMNINATIVE["bg"])
            _alt_bg = getattr(table, "_alt_bg", OMNINATIVE["surface"])
            _txt = getattr(table, "_txt", OMNINATIVE["fg_muted"])
            _primary = getattr(table, "_primary", OMNINATIVE["accent"])
            
            base_bg = _alt_bg if index.row() % 2 else _bg
            solid_bg = re.sub(r'\d+\)$', '255)', base_bg)
            
            editor.setStyleSheet(
                f"QTextEdit {{\n"
                f"background-color: {solid_bg}; "
                f"color: {_txt}; "
                f"border: 1px solid {_primary}; "
                f"border-radius: 0px; "
                f"padding: 3px 7px;"
                f"}}"
                f"QTextEdit:focus {{\n"
                f"outline: none;"
                f"border: 1px solid {_primary}; "
                f"}}"
                f"QTextEdit > QWidget {{\n"
                f"background-color: {solid_bg};"
                f"}}"
                f"QScrollBar:vertical {{"
                f"border: none;"
                f"background: {solid_bg};"
                f"width: 6px;"
                f"margin: 0px;"
                f"}}"
                f"QScrollBar::handle:vertical {{"
                f"background: {_txt};"
                f"min-height: 20px;"
                f"border-radius: 3px;"
                f"}}"
                f"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{"
                f"border: none;"
                f"background: none;"
                f"height: 0px;"
                f"}}"
            )

            table = self.parent()
            if hasattr(table, "on_textbox_enter") and table.on_textbox_enter:
                def _on_enter(before, after):
                    if hasattr(editor, "_current_index"):
                        table.on_textbox_enter(
                            editor._current_index.row(),
                            editor._current_index.column(),
                            before,
                            after,
                        )
                editor.on_enter_pressed.connect(_on_enter)

            if hasattr(table, "on_textbox_backspace") and table.on_textbox_backspace:
                def _on_backspace(text):
                    if hasattr(editor, "_current_index"):
                        table.on_textbox_backspace(
                            editor._current_index.row(),
                            editor._current_index.column(),
                            text,
                        )
                editor.on_backspace_pressed.connect(_on_backspace)
            return editor

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        try:
            editor._current_index = index
        except Exception:
            pass
        text = str(index.data(Qt.EditRole))
        if isinstance(editor, _QComboBox):
            idx = editor.findText(text)
            if idx >= 0:
                editor.setCurrentIndex(idx)
        elif isinstance(editor, OComboBox):
            editor.set(text)
        elif isinstance(editor, OTableTextEdit) or isinstance(editor, QTextEdit):
            editor.setPlainText(text)
            table = self.parent()
            if hasattr(table, "_focus_cursor_pos") and table._focus_cursor_pos is not None:
                cursor = editor.textCursor()
                cursor.setPosition(min(table._focus_cursor_pos, len(text)))
                editor.setTextCursor(cursor)
                table._focus_cursor_pos = None
            else:
                def _set_cursor():
                    from PySide6.QtGui import QCursor, QMouseEvent
                    from PySide6.QtCore import QEvent, Qt
                    from PySide6.QtWidgets import QApplication
                    try:
                        global_pos = QCursor.pos()
                        vp = editor.viewport()
                        vp_pos = vp.mapFromGlobal(global_pos)
                        if vp.rect().contains(vp_pos):
                            press = QMouseEvent(QEvent.MouseButtonPress, vp_pos, global_pos, Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
                            QApplication.postEvent(vp, press)
                            release = QMouseEvent(QEvent.MouseButtonRelease, vp_pos, global_pos, Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
                            QApplication.postEvent(vp, release)
                    except Exception:
                        pass
                
                from PySide6.QtCore import QTimer
                QTimer.singleShot(0, _set_cursor)
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor: QWidget, model: QAbstractTableModel, index: QModelIndex) -> None:
        if isinstance(editor, _QComboBox):
            model.setData(index, editor.currentText(), Qt.EditRole)
        elif isinstance(editor, OComboBox):
            model.setData(index, editor.get(), Qt.EditRole)
        elif isinstance(editor, OTableTextEdit) or isinstance(editor, QTextEdit):
            new_val = editor.toPlainText()
            old_val = index.data(Qt.EditRole)
            if isinstance(old_val, int):
                try: new_val = int(new_val)
                except ValueError: pass
            elif isinstance(old_val, float):
                try: new_val = float(new_val)
                except ValueError: pass
            model.setData(index, new_val, Qt.EditRole)
        else:
            super().setModelData(editor, model, index)

    def updateEditorGeometry(self, editor: QWidget, option: Any, index: QModelIndex) -> None:
        if isinstance(editor, OComboBox):
            h = 22
            y_off = (option.rect.height() - h) // 2
            editor.setGeometry(QRect(option.rect.x() + 4, option.rect.y() + y_off, option.rect.width() - 8, h))
        else:
            editor.setGeometry(option.rect)


class _RNativeTableModel(QAbstractTableModel):
    def __init__(self, columns: Tuple[str, ...], col_widgets: List[Dict[str, Any]], parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.columns = columns
        self.col_widgets = col_widgets
        self.table_data = []
        self.on_data_change_cb = None

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.table_data)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.columns)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid():
            return None
        if role in (Qt.DisplayRole, Qt.EditRole, Qt.ToolTipRole):
            if role == Qt.ToolTipRole:
                cls_name = self.col_widgets[index.column()].get("class", "QLabel")
                if cls_name != "QLabel" and cls_name != QLabel:
                    return None
            try:
                val = self.table_data[index.row()][index.column()]
                if val is None:
                    return ""
                return str(val)
            except Exception:
                pass
        return None

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.EditRole) -> bool:
        if index.isValid() and role == Qt.EditRole:
            row = list(self.table_data[index.row()])
            row[index.column()] = value
            self.table_data[index.row()] = tuple(row)
            self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
            if self.on_data_change_cb:
                self.on_data_change_cb(index.row(), index.column(), value)
            return True
        return False

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.columns[section]
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        flags = super().flags(index)
        col_cfg = self.col_widgets[index.column()]
        cls = col_cfg.get("class", "QLabel")
        if cls == "QLabel":
            cls = QLabel
        is_editable = (
            cls == OComboBox
            or cls == "OComboBox"
            or cls == OTextBox
            or cls == "OTextBox"
        )
        if is_editable:
            flags |= Qt.ItemIsEditable
        return flags


class OVirtualTable(QTableView):
    def __init__(
        self,
        master: Optional[QWidget] = None,
        columns: Tuple[str, ...] = ("Column 1",),
        column_widgets: Optional[List[Dict[str, Any]]] = None,
        hug: bool = True,
        visible_rows: Optional[int] = None,
        row_height: int = 24,
        header_height: int = 28,
        flexible_height: bool = False,
        bg_color: Optional[str] = None,
        alt_bg_color: Optional[str] = None,
        text_color: Optional[str] = None,
        border_color: Optional[str] = None,
        header_bg_color: Optional[str] = None,
        header_text_color: Optional[str] = None,
        primary_color: Optional[str] = None,
        border_radius: Optional[int] = None,
        font_size: Optional[int] = None,
        theme: Optional[dict] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master)

        self.columns = columns
        self.column_widgets = column_widgets or [
            {"class": "QLabel", "kwargs": {}}
        ] * len(columns)
        self._hug = hug
        self.visible_rows = visible_rows
        self.row_height = row_height
        self._header_height = header_height

        self.on_data_change = None
        self.on_textbox_enter = None
        self.on_textbox_backspace = None

        self.model = _RNativeTableModel(self.columns, self.column_widgets, self)
        self.setModel(self.model)

        self.delegates = []
        for i, cfg in enumerate(self.column_widgets):
            delegate = OTableItemDelegate(self, cfg)
            self.delegates.append(delegate)
            self.setItemDelegateForColumn(i, delegate)

        self._bg = o_theme_val(theme, "bg_color", bg_color, OMNINATIVE["bg"])
        self._alt_bg = o_theme_val(theme, "alt_bg_color", alt_bg_color, OMNINATIVE["surface"])
        self._txt = o_theme_val(theme, "text_color", text_color, OMNINATIVE["fg_muted"])
        self._bc = o_theme_val(theme, "border_color", border_color, OMNINATIVE["border"])
        self._header_bg = o_theme_val(theme, "header_bg_color", header_bg_color, OMNINATIVE["surface"])
        self._header_txt = o_theme_val(theme, "header_text_color", header_text_color, OMNINATIVE["fg_muted"])
        self._primary = o_theme_val(theme, "primary_color", primary_color, OMNINATIVE["accent"])
        self._br = o_theme_val(theme, "border_radius", border_radius, _CORNER)
        self._sz = o_theme_val(theme, "font_size", font_size, _FONT_SIZE_SM)

        self._corner_filler = QLabel(self)
        self._corner_filler.setStyleSheet(
            f"background-color: {self._header_bg}; border-bottom: 1px solid {self._bc}; border-top-right-radius: {self._br}px;"
        )

        self.setStyleSheet(
            f"""
            QTableView {{
                background-color: {self._bg};
                border: 1px solid {self._bc};
                border-radius: {self._br}px;
                gridline-color: transparent;
                outline: 0;
            }}
            QTableView::item {{
                border-bottom: 1px solid {self._bc};
            }}
            QTableView::item:selected {{
                background-color: transparent;
                color: {self._txt};
            }}
            QHeaderView::section {{
                background-color: {self._header_bg};
                color: {self._header_txt};
                padding: 4px 4px 4px 12px;
                border: none;
                border-bottom: 1px solid {self._bc};
                font-family: '{_FONT_FAMILY}';
                font-size: {self._sz}pt;
                font-weight: 700;
            }}
            QHeaderView::section:hover,
            QHeaderView::section:pressed,
            QHeaderView::section:checked {{
                background-color: {self._header_bg};
                color: {self._header_txt};
            }}
            QScrollBar:vertical {{
                border: none;
                background: {self._bg};
                width: 8px;
                border-radius: 4px;
                margin-top: {header_height}px;
            }}
            QScrollBar::handle:vertical {{
                background: {self._txt};
                border-radius: 4px;
            }}
        """
        )

        h_font = self.horizontalHeader().font()
        h_font.setBold(True)
        self.horizontalHeader().setFont(h_font)

        self.horizontalHeader().setHighlightSections(False)
        self.verticalHeader().setVisible(False)

        if self._hug:
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        else:
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.horizontalHeader().setFixedHeight(header_height)

        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.setShowGrid(False)

        self.verticalHeader().setDefaultSectionSize(row_height)
        self._base_row_height = row_height
        self._flexible_height = flexible_height

        self._update_height()

        # Let resizeEvent handle the proportions based on weight
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

    @property
    def data(self) -> List[Tuple[Any, ...]]:
        return self.model.table_data

    def set_column_kwargs(self, col_idx: int, **kwargs: Any) -> None:
        self.column_widgets[col_idx]["kwargs"].update(kwargs)

    def update_data(self, data: List[Tuple[Any, ...]], keep_scroll: bool = False) -> None:
        self.setCurrentIndex(self.model.index(-1, -1))
        self.clearFocus()

        for row in range(self.model.rowCount()):
            for col in range(self.model.columnCount()):
                idx = self.model.index(row, col)
                self.closePersistentEditor(idx)
                if self.indexWidget(idx):
                    self.indexWidget(idx).deleteLater()
                    self.setIndexWidget(idx, None)

        self.model.beginResetModel()
        self.model.table_data = data
        self.model.endResetModel()
        self._update_height()
        
        if self.on_data_change:
            self.model.on_data_change_cb = self.on_data_change

        for row in range(self.model.rowCount()):
            for col, cfg in enumerate(self.column_widgets):
                cls_name = cfg.get("class", "QLabel")
                if cls_name == "QLabel":
                    cls_name = QLabel
                if cls_name in (OComboBox, "OComboBox"):
                    self.openPersistentEditor(self.model.index(row, col))
        self._recalc_flexible_height()
        self.viewport().update()

    def _update_height(self) -> None:
        if self._hug:
            row_count = self.model.rowCount()
            total_h = self._header_height + (row_count * self._base_row_height) + 2
        else:
            visible = self.visible_rows or 8
            total_h = self._header_height + (visible * self._base_row_height) + 2

        if self._flexible_height:
            self.setMinimumHeight(total_h)
            self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        else:
            self.setFixedHeight(total_h)

    def _recalc_flexible_height(self) -> None:
        if hasattr(self, "_flexible_height") and self._flexible_height:
            h = self.viewport().height()
            rows = self.model.rowCount()
            if rows > 0:
                calc_h = max(self._base_row_height, int(h / rows))
                self.verticalHeader().setDefaultSectionSize(calc_h)

    def scroll_to_index(self, index: int) -> None:
        idx = self.model.index(index, 0)
        if idx.isValid():
            self.scrollTo(idx, QAbstractItemView.PositionAtTop)

    def focus_row(self, row: int, col: int, cursor_pos: Optional[int] = None) -> None:
        idx = self.model.index(row, col)
        if idx.isValid():
            self._focus_cursor_pos = cursor_pos
            self.setCurrentIndex(idx)
            self.edit(idx)

    def resizeEvent(self, event: Any) -> None:
        super().resizeEvent(event)
        
        header_h = self.horizontalHeader().height()
        sb_w = 8  # Hardcoded in CSS
        self._corner_filler.setGeometry(self.width() - sb_w - 1, 1, sb_w, header_h - 1)
        self._corner_filler.show()
        self._corner_filler.raise_()
        
        total_weight = sum(
            cfg.get("weight", 1) for cfg in self.column_widgets
        )
        if total_weight > 0:
            w = self.viewport().width()
            for i, cfg in enumerate(self.column_widgets):
                weight = cfg.get("weight", 1)
                self.setColumnWidth(i, int(w * (weight / total_weight)))
        self._recalc_flexible_height()

    def wheelEvent(self, event: Any) -> None:
        delta = event.angleDelta().y()
        if delta != 0:
            step = 1 if delta < 0 else -1
            sb = self.verticalScrollBar()
            sb.setValue(sb.value() + step * sb.singleStep())
            event.accept()
        else:
            super().wheelEvent(event)

    def omninativeui_prepaint(self) -> None:
        pass

    def pack(self, **kwargs: Any) -> None:
        pass

# ---------------------------------------------------------------------------
# OTreeWidget
# ---------------------------------------------------------------------------

class OTreeWidget(QWidget):
    def __init__(
        self,
        master: Optional[QWidget] = None,
        text: str = "Label",
        expanded: bool = True,
        width: Union[int, str] = "100%",
        height: Union[int, str] = "auto",
        header_height: int = 24,
        icon_width: int = 14,
        icon_height: int = 20,
        header_spacing: int = 8,
        indent: int = 20,
        content_spacing: int = 5,
        text_color: Optional[str] = None,
        icon_color: Optional[str] = None,
        icon_hover_color: Optional[str] = None,
        font_size: Optional[int] = None,
        theme: Optional[dict] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master)

        apply_layout_dimensions(self, width, height)

        self._icon_height = icon_height

        self.layout_ = QVBoxLayout(self)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(0)
        self.layout_.setAlignment(Qt.AlignTop)

        self.expanded = expanded
        self._hovered = False

        # Header (Chevron + Label)
        self.header = QWidget()
        self.header.setFixedHeight(header_height)
        self.header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.header_layout = QHBoxLayout(self.header)
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout.setSpacing(header_spacing)
        self.header_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.icon_lbl = QLabel()
        self.icon_lbl.setFixedSize(icon_width, icon_height)
        self.icon_lbl.setAlignment(Qt.AlignCenter)
        self.icon_lbl.setCursor(Qt.PointingHandCursor)

        self._txt_color = o_theme_val(theme, "text_color", text_color, OMNINATIVE['fg'])
        self._icon_color = o_theme_val(theme, "icon_color", icon_color, OMNINATIVE['fg_muted'])
        self._icon_hover_color = o_theme_val(theme, "icon_hover_color", icon_hover_color, self._txt_color)
        _sz = o_theme_val(theme, "font_size", font_size, _FONT_SIZE_SM)

        self.text_lbl = QLabel(text)
        self.text_lbl.setFixedHeight(icon_height)
        self.text_lbl.setFont(QFont(_FONT_FAMILY, _sz))
        self.text_lbl.setStyleSheet(f"color: {self._txt_color};")
        self.text_lbl.setCursor(Qt.PointingHandCursor)

        self.header_layout.addWidget(self.icon_lbl, 0, Qt.AlignVCenter)
        self.header_layout.addWidget(self.text_lbl, 0, Qt.AlignVCenter)
        self.header_layout.addStretch()

        self.layout_.addWidget(self.header)

        # Content Container
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(indent, content_spacing, 0, 0)
        self.content_layout.setSpacing(content_spacing)
        self.layout_.addWidget(self.content)

        self.icon_lbl.mousePressEvent = self.toggle
        self.text_lbl.mousePressEvent = self.toggle

        def on_enter(e):
            self._hovered = True
            self._update_icon()
        def on_leave(e):
            self._hovered = False
            self._update_icon()

        self.header.enterEvent = on_enter
        self.header.leaveEvent = on_leave

        self._update_icon()
        if not self.expanded:
            self.content.hide()

    def toggle(self, event: Any = None) -> None:
        self.expanded = not self.expanded
        self.content.setVisible(self.expanded)
        self._update_icon()

    def _update_icon(self) -> None:
        direction = "down" if self.expanded else "right"
        color = self._icon_hover_color if self._hovered else self._icon_color
        pixmap = _get_cached_chevron(size=self._icon_height, color=color, direction=direction, align="left")
        self.icon_lbl.setPixmap(pixmap)

    def add_widget(self, widget: QWidget) -> None:
        self.content_layout.addWidget(widget)

    def pack(self, **kwargs: Any) -> None: pass

# ---------------------------------------------------------------------------
# OTabs
# ---------------------------------------------------------------------------
class OTabs(QWidget):
    def __init__(
        self,
        master: Optional[QWidget] = None,
        eager: bool = True,
        width: Union[int, str] = "100%",
        height: Union[int, str] = "auto",
        header_height: int = 28,
        header_pad: int = 3,
        header_spacing: int = 4,
        tab_button_height: int = 20,
        content_gap: int = 10,
        bg_color: Optional[str] = None,
        border_color: Optional[str] = None,
        tab_bg_color: Optional[str] = None,
        tab_text_color: Optional[str] = None,
        tab_active_bg_color: Optional[str] = None,
        tab_active_text_color: Optional[str] = None,
        tab_hover_text_color: Optional[str] = None,
        border_radius: Optional[int] = None,
        font_size: Optional[int] = None,
        theme: Optional[dict] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master)

        apply_layout_dimensions(self, width, height)

        self._tab_button_height = tab_button_height

        self._bg = o_theme_val(theme, "bg_color", bg_color, OMNINATIVE['bg'])
        self._bc = o_theme_val(theme, "border_color", border_color, OMNINATIVE['border'])
        self._tab_bg = o_theme_val(theme, "tab_bg_color", tab_bg_color, self._bg)
        self._tab_txt = o_theme_val(theme, "tab_text_color", tab_text_color, OMNINATIVE['fg_muted'])
        self._tab_act_bg = o_theme_val(theme, "tab_active_bg_color", tab_active_bg_color, OMNINATIVE['surface'])
        self._tab_act_txt = o_theme_val(theme, "tab_active_text_color", tab_active_text_color, OMNINATIVE['fg'])
        self._tab_hov_txt = o_theme_val(theme, "tab_hover_text_color", tab_hover_text_color, OMNINATIVE['fg'])
        self._br = o_theme_val(theme, "border_radius", border_radius, _CORNER)
        self._sz = o_theme_val(theme, "font_size", font_size, _FONT_SIZE_SM)

        self.layout_ = QVBoxLayout(self)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(0)

        self.header_container = QFrame()
        self.header_container.setFixedHeight(header_height)
        self.header_container.setStyleSheet(f"""
            QFrame {{
                background: {self._bg};
                border: 1px solid {self._bc};
                border-radius: {self._br}px;
            }}
        """)
        self.header_layout = QHBoxLayout(self.header_container)
        self.header_layout.setContentsMargins(
            header_pad,
            header_pad,
            header_pad,
            header_pad,
        )
        self.header_layout.setSpacing(header_spacing)

        self.layout_.addWidget(self.header_container)
        self.layout_.addSpacing(content_gap)

        self.stacked_widget = QStackedWidget()
        self.layout_.addWidget(self.stacked_widget)

        self.tabs = {}
        self._active_tab = None

    def add(self, name: str, on_first_activate: Optional[Callable[[QWidget], None]] = None) -> QWidget:
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)

        btn = QPushButton(name)
        btn.setFixedHeight(self._tab_button_height)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {self._tab_bg};
                color: {self._tab_txt};
                border: none;
                border-radius: 3px;
                font-family: '{_FONT_FAMILY}';
                font-size: {self._sz}pt;
            }}
            QPushButton:hover {{
                color: {self._tab_hov_txt};
            }}
        """)

        btn.clicked.connect(lambda _, n=name: self.set_active(n))
        self.header_layout.addWidget(btn, 1)

        self.stacked_widget.addWidget(page)

        self.tabs[name] = {
            "page": page,
            "btn": btn,
            "on_first_activate": on_first_activate,
            "activated": on_first_activate is None
        }

        if self._active_tab is None:
            self.set_active(name)

        return page

    def set_active(self, name: str) -> None:
        if name not in self.tabs: return

        for t_name, info in self.tabs.items():
            if t_name == name:
                info["btn"].setStyleSheet(f"""
                    QPushButton {{
                        background: {self._tab_act_bg};
                        color: {self._tab_act_txt};
                        border: none;
                        border-radius: 3px;
                        font-family: '{_FONT_FAMILY}';
                        font-size: {self._sz}pt;
                    }}
                """)
                self.stacked_widget.setCurrentWidget(info["page"])
                if not info["activated"]:
                    info["activated"] = True
                    if info["on_first_activate"]:
                        info["on_first_activate"](info["page"])
            else:
                info["btn"].setStyleSheet(f"""
                    QPushButton {{
                        background: {self._tab_bg};
                        color: {self._tab_txt};
                        border: none;
                        border-radius: 3px;
                        font-family: '{_FONT_FAMILY}';
                        font-size: {self._sz}pt;
                    }}
                    QPushButton:hover {{
                        color: {self._tab_hov_txt};
                    }}
                """)
        self._active_tab = name

    def preload(self, name: str) -> None:
        if name in self.tabs:
            info = self.tabs[name]
            if not info["activated"]:
                info["activated"] = True
                if info["on_first_activate"]:
                    info["on_first_activate"](info["page"])

    def pack(self, **kwargs: Any) -> None: pass

# ---------------------------------------------------------------------------
# OSidebar
# ---------------------------------------------------------------------------
class OSidebarItem(QFrame):
    """
    A single navigation item for the OSidebar.
    Supports hover states and click events.
    """
    clicked = Signal(str)

    def __init__(
        self,
        master: Optional[QWidget],
        text: str,
        icon: Optional[str] = None,
        command: Optional[Callable[[], None]] = None,
        theme: Optional[dict] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(master)
        self.text = text
        self.command = command
        
        self.setObjectName("OSidebarItem")
        self.setFixedHeight(33)
        self.setCursor(Qt.PointingHandCursor)
        
        self._bg_hov = o_theme_val(theme, "item_hover_color", kwargs.get("item_hover_color"), OMNINATIVE["surface"])
        self._bg_active = o_theme_val(theme, "item_active_color", kwargs.get("item_active_color"), OMNINATIVE["surface"])
        self._text_color = o_theme_val(theme, "text_color", kwargs.get("text_color"), OMNINATIVE["fg"])
        self._font_family = o_theme_val(theme, "font_family", kwargs.get("font_family"), _FONT_FAMILY)
        
        self.layout_ = QHBoxLayout(self)
        self.layout_.setContentsMargins(10, 0, 10, 0)
        self.layout_.setSpacing(6)
        self.layout_.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        # If there's an icon, you could add an OLabel or icon renderer here
        # For now, just the text as per design, but scalable for icons
        self.lbl = QLabel(text)
        self.lbl.setStyleSheet("background: transparent; border: none;")
        self.lbl.setFont(QFont(self._font_family, _FONT_SIZE_SM, QFont.Normal))
        self.layout_.addWidget(self.lbl)
        
        self._is_active = False
        self._update_style()
        
    def _update_style(self, hovered: bool = False) -> None:
        if self._is_active:
            bg = self._bg_active
            text_color = self._text_color
        elif hovered:
            bg = self._bg_hov
            text_color = self._text_color
        else:
            bg = "transparent"
            text_color = OMNINATIVE.get("fg_muted", "#A0A0A0")
            
        self.setStyleSheet(f"""
            #OSidebarItem {{
                background-color: {bg};
                border-radius: 10px;
            }}
            QLabel {{
                color: {text_color};
                font-size: 12px;
                font-family: '{self._font_family}';
            }}
        """)
        
    def set_active(self, active: bool) -> None:
        self._is_active = active
        self._update_style()
        
    def enterEvent(self, event: Any) -> None:
        if not self._is_active:
            self._update_style(hovered=True)
        super().enterEvent(event)
        
    def leaveEvent(self, event: Any) -> None:
        if not self._is_active:
            self._update_style(hovered=False)
        super().leaveEvent(event)
        
    def mousePressEvent(self, event: Any) -> None:
        self.clicked.emit(self.text)
        if self.command:
            self.command()
        super().mousePressEvent(event)


class OSidebar(QFrame):
    """
    Native sidebar container with a header, body (for items), and footer.
    """
    def __init__(
        self,
        master: Optional[QWidget],
        width: Union[int, str] = 250,
        bg_color: Optional[str] = None,
        theme: Optional[dict] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(master)
        
        apply_layout_dimensions(self, width, "100%")
        self.setObjectName("OSidebar")
        
        self._bg = o_theme_val(theme, "bg_color", bg_color, "#282828")
        self.theme = theme
        self.kwargs = kwargs
        
        self.setStyleSheet(f"""
            #OSidebar {{
                background-color: {self._bg};
                border: none;
            }}
        """)
        
        self.layout_ = QVBoxLayout(self)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(0)
        
        # Header Group
        self.header_group = QFrame(self)
        self.header_group.setFixedHeight(60)
        self.header_layout = QHBoxLayout(self.header_group)
        self.header_layout.setContentsMargins(25, 0, 25, 0)
        self.header_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.layout_.addWidget(self.header_group)
        
        # Content Group
        self.content_group = QFrame(self)
        self.content_layout = QVBoxLayout(self.content_group)
        self.content_layout.setContentsMargins(15, 0, 15, 0)
        self.content_layout.setSpacing(5)
        self.content_layout.setAlignment(Qt.AlignTop)
        
        # Wrap content in a scroll area just in case there are many items
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.content_group)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; } QWidget#OSidebarContent { background: transparent; }")
        self.content_group.setObjectName("OSidebarContent")
        self.layout_.addWidget(self.scroll_area, 1) # flex-grow: 1
        
        # Footer Group
        self.footer_group = QFrame(self)
        self.footer_group.setFixedHeight(60)
        self.footer_layout = QHBoxLayout(self.footer_group)
        self.footer_layout.setContentsMargins(25, 12, 25, 12)
        self.footer_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.layout_.addWidget(self.footer_group)
        
        self._items: Dict[str, OSidebarItem] = {}
        
    def add_item(self, text: str, command: Optional[Callable[[], None]] = None) -> OSidebarItem:
        """Adds a navigation item to the sidebar."""
        item = OSidebarItem(self.content_group, text=text, command=command, theme=self.theme, **self.kwargs)
        self.content_layout.addWidget(item)
        self._items[text] = item
        
        # Optional: Auto-manage active state if you want a single active item
        item.clicked.connect(self.set_active_item)
        return item
        
    def set_active_item(self, text: str) -> None:
        """Sets the active state for the item with the given text, deactivating others."""
        for item_text, item in self._items.items():
            item.set_active(item_text == text)
            
    def pack(self, **kwargs: Any) -> None: pass
