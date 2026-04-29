"""Per-experience SVG diagrams used as the background of the CV date column.

Each function returns a ``Safe`` raw-SVG string (a ``str`` subclass) so it
can be passed directly to FastHTML containers and is preserved verbatim by
``to_xml`` — this preserves the camelCase ``viewBox`` attribute that the
SVG spec requires (FastHTML's element tree lowercases attribute names).

Conventions followed by every diagram:

- ``viewBox="0 0 200 200"`` and no fixed ``width``/``height`` (CSS sizes them).
- Strokes/fills use ``currentColor`` so a single CSS ``color`` rule themes
  every diagram uniformly (see ``.cv-date-bg`` in ``_components.py``).
- ``stroke-width="1.5"`` reads well at both small and scaled sizes.
- A non-empty ``<title>`` and ``<desc>`` are included for screen readers.
- Markup is intentionally stylized — these are decorative diagrams, not
  technical schematics.
"""

from __future__ import annotations

from collections.abc import Callable

from fasthtml.common import Safe


def genome_lm_bg() -> Safe:
    """Genome LM training: stacked transformer blocks feeding 4 GPU nodes."""
    return Safe(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" '
        'stroke="currentColor" fill="none" stroke-width="1.5">'
        "<title>Genome language model training</title>"
        "<desc>Four stacked transformer blocks on the left feed four GPU "
        "nodes on the right via gradient-sync arrows, with a 2B parameter "
        "callout.</desc>"
        # Four stacked transformer blocks (left column)
        '<rect x="20" y="40" width="60" height="18" rx="2" />'
        '<rect x="20" y="64" width="60" height="18" rx="2" />'
        '<rect x="20" y="88" width="60" height="18" rx="2" />'
        '<rect x="20" y="112" width="60" height="18" rx="2" />'
        # Inner attention dots
        '<circle cx="35" cy="49" r="1.5" fill="currentColor" />'
        '<circle cx="50" cy="49" r="1.5" fill="currentColor" />'
        '<circle cx="65" cy="49" r="1.5" fill="currentColor" />'
        '<circle cx="35" cy="121" r="1.5" fill="currentColor" />'
        '<circle cx="50" cy="121" r="1.5" fill="currentColor" />'
        '<circle cx="65" cy="121" r="1.5" fill="currentColor" />'
        # GPU nodes (right column)
        '<circle cx="160" cy="55" r="9" />'
        '<circle cx="160" cy="85" r="9" />'
        '<circle cx="160" cy="115" r="9" />'
        '<circle cx="160" cy="145" r="9" />'
        # DDP gradient-sync arrows: blocks -> GPU 1, GPU 4 -> blocks
        '<line x1="80" y1="50" x2="148" y2="55" />'
        '<line x1="80" y1="120" x2="148" y2="145" />'
        # Sync ring between GPUs
        '<line x1="160" y1="64" x2="160" y2="76" />'
        '<line x1="160" y1="94" x2="160" y2="106" />'
        '<line x1="160" y1="124" x2="160" y2="136" />'
        # 2B parameter callout
        '<text x="100" y="175" text-anchor="middle" '
        'font-family="monospace" font-size="14" font-weight="700" '
        'fill="currentColor" stroke="none">2B</text>'
        "</svg>"
    )


