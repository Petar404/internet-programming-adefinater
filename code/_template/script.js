// API endpoint
const API_URL = 'https://raw.githubusercontent.com/sweko/internet-programming-adefinater/refs/heads/main/data/doctor-who-episodes.json';

// Global state
let episodes = [];
let filteredEpisodes = [];
let currentSort = { field: 'rank', ascending: true };

// Initialize the application
function init() {
    loadEpisodes();
    setupEventListeners();
}

// Load episodes from API
async function loadEpisodes() {
    try {
        // TODO: Implement data loading
        console.log('Loading episodes from:', API_URL);
    } catch (error) {
        console.error('Error loading episodes:', error);
        showError('Failed to load episodes. Please try again later.');
    }
}

// Setup event listeners
function setupEventListeners() {
    // TODO: Add event listeners for filters and sorting
}

// Display episodes in the table
function displayEpisodes(episodesToDisplay) {
    // TODO: Implement episode display logic
}

// Filter episodes based on current filter values
function filterEpisodes() {
    // TODO: Implement filtering logic
}

// Sort episodes by field
function sortEpisodes(field) {
    // TODO: Implement sorting logic
}

// Show error message
function showError(message) {
    const errorElement = document.getElementById('error');
    errorElement.textContent = message;
    errorElement.style.display = 'block';
    document.getElementById('loading').style.display = 'none';
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
