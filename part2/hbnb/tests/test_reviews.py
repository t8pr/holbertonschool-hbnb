import unittest
from app import create_app
from app.services import facade

class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        """Set up the test client and clear the repositories."""
        self.app = create_app()
        self.client = self.app.test_client()
        
        facade.review_repo._storage = {}
        facade.place_repo._storage = {}
        facade.user_repo._storage = {}

        self.user = facade.create_user({
            "first_name": "Test", 
            "last_name": "Reviewer", 
            "email": "reviewer@example.com"
        })

        self.place = facade.create_place({
            "title": "Awesome Getaway",
            "price": 120.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.user.id
        })

    def test_create_review_success(self):
        """Test successful review creation."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Amazing experience, highly recommended!",
            "rating": 5,
            "user_id": self.user.id,
            "place_id": self.place.id
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
        self.assertEqual(response.json["text"], "Amazing experience, highly recommended!")
        self.assertEqual(response.json["rating"], 5)

    def test_create_review_invalid_rating(self):
        """Test creating a review with an invalid rating (out of 1-5 range)."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Off the charts!",
            "rating": 6,  # Invalid Input: Rating should be between 1 and 5
            "user_id": self.user.id,
            "place_id": self.place.id
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_create_review_empty_text(self):
        """Test creating a review with empty text."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",  # Invalid Input: Text cannot be empty
            "rating": 4,
            "user_id": self.user.id,
            "place_id": self.place.id
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_get_all_reviews(self):
        """Test retrieving all reviews."""
        # Create a review first
        self.client.post('/api/v1/reviews/', json={
            "text": "Good place.",
            "rating": 4,
            "user_id": self.user.id,
            "place_id": self.place.id
        })        
        response = self.client.get('/api/v1/reviews/')
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) > 0)