def multiomics_bg() -> Safe:
    """Three omics lanes converging into a single candidate gene node."""
    return Safe(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" '
        'stroke="currentColor" fill="none" stroke-width="1.5">'
        "<title>Multi-omics integration</title>"
        "<desc>Three horizontal lanes representing genomics, proteomics, "
        "and metabolomics converge into a single candidate gene node on "
        "the right.</desc>"
        # Three horizontal swimlanes (left)
        '<rect x="15" y="55" width="80" height="14" rx="2" />'
        '<rect x="15" y="93" width="80" height="14" rx="2" />'
        '<rect x="15" y="131" width="80" height="14" rx="2" />'
        # Lane sample dots
        '<circle cx="30" cy="62" r="1.8" fill="currentColor" />'
        '<circle cx="55" cy="62" r="1.8" fill="currentColor" />'
        '<circle cx="80" cy="62" r="1.8" fill="currentColor" />'
        '<circle cx="30" cy="100" r="1.8" fill="currentColor" />'
        '<circle cx="55" cy="100" r="1.8" fill="currentColor" />'
        '<circle cx="80" cy="100" r="1.8" fill="currentColor" />'
        '<circle cx="30" cy="138" r="1.8" fill="currentColor" />'
        '<circle cx="55" cy="138" r="1.8" fill="currentColor" />'
        '<circle cx="80" cy="138" r="1.8" fill="currentColor" />'
        # Convergence lines into the candidate hexagon
        '<line x1="95" y1="62" x2="150" y2="100" />'
        '<line x1="95" y1="100" x2="150" y2="100" />'
        '<line x1="95" y1="138" x2="150" y2="100" />'
        # Candidate gene hexagon (right)
        '<polygon points="170,100 162,86 146,86 138,100 146,114 162,114" />'
        '<circle cx="154" cy="100" r="3" fill="currentColor" />'
        # Lane labels (single letters for genomics/proteomics/metabolomics)
        '<text x="8" y="65" font-family="monospace" font-size="8" '
        'fill="currentColor" stroke="none">G</text>'
        '<text x="8" y="103" font-family="monospace" font-size="8" '
        'fill="currentColor" stroke="none">P</text>'
        '<text x="8" y="141" font-family="monospace" font-size="8" '
        'fill="currentColor" stroke="none">M</text>'
        "</svg>"
    )


def lcms_bg() -> Safe:
    """LC-MS chromatogram peaks feeding a CNN box with a spectral score."""
    return Safe(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" '
        'stroke="currentColor" fill="none" stroke-width="1.5">'
        "<title>LC-MS spectral matching</title>"
        "<desc>Chromatogram peaks at the top feed a small convolutional "
        "neural network box, producing a spectral match score shown as "
        "peaks at the bottom.</desc>"
        # Top chromatogram baseline + peaks
        '<line x1="15" y1="55" x2="185" y2="55" stroke-dasharray="2 2" />'
        '<path d="M15 55 L35 55 L42 30 L48 55 L70 55 L80 18 L88 55 '
        "L120 55 L128 38 L135 55 L160 55 L168 25 L175 55 L185 55"
        '" />'
        # CNN box (middle)
        '<rect x="60" y="85" width="80" height="32" rx="3" />'
        # Convolutional kernel hint inside the box
        '<rect x="72" y="93" width="14" height="16" />'
        '<rect x="93" y="93" width="14" height="16" />'
        '<rect x="114" y="93" width="14" height="16" />'
        '<text x="100" y="135" text-anchor="middle" '
        'font-family="monospace" font-size="7" fill="currentColor" '
        'stroke="none">CNN</text>'
        # Bottom spectral match peaks
        '<line x1="15" y1="170" x2="185" y2="170" />'
        '<line x1="40" y1="170" x2="40" y2="148" />'
        '<line x1="65" y1="170" x2="65" y2="155" />'
        '<line x1="90" y1="170" x2="90" y2="142" />'
        '<line x1="115" y1="170" x2="115" y2="158" />'
        '<line x1="140" y1="170" x2="140" y2="150" />'
        '<line x1="165" y1="170" x2="165" y2="160" />'
        "</svg>"
    )


