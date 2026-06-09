# omninative_ui/icons.py
from typing import Dict, Tuple, Any, Optional, Union
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QPen, QColor, QBrush
from PySide6.QtCore import Qt, QRect, QRectF, QPointF

# Importamos OMNINATIVE para los colores por defecto
from .tokens import OMNINATIVE

# Icons Cache
_icon_cache: Dict[Tuple[Any, ...], QPixmap] = {}
_audio_icon_cache: Dict[Tuple[Any, ...], QPixmap] = {}

def _get_cached_checkbox(size: int = 20, checked: bool = False, bg_color: Optional[str] = None, border_color: Optional[str] = None, check_color: Optional[str] = None, corner_radius: int = 3) -> QPixmap:
    if bg_color is None: bg_color = OMNINATIVE["dark"]
    if border_color is None: border_color = OMNINATIVE["gray"]
    if check_color is None: check_color = OMNINATIVE["bright"]
    key = ("checkbox", size, checked, bg_color, border_color, check_color, corner_radius)
    if key not in _icon_cache:
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = QRect(0, 0, size - 1, size - 1)
        painter.setBrush(QBrush(QColor(bg_color)))
        pen = QPen(QColor(border_color))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRoundedRect(rect, corner_radius, corner_radius)
        
        if checked:
            path = QPainterPath()
            path.moveTo(size * 0.28, size * 0.52)
            path.lineTo(size * 0.46, size * 0.70)
            path.lineTo(size * 0.76, size * 0.32)
            
            pen = QPen(QColor(check_color))
            pen.setWidthF(2.2)
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawPath(path)
            
        painter.end()
        _icon_cache[key] = pixmap
    return _icon_cache[key]

def _get_cached_chevron(size: int = 20, color: Optional[str] = None, direction: str = "down", align: str = "center") -> QPixmap:
    if color is None:
        color = OMNINATIVE["accent"]
    key = ("chevron", size, color, direction, align)
    if key not in _icon_cache:
        padding = size * 0.3
        path = QPainterPath()
        center_x = size / 2.0
        center_y = size / 2.0
        
        if direction == "down":
            left_x = padding
            right_x = size - padding
            mid_x = size / 2.0
            top_y = size * 0.4
            bot_y = size * 0.65
            path.moveTo(left_x, top_y)
            path.lineTo(mid_x, bot_y)
            path.lineTo(right_x, top_y)
            actual_width = right_x - left_x + 2
            shift_x = left_x - 1
            center_x = mid_x
            center_y = (top_y + bot_y) / 2.0
        elif direction == "right":
            top_y = padding
            bot_y = size - padding
            mid_y = size / 2.0
            left_x = size * 0.4
            right_x = size * 0.65
            path.moveTo(left_x, top_y)
            path.lineTo(right_x, mid_y)
            path.lineTo(left_x, bot_y)
            actual_width = right_x - left_x + 2
            shift_x = left_x - 1
            center_x = (left_x + right_x) / 2.0
            center_y = mid_y
            
        if align == "left":
            max_width = int(size * 0.7)
            pixmap = QPixmap(max_width, size)
        else:
            pixmap = QPixmap(size, size)
            
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        pen = QPen(QColor(color))
        pen.setWidthF(1.5)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        
        if align == "left":
            C = max_width / 2.0
            shift_x = center_x - C
            shift_y = center_y - (size / 2.0)
            painter.translate(-shift_x, -shift_y)
            
        painter.drawPath(path)
        painter.end()
        _icon_cache[key] = pixmap
    return _icon_cache[key]

def _get_cached_plus(size: int = 20, color: Optional[str] = None, weight: float = 1.5) -> QPixmap:
    if color is None:
        color = OMNINATIVE["accent"]
    key = ("plus", size, color, weight)
    if key not in _icon_cache:
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        pen = QPen(QColor(color))
        pen.setWidthF(weight)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        
        path = QPainterPath()
        path.moveTo(size * 0.25, size / 2.0)
        path.lineTo(size * 0.75, size / 2.0)
        path.moveTo(size / 2.0, size * 0.25)
        path.lineTo(size / 2.0, size * 0.75)
        
        painter.drawPath(path)
        painter.end()
        _icon_cache[key] = pixmap
    return _icon_cache[key]

