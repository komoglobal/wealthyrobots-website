
// Main JavaScript functionality
document.addEventListener("DOMContentLoaded", function() {
    // Newsletter signup functionality
    const newsletterForms = document.querySelectorAll(".newsletter-form, .email-signup");
    newsletterForms.forEach(form => {
        form.addEventListener("submit", function(e) {
            e.preventDefault();
            const email = this.querySelector("input[type=email]").value;
            if (email) {
                // Handle newsletter signup
                console.log("Newsletter signup:", email);
                alert("Thank you for subscribing!");
            }
        });
    });
    
    // Load latest articles
    loadLatestArticles();
    
    // Initialize search functionality
    initializeSearch();
});

function loadLatestArticles() {
    // Load articles dynamically
    const articlesContainer = document.getElementById("latest-articles");
    if (articlesContainer) {
        // Fetch and display latest articles
        console.log("Loading latest articles...");
    }
}

function initializeSearch() {
    // Initialize search functionality
    console.log("Search functionality initialized");
}
