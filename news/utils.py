import requests
from django.conf import settings
import google.generativeai as genai



def fetch_latest_news():
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': 'us',
        'pageSize': 10,
        'apiKey': settings.NEWS_API_KEY,
    }
    response = requests.get(url, params=params)
    data = response.json()

    articles = data.get("articles", [])

    # Extract needed fields only
    news_list = []
    for article in articles:
        news_list.append({
            "title": article["title"],
            "url": article["url"],
            "summary": article["description"],  # We'll replace with AI summary later
            "source": article["source"]["name"],
            "published_at": article["publishedAt"]
        })

    return news_list


genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-2.0-flash')

def summarize_text(text):
    prompt = f"Summarize this news article briefly:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()

def fetch_news_by_query(query):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'pageSize': 10,
        'sortBy': 'publishedAt',
        'language': 'en',
        'apiKey': settings.NEWS_API_KEY,
    }
    response = requests.get(url, params=params)
    data = response.json()

    articles = data.get("articles", [])

    news_list = []
    for article in articles:
        summary_input = article.get("description") or "No description available."
        summary = summarize_text(summary_input)

        news_list.append({
            "title": article["title"],
            "url": article["url"],
            "summary": summary,
            "source": article["source"]["name"],
            "published_at": article["publishedAt"]
        })

    return news_list
