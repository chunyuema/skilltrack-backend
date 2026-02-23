from rest_framework import generics, permissions

from .serializers import ProfileSerializer


class MyProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # This looks up the profile belonging to the logged-in user
        return self.request.user.profile
