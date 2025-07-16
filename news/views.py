# news/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import SavedNews
from .serializers import SavedNewsSerializer
from .utils import fetch_latest_news, summarize_text, fetch_news_by_query
from django.shortcuts import render


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
        raw_news = fetch_latest_news()

        summarized_news = []
        for article in raw_news:
            summary = summarize_text(article["summary"])
            article["summary"] = summary
            summarized_news.append(article)

        return Response(summarized_news)
    
class SearchNewsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q')
        if not query:
            return Response({"error": "Search term (q) is required."}, status=400)

        news = fetch_news_by_query(query)
        return Response(news)


def frontend(request):
    return render(request, 'index.html')
