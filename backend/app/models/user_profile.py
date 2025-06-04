from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, String, Text

from .base import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    # Primary key - Firebase UID
    uid = Column(String, primary_key=True, index=True)

    # Basic Information
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    location = Column(String(200), nullable=True)
    bio = Column(Text, nullable=True)
    website = Column(String(500), nullable=True)
    phone_number = Column(String(20), nullable=True)

    # Professional Information
    skills = Column(JSON, nullable=True)  # Array of skills
    experience = Column(String(20), nullable=True)  # entry, junior, mid, senior, lead

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<UserProfile(uid='{self.uid}', first_name='{self.first_name}', last_name='{self.last_name}')>"

    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            "uid": self.uid,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "location": self.location,
            "bio": self.bio,
            "website": self.website,
            "phone_number": self.phone_number,
            "skills": self.skills or [],
            "experience": self.experience,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
