"""Accessibility regression tests."""

import re
from unittest.mock import patch

from fasthtml.common import to_xml
from src.features.hero import HERO_PAGE
from src.features.cv import CV_PAGE


def _img_tags_without_alt(html: str) -> list[str]:
    """Return all <img ...> tags in html that lack an alt= attribute."""
    imgs = re.findall(r"<img[^>]*>", html)
    return [tag for tag in imgs if "alt=" not in tag]


def test_hero_page_has_no_img_without_alt():
    html = to_xml(HERO_PAGE)
    missing = _img_tags_without_alt(html)
    assert not missing, f"<img> tags missing alt in HERO_PAGE: {missing}"


def test_cv_page_has_no_img_without_alt():
    html = to_xml(CV_PAGE)
    missing = _img_tags_without_alt(html)
    assert not missing, f"<img> tags missing alt in CV_PAGE: {missing}"


@patch("src.features.projects.projects_page.ProjectService")
def test_blogs_index_has_no_img_without_alt(mock_service_cls):
    from src.features.projects.projects_page import create_masonry_page
    from src.models.project import Project

    mock_service = mock_service_cls.return_value
    mock_service.get_all_projects.return_value = [
        Project.from_dict(
            {
                "id": "p1",
                "title": "Test post",
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
    ]
    html = to_xml(create_masonry_page())
    missing = _img_tags_without_alt(html)
    assert not missing, f"<img> tags missing alt in /blogs: {missing}"


def test_navigation_has_aria_label():
    from src.components.layout.navigation import navigation

    html = to_xml(navigation())
    assert 'aria-label="Primary navigation"' in html or "aria-label='Primary navigation'" in html
