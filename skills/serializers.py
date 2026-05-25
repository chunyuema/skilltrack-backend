from rest_framework import serializers
from .models import Skill, SkillSubCategory, SkillTheme, Track


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ["id", "name", "track_type"]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name", "description"]


class SkillSubCategorySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    level = serializers.SerializerMethodField()
    maxLevel = serializers.IntegerField(default=5, read_only=True)

    class Meta:
        model = SkillSubCategory
        fields = ["id", "name", "skills", "level", "maxLevel"]

    def get_level(self, obj):
        profile = self.context.get("profile")
        if profile:
            user_skill = obj.userskill_set.filter(profile=profile).first()
            return user_skill.level if user_skill else 0
        return 0


class SkillThemeSerializer(serializers.ModelSerializer):
    track = TrackSerializer(read_only=True)
    subCategories = SkillSubCategorySerializer(
        many=True, read_only=True, source="sub_categories"
    )

    class Meta:
        model = SkillTheme
        fields = ["id", "name", "description", "track", "subCategories"]
