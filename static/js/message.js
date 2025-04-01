document.addEventListener('DOMContentLoaded', function() {
    const chatItems = document.querySelectorAll('.chat-item');
    const messageInput = document.querySelector('.message-input');
    const sendButton = document.querySelector('.send-button');
    const messagesContainer = document.querySelector('.messages');
    
    // Select conversation
    chatItems.forEach(item => {
        item.addEventListener('click', function() {
            chatItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            
            // In a real app, you would load the conversation messages here
            // For now, we'll just simulate it
            const username = this.querySelector('.username').textContent;
            document.querySelector('.chat-header h2').textContent = username;
            
            // Clear and add some dummy messages
            messagesContainer.innerHTML = `
                <div class="message received">
                    <span class="sender">${username}</span>
                    <p class="text">Hey there! How can I help you today?</p>
                    <span class="time">2 min ago</span>
                </div>
                <div class="message sent">
                    <span class="sender">You</span>
                    <p class="text">I was wondering if you could help me with JavaScript?</p>
                    <span class="time">1 min ago</span>
                </div>
            `;
        });
    });
    
    // Send message
    function sendMessage() {
        const text = messageInput.value.trim();
        if (text) {
            const messageEl = document.createElement('div');
            messageEl.className = 'message sent';
            messageEl.innerHTML = `
                <span class="sender">You</span>
                <p class="text">${text}</p>
                <span class="time">Just now</span>
            `;
            messagesContainer.appendChild(messageEl);
            messageInput.value = '';
            
            // Scroll to bottom
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            // Simulate reply after 1 second
            setTimeout(() => {
                const replyEl = document.createElement('div');
                replyEl.className = 'message received';
                const username = document.querySelector('.chat-header h2').textContent;
                replyEl.innerHTML = `
                    <span class="sender">${username}</span>
                    <p class="text">Sure, I'd be happy to help with that!</p>
                    <span class="time">Just now</span>
                `;
                messagesContainer.appendChild(replyEl);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }, 1000);
        }
    }
    
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Select first conversation by default
    if (chatItems.length > 0) {
        chatItems[0].click();
    }
});