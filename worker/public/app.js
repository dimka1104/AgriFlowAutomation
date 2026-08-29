async function apiFetch(path, options = {}) {
  const response = await fetch(path, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  return response;
}

async function getCurrentUser() {
  const response = await apiFetch("/api/auth/me");
  if (!response.ok) return null;
  return response.json();
}

function renderNav(user) {
  const nav = document.getElementById("navbar");
  if (!nav) return;
  nav.innerHTML = `
    <span class="brand">AgriFlow</span>
    <div class="nav-links">
      <a href="/dashboard">Dashboard</a>
      ${user.role === "master" ? '<a href="/admin">Admin</a>' : ""}
      <span class="nav-user">${user.username} (${user.role})</span>
      <a href="#" id="logout-link">Log out</a>
    </div>
  `;
  document.getElementById("logout-link").addEventListener("click", async (event) => {
    event.preventDefault();
    await apiFetch("/api/auth/logout", { method: "POST" });
    window.location.href = "/login";
  });
}

async function requireUser() {
  const user = await getCurrentUser();
  if (!user) {
    window.location.href = "/login";
    return null;
  }
  renderNav(user);
  return user;
}

async function requireMaster() {
  const user = await requireUser();
  if (!user) return null;
  if (user.role !== "master") {
    window.location.href = "/dashboard";
    return null;
  }
  return user;
}
