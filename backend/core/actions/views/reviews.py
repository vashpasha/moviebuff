from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Review, ReviewLike
from .serializers import ReviewSerializer, ReviewCreateSerializer
from ...movies.services import get_movie

class ReviewCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ReviewCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            review = serializer.save()
            response_serializer = ReviewSerializer(review)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewUpdateView(APIView):
    def put(self, request, pk,  *args, **kwargs):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({'detail': 'not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDeleteiew(APIView):
    def delete(self, request, pk, *args, **kwargs):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({'detail': 'not found'}, status=status.HTTP_404_NOT_FOUND)


        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewDetailView(APIView):
    def get_movie_data(self, movie_id):
        movie = get_movie(movie_id)
        return {
            'id': movie.get('imdbID'),
            'title': movie.get('Title'),
            'year': movie.get('Year'),
            'poster': movie.get('Poster')
        }

    def get(self, request, pk, *args, **kwargs):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({'detail': 'not found'}, status=status.HTTP_404_NOT_FOUND)

        review_data = ReviewSerializer(review).data
        movie_data = self.get_movie_data(review.movie_id)

        response_data = {
            'review': review_data,
            'movie': movie_data
        }
        return Response(response_data, status=status.HTTP_200_OK)


class ReviewListView(APIView):
    def get_movie_data(self, movie_id):
        movie = get_movie(movie_id)
        return {
            'id': movie.get('imdbID'),
            'title': movie.get('Title'),
            'year': movie.get('Year'),
            'poster': movie.get('Poster')
        }

    def get(self, request, *args, **kwargs):
        reviews = Review.objects.all()

        response_data = []
        for review in reviews:
            movie_data = self.get_movie_data(review.movie_id)
            review_data = ReviewSerializer(review).data
            response_data.append({
                'review': review_data,
                'movie': movie_data
            })

        return Response(response_data, status=status.HTTP_200_OK)


class ReviewLikeView(APIView):
    def post(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return Response({'detail': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if ReviewLike.objects.filter(user=user, review=review).exists():
            return Response({'detail': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)

        ReviewLike.objects.create(user=user, review=review)
        return Response({'detail': 'Liked'}, status=status.HTTP_201_CREATED)

    def delete(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return Response({'detail': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        like = ReviewLike.objects.filter(user=user, review=review).first()
        if not like:
            return Response({'detail': 'Not liked'}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({'detail': 'Unliked'}, status=status.HTTP_204_NO_CONTENT)