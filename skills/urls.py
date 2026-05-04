from django.urls import path
from .views import SkillListView, UpdateUserSkillView

urlpatterns = [
    path("skill-list/", SkillListView.as_view(), name="skill-list"),
    path("skills/update/", UpdateUserSkillView.as_view(), name="update-skill"),
]
