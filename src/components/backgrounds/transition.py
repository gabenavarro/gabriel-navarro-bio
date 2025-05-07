from fasthtml.common import Div, Style, Script
from typing import Tuple

def transition_js_css(
    background:str = "gradient-background"
) -> Tuple[str,str]:
    """Transition CSS and JS
    ---
    
    ### Args
        * background (str): CSS name of background for JS to monitor

    ### Return
        * css (str): CSS for...
        * js (str): Javascript for... 
    """


    css = """
    .gradient-sphere {
        position: absolute;
        border-radius: 50%;
        filter: blur(60px);
    }

    .sphere-1 {
        width: 40vw;
        height: 40vw;
        background: linear-gradient(40deg, rgba(255, 0, 128, 0.4), rgba(255, 102, 0, 0.2));
        top: 10vh;
        left: -10vw;
        animation: float-1 15s ease-in-out infinite alternate;
        /* Added will-change for better performance during animations */
        will-change: transform;
        transition: transform 0.3s ease-out, top 0.1s linear;
    }

    .sphere-2 {
        width: 45vw;
        height: 45vw;
        background: linear-gradient(240deg, rgba(72, 0, 255, 0.4), rgba(0, 183, 255, 0.2));
        top: 70vh;
        left: 70vw;
        animation: float-2 18s ease-in-out infinite alternate;
        /* Added will-change and transition for consistency with sphere-1 */
        will-change: transform;
        transition: transform 0.3s ease-out, top 0.1s linear;
    }

    .sphere-3 {
        width: 30vw;
        height: 30vw;
        background: linear-gradient(120deg, rgba(133, 89, 255, 0.25), rgba(98, 216, 249, 0.15));
        top: 50vh;
        left: 20vw;
        animation: float-3 20s ease-in-out infinite alternate;
        /* Added will-change and transition for consistency with sphere-1 */
        will-change: transform;
        transition: transform 0.3s ease-out, top 0.1s linear;
    }



    @keyframes float-1 {
        0% {
            transform: translate(0, 0) scale(1);
        }
        100% {
            transform: translate(10%, 10%) scale(1.1);
        }
    }

    @keyframes float-2 {
        0% {
            transform: translate(0, 0) scale(1);
        }
        100% {
            transform: translate(-10%, -5%) scale(1.15);
        }
    }

    @keyframes float-3 {
        0% {
            transform: translate(0, 0) scale(1);
            opacity: 0.3;
        }
        100% {
            transform: translate(-5%, 10%) scale(1.05);
            opacity: 0.6;
        }
    }

    .glow-1 {
        position: absolute;
        width: 40vw;
        height: 40vh;
        background: radial-gradient(circle, rgba(72, 0, 255, 0.15), transparent 70%);
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 2;
        animation: pulse 8s infinite alternate;
        filter: blur(30px);
        pointer-events: none;
    }

    .glow-2 {
        position: absolute;
        width: 30vw;
        height: 30vh;
        background: radial-gradient(circle, rgba(72, 0, 255, 0.15), transparent 70%);
        top: 80%;
        left: 70%;
        transform: translate(-50%, -50%);
        z-index: 2;
        animation: pulse 8s infinite alternate;
        filter: blur(30px);
        pointer-events: none;
    }

    @keyframes pulse {
        0% {
            opacity: 0.3;
            transform: translate(-50%, -50%) scale(0.9);
        }
        100% {
            opacity: 0.7;
            transform: translate(-50%, -50%) scale(1.1);
        }
    }

    .particles-container {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 3;
        pointer-events: none;
    }

    .particle {
        position: absolute;
        background: white;
        border-radius: 50%;
        opacity: 0;
        pointer-events: none;
    }

    /* Added a class for when spheres are fixed in position */
    .sphere-1.fixed, .sphere-2.fixed, .sphere-3.fixed {
        position: fixed;
        transform: translateY(-50%);
        animation-play-state: running; /* Ensure the float animation continues */
    }

    .sphere-1.fixed {
        top: 50vh;
    }

    .sphere-2.fixed {
        top: 50vh;
    }

    .sphere-3.fixed {
        top: 50vh;
    }
    """

    
    js = f"""
    document.addEventListener('DOMContentLoaded', function() {{
        // Create particle effect
        const particlesContainer = document.getElementById('particles-container');
        const particleCount = 280;
        
        // Get references to all spheres
        const spheres = document.querySelectorAll('.gradient-sphere');
        
        // Store information about each sphere
        const sphereInfo = [];
        
        // Initialize data for each sphere
        spheres.forEach((sphere, index) => {{
            // Get the computed style to retrieve actual CSS values
            const style = window.getComputedStyle(sphere);
            
            // Extract top and left values from the computed style
            let topValue = style.top;
            let leftValue = style.left;
            
            // Parse values, handling different units
            // For top positioning
            if (topValue.includes('vh')) {{
                // Already in vh, just get the number
                topValue = parseFloat(topValue);
            }} else if (style.bottom && style.bottom.includes('vh')) {{
                // Handle bottom positioning
                topValue = 100 - parseFloat(style.bottom);
            }} else if (topValue.includes('%')) {{
                // Convert % to vh
                topValue = parseFloat(topValue);
            }} else if (topValue.includes('px')) {{
                // Convert px to vh
                topValue = (parseFloat(topValue) / window.innerHeight) * 100;
            }}
            
            // For left positioning
            if (leftValue.includes('vw')) {{
                // Already in vw, just get the number
                leftValue = parseFloat(leftValue);
            }} else if (style.right && style.right.includes('vw')) {{
                // Handle right positioning
                leftValue = 100 - parseFloat(style.right);
            }} else if (leftValue.includes('%')) {{
                // Convert % to vw
                leftValue = parseFloat(leftValue);
            }} else if (leftValue.includes('px')) {{
                // Convert px to vw
                leftValue = (parseFloat(leftValue) / window.innerWidth) * 100;
            }}
            
            // Calculate initial and target positions based on requirements
            // Add 60vh below the original position
            const randomOffset = Math.floor(Math.random() * 21) - 10; // Random integer between -10 and 10
            const initialTop = topValue + 80;
            const targetPositionTop = topValue + randomOffset; // Original top position
            
            // Store info for this sphere
            sphereInfo.push({{
                element: sphere,
                initialTop: initialTop,
                initialLeft: leftValue,
                targetTop: targetPositionTop,
                isFixed: false
            }});
        }});
        
        // Scroll event handler for all spheres
        window.addEventListener('scroll', function() {{
            const gradientBackground = document.querySelector('.{background}');
            const backgroundRect = gradientBackground.getBoundingClientRect();
            const viewportHeight = window.innerHeight;
            
            // Calculate values needed for scroll progress
            const backgroundTopRelativeToViewport = backgroundRect.top;
            const totalScrollDistance = viewportHeight * 1; // Adjust this multiplier as needed
            
            // Calculate current scroll progress
            const scrollProgress = Math.max(0, Math.min(1, 
                (viewportHeight - backgroundTopRelativeToViewport) / totalScrollDistance
            ));
            
            // Update each sphere based on scroll progress
            sphereInfo.forEach((info, index) => {{
                const sphere = info.element;
                
                // If we've scrolled enough that the sphere should be fixed
                if (scrollProgress >= 1 && !info.isFixed) {{
                    // Fix the sphere in place at the middle of the viewport
                    sphere.classList.add('fixed');
                    info.isFixed = true;
                }} 
                // If we're scrolling back up and haven't reached the fixed threshold
                else if (scrollProgress < 1 && info.isFixed) {{
                    // Unfix the sphere
                    sphere.classList.remove('fixed');
                    info.isFixed = false;
                }}
                
                // If not fixed, move the sphere based on scroll progress
                if (!info.isFixed) {{
                    // Calculate new top position:
                    // Start at initialTop and move to targetTop
                    const newTopPosition = info.initialTop - (info.initialTop - info.targetTop) * scrollProgress;
                    sphere.style.top = `${{newTopPosition}}vh`;
                }}
            }});
        }});
        
        // Create particles
        for (let i = 0; i < particleCount; i++) {{
            createParticle();
        }}

        function createParticle() {{
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            // Random size (small)
            const size = Math.random() * 3 + 1;
            particle.style.width = `${{size}}px`;
            particle.style.height = `${{size}}px`;
            
            // Initial position
            resetParticle(particle);
            
            particlesContainer.appendChild(particle);
            
            // Animate
            animateParticle(particle);
        }}

        function resetParticle(particle) {{
            // Random position
            const posX = Math.random() * 100;
            const posY = Math.random() * 100;
            
            particle.style.left = `${{posX}}%`;
            particle.style.top = `${{posY}}%`;
            particle.style.opacity = '0';
            
            return {{
                x: posX,
                y: posY
            }};
        }}

        function animateParticle(particle) {{
            // Initial position
            const pos = resetParticle(particle);
            
            // Random animation properties
            const duration = Math.random() * 10 + 10;
            const delay = Math.random() * 5;
            
            // Animate with GSAP-like timing
            setTimeout(() => {{
                particle.style.transition = `all ${{duration}}s linear`;
                particle.style.opacity = Math.random() * 0.3 + 0.1;
                
                // Move in a slight direction
                const moveX = pos.x + (Math.random() * 20 - 10);
                const moveY = pos.y - Math.random() * 30; // Move upwards
                
                particle.style.left = `${{moveX}}%`;
                particle.style.top = `${{moveY}}%`;
                
                // Reset after animation completes
                setTimeout(() => {{
                    animateParticle(particle);
                }}, duration * 1000);
            }}, delay * 1000);
        }}

        // Scroll event handler for sphere-1
        window.addEventListener('scroll', function() {{
            const gradientBackground = document.querySelector('.{background}');
            const backgroundRect = gradientBackground.getBoundingClientRect();
            const viewportHeight = window.innerHeight;
            
            // Calculate the position of the sphere element relative to viewport
            const sphereRect = sphere1.getBoundingClientRect();
            
            // Calculate when the sphere first enters the viewport
            // We start animation when the bottom of the viewport crosses the top of the background
            const backgroundTopRelativeToViewport = backgroundRect.top;
            
            // Calculate total scroll distance needed to reach the midpoint (from when it enters viewport to when it should be fixed)
            // This is the distance we need to scroll to move the sphere from 60% below viewport to middle of viewport
            const totalScrollDistance = viewportHeight * 1.1; // Adjust this multiplier as needed
            
            // Calculate current scroll progress within this range
            // When backgroundTop is at viewport bottom (viewportHeight), progress is 0
            // When backgroundTop is negative enough that sphere should be fixed, progress is 1
            const scrollProgress = Math.max(0, Math.min(1, 
                (viewportHeight - backgroundTopRelativeToViewport) / totalScrollDistance
            ));
            
            // If we've scrolled enough that the sphere should be fixed
            if (scrollProgress >= 1 && !isFixed) {{
                // Fix the sphere in place at the middle of the viewport
                sphere1.classList.add('fixed');
                isFixed = true;
            }} 
            // If we're scrolling back up and haven't reached the fixed threshold
            else if (scrollProgress < 1 && isFixed) {{
                // Unfix the sphere
                sphere1.classList.remove('fixed');
                isFixed = false;
            }}
            
            // If not fixed, move the sphere based on scroll progress
            if (!isFixed) {{
                // Calculate new top position:
                // Start at initialTop (160% - below viewport) and move to targetPositionTop (50% - middle of viewport)
                const newTopPercentage = sphere1InitialTop - (sphere1InitialTop - targetPositionTop) * scrollProgress;
                sphere1.style.top = `${{newTopPercentage}}%`;
                
                // Keep the float animation by not explicitly setting transform
                // Let the CSS animation handle the jitter effect
            }}
        }});

        // Mouse interaction
        document.addEventListener('mousemove', (e) => {{
            const gradientBackground = document.querySelector('.{background}');
            const particlesContainer = document.getElementById('particles-container');
            
            // Get container's position relative to the viewport
            const containerRect = gradientBackground.getBoundingClientRect();
            
            // Check if mouse is inside the container
            if (
                e.clientX >= containerRect.left && 
                e.clientX <= containerRect.right && 
                e.clientY >= containerRect.top && 
                e.clientY <= containerRect.bottom
            ) {{
                // Calculate mouse position relative to the container (in percentage)
                const mouseX = ((e.clientX - containerRect.left) / containerRect.width) * 100;
                const mouseY = ((e.clientY - containerRect.top) / containerRect.height) * 100;
                
                // Create temporary particle
                const particle = document.createElement('div');
                particle.className = 'particle';
                
                // Small size
                const size = Math.random() * 4 + 2;
                particle.style.width = `${{size}}px`;
                particle.style.height = `${{size}}px`;
                
                // Position at mouse
                particle.style.left = `${{mouseX}}%`;
                particle.style.top = `${{mouseY}}%`;
                particle.style.opacity = '0.6';
                
                // particlesContainer.appendChild(particle);
                
                // Animate outward
                setTimeout(() => {{
                    particle.style.transition = 'all 2s ease-out';
                    particle.style.left = `${{mouseX + (Math.random() * 10 - 5)}}%`;
                    particle.style.top = `${{mouseY + (Math.random() * 10 - 5)}}%`;
                    particle.style.opacity = '0';
                    
                    // Remove after animation
                    setTimeout(() => {{
                        particle.remove();
                    }}, 2000);
                }}, 10);
                
                // Only apply subtle movement to non-fixed spheres
                const moveX = ((e.clientX - containerRect.left) / containerRect.width - 0.5) * 250;
                const moveY = ((e.clientY - containerRect.top) / containerRect.height - 0.5) * 250;
                
                sphereInfo.forEach(info => {{
                    const sphere = info.element;
                    // Only apply additional transform if not fixed
                    if (!info.isFixed) {{
                        sphere.style.transform = `translate(${{moveX}}px, ${{moveY}}px)`;
                    }}
                }});
            }}
        }});

        // Initial position check in case page loads already scrolled
        window.dispatchEvent(new Event('scroll'));
    }});
    """
    return css, js


def glow_object(
    number: int = 0,
    top: int = 80,
    left: int = 70,
    size: int = 30
):
    return f"""
    .glow-{number} {{
        position: absolute;
        width: {size}vw;
        height: {size}vh;
        background: radial-gradient(circle, rgba(72, 0, 255, 0.15), transparent 70%);
        top: {top}%;
        left: {left}%;
        transform: translate(-50%, -50%);
        z-index: 2;
        animation: pulse 8s infinite alternate;
        filter: blur(30px);
        pointer-events: none;
    }}
    """


_style,_script = transition_js_css()

_style += """
.gradient-background {
    height: 150vh;
    width: 100%;
    display: flex;
    position: relative;
    background: var(--black);
    z-index: 1;
}
"""

GRADIENT_TRANSITION = Div(
    Style(_style),
    Script(_script, defer=True),
    Div(
        Div(cls="gradient-sphere sphere-1"),
        Div(cls="gradient-sphere sphere-2"),
        Div(cls="gradient-sphere sphere-3"),
        Div(cls="glow-1"),
        Div(cls="glow-2"),
        Div(cls="particles-container", id="particles-container"),
        cls="gradient-background"
    )
)