from django.db import models
from profiles.models import Profile

class Track(models.Model):
    TRACK_TYPES = (
        ("CORE", "Core Essentials"),
        ("DOMAIN", "Standard Professional Domain"),
        ("SPECIAL", "Advanced Specialization"),
    )
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    track_type = models.CharField(max_length=10, choices=TRACK_TYPES, default="DOMAIN")

    def __str__(self):
        return f"{self.name} ({self.get_track_type_display()})"


class SkillTheme(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    track = models.ForeignKey(
        Track, on_delete=models.CASCADE, related_name="themes", null=True, blank=True
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"[{self.track.id if self.track else 'N/A'}] {self.name}"


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
    sub_category = models.ForeignKey(SkillSubCategory, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)

    class Meta:
        unique_together = ("profile", "sub_category")

    def __str__(self):
        return f"{self.profile.user.email} - {self.sub_category.name}: {self.level}"
