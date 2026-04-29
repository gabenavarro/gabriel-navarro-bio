"""Component styles: factory utilities, buttons, labels, cards, code blocks.

Visual primitives that compose into UI: titles, labels, CLI box, buttons,
cards, and the styled code-block treatment. Card classes here back the
`Card` primitive in `src/components/base/card.py`.
"""

COMPONENTS_CSS = """
/* Factory Specific Utilities */
.factory-title {
    font-size: 4.5rem;
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.05em;
    color: var(--color-white);
    margin-bottom: 2rem;
}

.factory-sub {
    font-size: 1.25rem;
    color: var(--color-base-300);
    max-width: 600px;
    line-height: 1.6;
}

.factory-accent {
    color: var(--color-accent-100);
}

.factory-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--color-accent-100);
    margin-bottom: 1rem;
}

.factory-label::before {
    content: "";
    display: block;
    width: 6px;
    height: 6px;
    background-color: var(--color-accent-100);
    border-radius: 50%;
}

/* CLI Box */
.cli-container {
    background-color: var(--dark-base-secondary);
    border: 1px solid var(--color-base-900);
    border-radius: var(--radius-lg);
    overflow: hidden;
    margin-top: 3rem;
    max-width: 500px;
}

.cli-header {
    background-color: var(--dark-base-primary);
    padding: 0.5rem 1rem;
    border-bottom: 1px solid var(--color-base-900);
    display: flex;
    gap: 1rem;
}

.cli-tab {
    font-size: 0.75rem;
    font-weight: 300;
    color: var(--color-base-500);
    cursor: pointer;
}

.cli-tab.active {
    color: var(--color-white);
}

.cli-body {
    padding: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: var(--font-geist-mono), monospace;
    font-size: 0.875rem;
}

.cli-prompt {
    color: var(--color-accent-100);
    margin-right: 0.5rem;
}

/* Buttons (back `src/components/base/buttons.py`) */
.factory-btn {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    border-radius: var(--radius-sm);
    text-decoration: none;
    cursor: pointer;
    border: 1px solid transparent;
    background: transparent;
    transition: color 0.2s ease, background-color 0.2s ease, border-color 0.2s ease;
}

.factory-btn-primary {
    background-color: var(--color-white) !important;
    color: var(--dark-base-primary) !important;
    padding: 0.5rem 1rem !important;
    text-transform: uppercase !important;
}

.factory-btn-outline {
    background-color: transparent !important;
    color: var(--color-accent-100) !important;
    border: 1px solid var(--color-accent-100) !important;
    padding: 0.5rem 1rem !important;
    text-transform: uppercase !important;
}

.factory-btn-outline:hover {
    background-color: var(--color-accent-100) !important;
    color: var(--dark-base-primary) !important;
}

.factory-btn-ghost {
    color: var(--color-accent-100) !important;
    padding: 0 !important;
    border: none !important;
    background: transparent !important;
}

.factory-btn-ghost:hover {
    color: var(--color-accent-200) !important;
}

/* Cards (back `src/components/base/card.py`) */
.factory-card {
    border: 1px solid var(--color-base-900);
    border-radius: var(--radius-lg);
    background: var(--dark-base-secondary);
    transition: border-color 0.3s ease;
    display: block;
    text-decoration: none;
    color: inherit;
}

.factory-card-padding-sm { padding: 0.75rem; }
.factory-card-padding-md { padding: 1.5rem; }
.factory-card-padding-lg { padding: 2rem; }

.factory-card-interactive:hover {
    border-color: var(--color-accent-100);
    cursor: pointer;
}

.factory-card-header {
    margin-bottom: 1rem;
}

.factory-card-body {
    /* default flow */
}

.factory-card-footer {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid var(--color-base-900);
}

/* Category Tags (single source of truth: --cat-* in _base.py) */
.card-category {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    border-radius: var(--radius-sm);
    font-size: 0.75rem;
    font-weight: 600;
}

.category-omics { background-color: var(--cat-omics); color: white; }
.category-machine-learning { background-color: var(--cat-ml); color: white; }
.category-ml { background-color: var(--cat-ml); color: white; }
.category-infrastructure { background-color: var(--cat-infra); color: white; }
.category-infra { background-color: var(--cat-infra); color: white; }
.category-visualization { background-color: var(--cat-viz); color: white; }
.category-viz { background-color: var(--cat-viz); color: white; }
.category-neutral { background-color: var(--cat-neutral); color: white; }
.cat-omics { background-color: var(--cat-omics); color: white; }
.cat-ml { background-color: var(--cat-ml); color: white; }
.cat-infra { background-color: var(--cat-infra); color: white; }
.cat-viz { background-color: var(--cat-viz); color: white; }
.cat-neutral { background-color: var(--cat-neutral); color: white; }

/* Code Blocks */
pre.shiki, .uk-codeblock {
    font-family: var(--font-geist-mono), monospace !important;
    font-size: 0.75rem !important;
    line-height: 1 !important;
    background-color: #0b0c0e !important;
    border: 1px solid var(--color-base-900) !important;
    border-radius: 1rem !important;
    margin: 2rem 0 !important;
    position: relative !important;
    padding-top: 2.5rem !important; /* Space for the simulated header */
}

.uk-codespan {
    font-weight: 300 !important;
    --font-mono: 'Cascadia Mono', monospace;
    font-size: 0.75rem !important;
    white-space: pre-wrap !important;
    background-color: #161719 !important;
    line-height: 1rem !important;
}

.language-python {
    line-height: 1.25rem !important;
    font-family: var(--font-geist-mono), monospace !important;
}

/* Header Simulation */
pre.shiki::before, .uk-codeblock::before {
    content: "—";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2.5rem;
    background-color: #161719;
    border-bottom: 1px solid var(--color-base-900);
    padding: 0 1rem;
    display: flex;
    align-items: center;
    color: var(--color-base-500);
    font-size: 0.75rem;
    font-weight: 700;
    border-top-left-radius: 1rem;
    border-top-right-radius: 1rem;
    z-index: 1;
}

/* Copy Icon Simulation (Visual only if we can't inject JS easily into markdown) */
pre.shiki::after, .uk-codeblock::after {
    content: "❑"; /* Simple icon-like character or we can use a small image/svg if needed */
    position: absolute;
    top: 0.75rem;
    right: 1rem;
    color: var(--color-base-500);
    font-size: 0.875rem;
    z-index: 2;
}

.shiki code, .uk-codeblock code {
    background-color: transparent !important;
    padding: 1.5rem !important;
    display: block !important;
    font-family: var(--font-geist-mono), monospace !important;
    font-size: 0.875rem !important;
    line-height: 1.7 !important;
    color: #D4D4D4 !important;
}

/* Syntax Highlighting Tweaks */
.shiki .line {
    display: block;
}

/* Overriding default shiki style if present in HTML */
.shiki {
    padding: 0 !important;
}

/* Codeblock padding background color */
.bg-base-200 {
    background-color: var(--background-color) !important;
}
"""
