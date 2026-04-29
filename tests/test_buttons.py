"""Tests for src.components.base.buttons."""

from fasthtml.common import to_xml

from src.components.base.buttons import button_ghost, button_outline, button_primary


def test_button_primary_with_href_renders_anchor_with_class():
    html = to_xml(button_primary("Sign in", href="/login"))
    assert "factory-btn" in html
    assert "factory-btn-primary" in html
    assert 'href="/login"' in html
    assert "Sign in" in html


def test_button_ghost_without_href_renders_button_element():
    html = to_xml(button_ghost("Cancel"))
    assert "factory-btn-ghost" in html
    # No href since none was passed
    assert "href=" not in html


def test_button_outline_with_extra_cls_appended():
    html = to_xml(button_outline("Read", href="/read", cls="extra-class"))
    assert "factory-btn-outline" in html
    assert "extra-class" in html
