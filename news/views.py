# news/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import SavedNews
from .serializers import SavedNewsSerializer
from .utils import fetch_latest_news, summarize_text, fetch_news_by_query
from django.shortcuts import render
from django.core.cache import cache
from .tasks import generate_latest_news, generate_search_news

class SavedNewsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        saved_news = SavedNews.objects.filter(user=request.user)
        serializer = SavedNewsSerializer(saved_news, many=True)
        return Response(serializer.data)

class SaveNewsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SavedNewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LatestNewsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        cached_news = cache.get("latest_news")

        if cached_news:
            print("Serving from cache")
            return Response(cached_news)

        news_status = cache.get('news_status')

        print("Generating fresh summaries")
        
        if news_status == 'processing':
            return Response({'status' : 'processing'})
        
        if news_status == 'failed':
            return Response(
                {'status': 'failed', "message": "Unable to generate summaries."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        
        cache.set("news_status", 'processing')
        
        generate_latest_news.delay()

        return Response({
            "status": "processing"})
    
class SearchNewsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q')
        if not query:
            return Response({"error": "Search term (q) is required."}, status=400)

        cache_key = f'query_news:{query.strip().lower()}'
        status_key = f'{cache_key}:status'
        cached_query_news = cache.get(cache_key)

        if cached_query_news:
            print('serving from cache')
            return Response(cached_query_news)
        
        query_status = cache.get(status_key)

        print("Generating fresh summaries")
        
        if query_status == 'processing':
            return Response({'status' : 'processing'})
        
        if query_status == 'failed':
            return Response(
                {'status': 'failed', "message": "Unable to generate summaries."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        
        cache.set(status_key, 'processing')
        
        generate_search_news.delay(query)

        return Response({
            "status": "processing"})

def frontend(request):
    return render(request, 'index.html')

# def frontend(request):
#     try:
#         response = requests.get(WORKER_URL, timeout=2)
#         print("Second service pinged:", response.status_code)
#     except requests.RequestException as e:
#         print("Worker not reachable:", e)

#     return render(request, "index.html")
