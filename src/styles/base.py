ROOT_CSS = """
:root {
    --primary-color: #023047;
    --accent-color: #94d2bd;
    --black: rgb(20, 20, 20);
    --white: rgb(238, 238, 238);
    --text-color: #333;
    --light-bg: #f5f8ff;
    --white: #ffffff;
    --container-max-width: 900px;
}

"""

BODY_CSS = """
/* Base styles */
body {
    font-family: system-ui, 'Inter', sans-serif;
    color: var(--text-color);
    line-height: 1.7;
    margin: 0;
    background-color: var(--black); /* rgba(154, 83, 48, 1); */
    overflow-x: hidden;
}

/* Native Scroll-Based Animation */
.scroll-left-hidden {
    opacity: 0;
    filter: blur(5px);
    transform: translateX(-100%);
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
}


.primary-color {
    color: var(--primary-color);
}

. {
    font-weight: bold;
}

"""


