from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review, ReviewLike


@receiver(post_save, sender=ReviewLike)
def increase_likes(sender, instance, **kwargs):
    review = instance.review
    review.likes = review.rlikes.count()
    review.save()

@receiver(post_delete, sender=ReviewLike)
def decrease_likes(sender, instance, **kwargs):
    review = instance.review
    review.likes = review.rlikes.count()
    review.save()