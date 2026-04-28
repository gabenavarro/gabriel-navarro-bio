"""Style aggregation for the Factory design system.

`FACTORY_CSS` is concatenated from per-concern files (base, layout,
components, pages) so `src/components/layout/page.py` can keep injecting a
single combined string via `Style(THEME_CSS + FACTORY_CSS + extra_styles)`.

Per-component CSS constants (CHIPS_CSS, BUTTON_CSS, BALL_BACKGROUND_CSS,
etc.) live in `custom_css.py` and are re-exported here for backwards
compatibility with existing per-component `Style(...)` injections.
"""

from ._base import BASE_CSS
from ._layout import LAYOUT_CSS
from ._components import COMPONENTS_CSS
from ._pages import PAGES_CSS
from .theme import THEME_CSS
from .custom_css import *  # noqa: F401,F403  re-export individual *_CSS constants

FACTORY_CSS = "\n".join([BASE_CSS, LAYOUT_CSS, COMPONENTS_CSS, PAGES_CSS])

__all__ = [
    "FACTORY_CSS",
    "THEME_CSS",
    "BASE_CSS",
    "LAYOUT_CSS",
    "COMPONENTS_CSS",
    "PAGES_CSS",
]
