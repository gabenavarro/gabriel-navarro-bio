"""Tests for `ProjectService` (BigQuery is mocked via the `mock_bq` fixture)."""

import pytest

from src.models.project import Project
from src.services.projects import ProjectService


def test_get_all_projects_returns_list_of_projects(mock_bq):
    """Multiple BigQuery rows should be wrapped in `Project` instances."""
    mock_bq.query.return_value = [
        {"id": "1", "title": "First", "tags": ["a"]},
        {"id": "2", "title": "Second", "tags": [{"v": "b"}]},
    ]

    service = ProjectService()
    result = service.get_all_projects()

    assert len(result) == 2
    assert all(isinstance(p, Project) for p in result)
    assert result[0].title == "First"
    assert result[1].tags == ["b"]


def test_get_all_projects_wraps_single_row_dict_in_list(mock_bq):
    """If BigQuery returns a single-row dict (not a list), it gets wrapped."""
    mock_bq.query.return_value = {"id": "solo", "title": "Lonely"}

    service = ProjectService()
    result = service.get_all_projects()

    assert len(result) == 1
    assert isinstance(result[0], Project)
    assert result[0].id == "solo"


@pytest.mark.xfail(reason="D4 implements disabled-filter; currently expected to fail")
def test_get_all_projects_filters_disabled_posts(mock_bq):
    """`disabled=True` rows should be filtered out (D4 will implement)."""
    mock_bq.query.return_value = [
        {"id": "1", "title": "Live A", "disabled": False},
        {"id": "2", "title": "Hidden", "disabled": True},
        {"id": "3", "title": "Live B", "disabled": False},
    ]

    service = ProjectService()
    result = service.get_all_projects()

    assert len(result) == 2
    assert all(not p.disabled for p in result)
    titles = {p.title for p in result}
    assert titles == {"Live A", "Live B"}


def test_get_project_by_id_returns_none_for_unknown_id(mock_bq):
    """When BigQuery returns no rows, the lookup should yield `None`."""
    mock_bq.query.return_value = []

    service = ProjectService()
    result = service.get_project_by_id("does-not-exist")

    assert result is None
