"""Tests for scripts.backfill_blog_html."""


def test_iter_blog_paths_returns_sorted_md_files(tmp_path):
    from scripts.backfill_blog_html import iter_blog_paths

    (tmp_path / "0003-c.md").write_text("@{}\n", encoding="utf-8")
    (tmp_path / "0001-a.md").write_text("@{}\n", encoding="utf-8")
    (tmp_path / "0002-b.md").write_text("@{}\n", encoding="utf-8")
    (tmp_path / "skip.txt").write_text("not md", encoding="utf-8")

    paths = iter_blog_paths(tmp_path)
    names = [p.name for p in paths]
    assert names == ["0001-a.md", "0002-b.md", "0003-c.md"]


def test_dry_run_does_not_call_submit(tmp_path, monkeypatch, capsys):
    """In --dry-run mode, the script previews each file without invoking BigQuery."""
    from scripts.backfill_blog_html import run_backfill
    from src.cli import blog as blog_module

    submit_calls: list[str] = []
    monkeypatch.setattr(
        blog_module, "_cmd_submit", lambda args: submit_calls.append(str(args.path)) or 0
    )

    # Stub out _payload_from_blog so we don't need real Pydantic frontmatter.
    def fake_payload(path):
        return {"id": "x", "body": path.read_text(), "body_html": "<p>html</p>"}

    monkeypatch.setattr(blog_module, "_payload_from_blog", fake_payload)

    blogs = tmp_path / "blogs"
    blogs.mkdir()
    (blogs / "0001-a.md").write_text("@{}\nbody", encoding="utf-8")

    rc = run_backfill(blogs, dry_run=True)
    assert rc == 0
    assert submit_calls == []  # nothing pushed
    captured = capsys.readouterr()
    assert "0001-a.md" in captured.out


def test_classify_streaming_buffer_error_recognizes_known_message():
    from scripts.backfill_blog_html import is_streaming_buffer_error

    class MockExc(Exception):
        pass

    err = MockExc(
        "UPDATE or DELETE statement over table ... would affect rows in the "
        "streaming buffer, which is not supported"
    )
    assert is_streaming_buffer_error(err)
    assert not is_streaming_buffer_error(MockExc("permission denied"))
