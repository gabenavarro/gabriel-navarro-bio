# Component Styles

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

BALL_BACKGROUND_CSS = """
.ball_background {
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
