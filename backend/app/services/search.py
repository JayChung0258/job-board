from app.models.job import Job
from app.models.tag import Tag
from app.schemas.job_filter import JobSearchFilter
from sqlalchemy import or_
from sqlalchemy.orm import Session


class SearchService:
    def __init__(self, db: Session):
        self.db = db

    def search_jobs(self, params: JobSearchFilter):
        query = self.db.query(Job)

        # Text search
        if params.query:
            search_term = f"%{params.query}%"
            query = query.filter(
                or_(
                    Job.job_position.ilike(search_term),
                    Job.company_name.ilike(search_term),
                    Job.job_location.ilike(search_term),
                )
            )

        # Location filter
        if params.location:
            query = query.filter(Job.job_location.ilike(f"%{params.location}%"))

        # Date range filter
        if params.date_from:
            query = query.filter(Job.job_posting_date >= params.date_from)
        if params.date_to:
            query = query.filter(Job.job_posting_date <= params.date_to)

        # Tag filters
        if params.tags or params.tag_categories:
            query = query.join(Job.tag_relations).join(Tag)

            if params.tags:
                query = query.filter(Tag.name.in_(params.tags))

            if params.tag_categories:
                query = query.filter(Tag.category.in_(params.tag_categories))

        # Get total count before pagination
        total = query.count()

        # Apply pagination
        query = query.offset((params.page - 1) * params.limit).limit(params.limit)

        # Execute query
        jobs = query.all()

        return {
            "items": jobs,
            "total": total,
            "page": params.page,
            "limit": params.limit,
            "pages": (total + params.limit - 1) // params.limit,
        }
