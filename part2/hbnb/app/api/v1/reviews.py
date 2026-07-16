"""Review API endpoints."""

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("reviews", description="Review operations")

review_model = api.model("Review", {
    "id": fields.String(readonly=True, description="The unique identifier of a review"),
    "text": fields.String(required=True, description="Text of the review"),
    "rating": fields.Integer(required=True, description="Rating of the place from 1 to 5"),
    "user_id": fields.String(required=True, description="ID of the user"),
    "place_id": fields.String(required=True, description="ID of the place")
})

review_update_model = api.model("ReviewUpdate", {
    "text": fields.String(required=False, description="New text of the review"),
    "rating": fields.Integer(required=False, description="New rating from 1 to 5")
})

@api.route("/")
class ReviewList(Resource):
    """Resource for review list operations."""

    @api.response(200, "Reviews successfully retrieved")
    def get(self):
        """Retrieve all reviews."""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

    @api.expect(review_model, validate=True)
    @api.response(201, "Review successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """Create a new review."""
        review_data = api.payload
        try:
            new_review = facade.create_review(review_data)
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400
        return new_review.to_dict(), 201

@api.route("/<string:review_id>")
@api.param("review_id", "The unique identifier of the review")
class ReviewResource(Resource):
    """Resource for individual review operations."""

    @api.response(200, "Review successfully retrieved")
    @api.response(404, "Review not found")
    def get(self, review_id):
        """Retrieve a review by ID."""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @api.expect(review_update_model, validate=True)
    @api.response(200, "Review successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(404, "Review not found")
    def put(self, review_id):
        """Update an existing review."""
        review_data = api.payload
        if not review_data:
            return {"error": "No update data provided"}, 400
        try:
            updated_review = facade.update_review(review_id, review_data)
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400
        
        if updated_review is None:
            return {"error": "Review not found"}, 404
        return {"message": "Review updated successfully"}, 200  

    @api.response(200, "Review successfully deleted")
    @api.response(404, "Review not found")
    def delete(self, review_id):
        """Delete an existing review."""
        deleted = facade.delete_review(review_id)
        if not deleted:
            return {"error": "Review not found"}, 404
        return {"message": "Review deleted successfully"}, 200