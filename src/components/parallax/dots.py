from fasthtml.common import Div, Style, Script

_parallax_style = """
/* Parallax Dots Background */

.parallax-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
  background-color: rgba(154, 83, 48, 1); /* Same as body background */
}

.dot {
  position: absolute;
  width: 8px;
  height: 8px;
  background-color: #000;
  border-radius: 50%;
  pointer-events: auto;
  transition: transform 0.3s ease;
}

.dot:hover {
  transform: scale(1.8);
}

/* Create a grid of dots using pseudo-elements */
@media (min-width: 768px) {
  .parallax-background::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: radial-gradient(circle, #000 4px, transparent 4px);
    background-size: 50px 50px;
    pointer-events: none;
  }
}
"""

_parallax_script = """
/**
 * Interactive Parallax Dots Background
 * 
 * This script creates an interactive dot background with parallax effects.
 * Dots grow on hover and move slightly based on mouse position.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Get the parallax background
  const background = document.querySelector('.parallax-background');
  if (!background) return;
  
  // Configuration
  const dotSize = 8;         // Size of dots in pixels
  const spacing = 50;        // Grid spacing
  const hoverScale = 2;      // How much dots grow on hover
  const parallaxStrength = 0.03; // Strength of parallax effect
  const parallaxRadius = 300;    // How far from mouse the parallax effect reaches
  
  // Calculate how many dots to create based on screen size
  const createDots = () => {
    // Clear existing dots
    const existingDots = background.querySelectorAll('.dot');
    existingDots.forEach(dot => dot.remove());
    
    // Calculate grid dimensions
    const width = window.innerWidth;
    const height = window.innerHeight;
    
    const cols = Math.floor(width / spacing);
    const rows = Math.floor(height / spacing);
    
    // Limit number of interactive dots for performance
    const maxDots = 100;
    const totalDots = cols * rows;
    const skipRatio = Math.ceil(totalDots / maxDots);
    
    let dotCount = 0;
    
    // Create dots in a grid pattern
    for (let i = 0; i < rows; i++) {
      for (let j = 0; j < cols; j++) {
        // Skip dots based on the ratio to limit total number
        dotCount++;
        if (dotCount % skipRatio !== 0) continue;
        
        const dot = document.createElement('div');
        dot.className = 'dot';
        
        // Position dot in grid with slight randomness
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
  
  // Add parallax effect on mouse move
  const handleMouseMove = (e) => {
    const dots = document.querySelectorAll('.dot');
    const mouseX = e.clientX;
    const mouseY = e.clientY;
    
    dots.forEach(dot => {
      const dotX = parseFloat(dot.getAttribute('data-x'));
      const dotY = parseFloat(dot.getAttribute('data-y'));
      
      // Calculate distance from mouse to dot
      const distX = mouseX - dotX;
      const distY = mouseY - dotY;
      const distance = Math.sqrt(distX * distX + distY * distY);
      
      // Apply parallax effect - closer dots move more
      if (distance < parallaxRadius) {
        const moveFactor = 1 - (distance / parallaxRadius);
        const moveX = distX * moveFactor * parallaxStrength;
        const moveY = distY * moveFactor * parallaxStrength;
        
        dot.style.transform = `translate(calc(-50% + ${moveX}px), calc(-50% + ${moveY}px))`;
        
        // Scale effect based on proximity
        const scaleValue = 1 + (moveFactor * (hoverScale - 1) * 0.5);
        dot.style.transform += ` scale(${scaleValue})`;
      } else {
        dot.style.transform = 'translate(-50%, -50%)';
      }
    });
  };
  
  // Handle hover effect directly on dots
  background.addEventListener('mouseover', (e) => {
    if (e.target.classList.contains('dot')) {
      e.target.style.transform = `translate(-50%, -50%) scale(${hoverScale})`;
    }
  });
  
  background.addEventListener('mouseout', (e) => {
    if (e.target.classList.contains('dot')) {
      e.target.style.transform = 'translate(-50%, -50%)';
    }
  });
  
  // Initialize
  createDots();
  document.addEventListener('mousemove', handleMouseMove);
  
  // Recreate dots when window is resized
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(createDots, 200);
  });
});
"""

DOT_PARALLAX = Div(
    Style(_parallax_style),
    Script(_parallax_script, defer=True),
    cls="parallax-background", 
)