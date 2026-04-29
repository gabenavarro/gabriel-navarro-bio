"""Tests for src.components.layout.footer."""

from datetime import datetime

from fasthtml.common import to_xml

from src.components.layout.footer import Footer
from src.config.settings import settings


def test_footer_contains_every_social_url_from_settings():
    """Footer renders every URL listed in settings.SOCIAL_LINKS."""
    html = to_xml(Footer())
    for link in settings.SOCIAL_LINKS:
        assert link["href"] in html, f"missing social link: {link['href']}"


def test_footer_contains_nav_links_in_bottom_row():
    """Footer also lists nav links (Projects, Blogs, CV) for footer navigation."""
    html = to_xml(Footer())
    for link in settings.NAV_LINKS:
        assert link["href"] in html
        assert link["label"] in html


def test_footer_contains_current_year_copyright():
    """Footer shows the current year in the copyright line."""
    html = to_xml(Footer())
    assert f"© {datetime.now().year}" in html
