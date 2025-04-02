document.addEventListener('DOMContentLoaded', function() {
    const skillSearch = document.getElementById('skill-search');
    const categoryFilter = document.getElementById('category-filter');
    const proficiencyFilter = document.getElementById('proficiency-filter');
    const locationFilter = document.getElementById('location-filter');
    
    // Function to filter skills
    function filterSkills() {
        const searchTerm = skillSearch.value.toLowerCase();
        const category = categoryFilter.value;
        const proficiency = proficiencyFilter.value;
        const location = locationFilter.value;
        
        document.querySelectorAll('.skill-card').forEach(card => {
            const skillName = card.querySelector('h4').textContent.toLowerCase();
            const skillCategory = card.querySelector('.skill-category').textContent.toLowerCase();
            const skillProficiency = card.querySelector('.skill-proficiency').textContent.toLowerCase();
            const skillLocation = card.querySelector('.user-location').textContent.toLowerCase();
            
            const matchesSearch = skillName.includes(searchTerm);
            const matchesCategory = !category || skillCategory === category.toLowerCase();
            const matchesProficiency = !proficiency || skillProficiency === proficiency.toLowerCase();
            const matchesLocation = !location || 
                (location === 'local' && skillLocation.includes('your city')) ||
                (location === 'online' && skillLocation.includes('online'));
            
            if (matchesSearch && matchesCategory && matchesProficiency && matchesLocation) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }
    
    // Event listeners for filters
    skillSearch.addEventListener('input', filterSkills);
    categoryFilter.addEventListener('change', filterSkills);
    proficiencyFilter.addEventListener('change', filterSkills);
    locationFilter.addEventListener('change', filterSkills);
    
    // Request skill swap buttons
    document.querySelectorAll('.skill-actions .btn-primary').forEach(button => {
        button.addEventListener('click', function() {
            const skillId = this.closest('.skill-card').dataset.skillId;
            // Implement skill swap request
            console.log('Request skill swap for:', skillId);
        });
    });

    // Handle radio buttons
    const radioButtons = document.querySelectorAll('input[type="radio"][name="search_type"]');
    
    // Add custom styling for checked radio buttons
    radioButtons.forEach(radio => {
        // Check initial state
        updateRadioStyle(radio);
        
        // Update on change
        radio.addEventListener('change', function() {
            radioButtons.forEach(updateRadioStyle);
        });
    });
    
    function updateRadioStyle(radio) {
        if (radio.checked) {
            radio.style.backgroundColor = 'transparent';
            // Create or update after element
            setTimeout(() => {
                if (!radio.nextElementSibling.classList.contains('radio-dot')) {
                    const dot = document.createElement('span');
                    dot.className = 'radio-dot';
                    dot.style.cssText = 'position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 8px; height: 8px; border-radius: 50%; background-color: #fff;';
                    radio.parentNode.insertBefore(dot, radio.nextSibling);
                }
            }, 0);
            
            // Highlight the text
            if (radio.nextElementSibling.tagName === 'SPAN') {
                radio.nextElementSibling.style.color = 'var(--primary)';
                radio.nextElementSibling.style.fontWeight = '500';
            }
        } else {
            // Remove the dot if exists
            const nextElem = radio.nextElementSibling;
            if (nextElem && nextElem.classList.contains('radio-dot')) {
                radio.parentNode.removeChild(nextElem);
            }
            
            // Reset text styling
            if (radio.nextElementSibling && radio.nextElementSibling.tagName === 'SPAN') {
                radio.nextElementSibling.style.color = '';
                radio.nextElementSibling.style.fontWeight = '';
            }
        }
    }
});