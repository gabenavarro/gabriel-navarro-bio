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


def test_project_card_renders_full_description_without_truncation():
    """A long description must render verbatim in the card body for masonry to vary card heights."""
    long_desc = (
        "FastP is an ultra-fast, all-in-one tool for trimming, filtering, and "
        "quality-checking FASTQ files, helping you quickly generate clean, "
        "high-quality datasets for genomics and transcriptomics projects. This "
        "guide walks you through installation, usage, and key features of FastP, "
        "making it an essential part of your NGS workflow."
    )
    project = Project.from_dict(
        {
            "id": "p1",
            "title": "Long",
            "description": long_desc,
            "image": "https://example.com/i.png",
            "tags": ["genomics"],
            "disabled": False,
            "views": 0,
            "likes": 0,
            "date": "2025-01-01T00:00:00Z",
            "body": "",
        }
    )
    from src.features.projects.components import render_project_card

    html = to_xml(render_project_card(0, project))
    # Full description present, end-to-end (the last clause must appear)
    assert "essential part of your NGS workflow" in html
    # And no CSS truncation utility silently slipped in via cls
    assert "line-clamp" not in html
    assert "truncate" not in html
