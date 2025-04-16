from fasthtml.common import Div, Style, Script

_style = """

.vertical_lines {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    margin: auto;
    width: 90vw;
    z-index: 100;
}

.vertical_line {
    position: absolute;
    width: 1px;
    top: 0;
    bottom: 0;
    left: 10vw;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.01);
    z-index: 100;
}

.vertical_line::after {
    content: '';
    display: block;
    position: absolute;
    height: 15vh;
    width: 100%;
    top: -50%;
    left: 0;
    z-index: 100;
    background: linear-gradient(to bottom, rgba(255, 255, 255, 0) 0%, #ffffff 75%, #ffffff 100%);
    animation: drop 10s 0s infinite;
    animation-fill-mode: forwards;
    animation-timing-function: cubic-bezier(0.4, 0.26, 0, 0.97);
}

.vertical_line:nth-child(1) {
    margin-left: -25%;
}

.vertical_line:nth-child(1)::after {
    animation-delay: 2s;
}

.vertical_line:nth-child(3) {
    margin-left: 25%;
}

.vertical_line:nth-child(3)::after {
    animation-delay: 2.5s;
}

@keyframes drop {
    0% {
        top: -20%;
    }
    100% {
        top: 110%;
    }
}
"""


_script = """
// Function to update the height of vertical lines
function updateVerticalLinesHeight() {
    // Get the document height (maximum of these values ensures cross-browser compatibility)
    const docHeight = Math.max(
        document.body.scrollHeight,
        document.body.offsetHeight,
        document.documentElement.clientHeight,
        document.documentElement.scrollHeight,
        document.documentElement.offsetHeight
    );
    
    // Set the height of the vertical lines container
    const verticalLines = document.getElementById('verticalLines');
    verticalLines.style.height = docHeight + 'px';
    
    // Set the height for each individual line
    const lines = document.querySelectorAll('.vertical_line');
    lines.forEach(line => {
        line.style.height = docHeight + 'px';
    });
}

// Update heights on initial load
updateVerticalLinesHeight();

// Update heights when window is resized
window.addEventListener('resize', updateVerticalLinesHeight);

// Update heights when content changes (if you have dynamic content)
const observer = new MutationObserver(updateVerticalLinesHeight);
observer.observe(document.body, { childList: true, subtree: true });

// For demonstration: Add more content dynamically after 2 seconds
setTimeout(() => {
    const extraContent = document.getElementById('extra-content');
    for (let i = 0; i < 20; i++) {
        const p = document.createElement('p');
        p.textContent = `Dynamically added paragraph ${i+1}. The vertical lines should still extend all the way.`;
        extraContent.appendChild(p);
    }
}, 2000);
"""


VERTICAL_LINE = Div(
    Script(_script),
    Style(_style),
    cls="vertical_line",
    id="verticalLines"
)