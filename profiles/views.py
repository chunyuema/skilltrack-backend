from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Experience, Skill, SkillTheme, UserSkill
from .serializers import (
    ExperienceSerializer,
    ProfileSerializer,
    SkillThemeSerializer,
)


class MyProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # This looks up the profile belonging to the logged-in user
        return self.request.user.profile


class ExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return experiences belonging to the logged-in user
        return Experience.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        # Automatically link the experience to the user's profile
        serializer.save(profile=self.request.user.profile)


class SkillListView(generics.ListAPIView):
    queryset = SkillTheme.objects.all()
    serializer_class = SkillThemeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["profile"] = self.request.user.profile
        return context


class UpdateUserSkillView(APIView):
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

        user_skill, created = UserSkill.objects.update_or_create(
            profile=request.user.profile, skill=skill, defaults={"level": level}
        )

        return Response({"status": "success", "level": user_skill.level})
