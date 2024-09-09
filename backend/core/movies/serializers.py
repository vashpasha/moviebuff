from rest_framework import serializers


class MovieSerializer(serializers.Serializer):
    Title = serializers.CharField(max_length=255)
    Year = serializers.CharField()
    Genre = serializers.CharField()
    Poster = serializers.CharField()
    Director = serializers.CharField()
    imdbRating = serializers.CharField()