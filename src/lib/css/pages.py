# Page Styles

MASONRY_PAGE_CSS = """
.masonry-container {
    max-width: var(--container-max-width);
    margin: auto auto;
    position: relative;
    z-index: 2;
    padding: 0 1rem;
    padding-top: 2rem;
    min-height: 100vh;
    overflow-y: hidden;
}

.masonry-card {
    background-color: var(--dark-newspaper-bg);
    border-radius: 5px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    padding: 0.75rem;
    margin-bottom: 1rem;
    transition: transform 0.3s ease;
}

.masonry-card:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    cursor: pointer;
    transition: transform 0.3s ease;
    z-index: 3;
    background-color: var(--dark-highlight-newspaper);
    color: var(--white);
    text-decoration: none;
    filter: brightness(1.05);
}

.masonry-card-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--white);
    margin-bottom: 0.5rem;
    margin-top: 0.5rem;
}

.masonry-card.hidden {
    height: 0%;
    overflow: hidden;
    padding: 0;
    margin: 0;
    visibility: hidden;
}

.masonry-sizer {
    max-width: 250px;
}

@media (max-width: 992px) {
    .masonry-sizer {
        max-width: 400px;
    }
}

@media (max-width: 768px) {
    .masonry-sizer {
        max-width: 600px;
    }
}

.rounded-img {
    width: 100%;
    height: auto;
    border-radius: 5px;
}

.a-card {
    text-decoration: none;
}

a.disabled {
  pointer-events: none;
  cursor: default;
  color: #999;
  text-decoration: none;
}

.card-category {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    margin-right: 5px;
    margin-bottom: 10px;
}

.category-machine-learning { background-color: #c70445; color: white; }
.category-omics { background-color: #0064b6; color: white; }
.category-infrastructure { background-color: #a48404; color: white; }
.category-visualization { background-color: #00a405; color: white; }
"""

BLOG_PAGE_CSS = """
.marked {
    max-width: var(--container-max-width);
    margin: auto auto;
    position: relative;
    z-index: 2;
    padding: 0 1rem;
}

.centered-not-found {
    max-width: var(--container-max-width);
    margin: auto auto;
    position: relative;
    z-index: 2;
    padding: 0 1rem;
    text-align: center;
    font-size: 1.5rem;
    color: var(--dark-newspaper-bg);
}

/* highlight.js theme placeholder - move to dedicated lib/css/highlight.py if needed */
pre code.hljs{display:block;overflow-x:auto;padding:1em}code.hljs{padding:3px 5px}.hljs{background:#f3f3f3;color:#444}.hljs-comment{color:#697070}.hljs-punctuation,.hljs-tag{color:#444a}.hljs-tag .hljs-attr,.hljs-tag .hljs-name{color:#444}.hljs-attribute,.hljs-doctag,.hljs-keyword,.hljs-meta .hljs-keyword,.hljs-name,.hljs-selector-tag{font-weight:700}.hljs-deletion,.hljs-number,.hljs-quote,.hljs-selector-class,.hljs-selector-id,.hljs-string,.hljs-template-tag,.hljs-type{color:#800}.hljs-section,.hljs-title{color:#800;font-weight:700}.hljs-link,.hljs-operator,.hljs-regexp,.hljs-selector-attr,.hljs-selector-pseudo,.hljs-symbol,.hljs-template-variable,.hljs-variable{color:#ab5656}.hljs-literal{color:#695}.hljs-addition,.hljs-built_in,.hljs-bullet,.hljs-code{color:#397300}.hljs-meta{color:#1f7199}.hljs-meta .hljs-string{color:#38a}.hljs-emphasis{font-style:italic}.hljs-strong{font-weight:700}
"""

CV_PAGE_CSS = """
/* ... (existing CV_PAGE_CSS content) ... */
"""

HERO_SECTION_CSS = """
/* Hero section */
.hero-section {
    height: 100vh;
    display: flex;
    align-items: center;
    position: relative;
    overflow: hidden;
    padding: 0;
    z-index: 1;
    isolation: isolate;
    background: linear-gradient(to bottom, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0) 90%, var(--black) 100%);
}

.animated-text {
    display: inline-block;
    min-width: 200px;
}

.cta-buttons {
    display: flex;
    gap: 1rem;
    margin-bottom: 2.5rem;
}

@media (max-width: 992px) {
    .platform {
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(3, 1fr);
    }
}

@media (max-width: 768px) {
    .hero-section {
        padding: 0 1rem;
        padding-top: 5rem;
    }

    .cta-buttons {
        flex-direction: column;
        gap: 0.75rem;
        width: 100%;
    }

    .platform {
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(3, 1fr);
        gap: 20px;
    }
}

/* Skills Rotator Controls CSS (previously injected via JS) */
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
    100% { transform: translateY(0px); }
}

.skill-nav-controls {
    display: flex;
    gap: 15px;
    margin-top: -10px;
    margin-bottom: 25px;
    align-items: center;
}

.skill-nav-btn {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
}

.skill-nav-btn:hover {
    background-color: rgba(74, 156, 247, 0.2);
    border-color: var(--primary-color);
}

.skill-prev::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 0;
    height: 0;
    border-top: 8px solid transparent;
    border-bottom: 8px solid transparent;
    border-right: 12px solid rgba(255, 255, 255, 0.8);
    margin-left: -2px;
}

.skill-next::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 0;
    height: 0;
    border-top: 8px solid transparent;
    border-bottom: 8px solid transparent;
    border-left: 12px solid rgba(255, 255, 255, 0.8);
    margin-left: 2px;
}

.skill-pause::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 4px;
    height: 14px;
    background-color: rgba(255, 255, 255, 0.8);
    margin-left: -4px;
}

.skill-pause::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 4px;
    height: 14px;
    background-color: rgba(255, 255, 255, 0.8);
    margin-left: 4px;
}

.skill-pause.highlighted {
    background-color: rgba(74, 156, 247, 0.2);
    border-color: var(--primary-color);
}

.skill-pause.highlighted::before,
.skill-pause.highlighted::after {
    background-color: var(--primary-color, rgba(74, 156, 247, 0.8));
}
"""

ABOUT_SECTION_CSS = """
.about-background {
    height: 100%;
    width: 100%;
    display: flex;
    position: relative;
    background-color: transparent;
    overflow: hidden;
    z-index: 1;
}

.about-block {
    position: relative;
    display: flex;
    flex-direction: column;
    min-height: 80vh;
    padding: 2rem;
}

.about-block-right-aligned {
    display: flex;
    width: 100%;
    justify-content: flex-end;
    padding-right: 4rem;
}
"""
