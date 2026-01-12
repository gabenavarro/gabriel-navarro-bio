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
