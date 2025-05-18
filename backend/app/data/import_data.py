import json
import os
from datetime import datetime

from app.core.config import settings
from app.models.job import Job
from app.models.job_tag import JobTag
from app.models.tag import Tag, TagCategory
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Create database connection
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def load_mock_data():
    """Load mock data from JSON file into the database"""
    db = SessionLocal()

    try:
        # Load mock data
        script_dir = os.path.dirname(os.path.abspath(__file__))
        mock_jobs_path = os.path.join(script_dir, "mock_jobs.json")
        tags_path = os.path.join(script_dir, "tags.json")

        with open(mock_jobs_path, "r") as f:
            mock_jobs_data = json.load(f)["jobs"]

        with open(tags_path, "r") as f:
            tags_data = json.load(f)["tags"]

        # Clear existing data
        clear_existing_data(db)

        # Import tags
        import_tags(db, tags_data)

        # Import jobs
        import_jobs(db, mock_jobs_data)

        db.commit()
        print("Data import completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error importing data: {e}")
    finally:
        db.close()


def clear_existing_data(db: Session):
    """Clear existing data from tables"""
    db.query(JobTag).delete()
    db.query(Job).delete()
    db.query(Tag).delete()
    db.commit()
    print("Cleared existing data")


def import_tags(db: Session, tags_data):
    """Import tags from the tags data"""
    tag_objects = {}

    # Map from category name in JSON to TagCategory enum values
    category_map = {
        "role": TagCategory.ROLE,
        "technology": TagCategory.TECHNOLOGY,
        "skill": TagCategory.SKILL,
        "methodology": TagCategory.METHODOLOGY,
        "tool": TagCategory.TOOL,
    }

    # Process all unique tags across categories
    unique_tags = {}

    # First collect all unique tags
    for category, tags in tags_data.items():
        tag_category = category_map[category]

        for tag_name in tags:
            if tag_name not in unique_tags:
                unique_tags[tag_name] = {
                    "name": tag_name,
                    "category": tag_category,
                    "description": f"{tag_name} in {category} category",
                }

    # Add unique tags to database
    for tag_data in unique_tags.values():
        tag = Tag(
            name=tag_data["name"],
            category=tag_data["category"],
            description=tag_data["description"],
        )
        db.add(tag)
        db.flush()

        # Store reference for later use
        category_value = tag_data["category"].value
        tag_objects[f"{category_value}:{tag_data['name']}"] = tag

    db.commit()
    print(f"Imported {len(tag_objects)} tags")
    return tag_objects


def import_jobs(db: Session, jobs_data):
    """Import jobs from the mock data"""
    # Get all tags from the database
    all_tags = {f"{tag.category.value}:{tag.name}": tag for tag in db.query(Tag).all()}

    for job_data in jobs_data:
        # Parse date
        posting_date = datetime.strptime(
            job_data["job_posting_date"], "%Y-%m-%d"
        ).date()

        # Create job
        job = Job(
            job_id=job_data["job_id"],
            job_position=job_data["job_position"],
            job_link=job_data["job_link"],
            company_name=job_data["company_name"],
            company_profile=job_data.get("company_profile", ""),
            job_location=job_data["job_location"],
            job_posting_date=posting_date,
            tags=job_data["tags"],  # Store original tags as JSON
        )
        db.add(job)
        db.flush()

        # Create job-tag relations
        for category, tag_names in job_data["tags"].items():
            for tag_name in tag_names:
                tag_key = f"{category}:{tag_name}"
                if tag_key in all_tags:
                    job_tag = JobTag(job_id=job.id, tag_id=all_tags[tag_key].id)
                    db.add(job_tag)

    db.commit()
    print(f"Imported {len(jobs_data)} jobs")


if __name__ == "__main__":
    load_mock_data()
