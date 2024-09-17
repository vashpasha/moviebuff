from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Review, ReviewLike


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'text', 'updated_at', 'likes']
        read_only = ['id', 'user', 'updated_at', 'likes']

class ReviewCreateSerializer(serializers.Serializer):
    movie_id = serializers.CharField(required=True)
    rating = serializers.IntegerField(
        required=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )
    text = serializers.TextField(required=True)

    def create(self, validated_data):
        movie_id = validated_data.pop('movie_id')
        user = self.context['request'].user
        review = Review.objects.create(movie_id=movie_id, user=user, **validated_data)
        return review
