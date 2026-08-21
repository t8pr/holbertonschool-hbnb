from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

api = Namespace("bookings", description="Booking operations")

booking_model = api.model("Booking", {
    "place_id": fields.String(required=True),
    "start_date": fields.String(required=True),
    "end_date": fields.String(required=True),
    "total_price": fields.Float(required=True)
})

@api.route("/")
class BookingList(Resource):
    @api.response(200, "Bookings retrieved successfully")
    @jwt_required()
    def get(self):
        """Get all bookings for the current user"""
        current_user = get_jwt_identity()
        bookings = facade.get_bookings_by_user(current_user)
        return [b.to_dict() for b in bookings], 200

    @api.expect(booking_model)
    @api.response(201, "Booking successfully created")
    @jwt_required()
    def post(self):
        """Create a new booking"""
        current_user = get_jwt_identity()
        data = api.payload
        data['user_id'] = current_user
        try:
            data['start_date'] = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            data['end_date'] = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
            new_booking = facade.create_booking(data)
            return new_booking.to_dict(), 201
        except Exception as e:
            return {"error": str(e)}, 400