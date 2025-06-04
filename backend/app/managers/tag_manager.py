"""
Tag Manager - Database access layer for Tag operations
"""

from typing import Dict, List, Optional

from app.models.tag import Tag, TagCategory
from sqlalchemy.orm import Session


class TagManager:
    """
    Handles all database operations for Tag entities.
    Provides a clean interface for tag-related data access.
    """

    def __init__(self, db: Session):
        self.db = db

    def find_by_category(self, category: TagCategory) -> List[Tag]:
        """Find all tags in a specific category."""
        return self.db.query(Tag).filter(Tag.category == category).all()

    def find_by_name(self, name: str) -> Optional[Tag]:
        """Find a tag by its name."""
        return self.db.query(Tag).filter(Tag.name == name).first()

    def find_all_categories(self) -> List[TagCategory]:
        """Get all available tag categories."""
        return [category for category in TagCategory]

    def create(self, name: str, category: TagCategory) -> Tag:
        """Create a new tag."""
        tag = Tag(name=name, category=category)
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag

    def exists_by_name(self, name: str) -> bool:
        """Check if a tag with the given name exists."""
        return self.db.query(Tag).filter(Tag.name == name).first() is not None

    def get_tags_for_jobs(self, job_ids: List[int]) -> Dict[int, List[Tag]]:
        """Get all tags for multiple jobs, organized by job ID."""
        from app.models.job_tag import JobTag

        results = (
            self.db.query(JobTag.job_id, Tag)
            .join(Tag)
            .filter(JobTag.job_id.in_(job_ids))
            .all()
        )

        # Organize results by job_id
        tags_by_job = {}
        for job_id, tag in results:
            if job_id not in tags_by_job:
                tags_by_job[job_id] = []
            tags_by_job[job_id].append(tag)

        return tags_by_job

    def find_by_names(self, names: List[str]) -> List[Tag]:
        """Find tags by their names."""
        return self.db.query(Tag).filter(Tag.name.in_(names)).all()

    def get_or_create(self, name: str, category: TagCategory) -> Tag:
        """Get an existing tag or create a new one if it doesn't exist."""
        tag = self.find_by_name(name)
        if tag:
            return tag
        return self.create(name, category)
