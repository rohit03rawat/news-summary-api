// frontend/script.js
let token = '';

function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  fetch("/api/token/", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  })
  .then(res => res.json())
  .then(data => {
    if (data.access) {
      token = data.access;
      document.getElementById("login-status").textContent = "✅ Logged in!";
    } else {
      document.getElementById("login-status").textContent = "❌ Login failed!";
    }
  });
}

function getLatestNews() {
  fetch("/api/news/latest/", {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
  .then(res => res.json())
  .then(data => displayNews(data));
}

function searchNews() {
  const term = document.getElementById("searchTerm").value;
  fetch(`/api/news/search/?q=${term}`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
  .then(res => res.json())
  .then(data => displayNews(data));
}

function saveNews(newsItem) {
  fetch("/api/news/save/", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(newsItem)
  }).then(() => alert("✅ News saved!"));
}

function displayNews(newsList) {
  const container = document.getElementById("news-container");
  container.innerHTML = '';
  newsList.forEach(news => {
    const card = document.createElement("div");
    card.className = "news-card";
    card.innerHTML = `
      <h3>${news.title}</h3>
      <p><strong>Source:</strong> ${news.source}</p>
      <p><strong>Published:</strong> ${news.published_at}</p>
      <p>${news.summary}</p>
      <a href="${news.url}" target="_blank">Read Full</a><br>
      <button onclick='saveNews(${JSON.stringify(news)})'>Save</button>
    `;
    container.appendChild(card);
  });
}
