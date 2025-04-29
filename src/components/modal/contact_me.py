from fasthtml.common import Style, Script, Div, H2, Span, Button, A
from src.components.svg import COPY_ICON, linkedin_icon, github_icon, bluesky_icon
css = """

/* Modal background overlay */
.modal-overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 1000;
    animation: fadeIn 0.3s;
}


/* Modal content styling */
.modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: white;

    padding-right: 1rem;
    padding-left: 1rem;
    padding-top: 0;
    padding-bottom: 0.25rem;
    border-radius: 8px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    width: 90%;
    max-width: 400px;
    z-index: 1001;
    animation: slideIn 0.3s;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.modal-title {
    font-size: 2.0rem;
    font-weight: 900;
    margin: 0;
    color: #333;
}

.close-modal-btn {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #888;
    transition: color 0.3s;
}

.close-modal-btn:hover {
    color: #333;
}

.modal-content {
    margin-bottom: 1rem;
    line-height: 1.6;
    color: #555;
}


/* Email container styling */
.email-container {
    display: flex;
    align-items: center;
    background-color: #f5f5f5;
    padding: 0.25rem;
    border-radius: 6px;
    margin-bottom: 24px;
}

.email-text {
    flex-grow: 1;
    font-weight: 500;
}

.copy-btn {
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 0;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background-color 0.3s;
}

.copy-btn:hover {
    background-color: #45a049;
}


/* Social links styling */
.social-links {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 20px;
}



/* Animations */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideIn {
    from { 
        opacity: 0;
        transform: translate(-50%, -60%);
    }
    to { 
        opacity: 1;
        transform: translate(-50%, -50%);
    }
}

"""

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
        Style(css),
        Script(js),
        # Modal Overlay
        Div(
            # Modal Overlay
            Div(
                # Modal Header
                Div(
                    H2("Connect", cls="modal-title"),
                    Button("x", cls="close-modal-btn", id="closeModalBtn"),
                    cls="modal-header"
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
                            cls="copy-btn"
                        ),
                        cls="email-container",
                    ),
                    # Social Links
                    Div(
                        Div(
                            linkedin_icon(),
                            github_icon(),
                            bluesky_icon(),
                            cls="social-links"
                        ),
                    ),


                    cls="modal-content"
                ),
                cls="modal"
            ),
            cls="modal-overlay",
            id="modalOverlay"
        )
    )