from datetime import datetime

from app.core.db import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship


class JobTag(Base):
    __tablename__ = "job_tags"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Define relationships with explicit foreign_keys to avoid ambiguity
    job = relationship("Job", foreign_keys=[job_id], back_populates="tag_relations")
    tag = relationship("Tag", foreign_keys=[tag_id], back_populates="job_relations")

    # Composite unique constraint to prevent duplicate job-tag relationships
    __table_args__ = (
        UniqueConstraint("job_id", "tag_id", name="unique_job_tag"),
        {"sqlite_autoincrement": True},
    )
