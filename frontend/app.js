const API_BASE = "http://127.0.0.1:8000";

async function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const message = document.getElementById("message");

  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  const response = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: formData
  });

  const data = await response.json();

  if (response.ok) {
    localStorage.setItem("token", data.access_token);
    window.location.href = "index.html";
  } else {
    message.textContent = data.detail || "Login failed";
  }
}

async function loadTodos() {
  const token = localStorage.getItem("token");
  if (!token) {
    window.location.href = "login.html";
    return;
  }

  const response = await fetch(`${API_BASE}/todos`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  const data = await response.json();
  const todoList = document.getElementById("todo-list");

  if (!todoList) return;

  todoList.innerHTML = "";

  data.forEach(todo => {
    const li = document.createElement("li");
    li.textContent = `${todo.title} - ${todo.completed ? "Done" : "Pending"}`;
    todoList.appendChild(li);
  });
}

async function createTodo() {
  const token = localStorage.getItem("token");
  const title = document.getElementById("title").value;
  const message = document.getElementById("message");

  const response = await fetch(`${API_BASE}/todos`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({
      title: title,
      completed: false
    })
  });

  const data = await response.json();

  if (response.ok) {
    document.getElementById("title").value = "";
    loadTodos();
  } else {
    message.textContent = data.detail || "Failed to create todo";
  }
}

function logout() {
  localStorage.removeItem("token");
  window.location.href = "login.html";
}
async function register() {
  const username = document.getElementById("reg-username").value;
  const email = document.getElementById("reg-email").value;
  const password = document.getElementById("reg-password").value;
  const message = document.getElementById("message");

  const response = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      username: username,
      email: email,
      password: password
    })
  });

  const data = await response.json();

  if (response.ok) {
    message.textContent = "Registration successful. Go to login.";
    window.location.href = "login.html";
  } else {
    message.textContent = data.detail || "Registration failed";
  }
}