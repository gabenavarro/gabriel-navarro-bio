"""
Emadamerho Nefe; https://codepen.io/nefejames

Example placement

<div class="ball_background">
  <span class="ball"></span>
  <span class="ball"></span>
  <span class="ball"></span>
  <span class="ball"></span>
  <span class="ball"></span>
  <span class="ball"></span>
</div>

"""
from fasthtml.common import Span, Style, Script

_css = """
ball_background
. {
    position: fixed;
    width: 100vw;
    height: 100vh;
    top: 0;
    left: 0;
    overflow: hidden; /* Required to hide out of bound balls */
    background: var(--background-color);
}

@keyframes move {
    100% {
        transform: translate3d(0, 0, 1px) rotate(360deg);
    }
}

.ball {
    position: absolute;
    width: 20vmin;
    height: 20vmin;
    border-radius: 50%;
    backface-visibility: hidden;
    animation: move linear infinite;
    z-index: 0;
    pointer-events: none;
}

.ball:nth-child(odd) {
    color: var(--primary-color);
}

.ball:nth-child(even) {
    color: var(--secondary-color);
}

/* Using a custom attribute for variability */
.ball:nth-child(1) {
    top: 77%;
    left: 88%;
    animation-duration: 40s;
    animation-delay: -3s;
    transform-origin: 16vw -2vh;
    box-shadow: 40vmin 0 5.703076368487546vmin currentColor;
}
.ball:nth-child(2) {
    top: 42%;
    left: 2%;
    animation-duration: 53s;
    animation-delay: -29s;
    transform-origin: -19vw 21vh;
    box-shadow: -40vmin 0 5.17594621519026vmin currentColor;
}
.ball:nth-child(3) {
    top: 28%;
    left: 18%;
    animation-duration: 49s;
    animation-delay: -8s;
    transform-origin: -22vw 3vh;
    box-shadow: 40vmin 0 5.248179047256236vmin currentColor;
}
.ball:nth-child(4) {
    top: 50%;
    left: 79%;
    animation-duration: 26s;
    animation-delay: -21s;
    transform-origin: -17vw -6vh;
    box-shadow: 40vmin 0 5.279749632220298vmin currentColor;
}
.ball:nth-child(5) {
    top: 46%;
    left: 15%;
    animation-duration: 36s;
    animation-delay: -40s;
    transform-origin: 4vw 0vh;
    box-shadow: -40vmin 0 5.964309466052033vmin currentColor;
}
.ball:nth-child(6) {
    top: 77%;
    left: 16%;
    animation-duration: 31s;
    animation-delay: -10s;
    transform-origin: 18vw 4vh;
    box-shadow: 40vmin 0 5.178483653434181vmin currentColor;
}
.ball:nth-child(7) {
    top: 22%;
    left: 17%;
    animation-duration: 55s;
    animation-delay: -6s;
    transform-origin: 1vw -23vh;
    box-shadow: -40vmin 0 5.703026794398318vmin currentColor;
}
.ball:nth-child(8) {
    top: 41%;
    left: 47%;
    animation-duration: 43s;
    animation-delay: -28s;
    transform-origin: 25vw -3vh;
    box-shadow: 40vmin 0 5.196265905749415vmin currentColor;
}
"""


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


BALL = Span(
    Style(_css),
    Script(_js),
    cls="ball"
)