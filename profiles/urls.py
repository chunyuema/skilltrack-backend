from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ExperienceViewSet, MyProfileView

router = DefaultRouter()
router.register(r"experiences", ExperienceViewSet, basename="experience")

urlpatterns = [
    path("me/", MyProfileView.as_view(), name="my-profile"),
    path("", include(router.urls)),
]
