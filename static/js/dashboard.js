document.addEventListener('DOMContentLoaded', function() {
    // Skill request handling
    document.querySelectorAll('.request-actions .btn').forEach(button => {
        button.addEventListener('click', function() {
            const requestItem = this.closest('.request-item');
            const requestId = requestItem.dataset.requestId;
            const action = this.classList.contains('btn-primary') ? 'accept' : 'decline';
            
            fetch(`/skill-request/${requestId}/${action}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrf_token')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    requestItem.remove();
                }
            });
        });
    });

    // Activity feed infinite scroll
    const activityList = document.querySelector('.activity-list');
    if (activityList) {
        let page = 1;
        let loading = false;
        
        window.addEventListener('scroll', function() {
            if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 500 && !loading) {
                loading = true;
                page++;
                
                fetch(`/api/activities?page=${page}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.activities.length > 0) {
                            data.activities.forEach(activity => {
                                const activityItem = document.createElement('div');
                                activityItem.className = 'activity-item';
                                activityItem.innerHTML = `
                                    <div class="activity-icon">
                                        <i class="fas fa-${activity.icon}"></i>
                                    </div>
                                    <div class="activity-content">
                                        <p>${activity.message}</p>
                                        <small class="text-muted">${activity.time_ago} ago</small>
                                    </div>
                                `;
                                activityList.appendChild(activityItem);
                            });
                        }
                        loading = false;
                    });
            }
        });
    }

    // Helper function to get CSRF token
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
});