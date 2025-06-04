"""
Job API Endpoints - HTTP layer for job-related operations
"""

from datetime import date
from typing import List, Optional

from app.core.dependencies import get_search_service
from app.schemas.job_filter import JobSearchFilter
from app.services.search import SearchService
from fastapi import APIRouter, Depends, Query

router = APIRouter()


@router.get("/search")
def search_jobs(
    query: Optional[str] = None,
    location: Optional[str] = None,
    tags: List[str] = Query(default=[]),
    tag_categories: List[str] = Query(default=[]),
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    page: int = 1,
    limit: int = 10,
    search_service: SearchService = Depends(get_search_service),
):
    """
    Search for jobs with various filters
    """

    search_params = JobSearchFilter(
        query=query,
        location=location,
        tags=tags,
        tag_categories=tag_categories,
        date_from=date_from,
        date_to=date_to,
        page=page,
        limit=limit,
    )

    return search_service.search_jobs(search_params)


@router.get("/{job_id}")
def get_job(
    job_id: str,
    search_service: SearchService = Depends(get_search_service),
):
    """
    Get a specific job by ID
    """
    return search_service.get_job_by_id(job_id)
