from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from skills.models import SkillTheme, SkillSubCategory, Skill, UserSkill

class SkillAPITests(APITestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password"
        )

        # Create basic skill structure
        self.theme = SkillTheme.objects.create(id="t1", name="Theme 1", order=0)
        self.subcat = SkillSubCategory.objects.create(id="sc1", theme=self.theme, name="Subcat 1", order=0)
        self.skill = Skill.objects.create(id="s1", sub_category=self.subcat, name="Skill 1", order=0)

        self.list_url = reverse("skill-list")
        self.update_url = reverse("update-skill")

    def test_fetch_skill_list_authenticated(self):
        """Verify an authenticated user can fetch the full skill tree."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], "t1")
        self.assertEqual(response.data[0]["subCategories"][0]["skills"][0]["id"], "s1")

    def test_fetch_skill_list_unauthenticated(self):
        """Verify anonymous requests are rejected."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_skill_level(self):
        """Verify a user can update their proficiency level."""
        self.client.force_authenticate(user=self.user1)
        data = {"skill_id": "s1", "level": 4}
        response = self.client.post(self.update_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["level"], 4)
        
        # Verify database record
        user_skill = UserSkill.objects.get(profile=self.user1.profile, skill=self.skill)
        self.assertEqual(user_skill.level, 4)

    def test_skill_level_isolation(self):
        """Verify that User A's skill levels do not affect User B."""
        # User 1 sets skill to 5
        self.client.force_authenticate(user=self.user1)
        self.client.post(self.update_url, {"skill_id": "s1", "level": 5}, format="json")

        # User 2 fetches list, should see level 0
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.list_url)
        
        skill_data = response.data[0]["subCategories"][0]["skills"][0]
        self.assertEqual(skill_data["id"], "s1")
        self.assertEqual(skill_data["level"], 0)

    def test_update_nonexistent_skill(self):
        """Verify updating a skill that doesn't exist returns 404."""
        self.client.force_authenticate(user=self.user1)
        data = {"skill_id": "nonexistent", "level": 3}
        response = self.client.post(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
