"""
Job Manager - Database access layer for Job operations
"""

from datetime import date
from typing import Dict, List, Optional

from app.models.job import Job
from app.models.job_tag import JobTag
from app.models.tag import Tag
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload


class JobManager:
    """
    Handles all database operations for Job entities.
    Provides a clean interface for job-related data access.
    """

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, job_id: str) -> Optional[Job]:
        """Find a job by its job_id."""
        return (
            self.db.query(Job)
            .options(joinedload(Job.tag_relations).joinedload(JobTag.tag))
            .filter(Job.job_id == job_id)
            .first()
        )

    def find_by_filters(
        self,
        query: Optional[str] = None,
        location: Optional[str] = None,
        tags: Optional[List[str]] = None,
        tag_categories: Optional[List[str]] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> List[Job]:
        """Find jobs based on various filters."""
        base_query = self.db.query(Job).options(
            joinedload(Job.tag_relations).joinedload(JobTag.tag)
        )

        # Apply filters
        filtered_query = self._apply_filters(
            base_query, query, location, tags, tag_categories, date_from, date_to
        )

        return filtered_query.limit(limit).offset(offset).all()

    def count_by_filters(
        self,
        query: Optional[str] = None,
        location: Optional[str] = None,
        tags: Optional[List[str]] = None,
        tag_categories: Optional[List[str]] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ) -> int:
        """Count jobs that match the given filters."""
        base_query = self.db.query(Job)

        # Apply filters
        filtered_query = self._apply_filters(
            base_query, query, location, tags, tag_categories, date_from, date_to
        )

        return filtered_query.count()

    def create(self, job_data: Dict) -> Job:
        """Create a new job."""
        job = Job(**job_data)
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def update(self, job_id: str, job_data: Dict) -> Optional[Job]:
        """Update an existing job."""
        job = self.find_by_id(job_id)
        if not job:
            return None

        for key, value in job_data.items():
            if hasattr(job, key):
                setattr(job, key, value)

        self.db.commit()
        self.db.refresh(job)
        return job

    def delete(self, job_id: str) -> bool:
        """Delete a job by its job_id."""
        job = self.find_by_id(job_id)
        if not job:
            return False

        self.db.delete(job)
        self.db.commit()
        return True

    def _apply_filters(
        self,
        query,
        text_query: Optional[str] = None,
        location: Optional[str] = None,
        tags: Optional[List[str]] = None,
        tag_categories: Optional[List[str]] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ):
        """Apply various filters to the query."""
        # Text search in job position and company name
        if text_query:
            query = query.filter(
                or_(
                    Job.job_position.ilike(f"%{text_query}%"),
                    Job.company_name.ilike(f"%{text_query}%"),
                    Job.job_location.ilike(f"%{text_query}%"),
                )
            )

        # Location filter
        if location:
            query = query.filter(Job.job_location.ilike(f"%{location}%"))

        # Tag filters
        if tags or tag_categories:
            query = query.join(JobTag).join(Tag)

            if tags:
                query = query.filter(Tag.name.in_(tags))

            if tag_categories:
                query = query.filter(Tag.category.in_(tag_categories))

        # Date range filters
        if date_from:
            query = query.filter(Job.job_posting_date >= date_from)

        if date_to:
            query = query.filter(Job.job_posting_date <= date_to)

        return query.distinct(Job.id)
