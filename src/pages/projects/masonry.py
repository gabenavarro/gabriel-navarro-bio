from fasthtml.common import *
from src.lib.javascript import MasonryJS
import random




css = """
.masonry-container {
    width: 100%;
    max-width: var(--container-max-width);
    margin: 0 auto;
    position: relative;
    z-index: 2;
    padding: 0 1rem;
}

"""
rando = random.Random()

def image_card(i):
    return Div(
        Img(src=f"https://picsum.photos/id/{i + 100}/400/{rando.randint(a=200,b=500)}", alt=f"Image {i}"),
        H3(f"Image Title {i}"),
        P(f"This is a description for image {i}"),
        cls="masonry-card"
    )


def create_blog_page():
    return Titled("Image Gallery",
        Style(css),
        MasonryJS(
            sel=".masonry-container",
            item_selector=".masonry-card",
            column_width=200,
            gutter=10,
            percent_position=True,
            horizontal_order=True,
            origin_left=True,
            origin_top=True,
        ),
        Div(
            H1("Photo Gallery"),
            Div(
                *[image_card(i) for i in range(1, 20)],
                cls="masonry-container",
            ),
        ),
        
    )



MASONRY_PAGE = create_blog_page()