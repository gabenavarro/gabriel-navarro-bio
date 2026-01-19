from fasthtml.svg import Svg, Path, Rect, Circle
from fasthtml.common import A, Style

SOCIAL_BTN_CSS = """
.social-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    color: white;
    transition: transform 0.3s, box-shadow 0.3s;
}

.social-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
"""

def linkedin_icon(
    href: str = "https://www.linkedin.com/in/gcnavarro/",
    color: str = "#0077B5",
):
    linkedin_css = (
        SOCIAL_BTN_CSS
        + f"""
.linkedin {{
    background-color: {color};
}}
    """
    )
    return A(
        Style(linkedin_css),
        Svg(
            Path(
                d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"
            ),
            Rect(x="2", y="9", width="4", height="12"),
            Circle(cx="4", cy="4", r="2"),
            xmlns="http://www.w3.org/2000/svg",
            width="20",
            height="20",
            viewBox="0 0 24 24",
            fill="none",
            stroke="currentColor",
            stroke_width="2",
            stroke_linecap="round",
            stroke_linejoin="round",
        ),
        href=href,
        cls="social-btn linkedin",
        title="LinkedIn",
    )

def github_icon(
    href: str = "https://github.com/gabenavarro",
    color: str = "#333",
):
    github_css = (
        SOCIAL_BTN_CSS
        + f"""
.github {{
    background-color: {color};
}}
    """
    )
    return A(
        Style(github_css),
        Svg(
            Path(
                d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"
            ),
            xmlns="http://www.w3.org/2000/svg",
            width="20",
            height="20",
            viewBox="0 0 24 24",
            fill="none",
            stroke="currentColor",
            stroke_width="2",
            stroke_linecap="round",
            stroke_linejoin="round",
        ),
        href=href,
        cls="social-btn github",
        title="GitHub",
    )

def bluesky_icon(
    href: str = "https://bsky.app/profile/gcnavarro.bsky.social", color: str = "#1DA1F2"
):
    bluesky_css = (
        SOCIAL_BTN_CSS
        + f"""
.bluesky {{
    background-color: {color};
}}
    """
    )
    return A(
        Style(bluesky_css),
        Svg(
            Path(d="M12 2L2 12l4 2 2 8 4-6 6 2 4-16z"),
            xmlns="http://www.w3.org/2000/svg",
            width="20",
            height="20",
            viewBox="0 0 24 24",
            fill="none",
            stroke="currentColor",
            stroke_width="2",
            stroke_linecap="round",
            stroke_linejoin="round",
        ),
        href=href,
        cls="social-btn bluesky",
        title="Bluesky",
    )

COPY_ICON = Svg(
    Rect(x="9", y="9", width="13", height="13", rx="2", ry="2"),
    Path(d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"),
    xmlns="http://www.w3.org/2000/svg",
    width="16",
    height="16",
    viewBox="0 0 24 24",
    fill="none",
    stroke="currentColor",
    stroke_width="2",
    stroke_linecap="round",
    stroke_linejoin="round",
)
