from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    # We pull the email from the linked User model
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "full_name",
            "title",
            "email",
            "phone",
            "location",
            "education",
            "visa_status",
            "years_of_experience",
            "github_url",
            "linkedin_url",
            "bio",
        ]
