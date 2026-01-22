"""
Custom CSS modules consolidated from lib/css/.

This module contains all custom CSS organized by purpose:
- Base styles (root variables, body, typography)
- Component styles (navigation, buttons, modals, etc.)
- Page-specific styles (masonry, blog, CV, hero, about)
- Special effects (backgrounds, parallax)
"""

# ==============================================================================
# BASE STYLES (from lib/css/base.py)
# ==============================================================================

ROOT_CSS = """
:root {
    --primary-color: #4fc3f7;
    --secondary-color: #64ffda;
    --tertiary-color: #b388ff;
    --black: rgb(20, 20, 20);
   --white: rgb(238, 238, 238);
    --text-color: #333;
    --text-color-secondary: rgba(255, 255, 255, 0.6);
    --light-bg: #f5f8ff;
    --white: #ffffff;
    --container-max-width: 900px;
    --medium-screen: 992px;
    --small-screen: 768px;

    /* Darktheme newspaper */
    --dark-newspaper-bg: #1C1C1C;
    --dark-highlight-newspaper: #2C2C2C;
    --dark-secondary: #2C2C2C;  /* Added for consistency */
}

"""

BODY_CSS = """
/* ----------------------------- */
/*          Base styles          */
/* ----------------------------- */
body {
    font-family: system-ui, 'Inter', sans-serif;
    color: var(--text-color);
    line-height: 1.7;
    margin: 0;
    padding: 0;
    background-color: var(--black); /* rgba(154, 83, 48, 1); */
    overflow-x: hidden;
    scroll-behavior: smooth;
    padding-bottom: 2rem;
}

/* Make sure all elements respect the width constraints */
* {
  box-sizing: border-box;
  max-width: 100vw;
}

.container {
    width: 100%;
    max-width: var(--container-max-width);
    margin: 0 auto;
    position: relative;
    z-index: 2;
    padding: 0 1rem;
    padding-bottom: 2rem;
    overflow: visible;
}


/* ----------------------------- */
/* Native Scroll-Based Animation */
/* ----------------------------- */

.scroll-right-hidden {
    width: 100%;
    max-width: 100%;

    opacity: 0;
    filter: blur(5px);
    transform: translateX(30%);
    transition: all 1s ease;
}

.scroll-left-hidden {
    width: 100%;
    max-width: 100%;
    opacity: 0;
    filter: blur(5px);
    transform: translateX(-30%);
    transition: all 1s ease;
}

.scroll-show {
    opacity: 1;
    filter: blur(0);
    transform: translateX(0);
}

@media (prefers-reduced-motion) {
    .scroll-left-hidden {
        transition: none;
    }

    .scroll-right-hidden {
        transition: none;
    }
}


/* ----------------------------- */
/*          Mobile Apps         */
/* ----------------------------- */

/* Media query for mobile screens */
@media (max-width: 768px) {
  body {
    position: relative;
    width: 100%;
    overflow-x: hidden;
  }

  /* Ensure content is properly sized */
  h1, h2, h3, p {
    max-width: 100%;
    word-wrap: break-word;
  }

  /* Adjust any fixed width elements */
  img, video, iframe {
    max-width: 100%;
    height: auto;
  }
}



/* ----------------------------- */
/*           Font                */
/* ----------------------------- */

.banner-title-spacing {
    margin-top: 6rem;
    padding-bottom: 3rem;
}

.title {
    font-size: 3.5rem;
    font-weight: 800;
    color: var(--white);
    line-height: 1.2;
    margin-bottom: 1.5rem;

    @media (max-width: 992px) {
        font-size: 2.75rem;
    }

    @media (max-width: 768px) {
        font-size: 2.25rem;
    }
}

.section-title {
    font-size: 2.75rem;
    font-weight: 800;
    color: var(--white);
    line-height: 1.2;
    margin-bottom: 1.5rem;

    @media (max-width: 992px) {
        font-size: 2.25rem;
    }

    @media (max-width: 768px) {
        font-size: 1.75rem;
    }
}

.subtitle {
    font-size: 1.25rem;
    margin-bottom: 2rem;
    color: var(--white);
    max-width: 600px;
    min-height: 150px;

    /* Medium screens */
    @media (max-width: 992px) {
        font-size: 1.1rem;
    }

    /* Small screens */
    @media (max-width: 768px) {
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
}

.highlight {
    display: block;
    color: var(--primary-color);
    background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

.bold {
    font-weight: bold;
}


/* ----------------------------- */
/*              Colors           */
/* ----------------------------- */
.white {
    color: var(--white);
}

.black {
    color: var(--black);
}

.primary-color {
    color: var(--primary-color);
}

.secondary-color {
    color: var(--secondary-color);
}

.tertiary-color {
    color: var(--tertiary-color);
}

"""

