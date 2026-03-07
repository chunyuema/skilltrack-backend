from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


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
            "title": "Software Engineer",
        }
        response = self.client.patch(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Updated")
        self.assertEqual(response.data["last_name"], "User")

        # Verify the underlying User object was updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "User")
