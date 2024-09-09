from django.db import models


class FeaturedMovie(models.Model):
    movie_id = models.CharField(max_length=20, unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.movie_id