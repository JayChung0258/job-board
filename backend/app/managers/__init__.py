"""
Data Access Layer - Managers

This package contains all database access logic, providing a clean interface
between the business logic (services) and the database models.
"""

from .job_manager import JobManager
from .job_tag_manager import JobTagManager
from .tag_manager import TagManager

__all__ = ["JobManager", "TagManager", "JobTagManager"]
