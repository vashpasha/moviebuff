from django.urls import path
from .views import MovieDetailView, MovieFeedView, MovieSearchView


urlpatterns = [
    path('feed/', MovieFeedView.as_view(), name='feed'),
    path('search/', MovieSearchView.as_view(), name='search'),
    path('detail/<str:movie_id>/', MovieDetailView.as_view(), name='detail'),

]