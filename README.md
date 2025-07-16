# 📰 News Summary API

This is a Django-based RESTful API that fetches the latest news using external APIs, summarizes them using Google Generative AI, and supports user authentication, news searching, saving, and viewing saved articles.

🔗 **Live Demo**: [https://news-summary-api-r2sf.onrender.com](https://news-summary-api-r2sf.onrender.com)

---

## 🔧 Features

- 🔐 JWT Authentication (Login & Register)
- 🧠 Google Generative AI for news summarization
- 🔎 Search news by keyword
- 💾 Save favorite news articles
- 📑 View saved articles
- 🌐 Simple frontend to interact with the API

---

## 🚀 Technologies Used

- **Backend**: Django, Django REST Framework, SimpleJWT
- **Frontend**: HTML, Vanilla JS
- **AI Integration**: `google-generativeai`
- **Deployment**: Render
- **Authentication**: JWT-based
- **Database**: SQLite (local)

---

## ⚙️ Getting Started (Local Setup)

### 🔁 Prerequisites

- Python 3.9+ (recommended)
- Virtualenv or `venv`

### 🛠️ Installation

```bash
git clone https://github.com/rohit03rawat/news-summary-api.git
cd news-summary-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 🔑 Environment Variables

Create a `.env` file in the root directory and add:

```
GOOGLE_API_KEY=your_google_gen_ai_key
NEWS_API_KEY=your_news_api_key
SECRET_KEY=your_django_secret_key
```

- Get your Google key from: https://makersuite.google.com/app/apikey  
- Get your News API key from: https://newsapi.org/  

---

### 📂 Static Files

```bash
python manage.py collectstatic --noinput
```

---

### 🗃️ Migrate Database

```bash
python manage.py migrate
```

---

### ▶️ Run the Server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 API Testing Guide

Use Postman or `curl` to test the API.

**1. Register User**  
POST `/api/users/register/`

```json
{
  "username": "testuser",
  "password": "securepassword"
}
```

**2. Get JWT Token**  
POST `/api/token/`

```json
{
  "username": "testuser",
  "password": "securepassword"
}
```

Copy the `access` token from the response.

**3. Get Latest News**  
GET `/api/news/latest/`  
Headers:  
`Authorization: Bearer <your_token>`

**4. Search News**  
GET `/api/news/search/?q=climate`  
Headers:  
`Authorization: Bearer <your_token>`

**5. Save News**  
POST `/api/news/save/`  
Headers:  
`Authorization: Bearer <your_token>`  
`Content-Type: application/json`

Body:
```json
{
  "title": "News Title",
  "summary": "Short summary",
  "source": "BBC",
  "url": "https://example.com/article",
  "published_at": "2025-07-15T10:00:00Z"
}
```

**6. View Saved News**  
GET `/api/news/saved/`  
Headers:  
`Authorization: Bearer <your_token>`

---

## 📁 Project Structure

```
news-summary-api/
├── news_api/              # Main Django project
│   └── urls.py            # URL routing
├── news/                  # News app: logic + API
├── users/                 # User registration logic
├── frontend/              # Static frontend
├── utils.py               # Summarization & fetching
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables
```

---

## 📦 Deployment (Render)

This app is deployed on Render.

### Steps:

1. Add `gunicorn` and `whitenoise` to `requirements.txt`
2. Set the following environment variables in Render:
   - `GOOGLE_API_KEY`
   - `NEWS_API_KEY`
   - `SECRET_KEY`
3. Build Command:
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   ```
4. Start Command:
   ```bash
   gunicorn news_api.wsgi:application
   ```

---

## 🙋 Author

**Rohit Rawat**  
GitHub: [@rohit03rawat](https://github.com/rohit03rawat)

---

## 📄 License

This project is intended for educational and demonstration purposes.
