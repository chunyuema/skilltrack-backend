from rest_framework import serializers
from .models import Skill, SkillSubCategory, SkillTheme

class SkillSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()
    maxLevel = serializers.IntegerField(default=5, read_only=True)

    class Meta:
        model = Skill
        fields = ["id", "name", "description", "level", "maxLevel"]

    def get_level(self, obj):
        # 1. Access the profile we passed into the context from the view
        profile = self.context.get("profile")
        if profile:
            # 2. Query the UserSkill junction table for this specific user and skill
            user_skill = obj.userskill_set.filter(profile=profile).first()
            # 3. Return the specific level, defaulting to 0 if they haven't set it
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
