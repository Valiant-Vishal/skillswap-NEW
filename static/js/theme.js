document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    
    // Check for saved theme preference or use system preference
    const currentTheme = localStorage.getItem('theme') || 
                        (prefersDarkScheme.matches ? 'dark' : 'light');
    
    // Apply the current theme
    if (currentTheme === 'dark') {
        document.body.setAttribute('data-theme', 'dark');
        if (themeToggle) themeToggle.textContent = '☀️ Light Mode';
    } else {
        document.body.removeAttribute('data-theme');
        if (themeToggle) themeToggle.textContent = '☾ Dark Mode';
    }
    
    // Toggle theme when button is clicked
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            let theme;
            if (document.body.getAttribute('data-theme') === 'dark') {
                document.body.removeAttribute('data-theme');
                themeToggle.textContent = '☾ Dark Mode';
                theme = 'light';
            } else {
                document.body.setAttribute('data-theme', 'dark');
                themeToggle.textContent = '☀️ Light Mode';
                theme = 'dark';
            }
            localStorage.setItem('theme', theme);
        });
    }
});