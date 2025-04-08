from fasthtml.common import Style, Div, H1, Span, P, Script, Button
from src.lib.statics import HERO_SKILLS, HERO_SKILLS_DESCRIPTION
from src.components.buttons import button_primary, button_outline

_script = f"""
htmx.onLoad(function() {{
    // Execute immediately on script load rather than waiting for DOMContentLoaded
    // Define and cache DOM elements
    const skills = {HERO_SKILLS};
    const skillDescriptions = {HERO_SKILLS_DESCRIPTION};
    let currentIndex = 0;
    let isPaused = false;
    let intervalId = null;
    
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', initializeSkillRotator);
    }} else {{
        initializeSkillRotator();
    }}
    
    function initializeSkillRotator() {{
        // Cache DOM elements (only once)
        const skillText = document.getElementById('hero-skill-text');
        const descriptionText = document.getElementById('hero-skill-description');
        const prevBtn = document.getElementById('skill-prev');
        const pauseBtn = document.getElementById('skill-pause');
        const nextBtn = document.getElementById('skill-next');
        
        if (!skillText || !descriptionText) return;
        
        // Add event delegation for better performance
        document.addEventListener('click', e => {{
            const target = e.target;
            
            // Handle prev button click
            if (target.id === 'skill-prev' || target.closest('#skill-prev')) {{
                clearInterval(intervalId);
                previousSkill();
                if (!isPaused) startInterval();
            }}
            
            // Handle next button click
            if (target.id === 'skill-next' || target.closest('#skill-next')) {{
                clearInterval(intervalId);
                nextSkill();
                if (!isPaused) startInterval();
            }}
            
            // Handle pause/play button click
            if (target.id === 'skill-pause' || target.closest('#skill-pause')) {{
                if (isPaused) {{
                    // Resume
                    pauseBtn.classList.remove('playing');
                    pauseBtn.classList.add('paused');
                    startInterval();
                }} else {{
                    // Pause
                    pauseBtn.classList.remove('paused');
                    pauseBtn.classList.add('playing');
                    clearInterval(intervalId);
                }}
                isPaused = !isPaused;
            }}
        }});
        
        // Function to update displayed skill - optimized with requestAnimationFrame
        function updateSkill(index) {{
            // Prepare the transition
            requestAnimationFrame(() => {{
                skillText.style.opacity = '0';
                descriptionText.style.opacity = '0';
                
                setTimeout(() => {{
                    // Update content while invisible
                    skillText.textContent = skills[index];
                    
                    if (skillDescriptions[skills[index]]) {{
                        descriptionText.textContent = skillDescriptions[skills[index]];
                    }}
                    
                    // Use requestAnimationFrame for fade-in to sync with browser's rendering cycle
                    requestAnimationFrame(() => {{
                        skillText.style.opacity = '1';
                        descriptionText.style.opacity = '1';
                    }});
                }}, 300); // Reduced from 500ms for better responsiveness
            }});
        }}
        
        // Function to show next skill
        function nextSkill() {{
            currentIndex = (currentIndex + 1) % skills.length;
            updateSkill(currentIndex);
        }}
        
        // Function to show previous skill
        function previousSkill() {{
            currentIndex = (currentIndex - 1 + skills.length) % skills.length;
            updateSkill(currentIndex);
        }}
        
        // Start the interval
        function startInterval() {{
            intervalId = setInterval(nextSkill, 5000);
        }}
        
        // Initialize with the first skill and start rotation
        updateSkill(currentIndex);
        startInterval();
    }}
    
    // Add styles with a single operation
    const styleEl = document.createElement('style');
    styleEl.textContent = `
        @keyframes float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-20px); }}
            100% {{ transform: translateY(0px); }}
        }}
        
        .skill-nav-controls {{
            display: flex;
            gap: 15px;
            margin-top: -10px;
            margin-bottom: 25px;
            align-items: center;
        }}
        
        .skill-nav-btn {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
        }}
        
        .skill-nav-btn:hover {{
            background-color: rgba(74, 156, 247, 0.2);
            border-color: var(--primary-color);
        }}
        
        /* Previous button arrow */
        .skill-prev::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 0;
            height: 0;
            border-top: 8px solid transparent;
            border-bottom: 8px solid transparent;
            border-right: 12px solid rgba(255, 255, 255, 0.8);
            margin-left: -2px;
        }}
        
        /* Next button arrow */
        .skill-next::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 0;
            height: 0;
            border-top: 8px solid transparent;
            border-bottom: 8px solid transparent;
            border-left: 12px solid rgba(255, 255, 255, 0.8);
            margin-left: 2px;
        }}
        
        /* Pause button */
        .skill-pause::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 4px;
            height: 14px;
            background-color: rgba(255, 255, 255, 0.8);
            margin-left: -4px;
        }}
        
        .skill-pause::after {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 4px;
            height: 14px;
            background-color: rgba(255, 255, 255, 0.8);
            margin-left: 4px;
        }}
        
        /* Play button (when paused) */
        .skill-pause.playing::before {{
            width: 0;
            height: 0;
            background-color: transparent;
            border-top: 7px solid transparent;
            border-bottom: 7px solid transparent;
            border-left: 14px solid rgba(255, 255, 255, 0.8);
            margin-left: 2px;
        }}
        
        .skill-pause.playing::after {{
            content: none;
        }}
    `;
    document.head.appendChild(styleEl);
}})();
"""

