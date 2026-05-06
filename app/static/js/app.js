// Use full API base to avoid origin issues when frontend served from file://
const API_PREFIX = "http://127.0.0.1:8001/api/v1";
// Store only the access token under a conventional key used in examples
const STORAGE_KEY = "access_token";
const THEME_KEY = "theme";

const authPanel = document.getElementById("authPanel");
const workspacePanel = document.getElementById("workspacePanel");
const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");
const forgotPasswordForm = document.getElementById("forgotPasswordForm");
const showLoginBtn = document.getElementById("showLoginBtn");
const showRegisterBtn = document.getElementById("showRegisterBtn");
const forgotPasswordBtn = document.getElementById("forgotPasswordBtn");
const backToLoginBtn = document.getElementById("backToLoginBtn");
const logoutBtn = document.getElementById("logoutBtn");
const refreshBtn = document.getElementById("refreshBtn");
const taskForm = document.getElementById("taskForm");
const taskList = document.getElementById("taskList");
const toast = document.getElementById("toast");
const themeToggle = document.getElementById("themeToggle");

const taskCount = document.getElementById("taskCount");
const completedCount = document.getElementById("completedCount");
const openCount = document.getElementById("openCount");

let authToken = localStorage.getItem(STORAGE_KEY) || "";
let activeUser = null;
let tasks = [];

function initTheme() {
  const savedTheme = localStorage.getItem(THEME_KEY) || "dark";
  if (savedTheme === "light") {
    document.body.classList.add("light-theme");
    themeToggle.querySelector(".theme-icon").textContent = "☀️";
  } else {
    document.body.classList.remove("light-theme");
    themeToggle.querySelector(".theme-icon").textContent = "🌙";
  }
}

function toggleTheme() {
  const isLight = document.body.classList.toggle("light-theme");
  const newTheme = isLight ? "light" : "dark";
  localStorage.setItem(THEME_KEY, newTheme);
  themeToggle.querySelector(".theme-icon").textContent = isLight ? "☀️" : "🌙";
  showToast(`Switched to ${newTheme} theme`, "success");
}

function showToast(message, tone = "info") {
  toast.textContent = message;
  toast.className = `toast-banner ${tone}`;
  toast.classList.remove("d-none");
  clearTimeout(showToast.timer);
  showToast.timer = setTimeout(() => toast.classList.add("d-none"), 2800);
}

function setAuthView(isAuthenticated) {
  authPanel.classList.toggle("d-none", isAuthenticated);
  workspacePanel.classList.toggle("d-none", !isAuthenticated);
}

function updateStats() {
  const total = tasks.length;
  const completed = tasks.filter((task) => task.status === "COMPLETED").length;
  taskCount.textContent = total;
  completedCount.textContent = completed;
  openCount.textContent = total - completed;
}

function statusLabel(status) {
  return status
    .toLowerCase()
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

function formatDate(value) {
  if (!value) return "No due date";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "No due date" : date.toLocaleDateString();
}

function getHeaders(includeJson = true) {
  const headers = {};
  if (includeJson) {
    headers["Content-Type"] = "application/json";
  }
  headers["Accept"] = "application/json";
  if (authToken) {
    headers.Authorization = `Bearer ${authToken}`;
  }
  return headers;
}

async function request(path, options = {}) {
  console.log("API request", { url: `${API_PREFIX}${path}`, options });
  const response = await fetch(`${API_PREFIX}${path}`, {
    ...options,
    headers: {
      ...getHeaders(options.body !== undefined),
      ...(options.headers || {}),
    },
  });

  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json") ? await response.json() : null;

  if (!response.ok) {
    const detail = payload?.detail;
    const message = Array.isArray(detail)
      ? detail.map((item) => item.msg || item.message || "Validation error").join(", ")
      : detail || "Request failed";
    console.error("API error", { status: response.status, message, payload });
    throw new Error(message);
  }

  console.log("API response", { status: response.status, payload });
  return payload;
}

function renderTasks() {
  if (!tasks.length) {
    taskList.innerHTML = `
      <div class="task-card">
        <h4>No tasks yet</h4>
        <p class="task-meta mb-0">Create the first item to start organizing the team workload.</p>
      </div>
    `;
    updateStats();
    return;
  }

  taskList.innerHTML = tasks
    .map(
      (task) => `
        <article class="task-card ${task.status === "COMPLETED" ? "completed" : ""}">
          <div class="d-flex justify-content-between gap-3 flex-wrap">
            <div>
              <div class="task-chip ${task.status.toLowerCase()}">${statusLabel(task.status)}</div>
              <h4 class="mt-2">${escapeHtml(task.title)}</h4>
              <p class="task-meta mb-1">${escapeHtml(task.description || "No description provided")}</p>
              <p class="task-meta mb-0">Due ${formatDate(task.due_date)}</p>
            </div>
            <div class="text-end">
              <p class="task-meta mb-1">${statusLabel(task.status)}</p>
              <small class="task-meta">Updated ${formatDate(task.updated_at)}</small>
            </div>
          </div>
          <div class="task-actions">
            <button class="btn btn-sm btn-outline-light" data-action="toggle" data-id="${task.id}">${task.status === "COMPLETED" ? "Mark open" : "Mark complete"}</button>
            <button class="btn btn-sm btn-outline-light" data-action="edit" data-id="${task.id}">Edit</button>
            <button class="btn btn-sm btn-outline-danger" data-action="delete" data-id="${task.id}">Delete</button>
          </div>
        </article>
      `,
    )
    .join("");

  updateStats();
}

function escapeHtml(value) {
  const element = document.createElement("div");
  element.textContent = value;
  return element.innerHTML;
}

async function refreshTasks() {
  tasks = await request("/tasks", { method: "GET", headers: getHeaders(false) });
  renderTasks();
}

async function loadProfile() {
  activeUser = await request("/auth/me", { method: "GET", headers: getHeaders(false) });
  showToast(`Welcome back, ${activeUser.name}.`, "success");
}

async function bootstrapWorkspace() {
  if (!authToken) {
    setAuthView(false);
    return;
  }

  try {
    await loadProfile();
    setAuthView(true);
    await refreshTasks();
  } catch (error) {
    authToken = "";
    localStorage.removeItem(STORAGE_KEY);
    setAuthView(false);
    showToast(error.message, "danger");
  }
}

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    const payload = await request("/auth/login", {
      method: "POST",
      body: JSON.stringify({
        email: document.getElementById("loginEmail").value.trim(),
        password: document.getElementById("loginPassword").value,
      }),
    });
    authToken = payload.access_token;
    console.log("login token", authToken);
    localStorage.setItem(STORAGE_KEY, authToken);
    showToast("Signed in successfully.", "success");
    await bootstrapWorkspace();
  } catch (error) {
    showToast(error.message, "danger");
  }
});

registerForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    const payload = await request("/auth/register", {
      method: "POST",
      body: JSON.stringify({
        name: document.getElementById("registerName").value.trim(),
        email: document.getElementById("registerEmail").value.trim(),
        password: document.getElementById("registerPassword").value,
      }),
    });
    authToken = payload.access_token;
    console.log("register token", authToken);
    localStorage.setItem(STORAGE_KEY, authToken);
    showToast("Account created.", "success");
    await bootstrapWorkspace();
  } catch (error) {
    showToast(error.message, "danger");
  }
});

showLoginBtn.addEventListener("click", () => {
  registerForm.classList.add("d-none");
  forgotPasswordForm.classList.add("d-none");
  loginForm.classList.remove("d-none");
  showLoginBtn.classList.add("active");
  showRegisterBtn.classList.remove("active");
});

showRegisterBtn.addEventListener("click", () => {
  loginForm.classList.add("d-none");
  forgotPasswordForm.classList.add("d-none");
  registerForm.classList.remove("d-none");
  showRegisterBtn.classList.add("active");
  showLoginBtn.classList.remove("active");
});

forgotPasswordBtn.addEventListener("click", () => {
  loginForm.classList.add("d-none");
  registerForm.classList.add("d-none");
  forgotPasswordForm.classList.remove("d-none");
});

backToLoginBtn.addEventListener("click", () => {
  forgotPasswordForm.classList.add("d-none");
  loginForm.classList.remove("d-none");
  document.getElementById("forgotEmail").value = "";
});

forgotPasswordForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const email = document.getElementById("forgotEmail").value.trim();
  showToast(`Reset link has been sent to ${email}. Please check your inbox.`, "success");
  document.getElementById("forgotEmail").value = "";
  setTimeout(() => {
    forgotPasswordForm.classList.add("d-none");
    loginForm.classList.remove("d-none");
  }, 2000);
});

if (themeToggle) {
  themeToggle.addEventListener("click", toggleTheme);
}

logoutBtn.addEventListener("click", () => {
  authToken = "";
  activeUser = null;
  tasks = [];
  localStorage.removeItem(STORAGE_KEY);
  renderTasks();
  setAuthView(false);
  showToast("Logged out.", "info");
});

refreshBtn.addEventListener("click", async () => {
  try {
    await refreshTasks();
    showToast("Tasks refreshed.", "success");
  } catch (error) {
    showToast(error.message, "danger");
  }
});

taskForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    await request("/tasks", {
      method: "POST",
      body: JSON.stringify({
        title: document.getElementById("taskTitle").value.trim(),
        description: document.getElementById("taskDescription").value.trim() || null,
          status: document.getElementById("taskStatus").value,
          due_date: document.getElementById("taskDueDate").value || null,
      }),
    });
    taskForm.reset();
    document.getElementById("taskStatus").value = "PENDING";
    await refreshTasks();
    showToast("Task created.", "success");
  } catch (error) {
    showToast(error.message, "danger");
  }
});

taskList.addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-action]");
  if (!button) return;

  const taskId = Number(button.dataset.id);
  const action = button.dataset.action;
  const task = tasks.find((item) => item.id === taskId);
  if (!task) return;

  try {
    if (action === "toggle") {
      await request(`/tasks/${taskId}`, {
        method: "PUT",
        body: JSON.stringify({
          status: task.status === "COMPLETED" ? "PENDING" : "COMPLETED",
        }),
      });
      showToast("Task updated.", "success");
    } else if (action === "delete") {
      if (!window.confirm(`Delete '${task.title}'?`)) return;
      await request(`/tasks/${taskId}`, { method: "DELETE", headers: getHeaders(false) });
      showToast("Task deleted.", "success");
    } else if (action === "edit") {
      const newTitle = window.prompt("Update the task title", task.title);
      if (newTitle === null) return;
      const newDescription = window.prompt("Update the task description", task.description || "") || null;
      await request(`/tasks/${taskId}`, {
        method: "PUT",
        body: JSON.stringify({
          title: newTitle.trim() || task.title,
          description: newDescription,
        }),
      });
      showToast("Task updated.", "success");
    }
    await refreshTasks();
  } catch (error) {
    showToast(error.message, "danger");
  }
});

initTheme();
bootstrapWorkspace();
