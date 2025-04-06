from fasthtml.common import Div, Style, Script


_parallax_style = """
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

/* Sun/moon */
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

/* Mountains in the background */
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
    clip-path: polygon(
        0% 100%,
        15% 60%,
        25% 70%,
        35% 50%,
        45% 65%,
        55% 45%,
        65% 55%,
        75% 35%,
        85% 45%,
        100% 20%,
        100% 100%
    );
}

.mountain-bg-2 {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 80%;
    background: #ba584a;
    opacity: 0.6;
    clip-path: polygon(
        0% 100%,
        10% 70%,
        20% 85%,
        30% 65%,
        40% 80%,
        50% 60%,
        60% 75%,
        70% 55%,
        80% 70%,
        90% 50%,
        100% 65%,
        100% 100%
    );
}

/* Water surface */
.water {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 50%;
    background: linear-gradient(180deg, #a34936 0%, #773428 100%);
    opacity: 0.8;
}

/* Water reflection */
.water-reflection {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 50%;
    background: repeating-linear-gradient(
        90deg,
        rgba(255, 255, 255, 0.1) 0px,
        rgba(255, 255, 255, 0.1) 20px,
        rgba(255, 255, 255, 0) 20px,
        rgba(255, 255, 255, 0) 40px
    );
}

/* Sun reflection */
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

/* Mountains foreground */
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
    clip-path: polygon(
        0% 100%,
        20% 80%,
        30% 70%,
        40% 60%,
        50% 65%,
        70% 35%,
        100% 100%
    );
}

.mountain-fg-right {
    position: absolute;
    bottom: 0;
    right: 0;
    width: 35%;
    height: 40%;
    background: #45211b;
    clip-path: polygon(
        0% 100%,
        30% 60%,
        60% 70%,
        100% 40%,
        100% 100%
    );
}

/* Tree silhouette */
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

/* Parallax effect */
@media (hover: hover) {
    .parallax-landscape {
        perspective: 1000px;
    }
    
    .sun, .mountains-bg, .water, .mountains-fg, .tree {
        will-change: transform;
        transition: transform 0.1s ease-out;
    }
}

/* Mouse movement parallax effect */
.parallax-active {
    transition: transform 0.1s ease-out;
}
"""


_parallax_script = """
document.addEventListener('DOMContentLoaded', function() {
    const parallaxBg = document.querySelector('.parallax-landscape');
    const sun = document.querySelector('.sun');
    const mountainsBg = document.querySelector('.mountains-bg');
    const water = document.querySelector('.water');
    const mountainsFg = document.querySelector('.mountains-fg');
    const tree = document.querySelector('.tree');
    
    document.addEventListener('mousemove', function(e) {
        if (!parallaxBg) return;
        
        const mouseX = e.clientX / window.innerWidth - 0.5;
        const mouseY = e.clientY / window.innerHeight - 0.5;
        
        // Move elements at different speeds for parallax effect
        if (sun) sun.style.transform = `translate(calc(-50% + ${mouseX * 20}px), ${mouseY * 10}px)`;
        if (mountainsBg) mountainsBg.style.transform = `translateX(${mouseX * 15}px)`;
        if (water) water.style.transform = `translateY(${mouseY * 5}px)`;
        if (mountainsFg) mountainsFg.style.transform = `translateX(${mouseX * 30}px)`;
        if (tree) tree.style.transform = `translate(${mouseX * 10}px, 50%)`;
    });
});
"""


SUNSET_PARALLAX = Div(
    # Script to handle mouse movement for parallax effect
    Script(_parallax_script),

    # Parallax style
    Style(_parallax_style),
    
    # Sun
    Div(cls="sun"),
    
    # Background mountains
    Div(
        Div(cls="mountain-bg"),
        Div(cls="mountain-bg-2"),
        cls="mountains-bg"
    ),
    
    # Water
    Div(cls="water"),
    
    # Water reflection with lines
    Div(cls="water-reflection"),
    
    # Sun reflection on water
    Div(cls="sun-reflection"),
    
    # Foreground mountains
    Div(
        Div(cls="mountain-fg-left"),
        Div(cls="mountain-fg-right"),
        cls="mountains-fg"
    ),
    
    # Tree silhouette
    Div(
        Div(cls="tree-branch-1"),
        Div(cls="tree-branch-2"),
        cls="tree"
    ),
    
    cls="parallax-landscape"
)