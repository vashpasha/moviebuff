from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    movie_id = models.CharField(max_length=20)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )
    text = models.TextField(null=False, blank=False)

    updated_at=models.DateTimeField(default=timezone.now)
    likes = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'moie_id'], name='unique_review')
        ]

    def save(self, *args, **kwargs):
        if self.pk and (self.rating != Review.objects.get(pk=self.pk).rating or
                        self.text != Review.objects.get(pk=self.pk).text):
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'reiew by {self.user} for {self.movie_id}'


class ReviewLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='reviewslikes'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='rlikes'
    )
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'review'], name='unique_reviewlike')
        ]

    def __str__(self):
        return f'{self.user} likes review {self.review.id}'