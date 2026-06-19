
const API_URL = "semester-project-production-0db2.up.railway.app";
function saveToken(token, username, role) {
  localStorage.setItem("token", token);
  localStorage.setItem("username", username);
  localStorage.setItem("role", role);
}

function getToken() {
  return localStorage.getItem("token");
}

function logout() {
  localStorage.clear();
  window.location.href = "login.html";
}

// Check if user is logged in (for protected pages)
function requireLogin() {
  if (!getToken()) {
    window.location.href = "login.html";
  }
}

// Call API with token
async function apiCall(endpoint, method = "GET", body = null) {
  const options = {
    method: method,
    headers: {
      "Content-Type": "application/json",
    },
  };

  const token = getToken();
  if (token) {
    options.headers["Authorization"] = "Bearer " + token;
  }

  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(API_URL + endpoint, options);
  const data = await response.json();

  if (!response.ok) {
    let message = "Something went wrong";
    if (typeof data.detail === "string") {
      message = data.detail;
    } else if (Array.isArray(data.detail)) {
      message = data.detail.map(function(d) { return d.msg; }).join(", ");
    }
    throw new Error(message);
  }

  return data;
}

// Show message on page
function showMessage(elementId, message, type) {
  const el = document.getElementById(elementId);
  if (!el) return;
  el.className = "alert alert-" + type;
  el.textContent = message;
  el.classList.remove("hidden");
}

// Format date for display
function formatDate(dateStr) {
  if (!dateStr) return "-";
  const d = new Date(dateStr);
  return d.toLocaleDateString();
}

// Format price
function formatPrice(price) {
  return "Rs. " + parseFloat(price).toFixed(2);
}

// Show logged in user name in navbar
function showUserInfo() {
  const userEl = document.getElementById("user-info");
  if (userEl) {
    const name = localStorage.getItem("username") || "User";
    userEl.textContent = "Hello, " + name;
  }
}
