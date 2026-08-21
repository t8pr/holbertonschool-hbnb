from app import db
from app.models.basemodel import BaseModel
from sqlalchemy.orm import validates


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True) 

    def __init__(self, name, description="", **kwargs):
        super().__init__(**kwargs)
        

        self.name = name
        self.description = description

    @validates("name")
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError("Amenity name is required")

        name = name.strip()

        if len(name) > 50:
            raise ValueError(
                "Amenity name cannot exceed 50 characters"
            )

        return name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat()
            if self.created_at else None,
            "updated_at": self.updated_at.isoformat()
            if self.updated_at else None
        }
    