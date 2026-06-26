# omninative_ui/tokens.py
from typing import Dict

OMNINATIVE: Dict[str, str] = {
    "background": "#2C2C2C",
    "dark": "#383838",
    "bright": "#FFFFFF",
    "accent": "#9E9B9B",
    "primary": "#B6FF0E",
    "gray": "#585858",
    "success": "#00D007",
    "danger": "#DF1515"
}

_FONT_FAMILY: str = "Segoe UI"
_FONT_SIZE_SM: int = 9
_FONT_SIZE_LG: int = 12
_CORNER: int = 4
_PAD: int = 4

def set_global_theme(new_theme: Dict[str, str]) -> None:
    """
    Overwrites the global OMNINATIVE dictionary.
    Call this right after importing the module and before instantiating any components.
    """
    OMNINATIVE.update(new_theme)
