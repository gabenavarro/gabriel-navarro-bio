"""Tests that the blog detail page reads body_html in preference to body."""
from src.models.project import Project


def test_blog_detail_uses_body_html_when_present():
    """Renderer prefers body_html when populated."""
    from src.features.projects import projects_page

    project = Project(
        id="x", blog_id="x", title="T", description="d", image="i",
        body="# markdown", body_html="<h1>html-rendered</h1>",
    )
    out = projects_page._render_blog_detail(project)
    rendered = str(out)
    assert "html-rendered" in rendered
    assert "# markdown" not in rendered  # markdown text not exposed raw


def test_blog_detail_falls_back_to_body_when_html_missing():
    """Renderer falls back to render_md(body) when body_html is empty."""
    from src.features.projects import projects_page

    project = Project(
        id="x", blog_id="x", title="T", description="d", image="i",
        body="# markdown", body_html="",
    )
    out = projects_page._render_blog_detail(project)
    rendered = str(out)
    # render_md should have produced an <h1> from the markdown.
    assert "<h1" in rendered
