SCROLL_JS = """
document.addEventListener('DOMContentLoaded', () => {

    // Query for both left and right hidden elements
    const hiddenElements = document.querySelectorAll('.scroll-left-hidden, .scroll-right-hidden');
    
    // Function to check if element is in viewport and handle visibility
    const checkVisibility = () => {
        hiddenElements.forEach(element => {
            const rect = element.getBoundingClientRect();
            const windowHeight = window.innerHeight || document.documentElement.clientHeight;
            
            // Element is visible if any part of it is in the viewport
            // We use a small negative value to ensure elements at the very top get detected
            if (rect.top <= windowHeight && rect.bottom >= -50) {
                element.classList.add('scroll-show');
            } else {
                // Only remove the class when element is completely above the viewport
                // This keeps the animation when scrolling down
                if (rect.bottom < 0) {
                    element.classList.remove('scroll-show');
                }
            }
        });
    };
    
    // Run on page load to show elements already in viewport
    checkVisibility();
    
    // Add scroll event listener
    window.addEventListener('scroll', checkVisibility);

});
"""