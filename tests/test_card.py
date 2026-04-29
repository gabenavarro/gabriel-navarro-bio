"""Tests for src.components.base.card."""

from fasthtml.common import to_xml

from src.components.base.card import Card


def test_card_emits_factory_card_class_with_default_padding():
    """Plain Card has factory-card and factory-card-padding-md classes."""
    html = to_xml(Card("body content"))
    assert "factory-card" in html
    assert "factory-card-padding-md" in html
    assert "body content" in html


def test_card_with_href_wraps_in_anchor():
    """Card(href="/x") wraps the card in <a href="/x"> for full-card click."""
    html = to_xml(Card("body", href="/blogs/abc-123"))
    assert '<a href="/blogs/abc-123"' in html
    assert "factory-card" in html


def test_card_interactive_adds_hover_class():
    """Card(interactive=True) carries the factory-card-interactive class for hover styling."""
    html = to_xml(Card("body", interactive=True))
    assert "factory-card-interactive" in html
