document.addEventListener('DOMContentLoaded', function() {
    const mobileMenu = document.querySelector('.mobile-menu');
    const navLinks = document.querySelector('.nav-links');
    const navbar = document.querySelector('.navbar');
    let isMenuOpen = false;

    // Toggle menu function
    mobileMenu.addEventListener('click', function() {
        isMenuOpen = !isMenuOpen;
        
        // Toggle the icon between bars and X
        mobileMenu.innerHTML = isMenuOpen ? 
            '<i class="fas fa-times"></i>' : 
            '<i class="fas fa-bars"></i>';
        
        // Toggle the menu visibility
        navLinks.classList.toggle('nav-active');
        
        // Prevent body scrolling when menu is open
        document.body.style.overflow = isMenuOpen ? 'hidden' : 'auto';
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        if (isMenuOpen && !navbar.contains(event.target)) {
            isMenuOpen = false;
            mobileMenu.innerHTML = '<i class="fas fa-bars"></i>';
            navLinks.classList.remove('nav-active');
            document.body.style.overflow = 'auto';
        }
    });

    // Close menu when clicking a link
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function() {
            if (isMenuOpen) {
                isMenuOpen = false;
                mobileMenu.innerHTML = '<i class="fas fa-bars"></i>';
                navLinks.classList.remove('nav-active');
                document.body.style.overflow = 'auto';
            }
        });
    });

});