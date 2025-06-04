"""
JobTag Manager - Database access layer for JobTag operations
"""

from typing import Dict, List

from app.models.job_tag import JobTag
from sqlalchemy.orm import Session


class JobTagManager:
    """
    Handles all database operations for JobTag entities.
    Manages the many-to-many relationship between jobs and tags.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_relations(self, job_id: int, tag_ids: List[int]) -> List[JobTag]:
        """Create job-tag relationships for a job with multiple tags."""
        job_tags = []
        for tag_id in tag_ids:
            job_tag = JobTag(job_id=job_id, tag_id=tag_id)
            self.db.add(job_tag)
            job_tags.append(job_tag)

        self.db.commit()

        # Refresh all objects to get their IDs
        for job_tag in job_tags:
            self.db.refresh(job_tag)

        return job_tags

    def delete_relations(self, job_id: int) -> bool:
        """Delete all job-tag relationships for a specific job."""
        deleted_count = self.db.query(JobTag).filter(JobTag.job_id == job_id).delete()
        self.db.commit()
        return deleted_count > 0

    def find_by_job_id(self, job_id: int) -> List[JobTag]:
        """Find all job-tag relationships for a specific job."""
        return self.db.query(JobTag).filter(JobTag.job_id == job_id).all()

    def find_by_tag_id(self, tag_id: int) -> List[JobTag]:
        """Find all job-tag relationships for a specific tag."""
        return self.db.query(JobTag).filter(JobTag.tag_id == tag_id).all()

    def bulk_create(self, relations: List[Dict]) -> List[JobTag]:
        """Create multiple job-tag relationships in bulk."""
        job_tags = []
        for relation in relations:
            job_tag = JobTag(**relation)
            self.db.add(job_tag)
            job_tags.append(job_tag)

        self.db.commit()

        # Refresh all objects to get their IDs
        for job_tag in job_tags:
            self.db.refresh(job_tag)

        return job_tags

    def update_job_tags(self, job_id: int, tag_ids: List[int]) -> List[JobTag]:
        """Update job-tag relationships by replacing all existing ones."""
        # Remove existing relationships
        self.delete_relations(job_id)

        # Create new relationships
        if tag_ids:
            return self.create_relations(job_id, tag_ids)

        return []

    def exists(self, job_id: int, tag_id: int) -> bool:
        """Check if a specific job-tag relationship exists."""
        return (
            self.db.query(JobTag)
            .filter(JobTag.job_id == job_id, JobTag.tag_id == tag_id)
            .first()
            is not None
        )
