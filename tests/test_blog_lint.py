"""Tests for src.services.blog_lint."""
import pytest

from src.services.blog_lint import LintError, LintFix, lint_body


def test_module_exports_public_surface():
    """The module exports `LintError`, `LintFix`, `lint_body` as the public API."""
    # LintError is an Exception subclass; raising and catching it works.
    with pytest.raises(LintError):
        raise LintError("test")
    # LintFix is a dataclass with the documented fields and Literal constraint.
    fix = LintFix(kind="named-entity", count=1, detail="example")
    assert fix.kind == "named-entity"
    assert fix.count == 1
    assert fix.detail == "example"


def test_lint_body_returns_tuple_of_text_and_fixes():
    text = "no svg here, just prose"
    fixed, fixes = lint_body(text)
    assert fixed == text
    assert fixes == []
