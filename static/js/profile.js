document.addEventListener('DOMContentLoaded', function() {
    // Follow button functionality
    const followBtn = document.querySelector('.follow-btn');
    if (followBtn) {
        followBtn.addEventListener('click', function() {
            if (this.textContent === 'Follow') {
                this.textContent = 'Following';
                this.style.backgroundColor = '#10b981'; // Success color
            } else {
                this.textContent = 'Follow';
                this.style.backgroundColor = '#3b82f6'; // Primary color
            }
        });
    }
    
    // Skill lists functionality
    function setupSkillList(listId, addButtonId) {
        const list = document.getElementById(listId);
        const addButton = document.getElementById(addButtonId);
        const input = document.querySelector(`#${listId}-input`);
        
        if (addButton && input) {
            addButton.addEventListener('click', function() {
                const skillValue = input.value.trim();
                if (skillValue) {
                    const skillItem = document.createElement('li');
                    skillItem.textContent = skillValue;
                    skillItem.classList.add('skill-item');
                    
                    const removeBtn = document.createElement('button');
                    removeBtn.textContent = '×';
                    removeBtn.classList.add('remove-skill');
                    removeBtn.addEventListener('click', function() {
                        skillItem.remove();
                    });
                    
                    skillItem.appendChild(removeBtn);
                    list.appendChild(skillItem);
                    input.value = '';
                }
            });
        }
    }
    
    setupSkillList('skills-known', 'add-known-skill');
    setupSkillList('skills-learning', 'add-learning-skill');
    setupSkillList('skills-recent', 'add-recent-skill');
    
    // Edit profile button
    const editProfileBtn = document.querySelector('.edit-profile-btn');
    if (editProfileBtn) {
        editProfileBtn.addEventListener('click', function(e) {
            // In a real app, this would navigate to the edit profile page
            // For now, we'll just show an alert
            alert('Redirecting to edit profile page');
        });
    }
});