FACTORY_CSS = """
:root {
    --color-orange-500: oklch(70.5% .213 47.604);
    --color-emerald-500: oklch(69.6% .17 162.48);
    --color-blue-400: oklch(70.7% .165 254.624);
    --color-gray-500: oklch(55.1% .027 264.364);
    --color-gray-700: oklch(37.3% .034 259.733);
    --color-neutral-600: oklch(43.9% 0 0);
    --color-neutral-900: oklch(20.5% 0 0);
    --color-white: #fff;
    --spacing: .25rem;
    --container-xs: 20rem;
    --text-xs: .75rem;
    --text-xs--line-height: calc(1/.75);
    --text-sm: .875rem;
    --text-sm--line-height: calc(1.25/.875);
    --text-base: 1rem;
    --text-base--line-height: calc(1.5/1);
    --text-lg: 1.125rem;
    --text-lg--line-height: calc(1.75/1.125);
    --text-xl: 1.25rem;
    --text-xl--line-height: calc(1.75/1.25);
    --text-2xl: 1.5rem;
    --text-2xl--line-height: calc(2/1.5);
    --text-4xl: 2.25rem;
    --text-4xl--line-height: calc(2.5/2.25);
    --text-5xl: 3rem;
    --text-5xl--line-height: 1;
    --text-6xl: 3.75rem;
    --text-6xl--line-height: 1;
    --text-7xl: 4.5rem;
    --text-7xl--line-height: 1;
    --font-weight-normal: 400;
    --font-weight-medium: 500;
    --font-weight-semibold: 600;
    --font-weight-bold: 700;
    --tracking-normal: 0em;
    --leading-tight: 1.25;
    --leading-snug: 1.375;
    --leading-relaxed: 1.625;
    --leading-loose: 2;
    --radius-xs: .125rem;
    --radius-sm: .25rem;
    --radius-md: .375rem;
    --radius-lg: .5rem;
    --radius-xl: .75rem;
    --radius-2xl: 1rem;
    --radius-3xl: 1.5rem;
    --ease-out: cubic-bezier(0,0,.2,1);
    --ease-in-out: cubic-bezier(.4,0,.2,1);
    --animate-spin: spin 1s linear infinite;
    --animate-pulse: pulse 2s cubic-bezier(.4,0,.6,1)infinite;
    --aspect-video: 16/9;
    --default-transition-duration: .15s;
    --default-transition-timing-function: cubic-bezier(.4,0,.2,1);
    --default-font-family: var(--font-geist-sans);
    --default-mono-font-family: var(--font-geist-mono);
    --color-background: var(--dark-base-primary);
    --color-foreground: var(--light-base-primary);
    --color-dark-base-primary: var(--dark-base-primary);
    --color-dark-base-secondary: var(--dark-base-secondary);
    --color-light-base-primary: var(--light-base-primary);
    --color-light-base-secondary: var(--light-base-secondary);
    --color-accent-100: var(--accent-100);
    --color-accent-200: var(--accent-200);
    --color-accent-300: var(--accent-300);
    --color-base-100: var(--neutral-100);
    --color-base-200: var(--neutral-200);
    --color-base-300: var(--neutral-300);
    --color-base-400: var(--neutral-400);
    --color-base-500: var(--neutral-500);
    --color-base-600: var(--neutral-600);
    --color-base-700: var(--neutral-700);
    --color-base-800: var(--neutral-800);
    --color-base-900: var(--neutral-900);
    --color-base-1000: var(--neutral-1000);
    -webkit-text-size-adjust: 100%;
    tab-size: 4;
    line-height: 1.5;
    font-feature-settings: var(--default-font-feature-settings,normal);
    font-variation-settings: var(--default-font-variation-settings,normal);
    -webkit-tap-highlight-color: transparent;
    --radius: .625rem;
    --accent-100: #ef6f2e;
    --accent-200: #ee6018;
    --accent-300: #d15010;
    --dark-base-primary: #000000;
    --dark-base-secondary: #0a0a0a;
    --light-base-primary: #eee;
    --light-base-secondary: #fafafa;
    --neutral-100: #d6d3d2;
    --neutral-200: #ccc9c7;
    --neutral-300: #b8b3b0;
    --neutral-400: #a49d9a;
    --neutral-500: #8a8380;
    --neutral-600: #5c5855;
    --neutral-700: #4d4947;
    --neutral-800: #3d3a39;
    --neutral-900: #2e2c2b;
    --neutral-1000: #1f1d1c;
    color-scheme: light dark;
}

html, body {
    box-sizing: border-box;
    border: 0 solid;
    margin: 0;
    padding: 0;
    border-color: var(--color-base-800);
    outline-color: var(--color-base-800);
    background-color: #000000 !important;
    font-family: var(--font-geist-sans), ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    color: var(--color-foreground) !important;
    -webkit-font-smoothing: antialiased;
    text-wrap: pretty;
    text-rendering: optimizeLegibility;
    --font-geist-sans: "Geist","Geist Fallback";
    --font-geist-mono: "Geist Mono","Geist Mono Fallback";
}

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

.factory-btn-primary {
    background-color: var(--color-white) !important;
    color: var(--dark-base-primary) !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    padding: 0.5rem 1rem !important;
    border-radius: var(--radius-sm) !important;
    text-transform: uppercase !important;
}

.factory-btn-secondary {
    background-color: var(--color-base-900) !important;
    color: var(--color-white) !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    padding: 0.5rem 1rem !important;
    border-radius: var(--radius-sm) !important;
    text-transform: uppercase !important;
}

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
    font-family: var(--font-geist-mono), monospace !important;
    font-size: 0.75rem !important;
    background-color: #161719 !important;
    line-height: 1rem !important;
}

.language-python {
    line-height: 1.25rem !important;
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
