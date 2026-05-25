from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Experience


class ProfileTests(APITestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
            first_name="Original",
            last_name="Name",
        )
        # Authenticate the user
        self.client.force_authenticate(user=self.user)
        self.url = reverse("my-profile")

    def test_get_profile_includes_first_and_last_name(self):
        """
        Verify that GET returns the separate first_name and last_name.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Original")
        self.assertEqual(response.data["last_name"], "Name")
        self.assertNotIn("full_name", response.data)

    def test_update_profile_first_and_last_name(self):
        """
        Verify that PATCH can update the user's first and last name via the profile API.
        """
        data = {
            "first_name": "Updated",
            "last_name": "User",
            "country": "Germany",
        }
        response = self.client.patch(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Updated")
        self.assertEqual(response.data["last_name"], "User")
        self.assertEqual(response.data["country"], "Germany")

        # Verify the underlying User object was updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "User")


class ExperienceAPITests(APITestCase):
    def setUp(self):
        # Create two users for isolation testing
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password"
        )

        self.list_create_url = reverse("experience-list")

    def test_create_experience(self):
        """
        Verify an authenticated user can create an experience.
        """
        self.client.force_authenticate(user=self.user1)
        data = {
            "company": "Tech Corp",
            "role": "Software Engineer",
            "start_date": "2022-01",
            "description": "Building cool stuff.",
            "technologies": ["Python", "Django"],
        }
        response = self.client.post(self.list_create_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Experience.objects.count(), 1)
        experience = Experience.objects.first()
        self.assertEqual(experience.profile, self.user1.profile)
        self.assertEqual(experience.company, "Tech Corp")

    def test_list_experiences_isolation(self):
        """
        Verify users only see their own experiences.
        """
        # Create experience for user 1
        Experience.objects.create(
            profile=self.user1.profile,
            company="User 1 Company",
            role="Dev",
            start_date="2020-01",
            description="desc",
        )
        # Create experience for user 2
        Experience.objects.create(
            profile=self.user2.profile,
            company="User 2 Company",
            role="Designer",
            start_date="2021-01",
            description="desc",
        )

        # Authenticate as user 1
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_create_url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["company"], "User 1 Company")

    def test_update_experience_permissions(self):
        """
        Verify a user cannot update another user's experience.
        """
        exp2 = Experience.objects.create(
            profile=self.user2.profile,
            company="User 2 Company",
            role="Designer",
            start_date="2021-01",
            description="desc",
        )
        detail_url = reverse("experience-detail", args=[exp2.id])

        # Try to update as user 1
        self.client.force_authenticate(user=self.user1)
        data = {"company": "Hacker Corp"}
        response = self.client.patch(detail_url, data, format="json")

        # DRF returns 404 when the object is filtered out of the queryset
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        exp2.refresh_from_db()
        self.assertEqual(exp2.company, "User 2 Company")

    def test_serialization_logic_present(self):
        """
        Verify that null end_date is serialized as 'Present'.
        """
        Experience.objects.create(
            profile=self.user1.profile,
            company="Current Job",
            role="Lead",
            start_date="2023-01",
            end_date=None,
            description="Still here",
        )
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.data[0]["end_date"], "Present")

    def test_unauthenticated_access_denied(self):
        """
        Verify anonymous requests are rejected.
        """
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