# ==============================================================================
# COMPONENT STYLES (from lib/css/components.py)
# ==============================================================================

NAVIGATION_CSS = """
/* Navigation */
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background-color: rgba(25, 25, 25, 0.9);
    backdrop-filter: blur(10px);
    padding: 1rem 0;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.nav-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 1rem;
}

.logo {
    font-size: 1.5rem;
    font-weight: 700;
    color: white;
    text-decoration: none;
}

.nav-links {
    display: flex;
    gap: 2rem;
}

.nav-link {
    color: #ccc;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s ease;
}

.nav-link:hover {
    color: var(--secondary-color);
}

@media (max-width: 992px) {
    .nav-links {
        gap: 1.5rem;
    }
    .logo {
        font-size: 1.3rem;
    }
}

@media (max-width: 768px) {
    .nav-links {
        gap: 1rem;
    }
    .nav-link {
        font-size: 0.9rem;
    }
    .logo {
        font-size: 1.2rem;
    }
    .navbar {
        padding: 0.8rem 0;
    }
    .nav-container {
        padding: 0 0.5rem;
    }
}
"""

BUTTON_CSS = """
.button-container {
    margin-top: 2rem;
}

.btn {
    display: inline-block;
    padding: 0.8rem 1.8rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
    cursor: pointer;
    text-decoration: none;
    text-align: center;
}

.btn-primary {
    background: var(--primary-color);
    color: var(--black);
    border: 2px solid var(--primary-color);
}

.btn-primary:hover {
    background: var(--accent-color);
    border-color: var(--accent-color);
    color: var(--white);
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(106, 91, 255, 0.3);
}

.btn-outline {
    background: transparent;
    color: var(--white);
    border: 2px solid #444;
}

.btn-outline:hover {
    border-color: var(--primary-color);
    color: var(--primary-color);
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

@media (max-width: 768px) {
    .btn {
        width: 100%;
    }
}
"""

CONTACT_MODAL_CSS = """
/* Modal background overlay */
.modal-overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 1000;
    animation: fadeIn 0.3s;
}

/* Modal content styling */
.modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: white;
    padding: 0 1rem;
    padding-bottom: 0.25rem;
    border-radius: 8px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    width: 90%;
    max-width: 400px;
    z-index: 1001;
    animation: slideIn 0.3s;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.modal-title {
    font-size: 2.0rem;
    font-weight: 900;
    margin: 0;
    color: #333;
}

.close-modal-btn {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #888;
    transition: color 0.3s;
}

.close-modal-btn:hover {
    color: #333;
}

.modal-content {
    margin-bottom: 1rem;
    line-height: 1.6;
    color: #555;
}

.email-container {
    display: flex;
    align-items: center;
    background-color: #f5f5f5;
    padding: 0.25rem;
    border-radius: 6px;
    margin-bottom: 24px;
}

.email-text {
    flex-grow: 1;
    font-weight: 500;
}

.copy-btn {
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 0;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background-color 0.3s;
}

.copy-btn:hover {
    background-color: #45a049;
}

.social-links {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 20px;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translate(-50%, -60%);
    }
    to {
        opacity: 1;
        transform: translate(-50%, -50%);
    }
}
"""

