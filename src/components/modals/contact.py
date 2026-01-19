from fasthtml.common import Style, Script, Div, H2, Span, Button
from src.components.base.icons import COPY_ICON, linkedin_icon, github_icon, bluesky_icon
from src.styles import CONTACT_MODAL_CSS

_js = """
document.addEventListener('DOMContentLoaded', () => {
    const openModalBtn = document.querySelector('.open-modal-btn');
    const modalOverlay = document.getElementById('modalOverlay');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const copyEmailBtn = document.getElementById('copyEmailBtn');
    const emailText = document.querySelector('.email-text');

    function openModal() { if(modalOverlay) modalOverlay.style.display = 'block'; }
    function closeModal() { if(modalOverlay) modalOverlay.style.display = 'none'; }
    
    function copyEmail() {
        const email = emailText.textContent;
        navigator.clipboard.writeText(email).then(() => {
            const originalColor = copyEmailBtn.style.backgroundColor;
            copyEmailBtn.style.backgroundColor = '#2e7d32';
            const tooltip = document.createElement('span');
            tooltip.textContent = 'Copied!';
            tooltip.style.cssText = 'position:absolute; background:rgba(0,0,0,0.7); color:white; padding:5px 10px; border-radius:4px; font-size:12px; right:0; top:-30px;';
            copyEmailBtn.style.position = 'relative';
            copyEmailBtn.appendChild(tooltip);
            setTimeout(() => {
                copyEmailBtn.style.backgroundColor = originalColor;
                copyEmailBtn.removeChild(tooltip);
            }, 1500);
        });
    }

    if(openModalBtn) openModalBtn.addEventListener('click', openModal);
    if(closeModalBtn) closeModalBtn.addEventListener('click', closeModal);
    if(copyEmailBtn) copyEmailBtn.addEventListener('click', copyEmail);
    if(modalOverlay) modalOverlay.addEventListener('click', (e) => { if(e.target === modalOverlay) closeModal(); });
});
"""

def ContactModal(email: str = "gchinonavarro@gmail.com"):
    """Returns a modal for contact information."""
    return Div(
        Style(CONTACT_MODAL_CSS),
        Script(_js),
        Div(
            Div(
                Div(
                    H2("Connect", cls="modal-title"),
                    Button("x", cls="close-modal-btn", id="closeModalBtn"),
                    cls="modal-header",
                ),
                Div(
                    Div(
                        Span(email, cls="email-text"),
                        Button(COPY_ICON, id="copyEmailBtn", title="Copy email", cls="copy-btn"),
                        cls="email-container",
                    ),
                    Div(
                        Div(
                            linkedin_icon(),
                            github_icon(),
                            bluesky_icon(),
                            cls="social-links",
                        ),
                    ),
                    cls="modal-content",
                ),
                cls="modal",
            ),
            cls="modal-overlay",
            id="modalOverlay",
        ),
    )
