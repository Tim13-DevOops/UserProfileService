from datetime import datetime
from .database import db
from dataclasses import dataclass, field


@dataclass
class UserProfile(db.Model):
    id: int
    username: str
    name: str
    email: str
    phone_number: str
    biography: str
    website: str
    public: bool
    taggable: bool
    deleted: bool
    timestamp: datetime = field(default_factory=datetime(2000, 1, 1))
    birth_date: datetime = field(default_factory=datetime(2000, 1, 1))

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    username = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    birth_date = db.Column(db.DateTime)
    biography = db.Column(db.String(1000))
    website = db.Column(db.String(255))
    public = db.Column(db.Boolean, default=False)
    taggable = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"UserProfile {self.username}"
