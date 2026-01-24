/* ===================================
   DASHBOARD.JS - Dashboard Functionality
   Crop Recommendation System
   =================================== */

/**
 * Initialize dashboard when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
  initializeDashboard();
});

/**
 * Main dashboard initialization
 */
function initializeDashboard() {
  // Initialize form submission
  const predictionForm = document.getElementById('prediction-form');
  if (predictionForm) {
    predictionForm.addEventListener('submit', handleFormSubmit);
  }
  
  // Initialize re-run buttons in history
  initializeRerunButtons();
}

/**
 * Handle prediction form submission
 * @param {Event} event - The form submit event
 */
function handleFormSubmit(event) {
  event.preventDefault();
  
  // Get form data
  const formData = getSliderValues();
  
  // Show loading state
  showLoadingState();
  
  // Get CSRF token for Django
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
  
  // Send prediction request
  fetch('/api/predict/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    body: JSON.stringify(formData)
  })
  .then(response => response.json())
  .then(data => {
    displayResults(data);
    hideLoadingState();
  })
  .catch(error => {
    console.error('Prediction error:', error);
    showError('Failed to get prediction. Please try again.');
    hideLoadingState();
  });
}

/**
 * Display prediction results
 * @param {Object} data - The prediction response data
 */
function displayResults(data) {
  const resultsContainer = document.getElementById('results-container');
  const placeholder = document.getElementById('results-placeholder');
  
  if (!resultsContainer) return;
  
  // Hide placeholder
  if (placeholder) {
    placeholder.style.display = 'none';
  }
  
  // Build results HTML
  let resultsHTML = '<div class="crop-results">';
  
  if (data.predictions && data.predictions.length > 0) {
    data.predictions.forEach((crop, index) => {
      const rankClass = index === 0 ? 'gold' : index === 1 ? 'silver' : 'bronze';
      resultsHTML += `
        <div class="crop-item">
          <div class="crop-rank ${rankClass}">${index + 1}</div>
          <div class="crop-info">
            <div class="crop-name">${crop.name}</div>
            <div class="crop-score">Confidence Score: ${(crop.score * 100).toFixed(1)}%</div>
          </div>
          <div class="crop-confidence">${(crop.score * 100).toFixed(0)}%</div>
        </div>
      `;
    });
  }
  
  resultsHTML += '</div>';
  
  // Add explanation if available
  if (data.explanation) {
    resultsHTML += `
      <div class="explanation-section">
        <h4 class="explanation-title">💡 Why this recommendation?</h4>
        <p class="explanation-text">${data.explanation}</p>
      </div>
    `;
  }
  
  resultsContainer.innerHTML = resultsHTML;
  
  // Update feature importance chart if data is available
  if (data.feature_importance) {
    updateFeatureChart(data.feature_importance);
  }
}

/**
 * Display placeholder results (for demo/testing)
 */
function displayPlaceholderResults() {
  const mockData = {
    predictions: [
      { name: 'Rice', score: 0.89 },
      { name: 'Wheat', score: 0.76 },
      { name: 'Maize', score: 0.68 }
    ],
    explanation: 'Based on the soil nutrients (N, P, K), temperature, and humidity levels you provided, Rice appears to be the most suitable crop for your conditions. The high nitrogen content and adequate rainfall support rice cultivation effectively.'
  };
  
  displayResults(mockData);
}

/**
 * Show loading state on submit button
 */
function showLoadingState() {
  const submitBtn = document.querySelector('.submit-btn');
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner"></span> Analyzing...';
  }
}

/**
 * Hide loading state on submit button
 */
function hideLoadingState() {
  const submitBtn = document.querySelector('.submit-btn');
  if (submitBtn) {
    submitBtn.disabled = false;
    submitBtn.innerHTML = '🌱 Get Crop Recommendation';
  }
}

/**
 * Show error message
 * @param {string} message - Error message to display
 */
function showError(message) {
  const resultsContainer = document.getElementById('results-container');
  if (resultsContainer) {
    resultsContainer.innerHTML = `
      <div class="alert alert-error">
        <span>⚠️</span>
        <span>${message}</span>
      </div>
    `;
  }
}

/**
 * Initialize re-run buttons in history table
 */
function initializeRerunButtons() {
  const rerunButtons = document.querySelectorAll('.rerun-btn');
  
  rerunButtons.forEach(button => {
    button.addEventListener('click', function() {
      const historyData = JSON.parse(this.dataset.values || '{}');
      populateFormFromHistory(historyData);
    });
  });
}

/**
 * Populate form sliders from history data
 * @param {Object} data - Historical prediction data
 */
function populateFormFromHistory(data) {
  Object.keys(data).forEach(key => {
    setSliderValue(key, data[key]);
  });
  
  // Scroll to form
  const form = document.getElementById('prediction-form');
  if (form) {
    form.scrollIntoView({ behavior: 'smooth' });
  }
}

/**
 * Format date for display
 * @param {string} dateString - ISO date string
 * @returns {string} - Formatted date string
 */
function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

/**
 * Add entry to history (client-side for demo)
 * @param {Object} inputData - The input values
 * @param {Object} resultData - The prediction results
 */
function addToHistory(inputData, resultData) {
  const historyBody = document.getElementById('history-body');
  if (!historyBody) return;
  
  const row = document.createElement('tr');
  row.innerHTML = `
    <td>${formatDate(new Date().toISOString())}</td>
    <td>${resultData.predictions?.[0]?.name || 'N/A'}</td>
    <td>${((resultData.predictions?.[0]?.score || 0) * 100).toFixed(1)}%</td>
    <td>
      <button class="rerun-btn" data-values='${JSON.stringify(inputData)}'>
        Re-run
      </button>
    </td>
  `;
  
  // Add to beginning of table
  historyBody.insertBefore(row, historyBody.firstChild);
  
  // Re-initialize rerun button
  row.querySelector('.rerun-btn').addEventListener('click', function() {
    populateFormFromHistory(inputData);
  });
}