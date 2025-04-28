from fasthtml.common import Style, Div, Img, H3, P, A
from src.components import NAVIGATION
from src.lib.css import ROOT_CSS, BODY_CSS
from src.lib.javascript import MasonryJS, MarkedJS
from typing import Optional
from src.lib.google.bigquery import BigQueryClient
from src.components.modal import get_modal

css = """
.masonry-container {
    max-width: var(--container-max-width);
    margin: auto auto;
    position: relative;
    z-index: 2;
    padding: 0 1rem;
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

.masonary-card-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--white);
    margin-bottom: 0.5rem;
    margin-top: 0.5rem;
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

"""

def generate_cards(tag:Optional[str] = None):
    """ Create a card with an image, title, and description."""
    client = BigQueryClient()
    blogs = client.query(sql="SELECT * FROM `noble-office-299208.portfolio.gn-blog` LIMIT 1000")
    
    return Div(
        *[
            A(
                Img(
                    src=entry["image"], 
                    alt=f"",
                    cls="rounded-img",
                ),
                H3(entry["title"], cls="masonary-card-title"),
                P(entry["description"], cls="white"),
                href=f"/projects/{entry['id']}",
                cls="masonry-card masonry-sizer a-card" if not entry["disabled"] else "masonry-card masonry-sizer a-card disabled",
            ) for entry in blogs],
        cls="masonry-container",
    )


def create_masonry_page():
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
        NAVIGATION,
        get_modal(),
        Div(style="height: 10vh;"),
        Div(
            generate_cards(),
        ),
        cls="container",
    )



MASONRY_PAGE = create_masonry_page()