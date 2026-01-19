from fasthtml.common import Div, Span, Style, Script
from src.styles import BALL_BACKGROUND_CSS, TRANSITION_CSS

# ==============================================================================
# Floating Balls Background
# ==============================================================================

_floating_balls_js = """
document.addEventListener('DOMContentLoaded', () => {
    const balls = document.querySelectorAll('.ball');
    let mouseX = 0;
    let mouseY = 0;
    let ballPositions = [];

    balls.forEach(ball => {
        const rect = ball.getBoundingClientRect();
        const initialX = rect.left + rect.width / 2;
        const initialY = rect.top + rect.height / 2;
        ballPositions.push({ initialX, initialY, currentX: initialX, currentY: initialY });
    });

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    function animateBalls() {
        balls.forEach((ball, index) => {
            const position = ballPositions[index];
            const dx = mouseX - position.currentX;
            const dy = mouseY - position.currentY;
            const distanceSquared = dx * dx + dy * dy;
            const force = Math.min(500, 1000 / (distanceSquared || 1));
            const attractionFactor = 0.02;
            const restitutionFactor = 0.01;

            position.currentX += dx * force * attractionFactor;
            position.currentY += dy * force * attractionFactor;
            position.currentX += (position.initialX - position.currentX) * restitutionFactor;
            position.currentY += (position.initialY - position.currentY) * restitutionFactor;

            ball.style.transform = `translate(${position.currentX - position.initialX}px, ${position.currentY - position.initialY}px)`;
        });
        requestAnimationFrame(animateBalls);
    }
    animateBalls();
});
"""

def FloatingBalls(num_balls: int = 8):
    """Returns a background with floating balls that react to mouse movement."""
    balls = [Div(cls="ball") for _ in range(num_balls)]
    return Div(
        Style(BALL_BACKGROUND_CSS),
        Script(_floating_balls_js),
        *balls,
        cls="ball_background"
    )

# ==============================================================================
# Vertical Lines Background
# ==============================================================================

VERTICAL_LINES_CSS = """
.vertical_lines_container {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    width: 100%; z-index: 0; pointer-events: none; overflow: hidden;
}
.vertical_line {
    position: absolute; width: 1px; top: 0; bottom: 0; left: 50%;
    background: rgba(255, 255, 255, 0.05);
}
.vertical_line::after {
    content: ''; display: block; position: absolute; height: 15vh; width: 100%;
    top: -50%; left: 0;
    background: linear-gradient(to bottom, rgba(255, 255, 255, 0) 0%, #ffffff 75%, #ffffff 100%);
    animation: drop 10s 0s infinite forwards cubic-bezier(0.4, 0.26, 0, 0.97);
}
.vertical_line:nth-child(1) { transform: translateX(-35vw); }
.vertical_line:nth-child(1)::after { animation-delay: 2s; }
.vertical_line:nth-child(2) { transform: translateX(0); }
.vertical_line:nth-child(2)::after { animation-delay: 4s; }
.vertical_line:nth-child(3) { transform: translateX(35vw); }
.vertical_line:nth-child(3)::after { animation-delay: 2.5s; }
@keyframes drop { 0% { top: -20%; } 100% { top: 110%; } }
"""

def VerticalLines():
    """Returns a background with falling vertical lines."""
    return Div(
        Style(VERTICAL_LINES_CSS),
        Div(cls="vertical_line"),
        Div(cls="vertical_line"),
        Div(cls="vertical_line"),
        cls="vertical_lines_container",
    )

# ==============================================================================
# Gradient Transition Background
# ==============================================================================

def GradientTransition():
    """Returns a background with animated gradient spheres for section transitions."""
    return Div(
        Style(TRANSITION_CSS),
        Div(cls="gradient-sphere sphere-1"),
        Div(cls="gradient-sphere sphere-2"),
        Div(cls="gradient-sphere sphere-3"),
        Div(cls="glow-1"),
        Div(cls="glow-2"),
        Div(cls="particles-container"),
        cls="gradient-background"
    )
