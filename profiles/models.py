from os import wait

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    # Link to our custom user. If user is deleted, profile is deleted.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    title = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=255, blank=True)
    education = models.TextField(blank=True)
    visa_status = models.CharField(max_length=50, blank=True)
    years_of_experience = models.IntegerField(null=True, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        if self.user:
            return f"Profile of {self.user.email}"
        return f"Profile (No User Assigned)"

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip()


class SkillTheme(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class SkillSubCategory(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    theme = models.ForeignKey(
        SkillTheme, on_delete=models.CASCADE, related_name="sub_categories"
    )
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.theme.name} > {self.name}"


class Skill(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    sub_category = models.ForeignKey(
        SkillSubCategory, on_delete=models.CASCADE, related_name="skills"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class UserSkill(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="skills"
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)

    class Meta:
        unique_together = ("profile", "skill")

    def __str__(self):
        return f"{self.profile.user.email} - {self.skill.name}: {self.level}"


class Experience(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="experiences"
    )
    company = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    start_date = models.CharField(max_length=7)  # e.g., "2022-01"
    end_date = models.CharField(
        max_length=7, blank=True, null=True
    )  # e.g., "2024-05" or null for "Present"
    description = models.TextField()
    technologies = models.JSONField(default=list)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.role} at {self.company}"
