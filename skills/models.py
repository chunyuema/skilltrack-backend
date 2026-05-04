from django.db import models
from profiles.models import Profile

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
