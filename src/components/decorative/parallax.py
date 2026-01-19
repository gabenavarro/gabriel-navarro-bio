from fasthtml.common import Div, Style, Script
from src.styles import DOT_PARALLAX_CSS, SUNSET_PARALLAX_CSS

# ==============================================================================
# Dot Parallax Effect
# ==============================================================================

_dot_parallax_js = """
document.addEventListener('DOMContentLoaded', () => {
    const background = document.querySelector('.parallax-background');
    if (!background) return;

    const spacing = 50;
    const hoverScale = 2;
    const parallaxStrength = 0.03;
    const parallaxRadius = 300;

    const createDots = () => {
        background.querySelectorAll('.dot').forEach(dot => dot.remove());
        const width = window.innerWidth;
        const height = window.innerHeight;
        const cols = Math.floor(width / spacing);
        const rows = Math.floor(height / spacing);
        const maxDots = 100;
        const totalDots = cols * rows;
        const skipRatio = Math.ceil(totalDots / maxDots);

        let dotCount = 0;
        for (let i = 0; i < rows; i++) {
            for (let j = 0; j < cols; j++) {
                dotCount++;
                if (dotCount % skipRatio !== 0) continue;
                const dot = document.createElement('div');
                dot.className = 'dot';
                const x = (j * spacing) + (spacing / 2) + (Math.random() * 10 - 5);
                const y = (i * spacing) + (spacing / 2) + (Math.random() * 10 - 5);
                dot.style.left = `${x}px`;
                dot.style.top = `${y}px`;
                dot.setAttribute('data-x', x);
                dot.setAttribute('data-y', y);
                background.appendChild(dot);
            }
        }
    };

    const handleMouseMove = (e) => {
        const dots = document.querySelectorAll('.dot');
        const mouseX = e.clientX;
        const mouseY = e.clientY;

        dots.forEach(dot => {
            const dotX = parseFloat(dot.getAttribute('data-x'));
            const dotY = parseFloat(dot.getAttribute('data-y'));
            const distX = mouseX - dotX;
            const distY = mouseY - dotY;
            const distance = Math.sqrt(distX * distX + distY * distY);

            if (distance < parallaxRadius) {
                const moveFactor = 1 - (distance / parallaxRadius);
                const moveX = distX * moveFactor * parallaxStrength;
                const moveY = distY * moveFactor * parallaxStrength;
                dot.style.transform = `translate(calc(-50% + ${moveX}px), calc(-50% + ${moveY}px)) scale(${1 + (moveFactor * 0.5)})`;
            } else {
                dot.style.transform = 'translate(-50%, -50%)';
            }
        });
    };

    createDots();
    document.addEventListener('mousemove', handleMouseMove);
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(createDots, 200);
    });
});
"""

def DotParallax():
    """Returns an interactive dot background with parallax effects."""
    return Div(
        Style(DOT_PARALLAX_CSS),
        Script(_dot_parallax_js),
        cls="parallax-background",
    )

# ==============================================================================
# Sunset Parallax Effect
# ==============================================================================

_sunset_parallax_js = """
document.addEventListener('mousemove', (e) => {
    const x = (e.clientX / window.innerWidth - 0.5) * 2;
    const y = (e.clientY / window.innerHeight - 0.5) * 2;
    
    document.querySelectorAll('.sun').forEach(el => el.style.transform = `translate(calc(-50% + ${-x*20}px), ${-y*10}px)`);
    document.querySelectorAll('.mountains-bg').forEach(el => el.style.transform = `translate(${-x*15}px, ${-y*5}px)`);
    document.querySelectorAll('.water').forEach(el => el.style.transform = `translate(${-x*10}px, 0)`);
    document.querySelectorAll('.mountains-fg').forEach(el => el.style.transform = `translate(${-x*30}px, ${-y*15}px)`);
    document.querySelectorAll('.tree').forEach(el => el.style.transform = `translate(calc(-50% + ${-x*40}px), ${-y*20}px)`);
});
"""

def SunsetParallax():
    """Returns a beautiful sunset landscape with parallax effects."""
    return Div(
        Style(SUNSET_PARALLAX_CSS),
        Script(_sunset_parallax_js),
        Div(cls="sun"),
        Div(Div(cls="mountain-bg"), Div(cls="mountain-bg-2"), cls="mountains-bg"),
        Div(Div(cls="water-reflection"), Div(cls="sun-reflection"), cls="water"),
        Div(Div(cls="mountain-fg-left"), Div(cls="mountain-fg-right"), cls="mountains-fg"),
        Div(Div(cls="tree-branch-1"), Div(cls="tree-branch-2"), cls="tree"),
        cls="parallax-landscape"
    )
