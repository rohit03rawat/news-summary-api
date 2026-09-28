from celery import shared_task
from .utils import fetch_latest_news, summarize_text, fetch_news_by_query
from django.core.cache import cache

def build_latest_news():
    summarized_news = []
    for article in fetch_latest_news():
        article["summary"] = summarize_text(article["summary"])
        summarized_news.append(article)
    return summarized_news


def build_search_news(query):
    summarized_news = []
    for article in fetch_news_by_query(query):
        article["summary"] = summarize_text(article["summary"])
        summarized_news.append(article)
    return summarized_news


def _set_cache(key, value, timeout=None):
    try:
        cache.set(key, value, timeout=timeout)
    except Exception:
        pass


@shared_task
def generate_latest_news():
    try:
        summarized_news = build_latest_news()
        _set_cache("latest_news", summarized_news, timeout=300)
        _set_cache("news_status", "success")

    except Exception:
        _set_cache("news_status", "failed")

@shared_task
def generate_search_news(query):
    try:
        summarized_news = build_search_news(query)
        cache_key = f'query_news:{query.strip().lower()}'
        _set_cache(cache_key, summarized_news, timeout=300)
        _set_cache(f'{cache_key}:status', 'success')
    except Exception:
        cache_key = f'query_news:{query.strip().lower()}'
        _set_cache(f'{cache_key}:status', 'failed')