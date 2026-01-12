from fasthtml.common import Span, Style, Script
from src.lib.css import BALL_BACKGROUND_CSS

_js = """
document.addEventListener('DOMContentLoaded', () => {
    const balls = document.querySelectorAll('.ball');
    let mouseX = 0;
    let mouseY = 0;
    let ballPositions = [];

    // Store initial positions of all balls
    balls.forEach(ball => {
        const rect = ball.getBoundingClientRect();
        const initialX = rect.left + rect.width / 2;
        const initialY = rect.top + rect.height / 2;
        ballPositions.push({ initialX, initialY, currentX: initialX, currentY: initialY });
    });

    // Track mouse position
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    // Animation function
    function animateBalls() {
        balls.forEach((ball, index) => {
            const position = ballPositions[index];

            // Calculate direction to mouse
            const dx = mouseX - position.currentX;
            const dy = mouseY - position.currentY;

            // Calculate distance (squared for efficiency)
            const distanceSquared = dx * dx + dy * dy;

            // Avoid division by zero and set maximum force
            const force = Math.min(500, 1000 / (distanceSquared || 1));

            // Calculate new position with attraction to mouse and reversion to initial position
            const attractionFactor = 0.02;  // Strength of mouse attraction
            const restitutionFactor = 0.01; // Strength of return to original position

            // Update position with mouse attraction
            position.currentX += dx * force * attractionFactor;
            position.currentY += dy * force * attractionFactor;

            // Apply restitution force to return to initial position
            position.currentX += (position.initialX - position.currentX) * restitutionFactor;
            position.currentY += (position.initialY - position.currentY) * restitutionFactor;

            // Apply new position to ball
            ball.style.transform = `translate(${position.currentX - position.initialX}px, ${position.currentY - position.initialY}px)`;
        });

        requestAnimationFrame(animateBalls);
    }

    // Start animation
    animateBalls();
});
"""


BALL = Span(Style(BALL_BACKGROUND_CSS), Script(_js), cls="ball")
