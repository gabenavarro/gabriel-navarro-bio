"""Regression tests for the navbar layout.

The first cut of `navigation()` wrapped nav links in `Ul(Li(A(...)), cls="uk-navbar-nav")`,
an old UIkit-3 pattern. FrankenUI 2 (MonsterUI's underlying CSS framework)
dropped the `.uk-navbar-nav` class entirely, so the UL silently fell back to
Tailwind's preflight `display: block` and the links stacked into a 61px-wide
vertical column. These tests assert the canonical MonsterUI shape so the
regression can't sneak back in.
"""

from fasthtml.common import to_xml

from src.components.layout.navigation import navigation
from src.config.settings import settings


def test_nav_links_render_as_top_level_anchors_not_wrapped_in_ul():
    """Every link from settings.NAV_LINKS appears as a top-level <a> in the navbar.

    Concretely: the rendered HTML must NOT contain `class="uk-navbar-nav"`
    (the dead class) and must contain one `<a class="factory-nav-link">` per
    settings.NAV_LINKS entry.
    """
    html = to_xml(navigation())

    assert "uk-navbar-nav" not in html, (
        "uk-navbar-nav is a no-op in FrankenUI 2; nav links must be passed "
        "as positional A(...) args to NavBar, not wrapped in Ul(Li(...))."
    )

    # One factory-nav-link <a> per configured nav link.
    assert html.count('class="factory-nav-link"') == len(settings.NAV_LINKS)

    # Every label and href makes it into the markup.
    for link in settings.NAV_LINKS:
        assert link["label"] in html
        assert f'href="{link["href"]}"' in html


def test_navbar_carries_aria_label_for_screen_readers():
    """The <nav> wrapper must carry aria-label='Primary navigation' (a11y from C5)."""
    html = to_xml(navigation())
    assert 'aria-label="Primary navigation"' in html


def test_brand_uses_factory_brand_class_no_inline_style():
    """Brand styling lives in the .factory-brand CSS class, not as an inline style.

    Inline styles in layout components were eliminated in Epic A; this test
    locks in that posture for the navbar brand specifically.
    """
    html = to_xml(navigation())
    assert "factory-brand" in html
    # No leaked inline style on the brand link
    assert "font-family: 'Geist'" not in html
