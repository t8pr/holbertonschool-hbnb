import unittest
from app import create_app
from app.services import facade

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        facade.place_repo._storage = {}
        facade.user_repo._storage = {}

        self.owner = facade.create_user({
            "first_name": "Host", "last_name": "User", 
            "email": "host@example.com", "User_Rule": "owner"
        })

    def test_create_place_success(self):
        """Test successful place creation."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "price": 45.0,
            "latitude": 24.7136,
            "longitude": 46.6753,
            "owner_id": self.owner.id
        })
        self.assertEqual(response.status_code, 201)

    def test_create_place_invalid_latitude(self):
        """Test creating place with invalid latitude."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Invalid Place",
            "price": 50.0,
            "latitude": 120.0,  # Invalid Input: Latitude should be between -90 and 90
            "longitude": 46.6753,
            "owner_id": self.owner.id
        })
        self.assertEqual(response.status_code, 400)