def _get_cached_arrow(size: int = 20, color: Optional[str] = None, direction: str = "up", weight: float = 2.0) -> QPixmap:
    if color is None:
        color = OMNINATIVE["gray"]
    key = ("arrow", size, color, direction, weight)
    if key not in _icon_cache:
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        pen = QPen(QColor(color))
        pen.setWidthF(weight)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        
        path = QPainterPath()
        mid_x = size / 2.0
        
        if direction == "up":
            top_y = size * 0.25
            bot_y = size * 0.75
            path.moveTo(mid_x, bot_y)
            path.lineTo(mid_x, top_y)
            path.moveTo(size * 0.3, size * 0.45)
            path.lineTo(mid_x, top_y)
            path.lineTo(size * 0.7, size * 0.45)
            
        painter.drawPath(path)
        painter.end()
        _icon_cache[key] = pixmap
    return _icon_cache[key]


def _get_cached_audio_icon(icon_type: str, size: int = 24, color: Union[str, 'QColor', None] = None) -> QPixmap:
    from PySide6.QtCore import QRectF, QPointF
    if color is None:
        color = OMNINATIVE["bright"]
    if type(color).__name__ == "QColor":
        color_hex = color.name()
    else:
        color_hex = str(color)
        color = QColor(color_hex)
        
    key = (icon_type, size, color_hex)
    if key not in _audio_icon_cache:
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        pen = QPen(color)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        
        brush = QBrush(color)
        c = size / 2.0
        
        if icon_type == "play":
            w_tri = size * 0.35
            h_tri = size * 0.42
            x_left = c - w_tri * 0.35
            x_tip = c + w_tri * 0.65
            y_top = c - h_tri * 0.5
            y_bot = c + h_tri * 0.5
            
            path = QPainterPath()
            path.moveTo(x_left, y_top)
            path.lineTo(x_tip, c)
            path.lineTo(x_left, y_bot)
            path.closeSubpath()
            
            painter.setPen(Qt.NoPen)
            painter.setBrush(brush)
            painter.drawPath(path)
            
        elif icon_type == "pause":
            w_bar = max(2, int(size * 0.12))
            h_bar = max(6, int(size * 0.42))
            gap = max(2, int(size * 0.12))
            x_left = c - w_bar - gap / 2.0
            x_right = c + gap / 2.0
            y_top = c - h_bar / 2.0
            
            painter.setPen(Qt.NoPen)
            painter.setBrush(brush)
            painter.drawRect(QRectF(x_left, y_top, w_bar, h_bar))
            painter.drawRect(QRectF(x_right, y_top, w_bar, h_bar))
            
        elif icon_type == "stop":
            w_sq = size * 0.38
            y_top = c - w_sq / 2.0
            x_left = c - w_sq / 2.0
            
            painter.setPen(Qt.NoPen)
            painter.setBrush(brush)
            painter.drawRoundedRect(QRectF(x_left, y_top, w_sq, w_sq), 1.5, 1.5)
            
        elif icon_type == "loop":
            r = size * 0.22
            pen.setWidthF(1.5)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            
            rect = QRectF(c - r, c - r, 2 * r, 2 * r)
            painter.drawArc(rect, 40 * 16, 280 * 16)
            
            import math
            angle_rad = math.radians(40)
            ax = c + r * math.cos(angle_rad)
            ay = c - r * math.sin(angle_rad)
            
            arrow_path = QPainterPath()
            arrow_path.moveTo(ax - 2.5, ay - 2.5)
            arrow_path.lineTo(ax, ay + 1.0)
            arrow_path.lineTo(ax - 3.5, ay + 2.0)
            arrow_path.closeSubpath()
            
            painter.setPen(Qt.NoPen)
            painter.setBrush(brush)
            painter.drawPath(arrow_path)
            
        elif icon_type == "mic":
            w_cap = size * 0.20
            h_cap = size * 0.37
            
            gap = size * 0.05
            stroke_w = max(1.5, size * 0.07)
            
            r_arc = w_cap / 2.0 + gap + stroke_w / 2.0
            
            total_h = h_cap - w_cap / 2.0 + r_arc
            y_cap = c - total_h / 2.0
            x_cap = c - w_cap / 2.0
            
            painter.setPen(Qt.NoPen)
            painter.setBrush(brush)
            painter.drawRoundedRect(QRectF(x_cap, y_cap, w_cap, h_cap), w_cap / 2.0, w_cap / 2.0)
            
            pen.setWidthF(stroke_w)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            
            cy_arc = y_cap + h_cap - w_cap / 2.0
            x_arc = c - r_arc
            y_arc = cy_arc - r_arc
            
            start_angle = -25 * 16
            span_angle = -130 * 16
            painter.drawArc(QRectF(x_arc, y_arc, r_arc * 2, r_arc * 2), start_angle, span_angle)
            
        elif icon_type.startswith("volume"):
            sp_w = size * 0.12
            sp_h = size * 0.22
            x_sp = c - size * 0.18
            y_sp = c - sp_h / 2.0
            
            cone_path = QPainterPath()
            cone_path.moveTo(x_sp + sp_w, y_sp)
            cone_path.lineTo(c, y_sp - size * 0.15)
            cone_path.lineTo(c, y_sp + sp_h + size * 0.15)
            cone_path.lineTo(x_sp + sp_w, y_sp + sp_h)
            cone_path.closeSubpath()
            
            painter.setPen(Qt.NoPen)
            painter.setBrush(brush)
            painter.drawRect(QRectF(x_sp, y_sp, sp_w, sp_h))
            painter.drawPath(cone_path)
            
            pen.setWidthF(1.2)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            
            if icon_type == "volume_mute":
                xx = c + size * 0.15
                x_size = size * 0.08
                painter.drawLine(xx - x_size, c - x_size, xx + x_size, c + x_size)
                painter.drawLine(xx - x_size, c + x_size, xx + x_size, c - x_size)
            else:
                r1 = size * 0.15
                r2 = size * 0.28
                if icon_type in ("volume_low", "volume_med", "volume_high"):
                    painter.drawArc(QRectF(c - r1, c - r1, 2 * r1, 2 * r1), -60 * 16, 120 * 16)
                if icon_type in ("volume_med", "volume_high"):
                    painter.drawArc(QRectF(c - r2, c - r2, 2 * r2, 2 * r2), -60 * 16, 120 * 16)
                    
        painter.end()
        _audio_icon_cache[key] = pixmap
    return _audio_icon_cache[key]

