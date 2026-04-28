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
