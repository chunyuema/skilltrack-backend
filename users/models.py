from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


# Automatically create the user profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    from profiles.models import Profile

    if created:
        Profile.objects.get_or_create(user=instance)
