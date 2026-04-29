"""Layout styles: navigation, container, footer.

Page-level scaffolding shared across every route. Component-internal layout
(card grids, hero columns, etc.) lives in `_pages.py` or per-feature files.
"""

LAYOUT_CSS = """
/* Navigation */
.factory-nav {
    background-color: transparent !important;
    padding: 1.5rem 2rem !important;
}

.factory-brand {
    font-family: 'Geist', sans-serif;
    font-weight: 900;
    letter-spacing: -0.05em;
    color: var(--color-white) !important;
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

/* Footer */
.factory-footer {
    border-top: 1px solid var(--color-base-900);
    padding: 3rem 2rem 2rem 2rem;
    margin-top: 6rem;
    background: var(--dark-base-primary);
}

.factory-footer-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1.5rem;
}

.factory-footer-col {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.factory-footer-brand {
    font-family: 'Geist', sans-serif;
    font-weight: 900;
    letter-spacing: -0.05em;
    color: var(--color-white);
    margin: 0;
}

.factory-footer-tagline {
    font-size: 0.75rem;
    color: var(--color-base-500);
    letter-spacing: 0.05em;
    margin: 0;
}

.factory-footer-link {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--color-base-400);
    text-decoration: none;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-right: 1rem;
}

.factory-footer-link:hover {
    color: var(--color-accent-100);
}

.factory-footer-divider {
    border-top: 1px solid var(--color-base-900);
    margin: 1.5rem 0;
}

.factory-footer-copyright {
    font-size: 0.75rem;
    color: var(--color-base-600);
    margin: 0;
}

@media (max-width: 768px) {
    .factory-footer-row {
        flex-direction: column;
        align-items: flex-start;
    }
}
"""
