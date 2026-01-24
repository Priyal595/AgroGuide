/* ===================================
   SLIDER.JS - Slider Functionality
   Crop Recommendation System
   =================================== */

/**
 * Initialize all sliders on the page
 */
function initializeSliders() {
  const sliders = document.querySelectorAll('.slider-input');
  
  sliders.forEach(slider => {
    // Set initial value display
    updateSliderValue(slider);
    
    // Add event listener for real-time updates
    slider.addEventListener('input', function() {
      updateSliderValue(this);
      updateSliderTrack(this);
    });
    
    // Initialize track color
    updateSliderTrack(slider);
  });
}

/**
 * Update the displayed value for a slider
 * @param {HTMLInputElement} slider - The slider input element
 */
function updateSliderValue(slider) {
  const valueDisplay = document.getElementById(`${slider.id}-value`);
  if (valueDisplay) {
    const value = parseFloat(slider.value);
    const unit = slider.dataset.unit || '';
    
    // Format value based on step
    const step = parseFloat(slider.step) || 1;
    const decimals = step < 1 ? String(step).split('.')[1]?.length || 1 : 0;
    
    valueDisplay.textContent = value.toFixed(decimals) + unit;
  }
}

/**
 * Update the slider track color to show progress
 * @param {HTMLInputElement} slider - The slider input element
 */
function updateSliderTrack(slider) {
  const min = parseFloat(slider.min) || 0;
  const max = parseFloat(slider.max) || 100;
  const value = parseFloat(slider.value);
  
  const percentage = ((value - min) / (max - min)) * 100;
  
  // Create gradient for filled portion
  slider.style.background = `linear-gradient(to right, 
    var(--primary-green) 0%, 
    var(--secondary-green) ${percentage}%, 
    var(--border-color) ${percentage}%, 
    var(--border-color) 100%)`;
}

/**
 * Get all slider values as an object
 * @returns {Object} - Object containing all slider values
 */
function getSliderValues() {
  const values = {};
  const sliders = document.querySelectorAll('.slider-input');
  
  sliders.forEach(slider => {
    values[slider.name || slider.id] = parseFloat(slider.value);
  });
  
  return values;
}

/**
 * Reset all sliders to their default values
 */
function resetSliders() {
  const sliders = document.querySelectorAll('.slider-input');
  
  sliders.forEach(slider => {
    const defaultValue = slider.dataset.default || slider.min || 0;
    slider.value = defaultValue;
    updateSliderValue(slider);
    updateSliderTrack(slider);
  });
}

/**
 * Set slider value programmatically
 * @param {string} sliderId - The ID of the slider
 * @param {number} value - The value to set
 */
function setSliderValue(sliderId, value) {
  const slider = document.getElementById(sliderId);
  if (slider) {
    slider.value = value;
    updateSliderValue(slider);
    updateSliderTrack(slider);
  }
}

// Initialize sliders when DOM is ready
document.addEventListener('DOMContentLoaded', initializeSliders);