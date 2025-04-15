SCROLL_JS = """
document.addEventListener('DOMContentLoaded', () => {

    // Query for both left and right hidden elements
    const hiddenElements = document.querySelectorAll('.scroll-left-hidden, .scroll-right-hidden');
    
    // Track elements that have been scrolled past
    const scrolledElements = new Set();
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            // Get the position of the element relative to the viewport
            const boundingRect = entry.target.getBoundingClientRect();
            const elementTop = boundingRect.top;
            
            if (entry.isIntersecting) {
                // Element is visible in the viewport, add the show class
                entry.target.classList.add('scroll-show');
                
                // Add this element to our tracked set
                scrolledElements.add(entry.target);
            } else {
                // Element is not visible
                // Only remove the class if we're scrolling up and the element is above the viewport
                if (elementTop > 0) { // Element is above the viewport
                    entry.target.classList.remove('scroll-show');
                    scrolledElements.delete(entry.target);
                }
                // If scrolling down (elementTop <= 0), keep the class
            }
        });
    }, {
        // Adding a small threshold to ensure smoother transitions
        threshold: 0.1
    });

    hiddenElements.forEach((el) => observer.observe(el));
});
"""