"""Tests for src.services.blog_frontmatter."""

from datetime import datetime, timezone

import pytest
import yaml
from pydantic import ValidationError

from src.services.blog_frontmatter import BlogFrontmatter, parse_blog


def test_parses_legacy_at_brace_format():
    """A real legacy `@{...}` post in assets/blogs parses into a BlogFrontmatter."""
    result = parse_blog("assets/blogs/0001-fastp.md")
    assert isinstance(result, BlogFrontmatter)
    assert result.id == "63844571-3f9b-448e-b410-aac83af3f4ee"
    assert result.title == "Speeding Up FASTQ Preprocessing with FastP"
    assert result.tags == ["bioinformatics", "docker", "genomics"]
    assert result.type == "note"
    assert result.disabled is False
    assert result.views == 0
    assert result.likes == 0
    assert result.date == datetime(2025, 4, 26, 0, 0, 0, tzinfo=timezone.utc)
    assert str(result.image).startswith("https://")
    assert result.body.strip().startswith("# Speeding Up FASTQ Preprocessing with FastP")


def test_parses_yaml_frontmatter_format(tmp_path):
    """A standard `---`-delimited YAML frontmatter post parses correctly."""
    md = tmp_path / "post.md"
    md.write_text(
        "---\n"
        'id: "test-id-123"\n'
        'title: "YAML Test Post"\n'
        'date: "2025-04-26T00:00:00Z"\n'
        'tags: ["python", "yaml"]\n'
        'description: "A short description."\n'
        'image: "https://example.com/img.png"\n'
        'type: "article"\n'
        "disabled: false\n"
        "views: 0\n"
        "likes: 0\n"
        "---\n"
        "Body text here.\n",
        encoding="utf-8",
    )
    result = parse_blog(md)
    assert result.id == "test-id-123"
    assert result.title == "YAML Test Post"
    assert result.type == "article"
    assert result.disabled is False
    assert result.tags == ["python", "yaml"]
    assert "Body text here." in result.body


def test_missing_required_field_raises_validation_error(tmp_path):
    """Omitting a required field (e.g. `description`) raises ValidationError."""
    md = tmp_path / "missing.md"
    md.write_text(
        "---\n"
        'id: "x"\n'
        'title: "T"\n'
        'date: "2025-04-26T00:00:00Z"\n'
        'tags: ["a"]\n'
        # description intentionally omitted
        'image: "https://example.com/img.png"\n'
        'type: "note"\n'
        "disabled: false\n"
        "views: 0\n"
        "likes: 0\n"
        "---\n"
        "Body.\n",
        encoding="utf-8",
    )
    with pytest.raises(ValidationError):
        parse_blog(md)


def test_malformed_yaml_raises_with_line_number(tmp_path):
    """A YAML syntax error surfaces a PyYAML error mentioning the line number."""
    md = tmp_path / "bad.md"
    md.write_text(
        '---\ntitle: "unclosed string\nbody\n---\nbody',
        encoding="utf-8",
    )
    with pytest.raises(yaml.YAMLError) as exc_info:
        parse_blog(md)
    assert "line" in str(exc_info.value).lower()


def test_empty_body_raises(tmp_path):
    """A post with an empty/whitespace-only body is rejected."""
    md = tmp_path / "empty_body.md"
    md.write_text(
        "---\n"
        'id: "x"\n'
        'title: "T"\n'
        'date: "2025-04-26T00:00:00Z"\n'
        'tags: ["a"]\n'
        'description: "d"\n'
        'image: "https://example.com/img.png"\n'
        'type: "note"\n'
        "disabled: false\n"
        "views: 0\n"
        "likes: 0\n"
        "---\n"
        "   \n",
        encoding="utf-8",
    )
    with pytest.raises(ValidationError):
        parse_blog(md)