def forager_bg() -> Safe:
    """Funnel from 20,000 compounds to 50 bioactives with a 100x callout."""
    return Safe(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" '
        'stroke="currentColor" fill="none" stroke-width="1.5">'
        "<title>Forager bioactive discovery funnel</title>"
        "<desc>A funnel narrows from twenty thousand candidate compounds "
        "down to fifty bioactives, with a one hundred times throughput "
        "callout.</desc>"
        # Funnel outline (trapezoid narrowing downward)
        '<polygon points="25,40 175,40 130,120 70,120" />'
        # Compound dots at the wide top
        '<circle cx="50" cy="55" r="1.5" fill="currentColor" />'
        '<circle cx="70" cy="58" r="1.5" fill="currentColor" />'
        '<circle cx="90" cy="52" r="1.5" fill="currentColor" />'
        '<circle cx="110" cy="60" r="1.5" fill="currentColor" />'
        '<circle cx="130" cy="55" r="1.5" fill="currentColor" />'
        '<circle cx="150" cy="58" r="1.5" fill="currentColor" />'
        '<circle cx="60" cy="70" r="1.5" fill="currentColor" />'
        '<circle cx="100" cy="72" r="1.5" fill="currentColor" />'
        '<circle cx="140" cy="70" r="1.5" fill="currentColor" />'
        # Funnel stem
        '<line x1="100" y1="120" x2="100" y2="150" />'
        # Output bioactives (small cluster at the bottom)
        '<circle cx="92" cy="160" r="3" />'
        '<circle cx="100" cy="165" r="3" />'
        '<circle cx="108" cy="160" r="3" />'
        # 100x callout to the right of the funnel
        '<text x="170" y="80" text-anchor="middle" '
        'font-family="monospace" font-size="14" font-weight="700" '
        'fill="currentColor" stroke="none">100x</text>'
        '<line x1="155" y1="85" x2="135" y2="100" />'
        "</svg>"
    )


def qc_bg() -> Safe:
    """Three factory nodes feeding an ML gate with a 90% callout."""
    return Safe(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" '
        'stroke="currentColor" fill="none" stroke-width="1.5">'
        "<title>Real-time QC gate</title>"
        "<desc>Three factory floor nodes on the left feed a machine "
        "learning decision gate on the right, with a ninety percent QC "
        "throughput callout.</desc>"
        # Three factory nodes (squares with chimneys)
        '<rect x="20" y="50" width="28" height="22" />'
        '<line x1="32" y1="50" x2="32" y2="42" />'
        '<rect x="20" y="92" width="28" height="22" />'
        '<line x1="32" y1="92" x2="32" y2="84" />'
        '<rect x="20" y="134" width="28" height="22" />'
        '<line x1="32" y1="134" x2="32" y2="126" />'
        # Lines feeding the diamond gate
        '<line x1="48" y1="61" x2="120" y2="100" />'
        '<line x1="48" y1="103" x2="120" y2="100" />'
        '<line x1="48" y1="145" x2="120" y2="100" />'
        # Diamond ML gate
        '<polygon points="140,100 120,80 100,100 120,120" />'
        # Pass / fail outputs
        '<line x1="140" y1="100" x2="170" y2="85" />'
        '<line x1="140" y1="100" x2="170" y2="115" />'
        '<circle cx="175" cy="83" r="3" fill="currentColor" />'
        '<circle cx="175" cy="117" r="3" />'
        # 90% callout
        '<text x="100" y="175" text-anchor="middle" '
        'font-family="monospace" font-size="14" font-weight="700" '
        'fill="currentColor" stroke="none">90%</text>'
        "</svg>"
    )


# Mapping from CV company name (as used in components.py) to its diagram fn.
COMPANY_DIAGRAMS: dict[str, Callable[[], Safe]] = {
    "Triplebar": genome_lm_bg,
    "Amyris": multiomics_bg,
    "Hexagon Bio": lcms_bg,
    "Brightseed": forager_bg,
    "Mondelez International": qc_bg,
}


def diagram_for(company: str) -> Safe | None:
    """Return the SVG diagram for a company, or ``None`` if unknown."""
    fn = COMPANY_DIAGRAMS.get(company)
    return fn() if fn is not None else None
