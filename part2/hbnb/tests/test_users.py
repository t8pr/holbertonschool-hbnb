import unittest
from app import create_app
from app.services import facade

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        """Test setup method to initialize the test client and clear the user repository."""
        self.app = create_app()
        self.client = self.app.test_client()
        facade.user_repo._storage = {}

    def test_create_user_success(self):
        """Test successful user creation."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Osama",
            "last_name": "Alhamdan",
            "email": "osama@example.com",
            "User_Rule": "owner"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_create_user_invalid_email(self):
        """test creating a user with an invalid email format."""
        self.client.post('/api/v1/users/', json={
            "first_name": "Osama",
            "last_name": "Alhamdan",
            "email": "osama@example.com",
            "User_Rule": "owner"
        })
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Ali",
            "last_name": "Ahmad",
            "email": "osama@example.com",
            "User_Rule": "user"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)