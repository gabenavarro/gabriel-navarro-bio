"""Tests for the Project dataclass and its `from_dict` classmethod."""

from src.models.project import Project


def test_from_dict_parses_bigquery_array_tag_shape():
    """BigQuery returns array-typed columns as `[{'v': value}, ...]`."""
    data = {
        "id": "p1",
        "title": "BQ tags",
        "tags": [{"v": "omics"}, {"v": "machine-learning"}],
    }

    project = Project.from_dict(data)

    assert project.tags == ["omics", "machine-learning"]
    assert project.id == "p1"
    assert project.title == "BQ tags"


def test_from_dict_parses_plain_string_tag_list():
    """Plain `["tag1", "tag2"]` should also be accepted (used in tests/fixtures)."""
    data = {"id": "p2", "tags": ["genomics", "cloud"]}

    project = Project.from_dict(data)

    assert project.tags == ["genomics", "cloud"]


def test_from_dict_falls_back_to_defaults_for_missing_fields():
    """An empty dict should produce a valid Project with all defaults."""
    project = Project.from_dict({})

    assert project.id == ""
    assert project.blog_id == ""
    assert project.title == ""
    assert project.description == ""
    assert project.image == ""
    assert project.tags == []
    assert project.disabled is False
    assert project.views == 0
    assert project.likes == 0
    assert project.date == ""
    assert project.body == ""


def test_project_from_dict_reads_body_html():
    data = {
        "id": "x",
        "title": "T",
        "description": "d",
        "image": "https://e.com/i.svg",
        "tags": ["t"],
        "disabled": False,
        "views": 0,
        "likes": 0,
        "date": "2026-01-01T00:00:00Z",
        "body": "# md",
        "body_html": "<h1>md</h1>",
    }
    p = Project.from_dict(data)
    assert p.body_html == "<h1>md</h1>"
    assert p.body == "# md"  # transitional: both fields populated


def test_project_from_dict_defaults_body_html_to_empty_string():
    """A row that doesn't have body_html (legacy/transitional) yields an empty string."""
    data = {"id": "x", "title": "T", "description": "d", "image": "i", "body": "md"}
    p = Project.from_dict(data)
    assert p.body_html == ""
