"""Layout styles: navigation, container, footer.

Page-level scaffolding shared across every route. Component-internal layout
(card grids, hero columns, etc.) lives in `_pages.py` or per-feature files.
"""

LAYOUT_CSS = """
/* Navigation */
.factory-nav {
    background-color: transparent !important;
    padding: 1.5rem 0;
}

.factory-nav {
    padding-right: 2rem !important;
    padding-left: 2rem !important;
}

.factory-nav-link {
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    color: var(--color-base-300) !important;
}

.factory-nav-link:hover {
    color: var(--color-white) !important;
}
"""
