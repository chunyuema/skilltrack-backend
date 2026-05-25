from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from .models import Skill, SkillTheme, UserSkill, Track, SkillSubCategory
from .serializers import SkillThemeSerializer, TrackSerializer


class TrackListView(generics.ListAPIView):
    """
    Returns all available tracks (CORE, DOMAIN, SPECIAL).
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticated]


class SkillListView(generics.ListAPIView):
    """
    Returns the filtered hierarchical skills matrix based on user selection.
    Always includes CORE tracks.
    """
    serializer_class = SkillThemeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        profile = self.request.user.profile
        # Filter: track_type is CORE OR track is in profile.selected_tracks
        return SkillTheme.objects.filter(
            Q(track__track_type="CORE") | Q(track__in=profile.selected_tracks.all())
        ).distinct()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["profile"] = self.request.user.profile
        return context


class UpdateUserTracksView(APIView):
    """
    Updates the user's selected tracks (Domains and Specializations).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        track_ids = request.data.get("track_ids", [])
        profile = request.user.profile
        
        # Only allow setting DOMAIN and SPECIAL tracks? 
        # Actually CORE is always included in the view, so setting it here doesn't hurt.
        tracks = Track.objects.filter(id__in=track_ids)
        profile.selected_tracks.set(tracks)
        
        return Response({"status": "success", "selected_tracks": [t.id for t in tracks]})

class UpdateUserSkillView(APIView):
    """
    Updates or creates a UserSkill record to track a specific 
    user's proficiency level in a specific skill subcategory.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        sub_category_id = request.data.get("sub_category_id")
        level = request.data.get("level")

        try:
            sub_category = SkillSubCategory.objects.get(id=sub_category_id)
        except SkillSubCategory.DoesNotExist:
            return Response(
                {"error": "SubCategory not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Update if it exists, otherwise create a new proficiency record
        user_skill, created = UserSkill.objects.update_or_create(
            profile=request.user.profile, sub_category=sub_category, defaults={"level": level}
        )

        return Response({"status": "success", "level": user_skill.level})
