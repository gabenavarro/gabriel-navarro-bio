from fasthtml.common import Style, Script, Div, H2, Span, Button, A, Img
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


/* Icon styles */
.linkedin {
    background-color: #0077B5;
}

.github {
    background-color: #333;
}

.bluesky {
    background-color: #1DA1F2;
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
from fasthtml.svg import Svg, Path, Rect, Circle


def get_modal(email: str = "gchinonavarro@gmail.com"):
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
                            Svg(
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
                                stroke_linejoin="round"
                            ),
                            id="copyEmailBtn",
                            title="Copy email",
                            cls="copy-btn"
                        ),
                        cls="email-container",
                    ),
                    # Social Links
                    Div(
                        Div(
                            A(
                                # LinkedIn Icon
                                Svg(
                                    Path(d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"),
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
                                    stroke_linejoin="round"
                                ),
                                href="https://www.linkedin.com/in/gcnavarro/",
                                cls="social-btn linkedin",
                                title="LinkedIn"
                            ),
                            A(
                                # GitHub Icon
                                Svg(
                                    Path(d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"),
                                    xmlns="http://www.w3.org/2000/svg",
                                    width="20", 
                                    height="20", 
                                    viewBox="0 0 24 24", 
                                    fill="none", 
                                    stroke="currentColor", 
                                    stroke_width="2", 
                                    stroke_linecap="round", 
                                    stroke_linejoin="round"
                                ),
                                href="https://github.com/gabenavarro",
                                cls="social-btn github",
                                title="GitHub"
                            ),
                            A(
                                # Bluesky Icon
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
                                    stroke_linejoin="round"
                                ),
                                href="https://bsky.app/profile/gcnavarro.bsky.social",
                                cls="social-btn bluesky",
                                title="Bluesky"
                            ),
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