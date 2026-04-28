"""Tests for src.config.settings."""

from src.config.settings import Settings


def test_google_project_id_overridden_by_env_var(monkeypatch):
    """Settings() reads GOOGLE_PROJECT_ID from the environment when set."""
    monkeypatch.setenv("GOOGLE_PROJECT_ID", "test-proj-google")
    assert Settings().GOOGLE_PROJECT_ID == "test-proj-google"


def test_bigquery_table_overridden_by_env_var(monkeypatch):
    """Settings() reads BIGQUERY_TABLE from the environment when set."""
    monkeypatch.setenv("BIGQUERY_TABLE", "alt-project.alt-dataset.alt-table")
    assert Settings().BIGQUERY_TABLE == "alt-project.alt-dataset.alt-table"
