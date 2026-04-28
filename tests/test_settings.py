"""Tests for src.config.settings."""

from src.config.settings import Settings, category_class


def test_google_project_id_overridden_by_env_var(monkeypatch):
    """Settings() reads GOOGLE_PROJECT_ID from the environment when set."""
    monkeypatch.setenv("GOOGLE_PROJECT_ID", "test-proj-google")
    assert Settings().GOOGLE_PROJECT_ID == "test-proj-google"


def test_bigquery_table_overridden_by_env_var(monkeypatch):
    """Settings() reads BIGQUERY_TABLE from the environment when set."""
    monkeypatch.setenv("BIGQUERY_TABLE", "alt-project.alt-dataset.alt-table")
    assert Settings().BIGQUERY_TABLE == "alt-project.alt-dataset.alt-table"


def test_category_class_maps_known_tags():
    """Known tags map to their cat-* class; unknown falls back to cat-neutral."""
    assert category_class("omics") == "cat-omics"
    assert category_class("genomics") == "cat-omics"
    assert category_class("Machine-Learning") == "cat-ml"  # case-insensitive
    assert category_class("docker") == "cat-infra"
    assert category_class("totally-unknown-tag") == "cat-neutral"
