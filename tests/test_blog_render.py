"""Tests for src.services.blog_render."""
from src.services.blog_render import render_to_html


def test_render_passes_simple_markdown_to_html():
    md = "# Hello\n\nWorld."
    html = render_to_html(md)
    assert "<h1" in html  # monsterui adds classes; just check the tag opened
    assert "Hello" in html
    assert "<p" in html
    assert "World." in html


def test_render_returns_plain_string_not_notstr():
    """The function must return `str`, not a FastHTML NotStr/FT object."""
    html = render_to_html("plain")
    assert isinstance(html, str)


def test_render_preserves_inline_svg_when_clean():
    md = (
        '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" role="img">\n'
        '  <title>t</title>\n'
        '  <text>x</text>\n'
        '</svg>'
    )
    html = render_to_html(md)
    assert "<svg" in html
    assert "<title" in html  # monsterui may rewrite case but tag stays
    assert "<text" in html
    # The diagnostic for the bug we're fixing — must NOT appear:
    assert "<p><svg" not in html
    assert "<p><text" not in html
