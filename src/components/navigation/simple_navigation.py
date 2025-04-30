from fasthtml.common import Div, A, Style

# TODO: Colors based on var from ROOT colors
css = """
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


def simple_navigation(logo: str = "Gabriel Navarro"):
    """ Returns the navigation bar. """
    return Div(
        Div(
            Style(css),
            Div(
                A(logo, href="/", cls="logo"),
                Div(
                    A("Home", href="/", cls="nav-link"),
                    A("Projects", href="/projects", cls="nav-link"),
                    A("Contact", href="#", cls="nav-link open-modal-btn"), # To open modal
                    cls="nav-links"
                ),
                cls="nav-container container"
            ),
            cls="navbar"
        ),
        Div(style="height: 10vh;"),
    )