_style = """
/* Hero section */
.hero-section {
    height: 110vh;
    display: flex;
    align-items: center;
    position: relative;
    overflow: hidden;
    padding: 0;
    z-index: 1;
    /* Ensure proper stacking context */
    isolation: isolate;
    background: linear-gradient(to bottom, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0) 90%, var(--black) 100%);

}

.hero-container {
    width: 100%;
    max-width: var(--container-max-width);
    margin: 0 auto;
    position: relative;
    z-index: 1;
    padding: 0 1rem;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    color: var(--white);
    line-height: 1.2;
    margin-bottom: 1.5rem;
}

@keyframes hero-typing {
    from {
        width
    }
}

.accent {
    color: var(--primary-color);
}

.hero-subtitle {
    font-size: 1.25rem;
    margin-bottom: 2rem;
    color: var(--white);
    max-width: 600px;
    min-height: 150px;
}

.animated-text {
    display: inline-block;
    min-width: 200px;
}

.cta-buttons {
    display: flex;
    gap: 1rem;
    margin-bottom: 2.5rem;
}


/* Medium screens */
@media (max-width: 992px) {
    .hero-title {
        font-size: 3rem;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
    }

    .platform {
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(3, 1fr);
    }
}

/* Small screens */
@media (max-width: 768px) {
    .hero-section {
        padding: 0 1rem;
        padding-top: 5rem;
    }
    
    .hero-title {
        font-size: 2.3rem;
    }
    
    .hero-subtitle {
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    .cta-buttons {
        flex-direction: column;
        gap: 0.75rem;
        width: 100%;
    }
    
    .platform {
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(3, 1fr);
        gap: 20px;
    }
}
"""

HERO_SECTION = Div(
    Style(_style),
    Script(_script),
    Div(
                    
        # Hero content wrapper
        Div(
            Div(
                H1(
                    "Hi, I'm Gabriel Navarro, a ",
                    Span(
                        "Computational Scientist",
                        id="hero-skill-text",
                        cls="accent animated-text"
                    ),
                    cls="hero-title"
                ),
                P(
                    "I employ cutting-edge computational methods to solve challenging scientific problems. Let's push the boundaries of research together!",
                    id="hero-skill-description",
                    cls="hero-subtitle"
                ),

                # Skill Navigation Controls
                # These buttons will be used to navigate through the skills with JavaScript
                Div(
                    Button("", cls="skill-nav-btn skill-prev", id="skill-prev", type="button"),
                    Button("", cls="skill-nav-btn skill-pause", id="skill-pause", type="button"),
                    Button("", cls="skill-nav-btn skill-next", id="skill-next", type="button"),
                    cls="skill-nav-controls"
                ),
                
                # CTA Buttons
                Div(
                    button_primary("View My Work", href="/projects"),   # Link to projects page
                    button_outline("About Me", href="#aboutme"),        # Scroll to about me section
                    button_outline("Contact Me", href="#contact"),      # Scroll to contact section
                    cls="cta-buttons"
                ),
            ),
            cls="hero-container"
        ),
        cls="hero-section"
    )
)