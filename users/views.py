from os import wait

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from profiles.models import Profile  # To verify it works

from .models import User


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]  # Anyone can sign up

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # TODO: Add validation on the email
        if not email or not password:
            return Response(
                {"error": "Email and password required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the user has already been created, return 400 if user exists
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "A user with this email already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # This will create user and also create an empty profile which allows update
        user = User.objects.create_user(
            email=email,
            password=password,
            username=email,
        )

        return Response(
            {"message": "User created successfully", "email": user.email},
            status=status.HTTP_201_CREATED,
        )
