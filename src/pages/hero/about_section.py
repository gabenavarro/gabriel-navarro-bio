from fasthtml.common import Style, Div, H1, Span, P, Button, Img, H2, A
from src.lib.statics import HERO_SKILLS, HERO_SKILLS_DESCRIPTION
from src.components.buttons import button_primary, button_outline


_style = """
/* About Me Section */
.about-section {
    padding: 6rem 0;
    background-color: var(--light-bg);
    position: relative;
    overflow: hidden;
    z-index: 2;
    /* Ensure this section creates a new stacking context */
    isolation: isolate;
    /* Create solid background that fully covers any content below */
    box-shadow: 0 0 0 100vmax var(--light-bg);
    clip-path: inset(0 -100vmax);
}

.about-container {
    width: 100%;
    max-width: var(--container-max-width);
    margin: 0 auto;
    position: relative;
    z-index: 1;
    padding: 0 1rem;
}

.about-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    background: linear-gradient(135deg, #f5f8ff 0%, #e6f0ff 100%);
    overflow: hidden;
}

.about-bg::before {
    content: '';
    position: absolute;
    width: 35%;
    height: 35%;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary-color) 20%, var(--accent-color) 100%);
    filter: blur(70px);
    opacity: 0.05;
    bottom: -10%;
    right: -5%;
}

.about-bg::after {
    content: '';
    position: absolute;
    width: 25%;
    height: 25%;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent-color) 20%, var(--primary-color) 100%);
    filter: blur(60px);
    opacity: 0.05;
    top: -5%;
    left: -5%;
}

.about-image {
    width: 100%;
    height: auto;
    border-radius: 12px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
    position: relative;
    z-index: 1;
}

.about-image-wrapper {
    position: relative;
    display: inline-block;
}

.about-image-wrapper::before {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    border: 2px solid var(--primary-color);
    border-radius: 12px;
    top: 15px;
    left: 15px;
    z-index: 0;
}

.about-image:hover {
    transform: translateY(-5px);
}

.about-info h2 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    color: var(--text-color);
}

.about-info .section-subtitle {
    font-size: 1.1rem;
    color: var(--primary-color);
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 1.5px;
    margin-bottom: 1rem;
}

.about-info p {
    margin-bottom: 1.5rem;
    font-size: 1.1rem;
    line-height: 1.7;
    color: var(--text-color);
}


/* Medium screens */
@media (max-width: 992px) {
    .about-content {
        gap: 2rem;
    }
    
    .about-info h2 {
        font-size: 2.2rem;
    }
}

.skills-list {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-top: 2rem;
}

.skill-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.skill-icon {
    color: var(--primary-color);
    font-size: 1.2rem;
}

/* Small screens */
@media (max-width: 768px) {
    .about-content {
        grid-template-columns: 1fr;
    }
    
    .about-image-wrapper {
        margin-bottom: 2rem;
    }
    
    .about-info h2 {
        font-size: 2rem;
    }

    .skills-list {
        grid-template-columns: 1fr;
    }
}
"""

ABOUT_SECTION  = Div(
    Style(_style),
    Div(
        # Left Column - Image
        Div(
            Img(
                src="/api/placeholder/400/500",
                alt="Gabriel Navarro",
                cls="about-image"
            ),
            cls="about-image-wrapper"
        ),
        
        # Right Column - Information
        Div(
            Span("About Me", cls="section-subtitle"),
            H2("Exploring the Intersection of Science and Computation"),
            P(
                "As a computational scientist with over 10 years of experience, I specialize in developing and applying advanced algorithms to solve complex scientific problems. My expertise spans across multiple domains including molecular dynamics, quantum chemistry, and machine learning applications in scientific research."
            ),
            P(
                "I'm passionate about leveraging computational methods to accelerate scientific discovery and create innovative solutions that bridge the gap between theoretical models and practical applications."
            ),
            
            # Skills List
            Div(
                Div(
                    Span("✓", cls="skill-icon"),
                    Span("Molecular Modeling"),
                    cls="skill-item"
                ),
                Div(
                    Span("✓", cls="skill-icon"),
                    Span("Quantum Chemistry"),
                    cls="skill-item"
                ),
                Div(
                    Span("✓", cls="skill-icon"),
                    Span("Scientific Programming"),
                    cls="skill-item"
                ),
                Div(
                    Span("✓", cls="skill-icon"),
                    Span("Machine Learning"),
                    cls="skill-item"
                ),
                Div(
                    Span("✓", cls="skill-icon"),
                    Span("High-Performance Computing"),
                    cls="skill-item"
                ),
                Div(
                    Span("✓", cls="skill-icon"),
                    Span("Data Visualization"),
                    cls="skill-item"
                ),
                cls="skills-list"
            ),
            
            # Buttons
            Div(
                A("Download CV", href="#", cls="btn btn-primary"),
                A("Contact Me", href="#contact", cls="btn btn-outline"),
                cls="button-container cta-buttons"
            ),
            
            cls="about-info"
        ),
        cls="about-container"
    ),
    cls="about-section"
)