from datetime import datetime

from app.core.db import Base
from sqlalchemy import JSON, Column, Date, Integer, String
from sqlalchemy.orm import relationship


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(50), unique=True, index=True, nullable=False)
    job_position = Column(String(255), nullable=False)
    job_link = Column(String(512), nullable=False)
    company_name = Column(String(255), nullable=False)
    company_profile = Column(String(512))
    job_location = Column(String(255))
    job_posting_date = Column(Date, nullable=False)
    tags = Column(JSON)  # Store tags as JSON for flexibility
    created_at = Column(Date, default=datetime.utcnow)
    updated_at = Column(Date, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with Tag model through JobTag
    tag_relations = relationship("JobTag", back_populates="job")
