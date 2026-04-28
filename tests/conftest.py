"""Shared pytest fixtures for the test suite."""

from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_bq(monkeypatch):
    """Replace BigQueryClient inside ProjectService so tests don't hit GCP.

    Returns a MagicMock instance whose `.query.return_value` can be set
    per-test to control what `ProjectService` sees from "BigQuery".
    """
    mock = MagicMock()
    monkeypatch.setattr(
        "src.services.projects.BigQueryClient", lambda *args, **kwargs: mock
    )
    return mock
