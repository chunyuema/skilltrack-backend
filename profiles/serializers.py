from rest_framework import serializers

from .models import Experience, Profile, Skill, SkillSubCategory, SkillTheme


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


class SkillSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()
    maxLevel = serializers.IntegerField(default=5, read_only=True)

    class Meta:
        model = Skill
        fields = ["id", "name", "description", "level", "maxLevel"]

    def get_level(self, obj):
        profile = self.context.get("profile")
        if profile:
            user_skill = obj.userskill_set.filter(profile=profile).first()
            return user_skill.level if user_skill else 0
        return 0


class SkillSubCategorySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = SkillSubCategory
        fields = ["id", "name", "skills"]


class SkillThemeSerializer(serializers.ModelSerializer):
    subCategories = SkillSubCategorySerializer(
        many=True, read_only=True, source="sub_categories"
    )

    class Meta:
        model = SkillTheme
        fields = ["id", "name", "description", "subCategories"]


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
            "experiences",
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
