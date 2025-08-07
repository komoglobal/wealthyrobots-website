// WealthyRobot Empire - Interactive JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize website functionality
    initializeWebsite();
    
    // Load latest articles
    loadLatestArticles();
    
    // Setup form handlers
    setupFormHandlers();
});

function initializeWebsite() {
    console.log('🤖 WealthyRobot Empire Website Initialized');
    
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.value-item, .article-card').forEach(el => {
        observer.observe(el);
    });
}

function loadLatestArticles() {
    // Simulate loading latest articles
    const articlesGrid = document.getElementById('latest-articles');
    if (!articlesGrid) return;
    
    const sampleArticles = [
        {
            title: 'AI Revenue Automation: From $0 to $50K Monthly',
            excerpt: 'Learn proven strategies to build automated revenue streams using AI...',
            image: '/assets/images/ai-automation.jpg',
            date: '2025-08-06',
            readTime: '8 min read'
        },
        {
            title: 'The 5 AI Tools Every Entrepreneur Needs',
            excerpt: 'Discover the essential AI tools that can transform your business...',
            image: '/assets/images/ai-tools.jpg',
            date: '2025-08-05',
            readTime: '6 min read'
        },
        {
            title: 'Building Passive Income with AI Automation',
            excerpt: 'Step-by-step guide to creating automated income streams...',
            image: '/assets/images/passive-income.jpg',
            date: '2025-08-04',
            readTime: '10 min read'
        }
    ];
    
    sampleArticles.forEach(article => {
        const articleCard = createArticleCard(article);
        articlesGrid.appendChild(articleCard);
    });
}

function createArticleCard(article) {
    const card = document.createElement('div');
    card.className = 'article-card';
    
    card.innerHTML = `
        <img src="${article.image}" alt="${article.title}" onerror="this.src='/assets/images/default-article.jpg'">
        <div class="article-content">
            <h3>${article.title}</h3>
            <p>${article.excerpt}</p>
            <div class="article-meta">
                <span>${article.date}</span>
                <span>${article.readTime}</span>
            </div>
        </div>
    `;
    
    return card;
}

function setupFormHandlers() {
    // Email signup form handler
    const emailForms = document.querySelectorAll('.email-signup, .newsletter-form');
    
    emailForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = this.querySelector('input[type="email"]').value;
            if (email) {
                // Simulate form submission
                showSuccessMessage('🎉 Welcome to the WealthyRobot Empire! Check your email for exclusive content.');
                this.reset();
            }
        });
    });
}

function showSuccessMessage(message) {
    // Create success notification
    const notification = document.createElement('div');
    notification.className = 'success-notification';
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #10b981;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 5000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Analytics tracking
function trackEvent(eventName, data = {}) {
    // Google Analytics 4 event tracking
    if (typeof gtag !== 'undefined') {
        gtag('event', eventName, data);
    }
    
    // Custom analytics
    console.log('📊 Event tracked:', eventName, data);
}

// Track page views
trackEvent('page_view', {
    page_title: document.title,
    page_location: window.location.href
});

// Track form submissions
document.addEventListener('submit', function(e) {
    if (e.target.matches('.email-signup, .newsletter-form')) {
        trackEvent('form_submit', {
            form_name: e.target.className,
            page_location: window.location.href
        });
    }
});