document.addEventListener("DOMContentLoaded", () => {
    const chatFeed = document.getElementById('chat-feed');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const ingestBtn = document.getElementById('ingest-btn');
    const ingestStatus = document.getElementById('ingest-status');
    const ingestIcon = document.getElementById('ingest-icon');

    // Auto-resize textarea
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // Enter to send (Shift+Enter for newline)
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    });

    sendBtn.addEventListener('click', handleSend);

    async function handleSend() {
        const text = userInput.value.trim();
        if (!text) return;

        // Reset input
        userInput.value = '';
        userInput.style.height = 'auto';
        sendBtn.disabled = true;

        // Append User Message
        appendMessage('user', text);

        // Append typing indicator
        const typingId = appendTypingIndicator();
        scrollToBottom();

        try {
            const response = await fetch('http://localhost:8000/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: text, top_k: 4 })
            });

            if (!response.ok) {
                throw new Error(`API returned status ${response.status}`);
            }

            const data = await response.json();
            
            // Remove typing indicator
            document.getElementById(typingId).remove();
            
            // Append AI response
            appendMessage('ai', data.answer, data.sources);
        } catch (error) {
            document.getElementById(typingId).remove();
            appendMessage('ai', `**Error:** An issue occurred while contacting the RAG backend. Make sure the FastAPI server is running on localhost:8000.\n\n\`${error.message}\``);
        }

        sendBtn.disabled = false;
        scrollToBottom();
    }

    function appendMessage(role, text, sources = []) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}-message slip-in`;

        // Avatar
        const avatar = document.createElement('div');
        avatar.className = `avatar ${role}-avatar`;
        avatar.textContent = role === 'ai' ? 'AI' : 'US';

        // Content Card
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content glass-card';
        
        // Parse markdown if AI
        if (role === 'ai') {
            contentDiv.innerHTML = marked.parse(text);
        } else {
            const p = document.createElement('p');
            p.textContent = text;
            contentDiv.appendChild(p);
        }

        // Add Sources mapping
        if (sources && sources.length > 0) {
            const sourcesDiv = document.createElement('div');
            sourcesDiv.className = 'sources-container';
            
            // Deduplicate source files visually
            const uniqueDocs = [...new Set(sources.map(s => s.document))];
            
            uniqueDocs.forEach(doc => {
                const pill = document.createElement('div');
                pill.className = 'source-pill';
                pill.innerHTML = `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg> ${doc}`;
                pill.title = 'Matching chunks found in this document.';
                sourcesDiv.appendChild(pill);
            });
            contentDiv.appendChild(sourcesDiv);
        }

        if (role === 'user') {
            msgDiv.appendChild(contentDiv);
            msgDiv.appendChild(avatar);
        } else {
            msgDiv.appendChild(avatar);
            msgDiv.appendChild(contentDiv);
        }

        chatFeed.appendChild(msgDiv);
    }

    function appendTypingIndicator() {
        const id = 'typing-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.id = id;
        msgDiv.className = `message ai-message slip-in`;

        msgDiv.innerHTML = `
            <div class="avatar ai-avatar">AI</div>
            <div class="message-content glass-card">
                <div class="spinner"></div>
            </div>
        `;
        chatFeed.appendChild(msgDiv);
        return id;
    }

    function scrollToBottom() {
        chatFeed.scrollTop = chatFeed.scrollHeight;
    }

    // Handle Admin Ingestion
    ingestBtn.addEventListener('click', async () => {
        ingestIcon.textContent = '⏳';
        ingestBtn.disabled = true;
        ingestStatus.textContent = 'Rebuilding index...';

        try {
            const response = await fetch('http://localhost:8000/ingest', { method: 'POST' });
            if (!response.ok) throw new Error('Ingest failed');
            const data = await response.json();
            
            ingestIcon.textContent = '✅';
            ingestStatus.textContent = `${data.chunks_indexed} chunks indexed.`;
            setTimeout(() => {
                ingestIcon.textContent = '⚡';
                ingestStatus.textContent = '';
                ingestBtn.disabled = false;
            }, 3000);
        } catch (error) {
            ingestIcon.textContent = '❌';
            ingestStatus.textContent = 'Error building index.';
            setTimeout(() => {
                ingestIcon.textContent = '⚡';
                ingestStatus.textContent = '';
                ingestBtn.disabled = false;
            }, 3000);
        }
    });
});
