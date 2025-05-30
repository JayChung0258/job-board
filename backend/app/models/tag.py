import enum

from app.core.db import Base
from sqlalchemy import Column, Enum, Integer, String, UniqueConstraint
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
    name = Column(String(100), index=True, nullable=False)
    category = Column(Enum(TagCategory), nullable=False)
    description = Column(String(255))

    # Use string for model name to avoid circular imports
    job_relations = relationship("JobTag", back_populates="tag")

    # Unique constraint on name and category combination
    __table_args__ = (
        UniqueConstraint("name", "category", name="unique_name_category"),
    )
