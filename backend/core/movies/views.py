from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

from .services import search_movie, get_movie
from .models import FeaturedMovie
from .serializers import MovieSerializer


class MovieSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('query')

        if not query:
            return Response({'error': 'query params is required'}, status=status.HTTP_400_BAD_REQUEST)

        movies = search_movie(query)
        if movies:
            serialized_movies = MovieSerializer(movies, many=True).data
            return Response(serialized_movies, status=status.HTTP_200_OK)
        return Response({'error':'no movies found'}, status=status.HTTP_404_NOT_FOUND)

class MovieDetailView(APIView):
    def get(self, request, movie_id):
        movie = get_movie(movie_id)
        
        if movie:
            return Response(movie, status=status.HTTP_200_OK)
        return Response({'error':'movie not found'}, status=status.HTTP_404_NOT_FOUND)

class MovieFeedView(APIView):
    def get(self, request):
        featured_movies = FeaturedMovie.objects.all().order_by('-added_at')
        movies = []

        for featured in featured_movies:
            movie_id = featured.movie_id
            cache_key = f'movie_detail_{movie_id}'
            movie = cache.get(cache_key)

            if not movie:
                movie = get_movie(movie_id)
                if movie:
                    cache.set(cache_key, movie, timeout=60*60)

            if movie:
                movies.append(movie)
        
        if movies:
            serialized_movies = MovieSerializer(movies, many=True).data
            return Response(serialized_movies, status=status.HTTP_200_OK)
        return Response({'error':'no movies found'}, status=status.HTTP_404_NOT_FOUND)
