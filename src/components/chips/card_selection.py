
from typing import List, Tuple
from fasthtml.common import Div, Button, Style


css = """
/* Chip container styles */
.chip-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 20px;
    padding: 16px;
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
    color: #f44336;
    outline: #f44336;
}

.chip.blue {
    color: #2196f3;
    outline: #2196f3;
}

.chip.green {
    color: #43a047;
    outline: #43a047;
}

.chip.yellow {
    color: #ff9800;
    outline: #ff9800;
}


.chip:hover {
    background-color: #e0e0e0;
}


/* Selected chip styles */
.chip.red.selected {
    background-color: #e91e63;
    color: white;
}

.chip.blue.selected {
    background-color: #1976d2;
    color: white;
}

.chip.green.selected {
    background-color: #43a047;
    color: white;
}

.chip.yellow.selected {
    background-color: #ff9800;
    color: white;
}
"""

def filter_chips(chips: List[Tuple[str,str]]):
    return Div(
        Style(css),
        *[Button(name, cls=f"chip {color}") for name, color in chips],
        cls="chip-container",
    )


# .chip-blue {
#     display: inline-flex;
#     align-items: center;
#     justify-content: center;
#     padding: 10px 20px;
#     border-radius: 50px;
#     font-size: 16px;
#     font-weight: 500;
#     cursor: pointer;
#     transition: all 0.2s ease;
#     user-select: none;
#     border: none;
#     background-color: rgba(255, 255, 255, 0.1);
#     color: #2196f3;
#     outline: #2196f3;
# }

# .chip-green {
#     display: inline-flex;
#     align-items: center;
#     justify-content: center;
#     padding: 10px 20px;
#     border-radius: 50px;
#     font-size: 16px;
#     font-weight: 500;
#     cursor: pointer;
#     transition: all 0.2s ease;
#     user-select: none;
#     border: none;
#     background-color: rgba(255, 255, 255, 0.1);
#     color: #4caf50;
#     outline: #4caf50;
# }

# .chip-yellow {
#     display: inline-flex;
#     align-items: center;
#     justify-content: center;
#     padding: 10px 20px;
#     border-radius: 50px;
#     font-size: 16px;
#     font-weight: 500;
#     cursor: pointer;
#     transition: all 0.2s ease;
#     user-select: none;
#     border: none;
#     background-color: rgba(255, 255, 255, 0.1);
#     color: #ffeb3b;
#     outline: #ffeb3b;
# }