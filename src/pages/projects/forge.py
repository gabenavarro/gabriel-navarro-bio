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
"""
rando = random.Random()

def image_card(i):
    return Div(
        Img(
            src=f"https://picsum.photos/id/{i + 100}/600/{rando.randint(a=200,b=500)}", 
            alt=f"Image {i}",
            cls="rounded-img",
        ),
        H3(f"Image Title {i}", cls="white"),
        P(f"This is a description for image {i}", cls="white"),
        cls="masonry-card masonry-sizer"
    )


def create_blog_page():
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
        NAVIGATION,
        Div(style="height: 10vh;"),
        Div(
            Div(
                *[image_card(i) for i in range(1, 20) if i != 5],
                cls="masonry-container",
            ),
        ),
        cls="container",
        
    )



MASONRY_PAGE = create_blog_page()