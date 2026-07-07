const benchmarks = {
  "Instagram": 3.0,
  "TikTok": 4.5,
  "X / Twitter": 1.0,
  "Facebook": 1.5,
  "LinkedIn": 2.0,
  "YouTube": 4.0
};

let selectedPlatform = "Instagram";
let latestResults = null;

const platformButtons = document.querySelectorAll(".platform");
const selectedPlatformBadge = document.getElementById("selectedPlatform");
const calculateBtn = document.getElementById("calculateBtn");
const resetBtn = document.getElementById("resetBtn");
const copyBtn = document.getElementById("copyBtn");
const downloadBtn = document.getElementById("downloadBtn");
const themeToggle = document.getElementById("themeToggle");

const fields = ["followers", "likes", "comments", "shares", "saves"];

platformButtons.forEach(button => {
  button.addEventListener("click", () => {
    platformButtons.forEach(btn => btn.classList.remove("active"));
    button.classList.add("active");
    selectedPlatform = button.dataset.platform;
    selectedPlatformBadge.textContent = selectedPlatform;
    document.getElementById("benchmark").textContent = `${benchmarks[selectedPlatform]}%`;
    if (latestResults) calculate();
  });
});

calculateBtn.addEventListener("click", calculate);
resetBtn.addEventListener("click", resetCalculator);
copyBtn.addEventListener("click", copyResults);
downloadBtn.addEventListener("click", downloadReport);
themeToggle.addEventListener("click", toggleTheme);

fields.forEach(id => {
  document.getElementById(id).addEventListener("input", () => {
    if (fields.every(field => document.getElementById(field).value !== "")) calculate();
  });
});

function getNumber(id) {
  return Number(document.getElementById(id).value || 0);
}

function calculate() {
  const followers = getNumber("followers");
  const likes = getNumber("likes");
  const comments = getNumber("comments");
  const shares = getNumber("shares");
  const saves = getNumber("saves");

  if (followers <= 0) {
    alert("Please enter a follower count greater than 0.");
    return;
  }

  const total = likes + comments + shares + saves;
  const rate = (total / followers) * 100;
  const benchmark = benchmarks[selectedPlatform];
  const score = Math.min(Math.round((rate / Math.max(benchmark, 1)) * 75), 100);
  const performance = classifyPerformance(rate, total);
  const comparison = rate >= benchmark ? "Above Benchmark" : "Below Benchmark";
  const tips = generateTips(rate, benchmark, likes, comments, shares, saves, followers);

  latestResults = { followers, likes, comments, shares, saves, total, rate, benchmark, score, performance, comparison, tips };

  document.getElementById("rate").textContent = `${rate.toFixed(2)}%`;
  document.getElementById("score").textContent = score;
  document.getElementById("total").textContent = total.toLocaleString();
  document.getElementById("benchmark").textContent = `${benchmark}%`;
  document.getElementById("performance").textContent = performance;
  document.getElementById("progressBar").style.width = `${score}%`;

  const ring = document.querySelector(".score-ring");
  ring.style.background = `conic-gradient(var(--purple) ${score * 3.6}deg, #e7e8f3 0deg)`;

  const tipsList = document.getElementById("tips");
  tipsList.innerHTML = "";
  tips.forEach(tip => {
    const li = document.createElement("li");
    li.textContent = tip;
    tipsList.appendChild(li);
  });
}

function classifyPerformance(rate, total) {
  if (total < 25) return "Needs Improvement";
  if (rate < 1) return "Low Engagement";
  if (rate < 3) return "Average Engagement";
  if (rate < 8) return "Strong Engagement";
  return "Excellent Engagement";
}

function generateTips(rate, benchmark, likes, comments, shares, saves, followers) {
  const tips = [];

  if (rate >= benchmark) {
    tips.push("This post is performing above the platform benchmark. Repurpose this content style.");
  } else {
    tips.push("Test stronger hooks, clearer captions, and a more direct call-to-action.");
  }

  if (saves / Math.max(followers, 1) > 0.01) {
    tips.push("Strong save behavior suggests this content is valuable or educational.");
  } else {
    tips.push("Add more save-worthy content such as checklists, tips, tutorials, or mini guides.");
  }

  if (comments < likes * 0.02) {
    tips.push("Increase comments by asking a specific question in the caption.");
  } else {
    tips.push("Comment quality looks healthy. Keep encouraging audience conversation.");
  }

  if (shares > saves) {
    tips.push("High share activity means the content is resonating beyond your current audience.");
  } else {
    tips.push("Try trend-based or relatable formats to increase shares.");
  }

  return tips;
}

function resetCalculator() {
  fields.forEach(id => document.getElementById(id).value = "");
  latestResults = null;
  document.getElementById("rate").textContent = "0.00%";
  document.getElementById("score").textContent = "0";
  document.getElementById("total").textContent = "0";
  document.getElementById("benchmark").textContent = `${benchmarks[selectedPlatform]}%`;
  document.getElementById("performance").textContent = "Waiting";
  document.getElementById("progressBar").style.width = "0%";
  document.querySelector(".score-ring").style.background = "conic-gradient(var(--purple) 0deg, #e7e8f3 0deg)";
  document.getElementById("tips").innerHTML = "<li>Enter your post metrics to generate recommendations.</li>";
}

function copyResults() {
  if (!latestResults) {
    alert("Calculate your engagement first.");
    return;
  }

  const text = formatReport();
  navigator.clipboard.writeText(text);
  copyBtn.textContent = "Copied!";
  setTimeout(() => copyBtn.textContent = "Copy Results", 1200);
}

function downloadReport() {
  if (!latestResults) {
    alert("Calculate your engagement first.");
    return;
  }

  const blob = new Blob([formatReport()], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "engagement-report.txt";
  link.click();
  URL.revokeObjectURL(url);
}

function formatReport() {
  return `Social Media Engagement Report

Platform: ${selectedPlatform}
Engagement Rate: ${latestResults.rate.toFixed(2)}%
Total Engagement: ${latestResults.total.toLocaleString()}
Benchmark: ${latestResults.benchmark}%
Performance: ${latestResults.performance}
Comparison: ${latestResults.comparison}

Metrics:
Followers: ${latestResults.followers.toLocaleString()}
Likes: ${latestResults.likes.toLocaleString()}
Comments: ${latestResults.comments.toLocaleString()}
Shares: ${latestResults.shares.toLocaleString()}
Saves: ${latestResults.saves.toLocaleString()}

Recommendations:
${latestResults.tips.map(tip => `- ${tip}`).join("\n")}

Designed & Developed by Abeni Townsend`;
}

function toggleTheme() {
  document.body.classList.toggle("dark");
  themeToggle.textContent = document.body.classList.contains("dark") ? "Light Mode" : "Dark Mode";
}
