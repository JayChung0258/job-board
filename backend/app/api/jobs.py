from datetime import date
from typing import List, Optional

from app.core.db import get_db
from app.models.job import Job
from app.schemas.job_filter import JobSearchFilter
from app.services.search import SearchService
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/search")
def search_jobs(
    query: Optional[str] = None,
    location: Optional[str] = None,
    tags: Optional[List[str]] = Query(None),
    tag_categories: Optional[List[str]] = Query(None),
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Search for jobs with various filters
    """
    search_service = SearchService(db)
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

    result = search_service.search_jobs(search_params)
    return result


@router.get("/{job_id}")
def get_job(job_id: str, db: Session = Depends(get_db)):
    """
    Get a specific job by ID
    """
    job = db.query(Job).filter(Job.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail=f"Job with ID {job_id} not found")

    return job