def _get_cached_app_icon(size: int = 64) -> 'QIcon':
    from PySide6.QtGui import QIcon
    key = ("app_icon", size)
    if key not in _icon_cache:
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = QRectF(0, 0, size, size)
        painter.setBrush(QBrush(QColor(OMNINATIVE["background"])))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, size * 0.22, size * 0.22)
        
        pen = QPen(QColor(OMNINATIVE["primary"]))
        pen.setWidthF(size * 0.12)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        
        o_rect = QRectF(size * 0.25, size * 0.25, size * 0.5, size * 0.5)
        painter.drawEllipse(o_rect)
        
        painter.end()
        _icon_cache[key] = QIcon(pixmap)
    return _icon_cache[key]

def _get_cached_file_icon(size: int = 24, color: Optional[str] = None) -> QPixmap:
    if color is None:
        color = OMNINATIVE["accent"]
    key = ("file", size, color)
    if key not in _icon_cache:
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        pen = QPen(QColor(color))
        pen.setWidthF(max(1.5, size * 0.08))
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        
        path = QPainterPath()
        # Outer shape
        path.moveTo(size * 0.25, size * 0.15)
        path.lineTo(size * 0.25, size * 0.85)
        path.lineTo(size * 0.75, size * 0.85)
        path.lineTo(size * 0.75, size * 0.35)
        path.lineTo(size * 0.55, size * 0.15)
        path.closeSubpath()
        
        # Inner fold
        path.moveTo(size * 0.55, size * 0.15)
        path.lineTo(size * 0.55, size * 0.35)
        path.lineTo(size * 0.75, size * 0.35)
        
        painter.drawPath(path)
        painter.end()
        _icon_cache[key] = pixmap
    return _icon_cache[key]
