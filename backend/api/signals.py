from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, Post
from django.utils import timezone

@receiver(post_save, sender=Comment)
def update_post_last_updated(sender, instance, **kwargs):
    # Get the related post
    post = instance.post
    # Update the last_updated field to the current time
    post.updated_at = timezone.now()
    # Save the post instance
    post.save()