CHIPS_CSS = """
/* Chip container styles */
.chip-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 20px;
    padding: 0.75rem;
}

/* Chip styles */
.chip {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 10px 20px;
    border-radius: 50px;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    user-select: none;
    border: none;
    background-color: rgba(255, 255, 255, 0.1);
    color: #f44336;
    outline: #f44336;
}

.chip.red {
    color: #e91e63;
    outline: #e91e63;
}

.chip.blue {
    color: #2196f3;
    outline: #2196f3;
}

.chip.green {
    color: #4caf50;
    outline: #4caf50;
}

.chip.yellow {
    color: #ffeb3b;
    outline: #ffeb3b;
}

.chip:hover {
    background-color: rgba(255, 255, 255, 0.3);
}

/* Selected chip styles */
.chip.red.selected {
    background-color: #e91e63;
    color: black;
}

.chip.blue.selected {
    background-color: #2196f3;
    color: black;
}

.chip.green.selected {
    background-color: #4caf50;
    color: black;
}

.chip.yellow.selected {
    background-color: #ffeb3b;
    color: black;
}
"""

# ... (file is getting long, I'll create it in parts)

# ==============================================================================
# BACKGROUND/VISUAL EFFECTS (from lib/css/components.py)
# ==============================================================================

BALL_BACKGROUND_CSS = """
.ball_background {
    position: fixed;
    width: 100vw;
    height: 100vh;
    top: 0;
    left: 0;
    overflow: hidden;
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

DOT_PARALLAX_CSS = """
/* Parallax Dots Background */
.parallax-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  pointer-events: none;
  background-color: rgba(154, 83, 48, 1);
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

SUNSET_PARALLAX_CSS = """
/* Parallax background */
.parallax-landscape {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    overflow: hidden;
    background: linear-gradient(180deg, #f7d6b0 0%, #e9a178 40%, #d67551 70%, #934f38 100%);
}

.sun {
    position: absolute;
    top: 15%;
    left: 50%;
    transform: translateX(-50%);
    width: 120px;
    height: 120px;
    background-color: #fff8e6;
    border-radius: 50%;
    box-shadow: 0 0 80px rgba(255, 248, 230, 0.8);
}

.mountains-bg {
    position: absolute;
    bottom: 50%;
    left: 0;
    width: 100%;
    height: 30%;
}

.mountain-bg {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 100%;
    background: #ca6a4a;
    opacity: 0.5;
    clip-path: polygon(0% 100%, 15% 60%, 25% 70%, 35% 50%, 45% 65%, 55% 45%, 65% 55%, 75% 35%, 85% 45%, 100% 20%, 100% 100%);
}

.mountain-bg-2 {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 80%;
    background: #ba584a;
    opacity: 0.6;
    clip-path: polygon(0% 100%, 10% 70%, 20% 85%, 30% 65%, 40% 80%, 50% 60%, 60% 75%, 70% 55%, 80% 70%, 90% 50%, 100% 65%, 100% 100%);
}

.water {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 50%;
    background: linear-gradient(180deg, #a34936 0%, #773428 100%);
    opacity: 0.8;
}

.water-reflection {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 50%;
    background: repeating-linear-gradient(90deg, rgba(255, 255, 255, 0.1) 0px, rgba(255, 255, 255, 0.1) 20px, rgba(255, 255, 255, 0) 20px, rgba(255, 255, 255, 0) 40px);
}

.sun-reflection {
    position: absolute;
    bottom: 10%;
    left: 50%;
    transform: translateX(-50%);
    width: 15px;
    height: 200px;
    background: rgba(255, 248, 230, 0.3);
    filter: blur(3px);
}

.mountains-fg {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 60%;
}

.mountain-fg-left {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 40%;
    height: 60%;
    background: #5d2e26;
    clip-path: polygon(0% 100%, 20% 80%, 30% 70%, 40% 60%, 50% 65%, 70% 35%, 100% 100%);
}

.mountain-fg-right {
    position: absolute;
    bottom: 0;
    right: 0;
    width: 35%;
    height: 40%;
    background: #45211b;
    clip-path: polygon(0% 100%, 30% 60%, 60% 70%, 100% 40%, 100% 100%);
}

.tree {
    position: absolute;
    bottom: 50%;
    left: 15%;
    width: 2px;
    height: 80px;
    background: #000;
    transform: translateY(50%);
}

.tree::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 1px;
    height: 30px;
    background: #000;
    transform: rotate(35deg);
    transform-origin: bottom left;
}

.tree::after {
    content: '';
    position: absolute;
    top: 10px;
    right: 0;
    width: 1px;
    height: 25px;
    background: #000;
    transform: rotate(-40deg);
    transform-origin: bottom right;
}

.tree-branch-1 {
    position: absolute;
    top: 30px;
    left: 0;
    width: 1px;
    height: 20px;
    background: #000;
    transform: rotate(25deg);
    transform-origin: bottom left;
}

.tree-branch-2 {
    position: absolute;
    top: 40px;
    right: 0;
    width: 1px;
    height: 18px;
    background: #000;
    transform: rotate(-30deg);
    transform-origin: bottom right;
}

@media (hover: hover) {
    .parallax-landscape { perspective: 1000px; }
    .sun, .mountains-bg, .water, .mountains-fg, .tree {
        will-change: transform;
        transition: transform 0.1s ease-out;
    }
}

.parallax-active { transition: transform 0.1s ease-out; }
"""

