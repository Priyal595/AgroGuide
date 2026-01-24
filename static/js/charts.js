/* ===================================
   CHARTS.JS - Chart.js Integration
   Crop Recommendation System
   =================================== */

// Chart instance reference
let featureImportanceChart = null;

/**
 * Initialize charts when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
  initializeCharts();
});

/**
 * Initialize all charts on the page
 */
function initializeCharts() {
  const chartCanvas = document.getElementById('feature-importance-chart');
  if (chartCanvas) {
    createFeatureImportanceChart(chartCanvas);
  }
}

/**
 * Create the feature importance chart
 * @param {HTMLCanvasElement} canvas - The canvas element for the chart
 */
function createFeatureImportanceChart(canvas) {
  // Default/placeholder data
  const defaultData = {
    labels: ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'Rainfall', 'pH'],
    values: [0, 0, 0, 0, 0, 0, 0]
  };
  
  // Chart.js configuration
  const config = {
    type: 'bar',
    data: {
      labels: defaultData.labels,
      datasets: [{
        label: 'Feature Importance',
        data: defaultData.values,
        backgroundColor: [
          'rgba(45, 106, 79, 0.8)',
          'rgba(64, 145, 108, 0.8)',
          'rgba(82, 183, 136, 0.8)',
          'rgba(149, 213, 178, 0.8)',
          'rgba(216, 243, 220, 0.8)',
          'rgba(45, 106, 79, 0.6)',
          'rgba(64, 145, 108, 0.6)'
        ],
        borderColor: [
          'rgba(45, 106, 79, 1)',
          'rgba(64, 145, 108, 1)',
          'rgba(82, 183, 136, 1)',
          'rgba(149, 213, 178, 1)',
          'rgba(216, 243, 220, 1)',
          'rgba(45, 106, 79, 1)',
          'rgba(64, 145, 108, 1)'
        ],
        borderWidth: 2,
        borderRadius: 6,
        barThickness: 40
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(26, 26, 46, 0.9)',
          titleColor: '#fff',
          bodyColor: '#fff',
          padding: 12,
          cornerRadius: 8,
          callbacks: {
            label: function(context) {
              return `Importance: ${(context.raw * 100).toFixed(1)}%`;
            }
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          max: 1,
          grid: {
            color: 'rgba(0, 0, 0, 0.05)'
          },
          ticks: {
            callback: function(value) {
              return (value * 100) + '%';
            },
            font: {
              size: 12
            }
          }
        },
        y: {
          grid: {
            display: false
          },
          ticks: {
            font: {
              size: 13,
              weight: '500'
            },
            color: '#1a1a2e'
          }
        }
      }
    }
  };
  
  // Create chart instance
  featureImportanceChart = new Chart(canvas, config);
}

/**
 * Update the feature importance chart with new data
 * @param {Object} data - Feature importance data from API
 */
function updateFeatureChart(data) {
  if (!featureImportanceChart) return;
  
  // Update chart data
  if (data.labels) {
    featureImportanceChart.data.labels = data.labels;
  }
  
  if (data.values) {
    featureImportanceChart.data.datasets[0].data = data.values;
  }
  
  // Animate the update
  featureImportanceChart.update('active');
}

/**
 * Display placeholder data for demo
 */
function showPlaceholderChartData() {
  const placeholderData = {
    labels: ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'Rainfall', 'pH'],
    values: [0.25, 0.18, 0.15, 0.14, 0.12, 0.10, 0.06]
  };
  
  updateFeatureChart(placeholderData);
}

/**
 * Reset chart to empty state
 */
function resetChart() {
  if (!featureImportanceChart) return;
  
  featureImportanceChart.data.datasets[0].data = [0, 0, 0, 0, 0, 0, 0];
  featureImportanceChart.update('active');
}

/**
 * Destroy chart instance (cleanup)
 */
function destroyChart() {
  if (featureImportanceChart) {
    featureImportanceChart.destroy();
    featureImportanceChart = null;
  }
}

/**
 * Create a simple pie chart for crop distribution
 * @param {string} canvasId - The canvas element ID
 * @param {Object} data - Crop distribution data
 */
function createCropDistributionChart(canvasId, data) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return null;
  
  return new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels: data.labels || ['Rice', 'Wheat', 'Maize'],
      datasets: [{
        data: data.values || [40, 35, 25],
        backgroundColor: [
          'rgba(45, 106, 79, 0.9)',
          'rgba(64, 145, 108, 0.9)',
          'rgba(82, 183, 136, 0.9)'
        ],
        borderColor: '#fff',
        borderWidth: 3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            padding: 20,
            font: {
              size: 13
            }
          }
        }
      }
    }
  });
}
