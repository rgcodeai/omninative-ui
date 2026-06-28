# omninative_ui/tokens.py
from typing import Dict

OMNINATIVE: Dict[str, str] = {
    "bg": "#2C2C2C",        # Base background (windows, panels)
    "surface": "#383838",   # Elevated surfaces (inputs, headers, hover states)
    "fg": "#FFFFFF",        # Primary foreground (text, active icons)
    "fg_muted": "#9E9B9B",  # Secondary foreground (dimmed text, inactive icons)
    "accent": "#B6FF0E",    # Brand color (focus rings, selection, interactive highlights)
    "border": "#585858",    # Borders, separators, divider lines
    "success": "#00D007",   # Success states
    "danger": "#DF1515"     # Error/danger states
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
