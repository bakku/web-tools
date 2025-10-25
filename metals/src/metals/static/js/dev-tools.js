// Dev tools functionality for development mode

function initDevTools() {
    const devToolsSelect = document.getElementById('dev-tools-select');
    
    if (devToolsSelect) {
        devToolsSelect.addEventListener('change', function(e) {
            const action = e.target.value;
            
            if (action === 'clear-portfolio-storage') {
                clearPortfolioStorage();
            }
            
            // Reset select to default option after action
            e.target.value = '';
        });
    }
}

function clearPortfolioStorage() {
    localStorage.removeItem('lastPortfolioId');
    alert('Portfolio storage cleared! The last used portfolio ID has been removed from local storage.');
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initDevTools();
});
