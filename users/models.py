from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Automatically create the user profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    from profiles.models import Profile

    if created:
        Profile.objects.create(user=instance)
