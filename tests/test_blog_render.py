"""Tests for src.services.blog_render."""

from src.services.blog_render import render_to_html
from src.services.blog_render import ValidationIssue, validate_html


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
        "  <title>t</title>\n"
        "  <text>x</text>\n"
        "</svg>"
    )
    html = render_to_html(md)
    assert "<svg" in html
    assert "<title" in html  # monsterui may rewrite case but tag stays
    assert "<text" in html
    # The diagnostic for the bug we're fixing — must NOT appear:
    assert "<p><svg" not in html
    assert "<p><text" not in html


def test_validate_returns_empty_for_clean_html():
    html = '<svg viewBox="0 0 1 1" role="img"><title>t</title></svg>'
    assert validate_html(html) == []


def test_validate_catches_p_wrapping_svg():
    bad = "<p><svg></svg></p>"
    issues = validate_html(bad)
    assert any(i.kind == "p-wraps-svg" for i in issues)
    assert all(isinstance(i, ValidationIssue) for i in issues)


def test_validate_catches_p_wrapping_text():
    bad = '<svg role="img"><title>t</title></svg>\n<p><text x="0">stray</text></p>'
    issues = validate_html(bad)
    assert any(i.kind == "p-wraps-svg" for i in issues)


def test_validate_catches_svg_tag_mismatch():
    bad = '<svg role="img"><title>t</title>'  # missing </svg>
    issues = validate_html(bad)
    assert any(i.kind == "svg-tag-mismatch" for i in issues)


def test_validate_catches_svg_missing_title():
    bad = '<svg viewBox="0 0 1 1" role="img"><text>x</text></svg>'  # no <title>
    issues = validate_html(bad)
    assert any(i.kind == "svg-missing-title" for i in issues)


def test_validate_catches_svg_missing_role_img():
    bad = '<svg viewBox="0 0 1 1"><title>t</title></svg>'  # no role="img"
    issues = validate_html(bad)
    assert any(i.kind == "svg-missing-role" for i in issues)


def test_validate_returns_multiple_issues_at_once():
    bad = "<p><svg></svg></p><p><text>x</text></p>"  # two <p> wraps + tag mismatch + missing title
    issues = validate_html(bad)
    kinds = [i.kind for i in issues]
    assert kinds.count("p-wraps-svg") >= 2


def test_validate_issue_includes_snippet():
    bad = "<p><svg></svg></p>"
    issues = validate_html(bad)
    p_issues = [i for i in issues if i.kind == "p-wraps-svg"]
    assert len(p_issues) >= 1
    assert "<svg" in p_issues[0].snippet
