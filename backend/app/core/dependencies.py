"""
Dependency Injection - Wire up services and managers
"""

from app.core.db import get_db
from app.managers.job_manager import JobManager
from app.managers.job_tag_manager import JobTagManager
from app.managers.tag_manager import TagManager
from app.services.search import SearchService
from app.services.tag_service import TagService
from fastapi import Depends
from sqlalchemy.orm import Session


# Manager Dependencies
def get_job_manager(db: Session = Depends(get_db)) -> JobManager:
    """Get JobManager instance with database session."""
    return JobManager(db)


def get_tag_manager(db: Session = Depends(get_db)) -> TagManager:
    """Get TagManager instance with database session."""
    return TagManager(db)


def get_job_tag_manager(db: Session = Depends(get_db)) -> JobTagManager:
    """Get JobTagManager instance with database session."""
    return JobTagManager(db)


# Service Dependencies
def get_search_service(
    job_manager: JobManager = Depends(get_job_manager),
    tag_manager: TagManager = Depends(get_tag_manager),
    job_tag_manager: JobTagManager = Depends(get_job_tag_manager),
) -> SearchService:
    """Get SearchService instance with required managers."""
    return SearchService(job_manager, tag_manager, job_tag_manager)


def get_tag_service(
    tag_manager: TagManager = Depends(get_tag_manager),
) -> TagService:
    """Get TagService instance with required managers."""
    return TagService(tag_manager)
