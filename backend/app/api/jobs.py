from datetime import date
from typing import List, Optional

from app.core.db import get_db
from app.schemas.search import JobSearchParams
from app.services.search import SearchService
from fastapi import APIRouter, Depends, Query
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
    search_params = JobSearchParams(
        query=query,
        location=location,
        tags=tags,
        tag_categories=tag_categories,
        date_from=date_from,
        date_to=date_to,
        page=page,
        limit=limit,
    )

    search_service = SearchService(db)
    return search_service.search_jobs(search_params)
