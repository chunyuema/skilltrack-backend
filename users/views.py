from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import User


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]  # Anyone can sign up

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")

        # TODO: Add validation on the email
        if not email or not password or not first_name or not last_name:
            return Response(
                {"error": "Missing email, password, first name, or last name"},
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
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        return Response(
            {
                "message": "User created successfully",
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            status=status.HTTP_201_CREATED,
        )
