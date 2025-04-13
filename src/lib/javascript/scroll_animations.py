SCROLL_JS = """
document.addEventListener('DOMContentLoaded', () => {

    const hiddenElements = document.querySelectorAll('.scroll-left-hidden');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('scroll-show');
            } else {
                entry.target.classList.remove('scroll-show');
            }
        });
    });

    hiddenElements.forEach((el) => observer.observe(el));
});
"""