from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.db import Base

class JobTag(Base):
    __tablename__ = "job_tags"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    job = relationship("Job", back_populates="tag_relations")
    tag = relationship("Tag", back_populates="job_relations")

    # Composite unique constraint
    __table_args__ = (
        # This ensures a job can't have the same tag multiple times
        # and allows for efficient querying of job-tag relationships
        {'sqlite_autoincrement': True},
    )
