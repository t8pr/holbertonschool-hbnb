import unittest
from app import create_app
from app.services import facade

class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        facade.amenity_repo._storage = {}

    def test_create_amenity_success(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi",
            "description": "High-speed internet access"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Wi-Fi")