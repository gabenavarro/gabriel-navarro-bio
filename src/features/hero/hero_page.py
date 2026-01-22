from src.components.layout.page import StandardPage
from .components import hero_section


def get_hero_page():
    """Assembles and returns the full hero page."""
    return StandardPage("Gabriel", hero_section())


HERO_PAGE = get_hero_page()
