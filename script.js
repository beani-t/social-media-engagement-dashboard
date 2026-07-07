const benchmarks = {
  "Instagram": 3.0,
  "TikTok": 4.5,
  "X / Twitter": 1.0,
  "Facebook": 1.5,
  "LinkedIn": 2.0,
  "YouTube": 4.0
};

let selectedPlatform = "Instagram";

const platformButtons = document.querySelectorAll(".platform");
const form = document.getElementById("calculatorForm");
const resetButton = document.getElementById("resetButton");
const results = document.getElementById("results");

platformButtons.forEach((button) => {
  button.addEventListener("click", () => {
    platformButtons.forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    selectedPlatform = button.dataset.platform;
  });
});

function getNumber(id) {
  return Number(document.getElementById(id).value);
}

function classifyPerformance(rate, total) {
  if (total < 25) return "Poor Engagement";

  if (total < 75) {
    return rate < 5 ? "Poor Engagement" : "Average Engagement";
  }

  if (total < 250) {
    return rate < 3 ? "Average Engagement" : "Strong Engagement";
  }

  if (rate < 1) return "Poor Engagement";
  if (rate < 3) return "Average Engagement";
  if (rate < 8) return "Strong Engagement";
  return "Excellent Engagement";
}

function getTip(level) {
  const tips = {
    "Poor Engagement": "Improve hooks, captions, posting consistency, and calls-to-action.",
    "Average Engagement": "Ask questions, test stronger formats, and compare performance by content type.",
    "Strong Engagement": "This post is performing well. Try turning the idea into reels, carousels, or a content series.",
    "Excellent Engagement": "This is a high-performing post. Repeat the structure, hook, and creative direction."
  };

  return tips[level];
}

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const followers = getNumber("followers");
  const likes = getNumber("likes");
  const comments = getNumber("comments");
  const shares = getNumber("shares");
  const saves = getNumber("saves");

  if (!followers || followers <= 0) {
    results.innerHTML = `<p class="error">Followers must be greater than 0.</p>`;
    return;
  }

  const totalEngagement = likes + comments + shares + saves;
  const engagementRate = (totalEngagement / followers) * 100;
  const performance = classifyPerformance(engagementRate, totalEngagement);
  const benchmark = benchmarks[selectedPlatform];
  const comparison = engagementRate > benchmark ? "Above Benchmark" : engagementRate === benchmark ? "At Benchmark" : "Below Benchmark";
  const comparisonClass = engagementRate >= benchmark ? "above" : "below";
  const tip = getTip(performance);

  results.innerHTML = `
    <div class="result-topline">
      <div class="rate">${engagementRate.toFixed(2)}%</div>
      <span class="badge ${comparisonClass}">${comparison}</span>
    </div>

    <div class="result-grid">
      <div class="stat-box">
        <small>Platform</small>
        <strong>${selectedPlatform}</strong>
      </div>
      <div class="stat-box">
        <small>Total Engagement</small>
        <strong>${totalEngagement.toLocaleString()}</strong>
      </div>
      <div class="stat-box">
        <small>Performance</small>
        <strong>${performance}</strong>
      </div>
    </div>

    <div class="tip-box">
      <strong>Marketing Recommendation:</strong> ${tip}
    </div>
  `;
});

resetButton.addEventListener("click", () => {
  form.reset();
  selectedPlatform = "Instagram";
  platformButtons.forEach((item) => item.classList.remove("active"));
  document.querySelector('[data-platform="Instagram"]').classList.add("active");
  results.innerHTML = `<p class="placeholder">Enter your metrics to see your engagement rate.</p>`;
});
