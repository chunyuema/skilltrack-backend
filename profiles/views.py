from rest_framework import generics, permissions, viewsets

from .models import Experience
from .serializers import ExperienceSerializer, ProfileSerializer


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
