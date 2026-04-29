"""Page-specific styles: hero parallax, blog masonry, CV-specific bits.

Reserved as the home for page-scoped CSS that can't be generalized into a
component yet. Epic B will add `.masonry-columns` here. Today this file
also carries CV/hero/project per-feature CSS that emerged from the A5
inline-style cleanup.
"""

PAGES_CSS = """
/* Generic vertical spacer used in page layouts (replaces inline height divs). */
.page-spacer-sm { height: 1.5rem; }
.page-spacer-md { height: 3rem; }
.page-spacer-lg { height: 4rem; }

/* Hero portrait (landing page). */
.hero-portrait-img {
    width: 100%;
    max-width: 400px;
    height: auto;
    filter: grayscale(100%);
    transition: all 0.5s ease;
    display: block;
    margin: 0 auto;
    object-fit: contain;
}
.hero-portrait-img:hover {
    filter: grayscale(0%);
    border-color: var(--color-accent-100);
}

/* Hero "principle" card inner content (item title, item body, subsection). */
.principle-item-title {
    font-weight: 700;
    font-size: 0.875rem;
    color: var(--color-white);
    margin-bottom: 0.5rem;
}
.principle-item-body {
    font-size: 0.875rem;
    color: var(--color-base-400);
    margin-top: 0;
    margin-bottom: 1.5rem;
    line-height: 1.6;
}
.principle-subsection-title {
    font-weight: 700;
    font-size: 0.75rem;
    color: var(--color-base-500);
    border-bottom: 1px solid var(--color-base-900);
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
    letter-spacing: 0.05em;
}
.principle-subsection-body {
    font-size: 0.875rem;
    color: var(--color-base-400);
    margin-bottom: 1rem;
    line-height: 1.6;
}

/* Project page (blog index + detail). */
.factory-title-tight-bottom { margin-bottom: 0; }
.factory-title-tight-top { margin-top: 0; }
.projects-grid-spacer { margin-top: 3rem; }
.blog-detail-meta {
    font-weight: 700;
    color: var(--color-accent-100);
    font-size: 0.75rem;
    border-bottom: 1px solid var(--color-base-900);
    padding-bottom: 1rem;
    margin-bottom: 2.5rem;
    letter-spacing: 0.05em;
}
.blog-detail-body {
    font-size: 1rem;
    color: var(--color-base-300);
    line-height: 1.8;
}

/* CV section header spacing. */
.cv-section-header { margin-top: 4rem; margin-bottom: 2rem; }

/* CV experience / education card spacing between siblings. */
.cv-experience-card { margin-bottom: 3rem; }
.cv-education-card { margin-bottom: 2rem; }

/* CV typography (period, role, company, bullets). */
.cv-period {
    font-weight: 700;
    color: var(--color-base-500);
    font-size: 0.875rem;
}
.cv-period-tight {
    font-weight: 700;
    color: var(--color-base-500);
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
}
.cv-role-title {
    margin-top: 0;
    color: var(--color-white);
    font-weight: 700;
    font-size: 1.125rem;
}
.cv-company {
    font-weight: 700;
    color: var(--color-accent-100);
    font-size: 0.75rem;
    margin-bottom: 1rem;
}
.cv-company-tight {
    font-weight: 700;
    color: var(--color-accent-100);
    font-size: 0.75rem;
}
.cv-bullets {
    margin-top: 1rem;
    list-style-type: none;
    padding-left: 0;
}
.cv-bullet {
    color: var(--color-base-400);
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
}

/* CV skills column (category title + items). */
.cv-skill-category-title {
    font-weight: 700;
    font-size: 0.875rem;
    color: var(--color-white);
    margin-bottom: 1rem;
    border-bottom: 1px solid var(--color-base-900);
    padding-bottom: 0.5rem;
}
.cv-skill-list {
    list-style-type: none;
    padding-left: 0;
}
.cv-skill-item {
    color: var(--color-base-400);
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
}

/* CV patent card. */
.cv-patent-title {
    margin-top: 0;
    color: var(--color-white);
    font-weight: 700;
    font-size: 1rem;
    line-height: 1.4;
}
.cv-patent-authors {
    color: var(--color-base-400);
    font-size: 0.75rem;
    margin-bottom: 1rem;
}
.cv-patent-link {
    color: var(--color-accent-100);
    font-weight: 700;
    font-size: 0.75rem;
    text-decoration: none;
    letter-spacing: 0.05em;
    margin-top: auto;
}
/* Patent cards stretch to equal grid-row height and use a flex column so */
/* the VIEW PATENT link can be pushed to the bottom (margin-top: auto). */
.cv-patent-card {
    height: 100%;
    display: flex;
    flex-direction: column;
}
.cv-patent-card .factory-card-body {
    flex: 1;
    display: flex;
    flex-direction: column;
}

/* CV publication entry (borderless; uses bottom border separator). */
.cv-publication-entry {
    padding: 1.5rem;
    border-bottom: 1px solid var(--color-base-900);
}
.cv-publication-title {
    margin-top: 0;
    color: var(--color-white);
    font-weight: 700;
    font-size: 1rem;
    line-height: 1.4;
}
.cv-publication-authors {
    color: var(--color-base-400);
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
}
.cv-publication-info {
    color: var(--color-accent-100);
    font-weight: 700;
    font-size: 0.75rem;
}

/* Blog masonry layout (CSS column-count for true variable-height tiling) */
.masonry-columns {
    column-count: 3;
    column-gap: 1.5rem;
}
.masonry-columns > * {
    break-inside: avoid;
    margin-bottom: 1.5rem;
    display: inline-block;
    width: 100%;
}
@media (max-width: 992px) {
    .masonry-columns { column-count: 2; }
}
@media (max-width: 640px) {
    .masonry-columns { column-count: 1; }
}
"""
