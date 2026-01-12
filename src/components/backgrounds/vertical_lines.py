from fasthtml.common import Div, Style

VERTICAL_LINES_CSS = """
.vertical_lines_container {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
}

.vertical_line {
    position: absolute;
    width: 1px;
    top: 0;
    bottom: 0;
    left: 50%;
    background: rgba(255, 255, 255, 0.05);
}

.vertical_line::after {
    content: '';
    display: block;
    position: absolute;
    height: 15vh;
    width: 100%;
    top: -50%;
    left: 0;
    background: linear-gradient(to bottom, rgba(255, 255, 255, 0) 0%, #ffffff 75%, #ffffff 100%);
    animation: drop 10s 0s infinite;
    animation-fill-mode: forwards;
    animation-timing-function: cubic-bezier(0.4, 0.26, 0, 0.97);
}

.vertical_line:nth-child(1) { transform: translateX(-35vw); }
.vertical_line:nth-child(1)::after { animation-delay: 2s; }
.vertical_line:nth-child(2) { transform: translateX(0); }
.vertical_line:nth-child(2)::after { animation-delay: 4s; }
.vertical_line:nth-child(3) { transform: translateX(35vw); }
.vertical_line:nth-child(3)::after { animation-delay: 2.5s; }

@keyframes drop {
    0% { top: -20%; }
    100% { top: 110%; }
}
"""

VERTICAL_LINE = Div(
    Style(VERTICAL_LINES_CSS),
    Div(cls="vertical_line"),
    Div(cls="vertical_line"),
    Div(cls="vertical_line"),
    cls="vertical_lines_container",
)
