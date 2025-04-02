document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('expanded');
            
            // Save state in localStorage
            if (sidebar.classList.contains('expanded')) {
                localStorage.setItem('sidebarState', 'expanded');
            } else {
                localStorage.setItem('sidebarState', 'collapsed');
            }
        });
        
        // Check for saved state
        const sidebarState = localStorage.getItem('sidebarState');
        if (sidebarState === 'expanded') {
            sidebar.classList.add('expanded');
        }
    }
    
    // Tooltips for sidebar items
    const sidebarItems = document.querySelectorAll('.nav-item');
    sidebarItems.forEach(item => {
        const tooltip = item.getAttribute('data-tooltip');
        if (tooltip) {
            item.addEventListener('mouseenter', function() {
                const tooltipEl = document.createElement('div');
                tooltipEl.className = 'sidebar-tooltip';
                tooltipEl.textContent = tooltip;
                document.body.appendChild(tooltipEl);
                
                const rect = item.getBoundingClientRect();
                tooltipEl.style.top = `${rect.top + window.scrollY}px`;
                tooltipEl.style.left = `${rect.right + window.scrollX + 10}px`;
                
                item.addEventListener('mouseleave', function() {
                    tooltipEl.remove();
                });
            });
        }
    });
});