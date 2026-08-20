from part4.backend.hbnb.app import db
from part4.backend.hbnb.app.models.basemodel import BaseModel
from sqlalchemy.orm import validates

place_amenity = db.Table(
    'place_amenity',
    db.Column("place_id", db.String(36), db.ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.String(36), db.ForeignKey("amenities.id"), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    reviews = db.relationship("Review", backref="place", lazy=True)
    amenities = db.relationship("Amenity", secondary=place_amenity, lazy="subquery", backref="places")

    def __init__(self, title, description, price, latitude, longitude, owner_id = None, **kwargs):
        super().__init__(**kwargs)
        

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
            

    @validates('title')
    def validate_title(self, key, title):
        if not title or not title.strip():
            raise ValueError("Title is required")

        if len(title.strip()) > 100:
            raise ValueError("Title cannot exceed 100 characters")

        return title.strip()

    @validates('price')
    def validate_price(self, key, price):
        try:
            price = float(price)
        except (ValueError, TypeError):
            raise ValueError("Price must be a number")

        if price < 0:
            raise ValueError("Price must be non-negative")

        return price

    @validates('latitude')
    def validate_latitude(self, key, latitude):
        try:
            latitude = float(latitude)
        except (ValueError, TypeError):
            raise ValueError("Latitude must be a number")

        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")

        return latitude

    @validates('longitude')
    def validate_longitude(self, key, longitude):
        try:
            longitude = float(longitude)
        except (ValueError, TypeError):
            raise ValueError("Longitude must be a number")

        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")

        return longitude

    def to_dict(self):
        data = super().to_dict()

        data.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id
        })

        return data

