# omninative_ui/__init__.py
"""
OmniNative UI — PySide6 component library with the OmniNative dark theme.

Usage:
    from omninative_ui import OButton, OWindow, OMNINATIVE
    from omninative_ui.chat import OChatView  # granular import
"""

from .tokens import (
    OMNINATIVE,
    _FONT_FAMILY,
    _FONT_SIZE_SM,
    _FONT_SIZE_LG,
    _CORNER,
    _PAD,
)

from .icons import (
    _icon_cache,
    _audio_icon_cache,
    _get_cached_checkbox,
    _get_cached_chevron,
    _get_cached_plus,
    _get_cached_arrow,
    _get_cached_audio_icon,
)

from ._utils import (
    get_global_stylesheet,
    _pixmap_to_data_url,
)

from .core import (
    OWindow,
    OGroup,
    OLabel,
    OElidedLabel,
    OSectionHeader,
    OSeparator,
    OButton,
    OOptionButton,
    OComboBox,
    ORadioButton,
    OCheckBoxBase,
    OCheckBox,
    OTableCheckBox,
    OStatusBar,
    OOptionRow,
)

from .inputs import (
    OLineEdit,
    OTextBox,
    OSpinBox,
    OSlider,
    _WheelIgnoredSlider,
    OProgressBar,
)

from .containers import (
    OScrollArea,
    OTreeWidget,
    OTabs,
    OVirtualTable,
    OTableTextEdit,
    OTableItemDelegate,
)

from .media import (
    OAudioButton,
    OAudioWaveform,
    OAudioPlayer,
    OImageViewer,
    OFullscreenViewer,
    OFileItem,
)

from .chat import (
    OChatMessage,
    OChatView,
    OChatInput,
    OActionMenuItem,
    OActionMenu,
)

# Re-export QTreeWidgetItem for convenience (used in demo)
from PySide6.QtWidgets import QTreeWidgetItem

__version__ = "0.1.4"
