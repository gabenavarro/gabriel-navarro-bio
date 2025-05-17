from fasthtml.common import Style, Div, Img, H3, P, A, Span
from src.components import simple_navigation, contact_me_modal
from src.lib.css import ROOT_CSS, BODY_CSS
from src.lib.javascript import MasonryJS, MarkedJS
from typing import Optional
from src.lib.google.bigquery import BigQueryClient
from src.components.chips import filter_chips

CATEGORY_MAP = {
    "bioinformatics": "omics",
    "genomics": "omics",
    "transcriptomics": "omics",
    "metabolomics": "omics",
    "proteomics": "omics",
    "protein folding": "machine-learning",
    "machine learning": "machine-learning",
    "deep-learning": "machine-learning",
    "state-space-models": "machine-learning",
    "flashattention": "machine-learning",
    "transformers": "machine-learning",
    "webdevelopment": "visualization",
    "html": "visualization",
    "css": "visualization",
    "javascript": "visualization",
    "docker": "infrastructure",
    "cloud": "infrastructure",
    "gcp": "infrastructure",
}

css = """
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

/* Hidden cards when filtered out */
.masonry-card.hidden {
    height: 0%;
    overflow: hidden;
    padding: 0;
    margin: 0;
    visibility: hidden;
}

.masonry-sizer {
    max-width: 250px;

    /* Medium screens */
    @media (max-width: 992px) {
        max-width: 400px;
    }

    /* Small screens */
    @media (max-width: 768px) {
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
  pointer-events: none;   /* no mouse events at all */
  cursor: default;        /* normal arrow, not the hand */
  color: #999;            /* visually muted */
  text-decoration: none;  /* remove underline */
}

/* Card category badges - updated for multi-category display */
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



def generate_cards(tag:Optional[str] = None):
    """ Create a card with an image, title, and description."""
    client = BigQueryClient()
    blogs = client.query(sql="SELECT * FROM `noble-office-299208.portfolio.gn-blog` LIMIT 1000")

    if isinstance(blogs, dict):
        blogs = [blogs]

    return Div(
        *[
            A(
                Img(
                    src=entry["image"], 
                    alt=f"",
                    cls="rounded-img",
                ),
                H3(entry["title"], cls="masonry-card-title"),
                *[Span(i["v"], cls=f"card-category category-{CATEGORY_MAP.get(i['v'], 'omics')}") for i in entry["tags"]],
                P(entry["description"], cls="white"),
                href=f"/projects/{entry['id']}",
                data_category=",".join(
                    sorted(list(set([CATEGORY_MAP.get(i["v"], "omics") for i in entry["tags"]])))
                ),
                cls="masonry-card masonry-sizer a-card" if not entry["disabled"] else "masonry-card masonry-sizer a-card disabled",
            ) for entry in blogs
        ],
        cls="masonry-container",
    )

def create_masonry_page(tag: str | None = None):
    chips = [
        ("Machine Learning", "red", "machine-learning", True if tag == "machine-learning" else False), 
        ("Omics", "blue", "omics", True if tag == "omics" else False), 
        ("Visualization", "green", "visualization", True if tag == "visualization" else False), 
        ("Infrastructure", "yellow", "infrastructure", True if tag == "infrastructure" else False)
    ]
    return Div(
        Style(ROOT_CSS + BODY_CSS + css),
        MasonryJS(
            sel=".masonry-container",
            item_selector=".masonry-card",
            column_width=".masonry-sizer",
            gutter=20,
            percent_position=False,
            horizontal_order=True,
            origin_left=True,
            origin_top=True,
        ),
        MarkedJS(),
        simple_navigation(),
        filter_chips(chips),
        contact_me_modal(),
        Div(
            generate_cards(),
        ),
        cls="container",
    )
