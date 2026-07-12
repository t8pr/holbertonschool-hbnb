from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity'),
    'description': fields.String(description='Description of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation

"""This part is for Post so we need to set the required field
   to True because we are creating a new place"""

place_model = api.model('Place', {
    'id': fields.String(readonly=True, description='The unique identifier of a place'),
    'title': fields.String(required=True,max_length=100, description='Title of the place'),
    'description': fields.String(required=False, description='Description of the place'),
    'price': fields.Float(required=True,min=0, description='Price per night'),
    'latitude': fields.Float(required=True,min=-90,max=90, description='Latitude of the place'),
    'longitude': fields.Float(required=True,min=-180,max=180, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=False, description="List of amenities ID's"),
    'available': fields.Boolean(required=False, description='Availability status of the place'),
})

"""This part is for PUT so no need to change the required field to True
   because we are updating the place and not creating a new one"""

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(required=False,max_length=100, description='Title of the place'),
    'description': fields.String(required=False, description='Description of the place'),
    'price': fields.Float(required=False,min=0, description='Price per night'),
    'latitude': fields.Float(required=False,min=-90,max=90, description='Latitude of the place'),
    'longitude': fields.Float(required=False,min=-180,max=180, description='Longitude of the place'),
    'owner_id': fields.String(required=False, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=False, description="List of amenities ID's"),
    'available': fields.Boolean(required=False, description='Availability status of the place')
})

def serialize_owner(owner):
    """Convert the owner into a safe dictionary."""
    return {
        "id": owner.id,
        "first_name": owner.first_name,
        "last_name": owner.last_name,
        "email": owner.email
    }

def serialize_place_amenity(amenity):
    """Convert an amenity into a nested dictionary."""
    return {
        "id": amenity.id,
        "name": amenity.name
    }


def serialize_created_place(place):
    """Serialize a newly created place."""
    return {
        "id": place.id,
        "title": place.title,
        "description": place.description,
        "price": place.price,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "owner_id": place.owner.id
    }


def serialize_place_summary(place):
    """Serialize a place for the places list."""
    return {
        "id": place.id,
        "title": place.title,
        "latitude": place.latitude,
        "longitude": place.longitude
    }


def serialize_place_details(place):
    """Serialize complete place details."""
    return {
        "id": place.id,
        "title": place.title,
        "description": place.description,
        "price": place.price,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "owner": serialize_owner(place.owner),
        "amenities": [
            serialize_place_amenity(amenity)
            for amenity in place.amenities
        ]
    }


@api.route("/")
class PlaceList(Resource):
    """Resource for place collection operations."""

    @api.expect(place_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """Register a new place."""
        place_data = api.payload

        try:
            new_place = facade.create_place(place_data)

            return serialize_created_place(new_place), 201

        except (ValueError, TypeError) as error:
            return {
                "error": str(error)
            }, 400

    @api.response(
        200,
        "List of places retrieved successfully"
    )
    def get(self):
        """Retrieve a list of all places."""
        places = facade.get_all_places()

        return [
            serialize_place_summary(place)
            for place in places
        ], 200


@api.route("/<string:place_id>")
@api.param(
    "place_id",
    "The unique identifier of the place"
)
class PlaceResource(Resource):
    """Resource for individual place operations."""

    @api.response(
        200,
        "Place details retrieved successfully"
    )
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get place details by ID."""
        place = facade.get_place(place_id)

        if place is None:
            return {
                "error": "Place not found"
            }, 404

        return serialize_place_details(place), 200

    @api.expect(place_update_model, validate=True)
    @api.response(200, "Place updated successfully")
    @api.response(404, "Place not found")
    @api.response(400, "Invalid input data")
    def put(self, place_id):
        """Update a place's information."""
        place_data = api.payload

        if not place_data:
            return {
                "error": "No update data provided"
            }, 400

        try:
            updated_place = facade.update_place(
                place_id,
                place_data
            )

            if updated_place is None:
                return {
                    "error": "Place not found"
                }, 404

            return {
                "message": "Place updated successfully"
            }, 200

        except (ValueError, TypeError) as error:
            return {
                "error": str(error)
            }, 400
