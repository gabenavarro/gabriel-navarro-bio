"""Regression tests for horizontal-overflow lock.

User-reported symptom on Edge desktop: after a trackpad swipe-back gesture,
the page renders shifted horizontally — cards extend past the viewport's
right edge and the navbar links are cut off. The bug couldn't be
reproduced in headless Chromium; the working hypothesis is Edge's BFCache
restoring a non-zero scrollX on back-navigation when ANY element renders
even one pixel wider than the viewport.

The defensive fix locks horizontal scrolling at the html level
(`overflow-x: clip` with `hidden` fallback) and resets `scrollX` to 0 in
the `pageshow` handler when the page is restored from BFCache. These tests
lock both pieces in place so they can't drift back out.
"""

from fasthtml.common import to_xml

from src.components.layout.page import StandardPage
from src.services.javascript.bfcache_scroll import BFCACHE_SCROLL_RESET_JS
from src.styles import FACTORY_CSS


def test_factory_css_locks_horizontal_overflow_on_html():
    """html element gets `overflow-x: hidden` (with `clip` upgrade) so any
    accidental pixel of overflow can never become a scrollable area."""
    assert "overflow-x: hidden" in FACTORY_CSS
    assert "overflow-x: clip" in FACTORY_CSS


def test_html_and_body_have_explicit_full_width():
    """Belt-and-braces: html/body explicitly width:100% so they never
    expand beyond the viewport (e.g., to fit a too-wide child)."""
    # Find the `html, body { ... }` block and confirm `width: 100%` is in it.
    block_start = FACTORY_CSS.find("html, body {")
    assert block_start != -1, "html, body rule block missing"
    block_end = FACTORY_CSS.find("}", block_start)
    block = FACTORY_CSS[block_start:block_end]
    assert "width: 100%" in block


def test_bfcache_scroll_reset_script_exists_and_handles_persisted_pageshow():
    """The pageshow handler resets scrollX when persisted (BFCache restore)."""
    html = to_xml(BFCACHE_SCROLL_RESET_JS)
    # Listens for pageshow and checks event.persisted
    assert "pageshow" in html
    assert "persisted" in html
    # Resets scrollX to 0 (preserving scrollY)
    assert "scrollTo(0," in html


def test_standard_page_includes_bfcache_script():
    """StandardPage emits the BFCACHE_SCROLL_RESET_JS so every rendered
    page gets the safety net, not just the ones that opt in."""
    html = to_xml(StandardPage("Test", "body content"))
    # The hallmark of the script is the persisted-pageshow guard.
    assert "event.persisted" in html
    assert "scrollTo(0," in html
