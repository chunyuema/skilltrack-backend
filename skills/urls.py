from django.urls import path
from .views import SkillListView, UpdateUserSkillView, TrackListView, UpdateUserTracksView

urlpatterns = [
    path("tracks/", TrackListView.as_view(), name="track-list"),
    path("tracks/update/", UpdateUserTracksView.as_view(), name="update-tracks"),
    path("skill-list/", SkillListView.as_view(), name="skill-list"),
    path("update/", UpdateUserSkillView.as_view(), name="update-skill"),
]
