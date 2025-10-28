function initDevTools() {
    const devToolsSelect = document.getElementById('dev-tools-select');
    
    if (devToolsSelect) {
        devToolsSelect.addEventListener('change', function(e) {
            const action = e.target.value;
            
            if (action === 'clear-portfolio-storage') {
                clearPortfolioStorage();
            }
            
            // Reset to default value.
            e.target.value = '';
        });
    }
}

function clearPortfolioStorage() {
    localStorage.removeItem('lastPortfolioId');
    window.location.reload();
}

document.addEventListener('DOMContentLoaded', initDevTools);
