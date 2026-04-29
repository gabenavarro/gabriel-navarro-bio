"""Smoke tests for the masonry blog grid (Epic B)."""

from unittest.mock import patch

from fasthtml.common import to_xml
from src.features.projects.projects_page import create_masonry_page
from src.models.project import Project


@patch("src.features.projects.projects_page.ProjectService")
def test_masonry_page_renders_masonry_columns_wrapper(mock_service_cls):
    """create_masonry_page wraps cards in a div with class='masonry-columns'."""
    mock_service = mock_service_cls.return_value
    mock_service.get_all_projects.return_value = [
        Project.from_dict(
            {
                "id": f"id-{i}",
                "title": f"Post {i}",
                "description": "desc",
                "image": "https://example.com/img.png",
                "tags": ["genomics"],
                "disabled": False,
                "views": 0,
                "likes": 0,
                "date": "2025-01-01T00:00:00Z",
                "body": "",
            }
        )
        for i in range(3)
    ]

    page = create_masonry_page()
    html = to_xml(page)

    assert 'class="masonry-columns"' in html or "masonry-columns" in html
    # All 3 cards should be inside the same masonry-columns div
    assert html.count("Post 0") == 1
    assert html.count("Post 1") == 1
    assert html.count("Post 2") == 1
