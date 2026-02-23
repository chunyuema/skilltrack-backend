from os import wait

from django.conf import settings
from django.db import models


class Profile(models.Model):
    # Link to our custom user. If user is deleted, profile is deleted.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )

    full_name = models.CharField(max_length=255)
    title = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=255)
    education = models.TextField(blank=True)
    visa_status = models.CharField(max_length=50, blank=True)
    years_of_experience = models.IntegerField(default=0)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        if self.user:
            return f"Profile of {self.user.email}"
        return f"Profile (No User Assigned)"
