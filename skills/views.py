from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Skill, SkillTheme, UserSkill
from .serializers import SkillThemeSerializer


class SkillListView(generics.ListAPIView):
    """
    Returns the full hierarchical skills matrix.
    Injects the current user's profile into the serializer context
    so that individual proficiency levels can be retrieved.
    """
    queryset = SkillTheme.objects.all()
    serializer_class = SkillThemeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Pass the logged-in user's profile to the serializer
        # Profile is imported in models.py of this app
        context["profile"] = self.request.user.profile
        return context


class UpdateUserSkillView(APIView):
    """
    Updates or creates a UserSkill record to track a specific 
    user's proficiency level in a specific skill.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        skill_id = request.data.get("skill_id")
        level = request.data.get("level")

        try:
            skill = Skill.objects.get(id=skill_id)
        except Skill.DoesNotExist:
            return Response(
                {"error": "Skill not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Update if it exists, otherwise create a new proficiency record
        user_skill, created = UserSkill.objects.update_or_create(
            profile=request.user.profile, skill=skill, defaults={"level": level}
        )

        return Response({"status": "success", "level": user_skill.level})
