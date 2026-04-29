"""Tests for OG/Twitter meta tags on blog detail pages."""

from unittest.mock import patch

from fasthtml.common import to_xml
from src.features.projects.projects_page import create_blog_page
from src.models.project import Project


@patch("src.features.projects.projects_page.ProjectService")
def test_blog_detail_emits_og_image_matching_project(mock_service_cls):
    """create_blog_page renders <meta property=og:image> matching the project's image URL."""
    mock_service = mock_service_cls.return_value
    img_url = "https://storage.googleapis.com/gn-portfolio/images/fastp-thumb.svg"
    mock_service.get_project_by_id.return_value = Project.from_dict(
        {
            "id": "abc",
            "title": "FastP",
            "description": "An ultra-fast tool",
            "image": img_url,
            "tags": ["genomics"],
            "disabled": False,
            "views": 0,
            "likes": 0,
            "date": "2025-04-26T00:00:00Z",
            "body": "Body text",
        }
    )

    html = to_xml(create_blog_page("abc"))

    assert 'property="og:image"' in html
    assert img_url in html
    assert 'property="og:title"' in html
    assert "FastP" in html
    assert 'property="og:description"' in html
    assert 'name="twitter:card"' in html
    assert 'rel="canonical"' in html
    # Slug-based canonical URL since the project has a slug (computed from title)
    assert "/blogs/slug/" in html
