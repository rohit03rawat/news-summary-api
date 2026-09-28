from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase
from rest_framework.test import APIRequestFactory

from .views import LatestNewsView, SearchNewsView


class RedisUnavailableFallbackTests(SimpleTestCase):
	def setUp(self):
		self.request_factory = RequestFactory()
		self.api_request_factory = APIRequestFactory()
		self.news = [{"title": "Test news", "summary": "A summary"}]

	@patch("news.views.build_latest_news")
	@patch("news.views.generate_latest_news.delay")
	@patch("news.views.cache.set", side_effect=ConnectionError)
	@patch("news.views.cache.get", side_effect=ConnectionError)
	def test_latest_news_runs_inline_when_cache_is_unavailable(
		self, cache_get, cache_set, enqueue, build_news
	):
		build_news.return_value = self.news

		response = LatestNewsView().get(self.request_factory.get("/news/latest/"))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data, self.news)
		enqueue.assert_not_called()

	@patch("news.views.build_latest_news")
	@patch("news.views.generate_latest_news.delay")
	@patch("news.views._celery_available", return_value=False)
	@patch("news.views.cache.set", return_value=True)
	@patch("news.views.cache.get", return_value=None)
	def test_latest_news_runs_inline_when_worker_is_unavailable(
		self, cache_get, cache_set, celery_available, enqueue, build_news
	):
		build_news.return_value = self.news

		response = LatestNewsView().get(self.request_factory.get("/news/latest/"))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data, self.news)
		enqueue.assert_not_called()

	@patch("news.views.build_search_news")
	@patch("news.views.generate_search_news.delay", side_effect=ConnectionError)
	@patch("news.views._celery_available", return_value=True)
	@patch("news.views.cache.set", return_value=True)
	@patch("news.views.cache.get", return_value=None)
	def test_search_news_runs_inline_when_celery_cannot_enqueue(
		self, cache_get, cache_set, celery_available, enqueue, build_news
	):
		build_news.return_value = self.news
		request = SearchNewsView().initialize_request(
			self.api_request_factory.get("/news/search/?q=technology")
		)

		response = SearchNewsView().get(request)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data, self.news)
		build_news.assert_called_once_with("technology")

	@patch("news.views.build_search_news")
	@patch("news.views.generate_search_news.delay")
	@patch("news.views._celery_available", return_value=False)
	@patch("news.views.cache.set", return_value=True)
	@patch("news.views.cache.get", side_effect=[None, "processing"])
	def test_search_news_recovers_when_processing_worker_disappears(
		self, cache_get, cache_set, celery_available, enqueue, build_news
	):
		build_news.return_value = self.news
		request = SearchNewsView().initialize_request(
			self.api_request_factory.get("/news/search/?q=technology")
		)

		response = SearchNewsView().get(request)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data, self.news)
		build_news.assert_called_once_with("technology")
		enqueue.assert_not_called()
