"""
Search Service - Business logic for job search operations
"""

from typing import Dict, List

from app.managers.job_manager import JobManager
from app.managers.job_tag_manager import JobTagManager
from app.managers.tag_manager import TagManager
from app.models.job import Job
from app.schemas.job_filter import JobSearchFilter
from fastapi import HTTPException


class SearchService:
    """
    Handles business logic for job search operations.
    Uses managers for all database interactions.
    """

    def __init__(
        self,
        job_manager: JobManager,
        tag_manager: TagManager,
        job_tag_manager: JobTagManager,
    ):
        self.job_manager = job_manager
        self.tag_manager = tag_manager
        self.job_tag_manager = job_tag_manager

    def search_jobs(self, params: JobSearchFilter) -> Dict:
        """
        Search for jobs based on provided filters.
        Returns paginated results with metadata.
        """
        # Calculate offset for pagination
        offset = (params.page - 1) * params.limit

        # Get total count
        total = self.job_manager.count_by_filters(
            query=params.query,
            location=params.location,
            tags=params.tags,
            tag_categories=params.tag_categories,
            date_from=params.date_from,
            date_to=params.date_to,
        )

        # Get paginated jobs
        jobs = self.job_manager.find_by_filters(
            query=params.query,
            location=params.location,
            tags=params.tags,
            tag_categories=params.tag_categories,
            date_from=params.date_from,
            date_to=params.date_to,
            limit=params.limit,
            offset=offset,
        )

        # Enrich jobs with tags and format response
        formatted_jobs = self._build_job_responses(jobs)

        return {
            "items": formatted_jobs,
            "total": total,
            "page": params.page,
            "limit": params.limit,
            "pages": self._calculate_pages(total, params.limit),
        }

    def get_job_by_id(self, job_id: str) -> Dict:
        """
        Get a specific job by its ID.
        Raises HTTPException if job not found.
        """
        job = self.job_manager.find_by_id(job_id)
        if not job:
            raise HTTPException(
                status_code=404, detail=f"Job with ID {job_id} not found"
            )

        return self._format_job_response(job)

    def _build_job_responses(self, jobs: List[Job]) -> List[Dict]:
        """Build formatted job responses with tags."""
        return [self._format_job_response(job) for job in jobs]

    def _format_job_response(self, job: Job) -> Dict:
        """Format a single job for API response."""
        # Build tags dictionary grouped by category
        tags_by_category = {}
        for job_tag in job.tag_relations:
            tag = job_tag.tag
            category = tag.category.value
            if category not in tags_by_category:
                tags_by_category[category] = []
            tags_by_category[category].append(tag.name)

        return {
            "job_id": job.job_id,
            "job_position": job.job_position,
            "job_link": job.job_link,
            "company_name": job.company_name,
            "job_location": job.job_location,
            "job_posting_date": job.job_posting_date,
            "tags": tags_by_category,
        }

    def _calculate_pages(self, total: int, limit: int) -> int:
        """Calculate total number of pages."""
        return (total + limit - 1) // limit
