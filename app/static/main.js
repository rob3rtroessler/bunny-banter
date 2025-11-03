// Main JavaScript file for Bunny Banter Databricks App
// Fetches data from the Flask API and displays it

// API endpoint
const API_ENDPOINT = '/api/data';

// DOM elements
const loadingEl = document.getElementById('loading');
const errorEl = document.getElementById('error');
const contentEl = document.getElementById('content');
const dataItemsEl = document.getElementById('data-items');
const totalCountEl = document.getElementById('total-count');

/**
 * Display error message to user
 */
function showError(message) {
    loadingEl.style.display = 'none';
    errorEl.style.display = 'block';
    errorEl.textContent = message;
}

/**
 * Display data successfully fetched
 */
function showData(response) {
    loadingEl.style.display = 'none';
    contentEl.style.display = 'block';
    
    // Display credentials
    const credentials = response.credentials || {};
    const credentialsHtml = `
        <div class="data-item">
            <div class="data-header">Credentials</div>
            <div class="data-value">
                <pre>${JSON.stringify(credentials, null, 2)}</pre>
            </div>
        </div>
    `;
    
    // Get data array
    const data = response.data || [];
    
    // Update total count
    totalCountEl.textContent = data.length;
    
    // Display credentials first, then data
    let itemsHtml = credentialsHtml;
    
    // Display data items
    if (data.length === 0) {
        itemsHtml += '<div class="data-item">No data available</div>';
        dataItemsEl.innerHTML = itemsHtml;
        return;
    }
    
    // Display first 10 items as preview
    const previewLimit = Math.min(10, data.length);
    const preview = data.slice(0, previewLimit);
    
    itemsHtml += preview.map((item, index) => {
        const html = `
            <div class="data-item">
                <div class="data-header">Record ${index + 1}</div>
                <div class="data-value">
                    ${JSON.stringify(item, null, 2)}
                </div>
            </div>
        `;
        return html;
    }).join('');
    
    if (data.length > previewLimit) {
        const moreCount = data.length - previewLimit;
        itemsHtml += `
            <div class="data-item">
                <div class="data-value">
                    ... and ${moreCount} more record${moreCount > 1 ? 's' : ''}
                </div>
            </div>
        `;
    }
    
    dataItemsEl.innerHTML = itemsHtml;
}

/**
 * Fetch data from the API
 */
async function fetchData() {
    try {
        console.log('Fetching data from:', API_ENDPOINT);
        
        const response = await fetch(API_ENDPOINT);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Data received:', data);
        
        showData(data);
        
    } catch (error) {
        console.error('Error fetching data:', error);
        showError(`Failed to fetch data: ${error.message}`);
    }
}

/**
 * Initialize the app when the page loads
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('Bunny Banter app initialized');
    fetchData();
});
