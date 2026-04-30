"""Smoke tests for src.cli.blog (validate path only — no BigQuery).

Tests for ``submit``/``update``/``disable``/``list`` are intentionally
omitted: they require GCP credentials and would fail in CI. The CLI
plumbing (argparse, dispatch, exit codes) is exercised through the
``validate`` subcommand.
"""

import pytest

from src.cli.__main__ import main


def test_blog_validate_exits_zero_on_valid_file(capsys):
    rc = main(["blog", "validate", "assets/blogs/0001-fastp.md"])
    assert rc == 0
    captured = capsys.readouterr()
    assert "OK" in captured.out
    assert "Speeding Up FASTQ Preprocessing with FastP" in captured.out


def test_blog_validate_exits_nonzero_on_missing_file(tmp_path, capsys):
    bad = tmp_path / "nonexistent.md"
    rc = main(["blog", "validate", str(bad)])
    assert rc == 1
    captured = capsys.readouterr()
    assert "INVALID" in captured.err


def test_blog_validate_exits_nonzero_on_invalid_frontmatter(tmp_path, capsys):
    bad = tmp_path / "bad.md"
    bad.write_text("not a frontmatter\nbody")
    rc = main(["blog", "validate", str(bad)])
    assert rc == 1
    captured = capsys.readouterr()
    assert "INVALID" in captured.err


def test_payload_from_blog_includes_body_html(tmp_path):
    """_payload_from_blog returns a dict with both `body` (markdown) and
    `body_html` (rendered)."""
    from src.cli.blog import _payload_from_blog
    md = tmp_path / "post.md"
    md.write_text(
        "@{title = \"T\"\n"
        "  date = \"2026-01-01T00:00:00Z\"\n"
        "  tags = [\"x\"]\n"
        "  views = 0\n"
        "  likes = 0\n"
        "  image = \"https://e.com/i.svg\"\n"
        "  description = \"d\"\n"
        "  type = \"note\"\n"
        "  disabled = false\n"
        "}\n"
        "# Body\n",
        encoding="utf-8",
    )
    payload = _payload_from_blog(md)
    assert "body" in payload
    assert "body_html" in payload
    assert "<h1" in payload["body_html"]


def test_payload_from_blog_persists_lint_fixes_to_disk(tmp_path, capsys):
    """If lint changes the body, the .md file is overwritten with the linted text."""
    from src.cli.blog import _payload_from_blog
    md = tmp_path / "post.md"
    raw = (
        "@{title = \"T\"\n"
        "  date = \"2026-01-01T00:00:00Z\"\n"
        "  tags = [\"x\"]\n"
        "  views = 0\n"
        "  likes = 0\n"
        "  image = \"https://e.com/i.svg\"\n"
        "  description = \"d\"\n"
        "  type = \"note\"\n"
        "  disabled = false\n"
        "}\n"
        "# Body\n"
        '<svg viewBox="0 0 100 100" xmlns="..." role="img">\n'
        "  <title>x &mdash; y</title>\n"
        "  <text>z</text>\n"
        "</svg>\n"
    )
    md.write_text(raw, encoding="utf-8")
    _payload_from_blog(md)
    after = md.read_text(encoding="utf-8")
    assert "&mdash;" not in after
    assert "—" in after
    captured = capsys.readouterr()
    assert "[lint]" in captured.out


def test_payload_from_blog_raises_on_validation_failure(tmp_path):
    """If validate_html finds an issue, _payload_from_blog raises."""
    from src.cli.blog import _payload_from_blog
    md = tmp_path / "post.md"
    # Body contains an SVG with no <title> and no role="img" — both will fail validation.
    md.write_text(
        "@{title = \"T\"\n"
        "  date = \"2026-01-01T00:00:00Z\"\n"
        "  tags = [\"x\"]\n"
        "  views = 0\n"
        "  likes = 0\n"
        "  image = \"https://e.com/i.svg\"\n"
        "  description = \"d\"\n"
        "  type = \"note\"\n"
        "  disabled = false\n"
        "}\n"
        "# Body\n"
        "<svg viewBox=\"0 0 100 100\"><text>x</text></svg>\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="validate_html"):
        _payload_from_blog(md)
