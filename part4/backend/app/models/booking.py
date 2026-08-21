from app import db
from app.models.basemodel import BaseModel
from datetime import datetime

class Booking(BaseModel):
    __tablename__ = 'bookings'
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "total_price": self.total_price,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }