// ============================================
// NENO AI - Enhanced JavaScript Features
// ============================================

class NenoChat {
    constructor() {
        this.chatBox = document.getElementById('chatBox');
        this.messageInput = document.getElementById('messageInput');
        this.chatForm = document.getElementById('chatForm');
        this.sendBtn = document.getElementById('sendBtn');
        
        this.init();
    }

    init() {
        // Essential event listeners
        this.bindEvents();
        
        // Initial setup
        this.scrollToBottom();
        this.focusInput();
        
        // Enhanced features
        this.setupTypingIndicator();
        this.setupSmoothAnimations();
        this.setupSoundEffects();
        
        console.log('🚀 Neno AI JavaScript loaded!');
    }

    // Core functionality
    bindEvents() {
        // Form submission
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });

        // Enter key (with Shift for new line)
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Input effects
        this.messageInput.addEventListener('input', () => {
            this.toggleSendButton();
        });

        // Window resize
        window.addEventListener('resize', () => {
            this.scrollToBottom();
        });
    }

    sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || message.length > 500) return;

        // Visual feedback
        this.showTypingIndicator();
        this.sendBtn.disabled = true;
        this.sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

        // Submit form (backend handles AI response)
        this.chatForm.submit();
    }

    // UI Enhancements
    scrollToBottom(smooth = true) {
        if (smooth) {
            this.chatBox.scrollTo({
                top: this.chatBox.scrollHeight,
                behavior: 'smooth'
            });
        } else {
            this.chatBox.scrollTop = this.chatBox.scrollHeight;
        }
    }

    focusInput() {
        this.messageInput.focus();
    }

    toggleSendButton() {
        const message = this.messageInput.value.trim();
        this.sendBtn.style.opacity = message ? '1' : '0.5';
        this.sendBtn.disabled = !message;
    }

    // Typing indicator
    showTypingIndicator() {
        // Remove any existing typing indicators
        const existing = this.chatBox.querySelector('.typing-indicator');
        if (existing) existing.remove();

        // Add new typing indicator
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-indicator';
        typingDiv.innerHTML = `
            <div class="message-content">
                <div class="typing-dots">
                    <span></span><span></span><span></span>
                </div>
                <small>Neno is typing...</small>
            </div>
        `;
        this.chatBox.appendChild(typingDiv);
        this.scrollToBottom(false);
    }

    // Smooth animations
    setupSmoothAnimations() {
        const messages = this.chatBox.querySelectorAll('.message');
        messages.forEach((msg, index) => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(20px)';
            setTimeout(() => {
                msg.style.transition = 'all 0.4s ease';
                msg.style.opacity = '1';
                msg.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }

    // Sound effects (optional)
    setupSoundEffects() {
        // Create audio context for subtle effects
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            console.log('Audio not supported');
        }
    }

    playSendSound() {
        if (!this.audioContext) return;
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.frequency.value = 800;
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.1);
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + 0.1);
    }

    // Auto-hide clear button after inactivity
    setupFabAnimation() {
        const fab = document.querySelector('.fab-container');
        let timeout;
        
        const showFab = () => {
            clearTimeout(timeout);
            fab.style.opacity = '1';
            fab.style.transform = 'translateY(0)';
        };
        
        const hideFab = () => {
            timeout = setTimeout(() => {
                fab.style.opacity = '0';
                fab.style.transform = 'translateY(20px)';
            }, 3000);
        };
        
        document.addEventListener('mousemove', showFab);
        document.addEventListener('keydown', showFab);
        hideFab();
    }

    // Message counter
    updateMessageCounter() {
        const messages = this.chatBox.querySelectorAll('.message').length;
        const counter = document.getElementById('message-counter');
        if (counter) {
            counter.textContent = `Messages: ${Math.floor(messages/2)}`;
        }
    }
}

// Initialize Neno when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.nenoChat = new NenoChat();
    
    // Fade in animation
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

// Service Worker for offline support (optional)
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
        .then(() => console.log('Neno SW registered'))
        .catch(() => console.log('No SW support'));
}