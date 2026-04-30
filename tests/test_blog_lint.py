"""Tests for src.services.blog_lint."""
from src.services.blog_lint import LintError, LintFix, lint_body


def test_lint_body_returns_tuple_of_text_and_fixes():
    text = "no svg here, just prose"
    fixed, fixes = lint_body(text)
    assert fixed == text
    assert fixes == []