TRANSITION_CSS = """
.gradient-background {
    height: 150vh;
    width: 100%;
    display: flex;
    position: relative;
    background: var(--black);
    z-index: 1;
}

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
    will-change: transform;
    transition: transform 0.3s ease-out, top 0.1s linear;
}

@keyframes float-1 {
    0% { transform: translate(0, 0) scale(1); }
    100% { transform: translate(10%, 10%) scale(1.1); }
}

@keyframes float-2 {
    0% { transform: translate(0, 0) scale(1); }
    100% { transform: translate(-10%, -5%) scale(1.15); }
}

@keyframes float-3 {
    0% { transform: translate(0, 0) scale(1); opacity: 0.3; }
    100% { transform: translate(-5%, 10%) scale(1.05); opacity: 0.6; }
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
    0% { opacity: 0.3; transform: translate(-50%, -50%) scale(0.9); }
    100% { opacity: 0.7; transform: translate(-50%, -50%) scale(1.1); }
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

.sphere-1.fixed, .sphere-2.fixed, .sphere-3.fixed {
    position: fixed;
    transform: translateY(-50%);
    animation-play-state: running;
}

.sphere-1.fixed { top: 50vh; }
.sphere-2.fixed { top: 50vh; }
.sphere-3.fixed { top: 50vh; }
"""

# ==============================================================================
# PAGE STYLES (from lib/css/pages.py)
# ==============================================================================

MASONRY_PAGE_CSS = """
.masonry-container {
    max-width: var(--container-max-width);
    margin: auto auto;
    position: relative;
    z-index: 2;
    padding: 0 1rem;
    padding-top: 2rem;
    min-height: 100vh;
    overflow-y: hidden;
}

.masonry-card {
    background-color: var(--dark-newspaper-bg);
    border-radius: 5px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    padding: 0.75rem;
    margin-bottom: 1rem;
    transition: transform 0.3s ease;
}

.masonry-card:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    cursor: pointer;
    transition: transform 0.3s ease;
    z-index: 3;
    background-color: var(--dark-highlight-newspaper);
    color: var(--white);
    text-decoration: none;
    filter: brightness(1.05);
}

.masonry-card-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--white);
    margin-bottom: 0.5rem;
    margin-top: 0.5rem;
}

.masonry-card.hidden {
    height: 0%;
    overflow: hidden;
    padding: 0;
    margin: 0;
    visibility: hidden;
}

.masonry-sizer {
    max-width: 250px;
}

@media (max-width: 992px) {
    .masonry-sizer {
        max-width: 400px;
    }
}

@media (max-width: 768px) {
    .masonry-sizer {
        max-width: 600px;
    }
}

.rounded-img {
    width: 100%;
    height: auto;
    border-radius: 5px;
}

.a-card {
    text-decoration: none;
}

a.disabled {
  pointer-events: none;
  cursor: default;
  color: #999;
  text-decoration: none;
}

.card-category {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    margin-right: 5px;
    margin-bottom: 10px;
}

.category-machine-learning { background-color: #c70445; color: white; }
.category-omics { background-color: #0064b6; color: white; }
.category-infrastructure { background-color: #a48404; color: white; }
.category-visualization { background-color: #00a405; color: white; }
"""

