"""Tests for `ProjectService` (BigQuery is mocked via the `mock_bq` fixture)."""

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


def test_get_all_projects_filters_disabled_posts(mock_bq):
    """`disabled=True` rows should be filtered out via SQL `WHERE disabled = false`.

    The mock inspects the emitted SQL and applies the same filter the real
    BigQuery engine would, so this is an end-to-end behavioral check that the
    service produces the right query.
    """
    all_rows = [
        {"id": "1", "title": "Live A", "disabled": False},
        {"id": "2", "title": "Hidden", "disabled": True},
        {"id": "3", "title": "Live B", "disabled": False},
    ]

    def fake_query(sql, params=None):
        if "disabled = false" in sql:
            return [r for r in all_rows if not r.get("disabled", False)]
        return all_rows

    mock_bq.query.side_effect = fake_query

    service = ProjectService()
    result = service.get_all_projects()

    assert len(result) == 2
    assert all(not p.disabled for p in result)
    titles = {p.title for p in result}
    assert titles == {"Live A", "Live B"}


def test_get_all_projects_with_include_disabled_returns_all(mock_bq):
    """`include_disabled=True` should bypass the SQL filter and return everything."""
    all_rows = [
        {"id": "1", "title": "Live A", "disabled": False},
        {"id": "2", "title": "Hidden", "disabled": True},
        {"id": "3", "title": "Live B", "disabled": False},
    ]

    def fake_query(sql, params=None):
        if "disabled = false" in sql:
            return [r for r in all_rows if not r.get("disabled", False)]
        return all_rows

    mock_bq.query.side_effect = fake_query

    service = ProjectService()
    result = service.get_all_projects(include_disabled=True)

    assert len(result) == 3
    titles = {p.title for p in result}
    assert titles == {"Live A", "Hidden", "Live B"}


def test_get_project_by_id_returns_none_for_unknown_id(mock_bq):
    """When BigQuery returns no rows, the lookup should yield `None`."""
    mock_bq.query.return_value = []

    service = ProjectService()
    result = service.get_project_by_id("does-not-exist")

    assert result is None


def test_get_all_projects_orders_by_date_desc_in_sql(mock_bq):
    """SQL emitted by get_all_projects includes ORDER BY date DESC."""
    mock_bq.query.return_value = []
    ProjectService().get_all_projects()
    # Inspect what was passed to mock_bq.query
    call = mock_bq.query.call_args
    sql = call.kwargs.get("sql") or call.args[0]
    assert "order by date desc" in sql.lower()


def test_get_projects_by_tag_orders_by_date_desc_in_sql(mock_bq):
    """get_projects_by_tag also emits ORDER BY date DESC."""
    mock_bq.query.return_value = []
    ProjectService().get_projects_by_tag("genomics")
    call = mock_bq.query.call_args
    sql = call.kwargs.get("sql") or call.args[0]
    assert "order by date desc" in sql.lower()


def test_from_dict_computes_slug_from_title_when_missing(mock_bq):
    """Project.from_dict computes slug from title if BQ row lacks slug."""
    p = Project.from_dict(
        {
            "id": "x",
            "title": "Speeding Up FASTQ Preprocessing with FastP",
            "description": "",
            "image": "",
            "tags": [],
            "disabled": False,
            "views": 0,
            "likes": 0,
            "date": "2025-01-01T00:00:00Z",
            "body": "",
        }
    )
    assert p.slug == "speeding-up-fastq-preprocessing-with-fastp"


def test_get_project_by_slug_returns_matching_project(mock_bq):
    """get_project_by_slug scans all projects and returns the match (or None)."""
    mock_bq.query.return_value = [
        {
            "id": "1",
            "title": "Hello World",
            "description": "",
            "image": "",
            "tags": [],
            "disabled": False,
            "views": 0,
            "likes": 0,
            "date": "2025-01-01T00:00:00Z",
            "body": "",
            "slug": "",
        },
        {
            "id": "2",
            "title": "Another Post",
            "description": "",
            "image": "",
            "tags": [],
            "disabled": False,
            "views": 0,
            "likes": 0,
            "date": "2025-01-01T00:00:00Z",
            "body": "",
            "slug": "",
        },
    ]
    service = ProjectService()
    found = service.get_project_by_slug("hello-world")
    assert found is not None
    assert found.id == "1"
    assert service.get_project_by_slug("does-not-exist") is None
