"""Place API endpoints."""

from flask_restx import Namespace, Resource, fields
from app.services import facade
from part2.hbnb.app.models import place

api = Namespace("places", description="Place operations")

user_model = api.model("PlaceUser", {
    "id": fields.String(readonly=True, description="User ID"),
    "first_name": fields.String(description="First name of the owner"),
    "last_name": fields.String(description="Last name of the owner"),
    "email": fields.String(description="Email of the owner")
})

amenity_model = api.model("PlaceAmenity", {
    "id": fields.String(readonly=True, description="Amenity ID"),
    "name": fields.String(description="Name of the amenity")
})

review_model = api.model("PlaceReview", {
    "id": fields.String(readonly=True, description="Review ID"),
    "text": fields.String(description="Text of the review"),
    "rating": fields.Integer(description="Rating of the place from 1 to 5"),
    "user_id": fields.String(description="ID of the user")
})

"""we will use this for both the Place and PlaceUpdate models to avoid redundancy"""
place_model = api.model("Place", {
    "title": fields.String(required=True, description="Title of the place"),
    "description": fields.String(required=False, description="Description of the place"),
    "price": fields.Float(required=True, description="Price per night"),
    "latitude": fields.Float(required=True, description="Latitude of the place"),
    "longitude": fields.Float(required=True, description="Longitude of the place"),
    "owner_id": fields.String(required=True, description="ID of the owner"),
    "amenities": fields.List(fields.String, required=False, description="List of amenity IDs")
    })


@api.route("/")
class PlaceList(Resource):
    """Handle operations on all places."""

@api.response(200,"List of places retrieved successfully")
def get(self):
        """Get all places"""
        places = facade.get_all_places()

        return [place.to_dict(detailed=False) for place in places], 200

@api.expect(place_model, validate=True)
@api.response(201,"Place successfully created")
@api.response(400,"Invalid input data")
def post(self):
        
        """Create a new place"""
        place_data = api.payload 

        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201

        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400

@api.route("/<string:place_id>")
@api.param("place_id", "The unique identifier of the place")

class PlaceResource(Resource):
    """Handle operations on one place"""

@api.response(200,"Place details retrieved successfully")
@api.response(404,"Place not found")
def get(self, place_id):

        """Retrieve place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,

            "owner": {
                "id": place.owner.id,
                "first_name": place.owner.first_name,
                "last_name": place.owner.last_name,
                "email": place.owner.email
            },

            "amenities": [
                {
                    "id": amenity.id,
                    "name": amenity.name
                }
                for amenity in place.amenities
            ],

            "reviews": [
                {
                    "id": review.id,
                    "text": review.text,
                    "rating": review.rating,
                    "user_id": review.user.id
                }
                for review in place.reviews
            ]
        }, 200

""" return place.to_dict(), 200 """

@api.expect(place_update_model,validate=True)
@api.response(200,"Place successfully updated")
@api.response(400, "Invalid input data")
@api.response(404, "Place not found")
def put(self, place_id):
        """Update an existing place."""
        place_data = api.payload 

        if not place_data:
            return {"error": "No update data provided"}, 400

        try:
            updated_place = facade.update_place(
                place_id,
                place_data
            )

            if not updated_place:
                return {"error": "Place not found"}, 404

            return updated_place.to_dict(), 200

        except (ValueError, TypeError) as error:
            return {
                "error": str(error)
            }, 400
