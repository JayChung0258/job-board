import enum

from app.core.db import Base
from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship


class TagCategory(str, enum.Enum):
    ROLE = "role"
    TECHNOLOGY = "technology"
    SKILL = "skill"
    METHODOLOGY = "methodology"
    TOOL = "tool"


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    category = Column(Enum(TagCategory), nullable=False)
    description = Column(String(255))

    # Relationship with Job model through JobTag
    job_relations = relationship("JobTag", back_populates="tag")
