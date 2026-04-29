"""Base styles: CSS custom properties (root vars), reset, body/typography defaults.

This is the foundation layer of the Factory design system. It defines the
color palette, spacing scale, typography scale, radii, easings, and the
global html/body resets that every page inherits.
"""

BASE_CSS = """
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
    --primary-color: #4a9cf7;
    --secondary-color: #c70445;
    --white: #ffffff;
    --black: #000000;
    --cat-omics: #0064b6;
    --cat-ml: #c70445;
    --cat-infra: #a48404;
    --cat-viz: #00a405;
    --cat-neutral: var(--color-base-700);
    color-scheme: light dark;
}

html, body {
    box-sizing: border-box;
    border: 0 solid;
    margin: 0;
    padding: 0;
    width: 100%;
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

/* Lock the page to vertical-only scrolling. Without this, any element that
 * for any reason renders even one pixel wider than the viewport (timing of
 * scrollbar appearance, sticky-navbar measurement, BFCache restore in Edge,
 * a stray 100vw that leaks in) makes the page horizontally scrollable, and
 * Edge's BFCache will sometimes restore a non-zero scrollX after a
 * trackpad-back gesture — leaving the whole layout shifted horizontally
 * with the navbar links cut off the right edge until a hard refresh.
 *
 * `overflow-x: clip` is the modern equivalent of `hidden` that does NOT
 * create a new containing block for `position: fixed/sticky` descendants —
 * important so the sticky navbar keeps sticking. Fall back to `hidden` for
 * the small slice of browsers without `clip` support.
 */
html {
    overflow-x: hidden;
    overflow-x: clip;
}

/* Keyboard focus rings (visible only on keyboard nav, not on click) */
*:focus { outline: none; }
*:focus-visible {
    outline: 2px solid var(--color-accent-100);
    outline-offset: 3px;
    border-radius: var(--radius-sm);
}
"""
