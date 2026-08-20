"""Review API endpoints"""

from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

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
    """Resource for review list operations"""

    @api.response(200, "Reviews successfully retrieved")
    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

    @api.expect(review_model, validate=True)
    @api.response(201, "Review successfully created")
    @api.response(400, "Invalid input data")
    @api.response(401, "Unauthorized")
    @jwt_required() 
    def post(self):
        """Create a new review"""
        current_user = get_jwt_identity()
        review_data = api.payload

        place = facade.get_place(review_data['place_id'])
        if not place:
            return {"error": "Place not found"}, 404

        if place.owner_id == current_user:
            return {'error': 'You cannot review your own place.'}, 400

        existing_reviews = facade.get_reviews_by_place(place.id)
        if any(r.user_id == current_user for r in existing_reviews):
            return {'error': 'You have already reviewed this place.'}, 400

        review_data['user_id'] = current_user

        try:
            new_review = facade.create_review(review_data)
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400
        
        return new_review.to_dict(), 201

@api.route("/<string:review_id>")
@api.param("review_id", "The unique identifier of the review")
class ReviewResource(Resource):
    """Resource for individual review operations"""

    @api.response(200, "Review successfully retrieved")
    @api.response(404, "Review not found")
    def get(self, review_id):
        """Retrieve a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @api.expect(review_update_model, validate=True)
    @api.response(200, "Review successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Review not found")
    @jwt_required()
    def put(self, review_id):
        """Update an existing review"""
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if not is_admin and review.user_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        review_data = api.payload
        if not review_data:
            return {"error": "No update data provided"}, 400

        try:
            updated_review = facade.update_review(review_id, review_data)
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400

        return updated_review.to_dict(), 200

    @api.response(200, "Review successfully deleted")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Review not found")
    @jwt_required()
    def delete(self, review_id):
        """Delete an existing review"""
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if not is_admin and review.user_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200

@api.route("/<string:place_id>/reviews")
@api.param("place_id", "The unique identifier of the place")
class PlaceReviewList(Resource):
    """Resource for retrieving reviews of a specific place"""

    @api.response(200, "Reviews successfully retrieved")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Retrieve all reviews associated with a specific place"""

        reviews = facade.get_reviews_by_place(place_id)

        if reviews is None:
            return {"error": "Place not found"}, 404

        return [review.to_dict()
                for review in reviews], 200
