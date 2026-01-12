from fasthtml.common import Style, Script, Div, H2, Span, Button
from src.components.svg import COPY_ICON, linkedin_icon, github_icon, bluesky_icon
from src.lib.css import CONTACT_MODAL_CSS

js = """
document.addEventListener('DOMContentLoaded', () => {
    // Get DOM elements
    const openModalBtn = document.querySelector('.open-modal-btn');
    const modalOverlay = document.getElementById('modalOverlay');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const modal = document.querySelector('.modal');
    const copyEmailBtn = document.getElementById('copyEmailBtn');
    const emailText = document.querySelector('.email-text');

    // Function to open modal
    function openModal() {
        modalOverlay.style.display = 'block';
    }

    // Function to close modal
    function closeModal() {
        modalOverlay.style.display = 'none';
    }

    // Function to copy email to clipboard
    function copyEmail() {
        const email = emailText.textContent;
        navigator.clipboard.writeText(email)
            .then(() => {
                // Show feedback (optional)
                const originalColor = copyEmailBtn.style.backgroundColor;
                copyEmailBtn.style.backgroundColor = '#2e7d32';

                // Create and show tooltip
                const tooltip = document.createElement('span');
                tooltip.textContent = 'Copied!';
                tooltip.style.position = 'absolute';
                tooltip.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
                tooltip.style.color = 'white';
                tooltip.style.padding = '5px 10px';
                tooltip.style.borderRadius = '4px';
                tooltip.style.fontSize = '12px';
                tooltip.style.right = '0';
                tooltip.style.top = '-30px';

                copyEmailBtn.style.position = 'relative';
                copyEmailBtn.appendChild(tooltip);

                // Reset after animation
                setTimeout(() => {
                    copyEmailBtn.style.backgroundColor = originalColor;
                    copyEmailBtn.removeChild(tooltip);
                }, 1500);
            })
            .catch(err => {
                console.error('Failed to copy: ', err);
            });
    }

    // Event listener for open button
    openModalBtn.addEventListener('click', openModal);

    // Event listener for close button
    closeModalBtn.addEventListener('click', closeModal);

    // Event listener for copy button
    copyEmailBtn.addEventListener('click', copyEmail);

    // Event listener for clicking outside modal
    modalOverlay.addEventListener('click', function(event) {
        // Only close if the click is directly on the overlay, not on the modal itself
        if (event.target === modalOverlay) {
            closeModal();
        }
    });
});
"""


def contact_me_modal(email: str = "gchinonavarro@gmail.com"):
    return Div(
        Style(CONTACT_MODAL_CSS),
        Script(js),
        # Modal Overlay
        Div(
            # Modal Overlay
            Div(
                # Modal Header
                Div(
                    H2("Connect", cls="modal-title"),
                    Button("x", cls="close-modal-btn", id="closeModalBtn"),
                    cls="modal-header",
                ),
                # Modal Content
                Div(
                    # Email Container
                    Div(
                        Span(email, cls="email-text"),
                        Button(
                            COPY_ICON,
                            id="copyEmailBtn",
                            title="Copy email",
                            cls="copy-btn",
                        ),
                        cls="email-container",
                    ),
                    # Social Links
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
