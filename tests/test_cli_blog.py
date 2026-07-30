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
        '@{title = "T"\n'
        '  date = "2026-01-01T00:00:00Z"\n'
        '  tags = ["x"]\n'
        "  views = 0\n"
        "  likes = 0\n"
        '  image = "https://e.com/i.svg"\n'
        '  description = "d"\n'
        '  type = "note"\n'
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
        '@{title = "T"\n'
        '  date = "2026-01-01T00:00:00Z"\n'
        '  tags = ["x"]\n'
        "  views = 0\n"
        "  likes = 0\n"
        '  image = "https://e.com/i.svg"\n'
        '  description = "d"\n'
        '  type = "note"\n'
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
        '@{title = "T"\n'
        '  date = "2026-01-01T00:00:00Z"\n'
        '  tags = ["x"]\n'
        "  views = 0\n"
        "  likes = 0\n"
        '  image = "https://e.com/i.svg"\n'
        '  description = "d"\n'
        '  type = "note"\n'
        "  disabled = false\n"
        "}\n"
        "# Body\n"
        '<svg viewBox="0 0 100 100"><text>x</text></svg>\n',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="validate_html"):
        _payload_from_blog(md)


def test_validate_reports_lint_issues_without_writing(tmp_path, capsys):
    """`blog validate` reports lint issues but does NOT write the file."""
    from src.cli.__main__ import main

    md = tmp_path / "post.md"
    raw = (
        '@{id = "00000000-0000-0000-0000-000000000000"\n'
        '  title = "T"\n'
        '  date = "2026-01-01T00:00:00Z"\n'
        '  tags = ["x"]\n'
        "  views = 0\n"
        "  likes = 0\n"
        '  image = "https://e.com/i.svg"\n'
        '  description = "d"\n'
        '  type = "note"\n'
        "  disabled = false\n"
        "}\n"
        "# B\n"
        '<svg viewBox="0 0 1 1" xmlns="..." role="img">\n'
        "  <title>x &mdash; y</title>\n"
        "</svg>\n"
    )
    md.write_text(raw, encoding="utf-8")
    rc = main(["blog", "validate", str(md)])
    assert rc == 0
    after = md.read_text(encoding="utf-8")
    # File must be unchanged.
    assert after == raw
    captured = capsys.readouterr()
    # Validate should report what lint WOULD do.
    assert "lint" in captured.out.lower() or "would" in captured.out.lower()


def test_validate_exits_nonzero_on_validation_issue(tmp_path):
    """`blog validate` exits nonzero when validate_html finds an issue."""
    from src.cli.__main__ import main

    md = tmp_path / "post.md"
    md.write_text(
        '@{id = "00000000-0000-0000-0000-000000000000"\n'
        '  title = "T"\n'
        '  date = "2026-01-01T00:00:00Z"\n'
        '  tags = ["x"]\n'
        "  views = 0\n"
        "  likes = 0\n"
        '  image = "https://e.com/i.svg"\n'
        '  description = "d"\n'
        '  type = "note"\n'
        "  disabled = false\n"
        "}\n"
        '# B\n<svg viewBox="0 0 1 1"><text>missing title and role</text></svg>\n',
        encoding="utf-8",
    )
    rc = main(["blog", "validate", str(md)])
    assert rc == 1


# ---------------------------------------------------------------------------
# disable / enable
# ---------------------------------------------------------------------------
#
# These two do reach BigQuery, but the client is stubbed at the _bq_client
# boundary, so no credentials are needed. What matters is the emitted SQL:
# `enable` must be the exact inverse of `disable` and must be a single atomic
# UPDATE, never a delete-then-insert.


class _FakeQueryJob:
    def result(self):
        return None


class _FakeClient:
    def __init__(self):
        self.calls: list[tuple[str, object]] = []

    def query(self, sql, job_config=None):
        self.calls.append((sql, job_config))
        return _FakeQueryJob()


def _params(job_config) -> dict[str, object]:
    return {p.name: p.value for p in job_config.query_parameters}


@pytest.fixture
def fake_bq(monkeypatch):
    """Stub src.cli.blog._bq_client and hand back the fake client."""
    from src.cli import blog

    client = _FakeClient()
    monkeypatch.setattr(blog, "_bq_client", lambda: client)
    return client


@pytest.mark.parametrize(
    ("subcommand", "expected"),
    [("disable", True), ("enable", False)],
)
def test_disable_and_enable_issue_one_atomic_update(fake_bq, capsys, subcommand, expected):
    rc = main(["blog", subcommand, "abc-123"])
    assert rc == 0

    assert len(fake_bq.calls) == 1, "must be a single statement, not delete-then-insert"
    sql, job_config = fake_bq.calls[0]

    assert sql.startswith("UPDATE ")
    assert "SET disabled = @disabled" in sql
    assert "WHERE id = @id" in sql
    assert "DELETE" not in sql.upper()

    assert _params(job_config) == {"id": "abc-123", "disabled": expected}

    captured = capsys.readouterr()
    assert f"{subcommand}d abc-123" in captured.out


def test_enable_is_the_exact_inverse_of_disable(fake_bq):
    """The two subcommands must differ only in the boolean they bind."""
    main(["blog", "disable", "x"])
    main(["blog", "enable", "x"])

    disable_sql, disable_cfg = fake_bq.calls[0]
    enable_sql, enable_cfg = fake_bq.calls[1]

    assert disable_sql == enable_sql
    assert _params(disable_cfg)["disabled"] is True
    assert _params(enable_cfg)["disabled"] is False


def test_enable_honours_table_override(fake_bq):
    rc = main(["blog", "enable", "abc-123", "--table", "proj.ds.other"])
    assert rc == 0
    sql, _ = fake_bq.calls[0]
    assert "`proj.ds.other`" in sql
