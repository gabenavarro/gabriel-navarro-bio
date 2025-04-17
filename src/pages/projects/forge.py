from fasthtml.common import Style, Div, Script, Img, H1, H3, P
from src.components import NAVIGATION
from src.lib.css import ROOT_CSS, BODY_CSS
from src.lib.javascript import MasonryJS
import random


MAX_CARD_WIDTH = 250

css = """
.masonry-container {
    max-width: var(--container-max-width);
    margin: auto auto;
    position: relative;
    z-index: 2;
    padding: 0 1rem;
}

.masonry-card {
    background-color: var(--black);
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    padding: 1rem;
    margin-bottom: 1rem;
    transition: transform 0.3s ease;
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
"""
rando = random.Random()

def image_card(i):
    return Div(
        Img(src=f"https://picsum.photos/id/{i + 100}/600/{rando.randint(a=200,b=500)}", alt=f"Image {i}"),
        H3(f"Image Title {i}"),
        P(f"This is a description for image {i}"),
        cls="masonry-card masonry-sizer"
    )


def create_blog_page():
    return Div(
        Style(ROOT_CSS + BODY_CSS + css),
        MasonryJS(
            sel=".masonry-container",
            item_selector=".masonry-card",
            column_width=".masonry-sizer",
            gutter=0,
            percent_position=False,
            horizontal_order=True,
            origin_left=True,
            origin_top=True,
        ),
        NAVIGATION,
        Div(
            Div(
                *[image_card(i) for i in range(1, 20) if i != 5],
                cls="masonry-container",
            ),
        ),
        cls="container",
        
    )



MASONRY_PAGE = create_blog_page()