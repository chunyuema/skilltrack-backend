from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ExperienceViewSet,
    MyProfileView,
    SkillListView,
    UpdateUserSkillView,
)

router = DefaultRouter()
router.register(r"experiences", ExperienceViewSet, basename="experience")

urlpatterns = [
    path("me/", MyProfileView.as_view(), name="my-profile"),
    path("skill-list/", SkillListView.as_view(), name="skill-list"),
    path("skills/update/", UpdateUserSkillView.as_view(), name="update-skill"),
    path("", include(router.urls)),
]
