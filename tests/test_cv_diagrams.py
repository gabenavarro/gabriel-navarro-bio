"""Tests for CV experience SVG diagrams."""

import re

import pytest
from fasthtml.common import to_xml

from src.features.cv.diagrams import (
    COMPANY_DIAGRAMS,
    diagram_for,
    forager_bg,
    genome_lm_bg,
    lcms_bg,
    multiomics_bg,
    qc_bg,
)


@pytest.mark.parametrize("fn", [genome_lm_bg, multiomics_bg, lcms_bg, forager_bg, qc_bg])
def test_diagram_fn_returns_svg_with_title_and_desc(fn):
    """Each diagram returns an SVG with non-empty <title> and <desc> for a11y."""
    html = to_xml(fn())
    assert "<svg" in html
    assert "viewBox" in html
    assert "<title>" in html
    assert "</title>" in html
    # Title must be non-empty.
    title_match = re.search(r"<title>(.*?)</title>", html)
    assert title_match and title_match.group(1).strip()
    assert "<desc>" in html


def test_diagram_for_known_company_returns_svg():
    html = to_xml(diagram_for("Triplebar"))
    assert "<svg" in html


def test_diagram_for_unknown_company_returns_none():
    assert diagram_for("Some Company That Doesnt Exist") is None


def test_company_diagrams_covers_all_five_roles():
    expected = {
        "Triplebar",
        "Amyris",
        "Hexagon Bio",
        "Brightseed",
        "Mondelez International",
    }
    assert set(COMPANY_DIAGRAMS.keys()) == expected
