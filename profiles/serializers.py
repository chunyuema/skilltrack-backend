from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    # These are read-only because they come from the User model
    email = serializers.EmailField(source="user.email", read_only=True)
    full_name = serializers.ReadOnlyField()

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

        # This ensures PATCH requests don't require these fields
        extra_kwargs = {
            field: {"required": False, "allow_blank": True}
            for field in [
                "title",
                "phone",
                "location",
                "education",
                "visa_status",
                "github_url",
                "linkedin_url",
                "bio",
            ]
        }
