from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from accounts.models import CustomUser

User = get_user_model()

class UserAuthTests(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = CustomUser.objects.create_user(
            name='Test User',
            email='testuser@example.com',
            password='testpassword',
            roles='client'  # Default role as client
        )
        self.admin_user = CustomUser.objects.create_superuser(
            name='Admin User',
            email='admin@example.com',
            password='adminpassword',
            roles='admin'
        )

    def test_user_registration(self):
        # Test user registration
        response = self.client.post(reverse('signup'), {
            'name': 'New User',
            'email': 'newuser@example.com',
            'password1': 'newpassword',
            'password2': 'newpassword',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_login_with_valid_credentials(self):
        # Test login with valid credentials
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_with_invalid_credentials(self):
        # Test login with invalid credentials
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_restricted_page_as_client(self):
        # Test access to a page restricted to admin
        self.client.login(email='testuser@example.com', password='testpassword')
        response = self.client.get(reverse('admin_page'))  # Assume 'admin_page' is a URL restricted to admin
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_restricted_page_as_admin(self):
        # Test access to a page restricted to admin
        self.client.login(email='admin@example.com', password='adminpassword')
        response = self.client.get(reverse('admin_page'))  # Assume 'admin_page' is a URL restricted to admin
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logout(self):
        # Test user logout
        self.client.login(email='testuser@example.com', password='testpassword')
        response = self.client.post(reverse('logout'))  # Assume logout URL
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)