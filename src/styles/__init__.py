"""Style aggregation for the Factory design system.

`FACTORY_CSS` is concatenated from per-concern files (base, layout,
components, pages) so `src/components/layout/page.py` can keep injecting a
single combined string via `Style(THEME_CSS + FACTORY_CSS + extra_styles)`.

Per-component CSS constants (CHIPS_CSS, BUTTON_CSS, BALL_BACKGROUND_CSS,
etc.) live in `custom_css.py` and are re-exported here for backwards
compatibility with existing per-component `Style(...)` injections.
"""

from ._base import BASE_CSS
from ._components import COMPONENTS_CSS
from ._layout import LAYOUT_CSS
from ._pages import PAGES_CSS
from .custom_css import *
from .theme import THEME_CSS

FACTORY_CSS = f"{BASE_CSS}\n{LAYOUT_CSS}\n{COMPONENTS_CSS}\n{PAGES_CSS}"

__all__ = [
    "BASE_CSS",
    "COMPONENTS_CSS",
    "FACTORY_CSS",
    "LAYOUT_CSS",
    "PAGES_CSS",
    "THEME_CSS",
]
