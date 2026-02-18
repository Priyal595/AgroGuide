/* ===================================
   DASHBOARD.JS - Dashboard Functionality
   =================================== */

// document.addEventListener("DOMContentLoaded", () => {
//   initializeDashboard();
// });

document.addEventListener("DOMContentLoaded", () => {
  console.log("Dashboard JS Loaded");
  initializeDashboard();
});

function initializeDashboard() {
  const form = document.getElementById("prediction-form");
  if (form) {
    form.addEventListener("submit", handleFormSubmit);
  }
  loadPredictionHistory();
  loadInsights();
}

/* ===============================
   HANDLE FORM SUBMISSION
   =============================== */
function handleFormSubmit(e) {
  e.preventDefault();

  const formData = getSliderValues();
  showLoadingState();

  const csrfToken = document.querySelector(
    "[name=csrfmiddlewaretoken]"
  )?.value;

  fetch("/api/predict/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify(formData),
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error("Server error");
      }
      return res.json();
    })
    .then((data) => {
      displayResults(data);

      // 🔥 UPDATE FEATURE IMPORTANCE CHART
      if (data.feature_importance) {
        updateFeatureChart(data.feature_importance);
      }

      hideLoadingState();
    })
    .catch((err) => {
      console.error("Prediction Error:", err);
      showError("Prediction failed. Please try again.");
      resetChart(); // Clear chart on error
      hideLoadingState();
    });
}

/* ===============================
   DISPLAY PREDICTION RESULTS
   =============================== */
function displayResults(data) {
  const container = document.getElementById("results-container");
  if (!container) return;

  if (!data.predictions || data.predictions.length === 0) {
    container.innerHTML = `<div class="alert alert-error">No predictions available.</div>`;
    return;
  }

  let html = `<div class="crop-results">`;

  data.predictions.forEach((item, idx) => {
    const score = (item.confidence * 100).toFixed(1);
    const rank =
      idx === 0 ? "gold" : idx === 1 ? "silver" : "bronze";

    html += `
      <div class="crop-item">
        <div class="crop-rank ${rank}">${idx + 1}</div>
        <div class="crop-info">
          <div class="crop-name">${item.crop}</div>
          <div class="crop-score">Confidence: ${score}%</div>
        </div>
        <div class="crop-confidence">${score}%</div>
      </div>
    `;
  });

  html += `</div>`;

  if (data.explanation) {
    html += `
      <div class="explanation-section">
        <h4>💡 Why this recommendation?</h4>
        <p>${data.explanation}</p>
      </div>
    `;
  }

  container.innerHTML = html;
}

/* ===============================
   LOADING STATE
   =============================== */
function showLoadingState() {
  const btn = document.querySelector(".submit-btn");
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = "Analyzing...";
  }
}

function hideLoadingState() {
  const btn = document.querySelector(".submit-btn");
  if (btn) {
    btn.disabled = false;
    btn.innerHTML = "🌱 Get Crop Recommendation";
  }
}

/* ===============================
   ERROR DISPLAY
   =============================== */
function showError(msg) {
  const container = document.getElementById("results-container");
  if (container) {
    container.innerHTML = `<div class="alert alert-error">${msg}</div>`;
  }
}

/* ===============================
   LOAD PREDICTION HISTORY
   =============================== */
function loadPredictionHistory() {
  fetch("/api/history/", { credentials: "same-origin" })
    .then((res) => res.json())
    .then((data) => {
      const tbody = document.getElementById("history-body");
      if (!tbody) return;

      tbody.innerHTML = "";

      if (!data.history || data.history.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="4">No history yet</td>
          </tr>`;
        return;
      }

      data.history.forEach((item) => {
        if (!item.result || !item.result.predictions) return;

        const top = item.result.predictions[0];
        const row = document.createElement("tr");

        row.innerHTML = `
          <td>${new Date(item.created_at).toLocaleString()}</td>
          <td>${top.crop}</td>
          <td>${(top.confidence * 100).toFixed(1)}%</td>
          <td><button disabled>Re-run</button></td>
        `;

        tbody.appendChild(row);
      });
    })
    .catch((err) => {
      console.error("History load error:", err);
    });
}

function loadInsights() {
  console.log("Loading insights...");
  fetch("/api/insights/", { credentials: "same-origin" })
    .then((res) => res.json())
    .then((data) => {
      renderInsightsSummary(data);
      renderCropFrequencyChart(data.crop_frequency);
      renderConfidenceChart(data.confidence_distribution);
    })
    .catch((err) => {
      console.error("Insights error:", err);
    });
}


function renderInsightsSummary(data) {
  const container = document.getElementById("insights-summary");
  if (!container) return;

  if (data.total_predictions === 0) {
    container.innerHTML = "<p>No insights available yet.</p>";
    return;
  }

  container.innerHTML = `
    <div class="insight-metrics">
      <p><strong>Total Predictions:</strong> ${data.total_predictions}</p>
      <p><strong>Most Recommended Crop:</strong> ${data.most_recommended_crop}</p>
      <p><strong>Avg Rainfall:</strong> ${data.average_conditions.rainfall} mm</p>
      <p><strong>Avg Temperature:</strong> ${data.average_conditions.temperature} °C</p>
      <p><strong>Avg Soil pH:</strong> ${data.average_conditions.ph}</p>
    </div>
  `;
}


function renderCropFrequencyChart(cropFrequency) {
  const ctx = document.getElementById("cropFrequencyChart");
  if (!ctx) return;

  const labels = Object.keys(cropFrequency);
  const values = Object.values(cropFrequency);

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "Frequency",
        data: values,
        backgroundColor: "rgba(75, 192, 192, 0.6)"
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      }
    }
  });
}


function renderConfidenceChart(confidenceData) {
  const ctx = document.getElementById("confidenceChart");
  if (!ctx) return;

  new Chart(ctx, {
    type: "pie",
    data: {
      labels: ["High", "Medium", "Low"],
      datasets: [{
        data: [
          confidenceData.high,
          confidenceData.medium,
          confidenceData.low
        ],
        backgroundColor: [
          "rgba(75, 192, 192, 0.7)",
          "rgba(255, 206, 86, 0.7)",
          "rgba(255, 99, 132, 0.7)"
        ]
      }]
    },
    options: {
      responsive: true
    }
  });
}
