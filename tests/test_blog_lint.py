"""Tests for src.services.blog_lint."""
import pytest

from src.services.blog_lint import LintError, LintFix, lint_body


def test_module_exports_public_surface():
    """The module exports `LintError`, `LintFix`, `lint_body` as the public API."""
    # LintError is an Exception subclass; raising and catching it works.
    with pytest.raises(LintError):
        raise LintError("test")
    # LintFix is a dataclass with the documented fields and Literal constraint.
    fix = LintFix(kind="named-entity", count=1, detail="example")
    assert fix.kind == "named-entity"
    assert fix.count == 1
    assert fix.detail == "example"


def test_lint_body_returns_tuple_of_text_and_fixes():
    text = "no svg here, just prose"
    fixed, fixes = lint_body(text)
    assert fixed == text
    assert fixes == []


def test_lint_replaces_mdash_with_unicode():
    src = "<svg><text>A &mdash; B</text></svg>"
    fixed, fixes = lint_body(src)
    assert "&mdash;" not in fixed
    assert "—" in fixed
    assert any(f.kind == "named-entity" and f.count == 1 for f in fixes)


def test_lint_replaces_multiple_named_entities():
    src = "<svg><text>x &times; y &rarr; z</text></svg>"
    fixed, _ = lint_body(src)
    assert "&times;" not in fixed
    assert "&rarr;" not in fixed
    assert "×" in fixed and "→" in fixed


def test_lint_preserves_xml_safe_entities():
    src = "<svg><text>x &lt; y &amp; z &gt; w</text></svg>"
    fixed, fixes = lint_body(src)
    assert fixed == src
    assert fixes == []


def test_lint_raises_on_unmapped_entity():
    src = "<svg><text>nonsense &zzznotreal;</text></svg>"
    with pytest.raises(LintError, match="zzznotreal"):
        lint_body(src)


def test_lint_collapses_multi_line_svg_open():
    src = (
        '<svg viewBox="0 0 100 100"\n'
        '     xmlns="http://www.w3.org/2000/svg"\n'
        '     role="img">\n'
        '  <title>x</title>\n'
        '</svg>'
    )
    fixed, fixes = lint_body(src)
    first_line = fixed.split("\n", 1)[0]
    assert first_line == '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" role="img">'
    assert any(f.kind == "multi-line-svg-open" and f.count == 1 for f in fixes)


def test_lint_leaves_single_line_svg_open_alone():
    src = '<svg viewBox="0 0 100 100" xmlns="..." role="img"><title>x</title></svg>'
    fixed, fixes = lint_body(src)
    assert fixed == src
    assert all(f.kind != "multi-line-svg-open" for f in fixes)


def test_lint_collapses_only_svg_tag_not_other_multi_line_tags():
    # <text> spanning lines is FINE — common in SVG body. We only care about <svg> opens.
    src = (
        '<svg viewBox="0 0 100 100" xmlns="..." role="img">\n'
        '  <text x="10" y="20"\n'
        '        font-size="13">hello</text>\n'
        '</svg>'
    )
    fixed, _ = lint_body(src)
    # The multi-line <text> should be unchanged; the <svg> open is already on one line.
    assert "<text x=\"10\" y=\"20\"\n        font-size=\"13\">" in fixed


def test_lint_strips_blank_lines_inside_svg():
    src = (
        '<svg>\n'
        '  <title>t</title>\n'
        '\n'
        '  <text>line a</text>\n'
        '\n'
        '  <text>line b</text>\n'
        '</svg>'
    )
    fixed, fixes = lint_body(src)
    inside = fixed[fixed.index("<svg>"):fixed.index("</svg>")]
    assert "\n\n" not in inside
    assert "<text>line a</text>" in fixed and "<text>line b</text>" in fixed
    assert any(f.kind == "blank-line-in-svg" for f in fixes)


def test_lint_preserves_blank_lines_outside_svg():
    src = (
        "Paragraph one.\n"
        "\n"
        "Paragraph two.\n"
        "\n"
        '<svg>\n'
        '  <title>t</title>\n'
        '\n'
        '  <text>x</text>\n'
        '</svg>\n'
        "\n"
        "Paragraph three.\n"
    )
    fixed, _ = lint_body(src)
    assert "Paragraph one.\n\nParagraph two." in fixed
    assert "</svg>\n\nParagraph three." in fixed


def test_lint_preserves_indentation_in_svg():
    src = (
        '<svg>\n'
        '  <title>t</title>\n'
        '\n'
        '  <text>indented body</text>\n'
        '</svg>'
    )
    fixed, _ = lint_body(src)
    assert "  <text>indented body</text>" in fixed
