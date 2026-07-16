"""Amenity API endpoints"""

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("amenities", description="Amenity operations")

amenity_model = api.model("Amenity", {
    "name": fields.String(required=True, description="Name of the amenity")
})

amenity_update_model = api.model("AmenityUpdate", {
    "name": fields.String(required=False, description="New name of the amenity")
})

@api.route("/")
class AmenityList(Resource):
    """Handle operations on all amenities"""

    @api.response(200, "List of amenities retrieved successfully")
    def get(self):
        """Get all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

    @api.expect(amenity_model, validate=True)
    @api.response(201, "Amenity successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """Create a new amenity"""
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400

@api.route("/<string:amenity_id>")
@api.param("amenity_id", "The unique identifier of the amenity")
class AmenityResource(Resource):
    """Handle operations on one amenity"""

    @api.response(200, "Amenity successfully retrieved")
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        """Get an amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_update_model, validate=True)
    @api.response(200, "Amenity successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(404, "Amenity not found")
    def put(self, amenity_id):
        """Update an existing amenity."""
        amenity_data = api.payload
        if not amenity_data:
            return {"error": "No update data provided"}, 400
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if not updated_amenity:
                return {"error": "Amenity not found"}, 404
            return updated_amenity.to_dict(), 200
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400