BLOG_PAGE_CSS = """
.marked {
    max-width: var(--container-max-width);
    margin: auto auto;
    position: relative;
    z-index: 2;
    padding: 0 1rem;
}

.centered-not-found {
    max-width: var(--container-max-width);
    margin: auto auto;
    position: relative;
    z-index: 2;
    padding: 0 1rem;
    text-align: center;
    font-size: 1.5rem;
    color: var(--dark-newspaper-bg);
}

/* highlight.js theme */
pre code.hljs{display:block;overflow-x:auto;padding:1em}code.hljs{padding:3px 5px}.hljs{background:#f3f3f3;color:#444}.hljs-comment{color:#697070}.hljs-punctuation,.hljs-tag{color:#444a}.hljs-tag .hljs-attr,.hljs-tag .hljs-name{color:#444}.hljs-attribute,.hljs-doctag,.hljs-keyword,.hljs-meta .hljs-keyword,.hljs-name,.hljs-selector-tag{font-weight:700}.hljs-deletion,.hljs-number,.hljs-quote,.hljs-selector-class,.hljs-selector-id,.hljs-string,.hljs-template-tag,.hljs-type{color:#800}.hljs-section,.hljs-title{color:#800;font-weight:700}.hljs-link,.hljs-operator,.hljs-regexp,.hljs-selector-attr,.hljs-selector-pseudo,.hljs-symbol,.hljs-template-variable,.hljs-variable{color:#ab5656}.hljs-literal{color:#695}.hljs-addition,.hljs-built_in,.hljs-bullet,.hljs-code{color:#397300}.hljs-meta{color:#1f7199}.hljs-meta .hljs-string{color:#38a}.hljs-emphasis{font-style:italic}.hljs-strong{font-weight:700}
"""

CV_PAGE_CSS = """
/* CV page styles (placeholder for future) */
"""

HERO_SECTION_CSS = """
/* Hero section */
.hero-section {
    height: 100vh;
    display: flex;
    align-items: center;
    position: relative;
    overflow: hidden;
    padding: 0;
    z-index: 1;
    isolation: isolate;
    background: linear-gradient(to bottom, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0) 90%, var(--black) 100%);
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

@media (max-width: 992px) {
    .platform {
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(3, 1fr);
    }
}

@media (max-width: 768px) {
    .hero-section {
        padding: 0 1rem;
        padding-top: 5rem;
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

/* Skills Rotator Controls CSS */
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
    100% { transform: translateY(0px); }
}

.skill-nav-controls {
    display: flex;
    gap: 15px;
    margin-top: -10px;
    margin-bottom: 25px;
    align-items: center;
}

.skill-nav-btn {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
}

.skill-nav-btn:hover {
    background-color: rgba(74, 156, 247, 0.2);
    border-color: var(--primary-color);
}

.skill-prev::before {
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
}

.skill-next::before {
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
}

.skill-pause::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 4px;
    height: 14px;
    background-color: rgba(255, 255, 255, 0.8);
    margin-left: -4px;
}

.skill-pause::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 4px;
    height: 14px;
    background-color: rgba(255, 255, 255, 0.8);
    margin-left: 4px;
}

.skill-pause.highlighted {
    background-color: rgba(74, 156, 247, 0.2);
    border-color: var(--primary-color);
}

.skill-pause.highlighted::before,
.skill-pause.highlighted::after {
    background-color: var(--primary-color, rgba(74, 156, 247, 0.8));
}
"""

ABOUT_SECTION_CSS = """
.about-background {
    height: 100%;
    width: 100%;
    display: flex;
    position: relative;
    background-color: transparent;
    overflow: hidden;
    z-index: 1;
}

.about-block {
    position: relative;
    display: flex;
    flex-direction: column;
    min-height: 80vh;
    padding: 2rem;
}

.about-block-right-aligned {
    display: flex;
    width: 100%;
    justify-content: flex-end;
    padding-right: 4rem;
}
"""
