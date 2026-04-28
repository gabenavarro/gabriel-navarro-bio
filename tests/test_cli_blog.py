"""Smoke tests for src.cli.blog (validate path only — no BigQuery).

Tests for ``submit``/``update``/``disable``/``list`` are intentionally
omitted: they require GCP credentials and would fail in CI. The CLI
plumbing (argparse, dispatch, exit codes) is exercised through the
``validate`` subcommand.
"""

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
