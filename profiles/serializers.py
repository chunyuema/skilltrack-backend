from rest_framework import serializers

from .models import Experience, Profile


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            "id",
            "company",
            "role",
            "start_date",
            "end_date",
            "description",
            "technologies",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data["end_date"]:
            data["end_date"] = "Present"
        return data


class ProfileSerializer(serializers.ModelSerializer):
    # These are read-only because they come from the User model
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(
        source="user.first_name", required=False, allow_blank=True
    )
    last_name = serializers.CharField(
        source="user.last_name", required=False, allow_blank=True
    )
    experiences = ExperienceSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "country",
            "location",
            "education",
            "visa_status",
            "years_of_experience",
            "github_url",
            "linkedin_url",
            "bio",
            "experiences",
        ]

        # This ensures PATCH requests don't require these fields
        extra_kwargs = {
            field: {"required": False, "allow_blank": True}
            for field in [
                "phone",
                "country",
                "location",
                "education",
                "visa_status",
                "github_url",
                "linkedin_url",
                "bio",
            ]
        }

    def update(self, instance, validated_data):
        # Extract user data from validated_data
        # When using source="user.first_name", DRF puts it in validated_data['user']['first_name']
        user_data = validated_data.pop("user", {})
        first_name = user_data.get("first_name")
        last_name = user_data.get("last_name")

        # Update the User object associated with the Profile
        user = instance.user
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name

        if first_name is not None or last_name is not None:
            user.save()

        # Update the Profile object with the remaining validated_data
        return super().update(instance, validated_data)
