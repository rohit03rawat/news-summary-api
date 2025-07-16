from django.urls import path
from .views import SavedNewsView, SaveNewsView, LatestNewsView, SearchNewsView

urlpatterns = [
    path('saved/', SavedNewsView.as_view(), name='saved-news'),
    path('save/', SaveNewsView.as_view(), name='save-news'),
    path('latest/', LatestNewsView.as_view(), name='latest-news'),
    path('search/', SearchNewsView.as_view(), name='search-news'),

]
