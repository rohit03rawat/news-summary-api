import requests
from django.conf import settings
from google import genai
from django.conf import settings


client = genai.Client(api_key=settings.GEMINI_API_KEY)

def summarize_text(text):
    try:
        prompt = f"Summarize this news article briefly:\n\n{text}"
        response = client.models.generate_content(model='gemini-3.1-flash-lite',
        contents=prompt)
        return response.text.strip()
    except Exception as e:
        print(f'error in summarise : {e}')
        return "summary unavailable - Daily limit reached"

def fetch_latest_news():
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': 'us',
        'pageSize': 4,
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
            "summary": article["description"],  # replace with AI summary later
            "source": article["source"]["name"],
            "published_at": article["publishedAt"]
        })

    return news_list

def fetch_news_by_query(query):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'pageSize': 2,
        'sortBy': 'publishedAt',
        'language': 'en',
        'apiKey': settings.NEWS_API_KEY,
    }
    response = requests.get(url, params=params)
    data = response.json()

    articles = data.get("articles", [])

    news_list = []

    for article in articles:
        
        news_list.append({
            "title": article["title"],
            "url": article["url"],
            "summary": article['description'],
            "source": article["source"]["name"],
            "published_at": article["publishedAt"]
        })

    return news_list
