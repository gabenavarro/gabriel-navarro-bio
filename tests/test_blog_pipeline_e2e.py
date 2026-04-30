"""End-to-end tests: real posts through the full pipeline (lint → render → validate).

Uses real files in assets/blogs/ as fixtures. These tests run BEFORE BigQuery
is touched — they exercise pure-Python pipeline only.
"""
from pathlib import Path

from src.services.blog_lint import lint_body
from src.services.blog_render import render_to_html, validate_html


def _full_pipeline(md_path: Path) -> tuple[str, list]:
    """Run a markdown file through lint → render → validate.

    Returns (rendered_html, validation_issues). Does not write to disk.
    """
    src = md_path.read_text(encoding="utf-8")
    fixed, _ = lint_body(src)
    html = render_to_html(fixed)
    return html, validate_html(html)


def test_e2e_post_0020_renders_clean():
    """Control: a prose-heavy post with a few SVGs renders with no issues."""
    html, issues = _full_pipeline(Path("assets/blogs/0020-fm-purturb.md"))
    assert issues == [], f"Issues found: {[i.kind for i in issues]}"
    assert len(html) > 1000  # sanity: didn't render to nothing


def test_e2e_post_0022_renders_clean():
    """Canary: post 0022 originally had 33 mistletoe foot-gun sites; must be clean now."""
    html, issues = _full_pipeline(Path("assets/blogs/0022-spike-sparse-sink-anatomy-massive.md"))
    assert issues == [], f"Issues found: {[i.kind for i in issues]}"
    # Spot-check that the SVGs survived.
    assert html.count("<svg") >= 10


def test_e2e_post_0001_renders_clean():
    """Old prose-only post (no SVG) should still pass through cleanly."""
    html, issues = _full_pipeline(Path("assets/blogs/0001-fastp.md"))
    assert issues == [], f"Issues found: {[i.kind for i in issues]}"


def test_e2e_lint_is_idempotent_against_real_posts():
    """Running lint twice on every real post produces identical output."""
    for md_path in sorted(Path("assets/blogs").glob("*.md")):
        src = md_path.read_text(encoding="utf-8")
        once, _ = lint_body(src)
        twice, _ = lint_body(once)
        assert once == twice, f"lint is not idempotent on {md_path.name}"
