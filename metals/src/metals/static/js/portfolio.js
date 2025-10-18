// Store portfolio ID in localStorage when viewing a portfolio
function storePortfolioId(portfolioId) {
    localStorage.setItem('lastPortfolioId', portfolioId);
}

// Get last portfolio ID from localStorage
function getLastPortfolioId() {
    return localStorage.getItem('lastPortfolioId');
}

// Update home page button based on whether a portfolio exists
function updateHomeButton() {
    const lastPortfolioId = getLastPortfolioId();
    const form = document.querySelector('form[action="/p"]');
    const button = form?.querySelector('button');
    
    if (lastPortfolioId && button && form) {
        button.textContent = 'Open portfolio';
        form.action = `/p/${lastPortfolioId}`;
        form.method = 'get';
    }
}
