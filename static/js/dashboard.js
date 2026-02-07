/* ===================================
   DASHBOARD.JS - Dashboard Functionality
   =================================== */

document.addEventListener("DOMContentLoaded", () => {
  initializeDashboard();
});

function initializeDashboard() {
  const form = document.getElementById("prediction-form");
  if (form) {
    form.addEventListener("submit", handleFormSubmit);
  }
  loadPredictionHistory();
}

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
    .then((res) => res.json())
    .then((data) => {
      displayResults(data);
      hideLoadingState();
    })
    .catch((err) => {
      console.error(err);
      showError("Prediction failed");
      hideLoadingState();
    });
}

function displayResults(data) {
  const container = document.getElementById("results-container");
  if (!container) return;

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

function showError(msg) {
  const container = document.getElementById("results-container");
  container.innerHTML = `<div class="alert alert-error">${msg}</div>`;
}

function loadPredictionHistory() {
  fetch("/api/history/", { credentials: "same-origin" })
    .then((res) => res.json())
    .then((data) => {
      const tbody = document.getElementById("history-body");
      tbody.innerHTML = "";

      if (!data.history || data.history.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="4">No history yet</td>
          </tr>`;
        return;
      }

      data.history.forEach((item) => {
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
    });
}
