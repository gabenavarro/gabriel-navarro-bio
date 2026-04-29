"""Tests for the RSS feed at /feed.xml."""

from src.features.feed.rss import build_rss_feed
from src.models.project import Project


def _make_project(idx: int, **overrides) -> Project:
    base = {
        "id": f"id-{idx}",
        "title": f"Post {idx}",
        "description": f"Description {idx}",
        "image": "",
        "tags": ["genomics", "bioinformatics"],
        "disabled": False,
        "views": 0,
        "likes": 0,
        "date": f"2025-04-{20 + idx:02d}T00:00:00Z",
        "body": "",
    }
    base.update(overrides)
    return Project.from_dict(base)


def test_build_rss_feed_emits_rss20_with_items_for_each_project():
    """build_rss_feed produces valid RSS 2.0 with one <item> per project."""
    projects = [_make_project(i) for i in range(3)]
    xml = build_rss_feed(projects)

    # RSS 2.0 envelope
    assert '<?xml version="1.0" encoding="UTF-8"?>' in xml
    assert '<rss version="2.0"' in xml
    assert "<channel>" in xml
    # 3 items
    assert xml.count("<item>") == 3
    # Categories rendered per tag
    assert "<category>genomics</category>" in xml
    assert "<category>bioinformatics</category>" in xml
    # Slug-based links (since slug auto-computed from title in from_dict)
    for i in range(3):
        assert f"/blogs/slug/post-{i}" in xml
    # Each item has its title CDATA-wrapped
    for i in range(3):
        assert f"<![CDATA[Post {i}]]>" in xml
    # GUID is the UUID, not perma
    assert '<guid isPermaLink="false">id-0</guid>' in xml


def test_build_rss_feed_caps_at_50_items():
    """Even when given more, only 50 items appear."""
    projects = [_make_project(i) for i in range(75)]
    xml = build_rss_feed(projects)
    assert xml.count("<item>") == 50
