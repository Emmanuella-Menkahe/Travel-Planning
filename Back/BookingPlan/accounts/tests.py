from django.test import TestCase
from .models import TravelPlan, Agency
from django.contrib.auth import get_user_model

class CustomUserModelTests(TestCase):

    def setUp(self):
        """Create a custom user instance for testing."""
        self.User = get_user_model()  # Get the user model defined in settings
        self.user = self.User.objects.create_user(
            username="testuser",
            password="password123",
            roles="accommodation_receptionist"  # Set a specific role
        )

    def test_user_creation(self):
        """Test that a custom user is created correctly."""
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.check_password("password123"))  # Check password is hashed and valid
        self.assertEqual(self.user.roles, "accommodation_receptionist")

    def test_default_role(self):
        """Test that the default role is set correctly."""
        default_user = self.User.objects.create_user(
            username="defaultuser",
            password="password123"
        )
        self.assertEqual(default_user.roles, "client")  # Check the default role

    def test_string_representation(self):
        """Test the string representation of the user."""
        self.assertEqual(str(self.user), "testuser")  # Should return username

    def test_null_role(self):
        """Test that a user can be created without a specified role."""
        null_role_user = self.User.objects.create_user(
            username="nullroleuser",
            password="password123",
            roles=None  # Explicitly set role to None
        )
        self.assertIsNone(null_role_user.roles)  # Role should be None



#class TravelPlanModelTests(TestCase):
#     def setUp(self):
#         # Create a sample agency for testing
#         self.agency = Agency.objects.create(
#             name='Test Agency',
#             description='A test agency',
#             image='path/to/image.jpg',
#         )

#         # Create a sample travel plan
#         self.travel_plan = TravelPlan.objects.create(
#             departure='Yaoundé',
#             time='08:00:00',
#             price=200.00,
#             type='simple',
#             date='2024-12-01',
#             destination='Douala',
#             number_of_places=10,
#             number_of_available_places=10,
#             agency=self.agency,
#             status='active'
#         )

#     def test_travel_plan_str(self):
#         # Test the string representation of the travel plan
#         expected_str = "Yaoundé to Douala on 2024-12-01"
#         self.assertEqual(str(self.travel_plan), expected_str)

#     def test_update_available_places_success(self):
#         # Test that available places are updated correctly
#         self.travel_plan.update_available_places(5)
#         self.assertEqual(self.travel_plan.number_of_available_places, 5)

#     def test_update_available_places_not_enough(self):
#         # Test that updating available places raises an error when not enough places
#         with self.assertRaises(ValueError):
#             self.travel_plan.update_available_places(15)

#     def test_save_travel_plan_complete_status(self):
#         # Test that status is set to 'complete' when no available places
#         self.travel_plan.number_of_available_places = 0
#         self.travel_plan.save()
#         self.assertEqual(self.travel_plan.status, 'complete')

#     def test_save_travel_plan_active_status(self):
#         # Test that status remains 'active' when there are available places
#         self.travel_plan.number_of_available_places = 5
#         self.travel_plan.save()
#         self.assertEqual(self.travel_plan.status, 'active')
#