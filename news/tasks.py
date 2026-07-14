from celery import shared_task
from .utils import fetch_latest_news, summarize_text, fetch_news_by_query
from django.core.cache import cache

@shared_task
def generate_latest_news():

    try:

        raw_news = fetch_latest_news()

        summarized_news = []

        for article in raw_news:
                summary = summarize_text(article["summary"])
                article["summary"] = summary
                summarized_news.append(article)

        cache.set(
                "latest_news",
                summarized_news,
                timeout=300
            )
        cache.set('news_status' , 'success')

    except Exception:
            cache.set("news_status", "failed")

@shared_task
def generate_search_news(query):
      
    try:
            query_news = fetch_news_by_query(query)

            summarized_query_news = []

            for article in query_news:
                summary = summarize_text(article["summary"])
                article["summary"] = summary
                summarized_query_news.append(article)
                  
            cache.set(
                "query_news",
                summarized_query_news,
                timeout=300
            )
           
            cache.set('query_news_status' , 'success')



    except Exception:
            cache.set('query_news_status', 'failed')