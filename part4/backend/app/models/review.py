from app import db
from app.models.basemodel import BaseModel
from sqlalchemy.orm import validates

class Review(BaseModel):
    __tablename__ = 'reviews'


    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)


    def __init__(self, text, rating, place_id, user_id, **kwargs):
        super().__init__(**kwargs)
       

        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id


    @validates("text")
    def validate_text(self, key, text):
        if not text or not text.strip():
            raise ValueError("Review text cannot be empty")

        return text.strip()

    @validates("rating")
    def validate_rating(self, key, rating):
        try:
            rating = int(rating)
        except (ValueError, TypeError):
            raise ValueError("Rating must be an integer")

        if not 1 <= rating <= 5:
            raise ValueError(
                "Rating must be an integer between 1 and 5"
            )
        return rating

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "created_at": self.created_at.isoformat()
            if self.created_at else None,
            "updated_at": self.updated_at.isoformat()
            if self.updated_at else None
        }
