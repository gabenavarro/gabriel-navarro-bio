from fasthtml.common import Div, Style, Script

_style = """

.vertical_lines {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100%;
  margin: auto;
  width: 90vw;
}

.vertical_line {
  position: absolute;
  width: 1px;
  height: 100%;
  top: 0;
  left: 10vw;
  background: rgba(255, 255, 255, 0.1);
  overflow: hidden;
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
  animation: drop 7s 0s infinite;
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
    top: 120%;
  }
}
"""

VERTICAL_LINES = Div(
    Style(_style),
    Div(cls="vertical_line"),
    cls="vertical_lines"
)