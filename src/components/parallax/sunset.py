from fasthtml.common import Div, Style, Script
from src.lib.css import SUNSET_PARALLAX_CSS


_parallax_script = """
document.addEventListener('DOMContentLoaded', function() {
    const parallaxBg = document.querySelector('.parallax-landscape');
    const sun = document.querySelector('.sun');
    const mountainsBg = document.querySelector('.mountains-bg');
    const water = document.querySelector('.water');
    const mountainsFg = document.querySelector('.mountains-fg');
    const tree = document.querySelector('.tree');

    document.addEventListener('mousemove', function(e) {
        if (!parallaxBg) return;

        const mouseX = e.clientX / window.innerWidth - 0.5;
        const mouseY = e.clientY / window.innerHeight - 0.5;

        // Move elements at different speeds for parallax effect
        if (sun) sun.style.transform = `translate(calc(-50% + ${mouseX * 20}px), ${mouseY * 10}px)`;
        if (mountainsBg) mountainsBg.style.transform = `translateX(${mouseX * 15}px)`;
        if (water) water.style.transform = `translateY(${mouseY * 5}px)`;
        if (mountainsFg) mountainsFg.style.transform = `translateX(${mouseX * 30}px)`;
        if (tree) tree.style.transform = `translate(${mouseX * 10}px, 50%)`;
    });
});
"""


SUNSET_PARALLAX = Div(
    # Script to handle mouse movement for parallax effect
    Script(_parallax_script),
    # Parallax style
    Style(SUNSET_PARALLAX_CSS),
    # Sun
    Div(cls="sun"),
    # Background mountains
    Div(Div(cls="mountain-bg"), Div(cls="mountain-bg-2"), cls="mountains-bg"),
    # Water
    Div(cls="water"),
    # Water reflection with lines
    Div(cls="water-reflection"),
    # Sun reflection on water
    Div(cls="sun-reflection"),
    # Foreground mountains
    Div(Div(cls="mountain-fg-left"), Div(cls="mountain-fg-right"), cls="mountains-fg"),
    # Tree silhouette
    Div(Div(cls="tree-branch-1"), Div(cls="tree-branch-2"), cls="tree"),
    cls="parallax-landscape",
)
