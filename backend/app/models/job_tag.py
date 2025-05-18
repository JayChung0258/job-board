from datetime import datetime

from app.core.db import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer
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

    # Composite unique constraint
    __table_args__ = (
        # This ensures a job can't have the same tag multiple times
        # and allows for efficient querying of job-tag relationships
        {"sqlite_autoincrement": True},
    )
