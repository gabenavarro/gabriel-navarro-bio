"""Tests for src.config.settings."""

import importlib
import sys


def test_google_project_id_overridden_by_env_var(monkeypatch):
    """GOOGLE_PROJECT_ID should be read from the environment when set."""
    monkeypatch.setenv("GOOGLE_PROJECT_ID", "test-proj")

    # The package __init__ shadows the submodule attribute with the singleton,
    # so grab the module directly out of sys.modules to reload it.
    import src.config.settings  # noqa: F401  (ensure it's in sys.modules)
    settings_module = sys.modules["src.config.settings"]

    reloaded = importlib.reload(settings_module)

    assert reloaded.settings.GOOGLE_PROJECT_ID == "test-proj"
