from datetime import date

import pytest
from app.core.db import Base
from app.models.job import Job
from app.models.job_tag import JobTag
from app.models.tag import Tag, TagCategory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test database setup
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """Create a test database session"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


class TestJobModel:
    """Test cases for Job model"""

    def test_job_creation_valid_data(self, db_session):
        """Test creating a job with valid data"""
        job = Job(
            job_id="TEST001",
            job_position="Senior Python Developer",
            job_link="https://example.com/job/test001",
            company_name="Tech Corp",
            company_profile="https://example.com/techcorp",
            job_location="San Francisco, CA",
            job_posting_date=date.today(),
            tags={
                "technology": ["python", "fastapi"],
                "skill": ["backend", "api-development"],
            },
        )

        db_session.add(job)
        db_session.commit()
        db_session.refresh(job)

        assert job.id is not None
        assert job.job_id == "TEST001"
        assert job.job_position == "Senior Python Developer"
        assert job.company_name == "Tech Corp"
        assert job.job_location == "San Francisco, CA"
        assert job.tags["technology"] == ["python", "fastapi"]

    def test_job_creation_minimal_data(self, db_session):
        """Test creating a job with minimal required data"""
        job = Job(
            job_id="TEST002",
            job_position="Junior Developer",
            job_link="https://example.com/job/test002",
            company_name="StartupXYZ",
            job_posting_date=date.today(),
        )

        db_session.add(job)
        db_session.commit()
        db_session.refresh(job)

        assert job.id is not None
        assert job.job_id == "TEST002"
        assert job.company_profile is None
        assert job.job_location is None
        assert job.tags is None

    def test_job_unique_job_id_constraint(self, db_session):
        """Test that job_id must be unique"""
        job1 = Job(
            job_id="DUPLICATE",
            job_position="Developer 1",
            job_link="https://example.com/job/1",
            company_name="Company A",
            job_posting_date=date.today(),
        )

        job2 = Job(
            job_id="DUPLICATE",
            job_position="Developer 2",
            job_link="https://example.com/job/2",
            company_name="Company B",
            job_posting_date=date.today(),
        )

        db_session.add(job1)
        db_session.commit()

        db_session.add(job2)
        with pytest.raises(Exception):  # Should raise IntegrityError for duplicate
            db_session.commit()

    def test_job_timestamps(self, db_session):
        """Test that created_at and updated_at timestamps work correctly"""
        job = Job(
            job_id="TEST003",
            job_position="Full Stack Developer",
            job_link="https://example.com/job/test003",
            company_name="WebDev Inc",
            job_posting_date=date.today(),
        )

        db_session.add(job)
        db_session.commit()
        db_session.refresh(job)

        assert job.created_at is not None
        assert job.updated_at is not None

        # Test update timestamp
        original_updated_at = job.updated_at
        job.job_position = "Senior Full Stack Developer"
        db_session.commit()
        db_session.refresh(job)

        # Note: updated_at might not change in the same test due to precision
        assert job.updated_at >= original_updated_at


class TestTagModel:
    """Test cases for Tag model"""

    def test_tag_creation_valid_data(self, db_session):
        """Test creating a tag with valid data"""
        tag = Tag(name="python", category=TagCategory.TECHNOLOGY)

        db_session.add(tag)
        db_session.commit()
        db_session.refresh(tag)

        assert tag.id is not None
        assert tag.name == "python"
        assert tag.category == TagCategory.TECHNOLOGY

    def test_tag_categories_enum(self):
        """Test all tag category enum values"""
        expected_categories = ["role", "technology", "skill", "methodology", "tool"]
        actual_categories = [cat.value for cat in TagCategory]

        assert set(actual_categories) == set(expected_categories)

    def test_tag_unique_name_category_constraint(self, db_session):
        """Test that (name, category) combination must be unique"""
        tag1 = Tag(name="python", category=TagCategory.TECHNOLOGY)
        tag2 = Tag(name="python", category=TagCategory.TECHNOLOGY)

        db_session.add(tag1)
        db_session.commit()

        db_session.add(tag2)
        with pytest.raises(Exception):  # Should raise IntegrityError for duplicate
            db_session.commit()

    def test_tag_same_name_different_categories(self, db_session):
        """Test that same name can exist in different categories"""
        tag1 = Tag(name="backend", category=TagCategory.SKILL)
        tag2 = Tag(name="backend", category=TagCategory.ROLE)

        db_session.add_all([tag1, tag2])
        db_session.commit()

        tags = db_session.query(Tag).filter(Tag.name == "backend").all()
        assert len(tags) == 2
        assert {tag.category for tag in tags} == {TagCategory.SKILL, TagCategory.ROLE}


class TestJobTagModel:
    """Test cases for JobTag relationship model"""

    def test_job_tag_relationship(self, db_session):
        """Test creating job-tag relationships"""
        # Create job
        job = Job(
            job_id="TEST004",
            job_position="Python Developer",
            job_link="https://example.com/job/test004",
            company_name="PyTech",
            job_posting_date=date.today(),
        )

        # Create tags
        tag1 = Tag(name="python", category=TagCategory.TECHNOLOGY)
        tag2 = Tag(name="backend", category=TagCategory.SKILL)

        db_session.add_all([job, tag1, tag2])
        db_session.commit()

        # Create relationships
        job_tag1 = JobTag(job_id=job.id, tag_id=tag1.id)
        job_tag2 = JobTag(job_id=job.id, tag_id=tag2.id)

        db_session.add_all([job_tag1, job_tag2])
        db_session.commit()

        # Verify relationships
        assert len(job.tag_relations) == 2
        tag_names = [rel.tag.name for rel in job.tag_relations]
        assert "python" in tag_names
        assert "backend" in tag_names

    def test_job_tag_unique_constraint(self, db_session):
        """Test that job-tag relationship must be unique"""
        job = Job(
            job_id="TEST005",
            job_position="Developer",
            job_link="https://example.com/job/test005",
            company_name="TestCorp",
            job_posting_date=date.today(),
        )

        tag = Tag(name="java", category=TagCategory.TECHNOLOGY)

        db_session.add_all([job, tag])
        db_session.commit()

        # Create first relationship
        job_tag1 = JobTag(job_id=job.id, tag_id=tag.id)
        db_session.add(job_tag1)
        db_session.commit()

        # Try to create duplicate relationship - should fail
        job_tag2 = JobTag(job_id=job.id, tag_id=tag.id)
        db_session.add(job_tag2)
        with pytest.raises(Exception):  # Should raise IntegrityError for duplicate
            db_session.commit()


class TestModelIntegration:
    """Integration tests for model relationships"""

    def test_job_with_multiple_categories(self, db_session):
        """Test a job with tags from multiple categories"""
        job = Job(
            job_id="TEST006",
            job_position="Full Stack Engineer",
            job_link="https://example.com/job/test006",
            company_name="FullStack Inc",
            job_posting_date=date.today(),
            tags={
                "technology": ["react", "python", "postgresql"],
                "skill": ["frontend", "backend", "database"],
                "methodology": ["agile", "tdd"],
            },
        )

        # Create corresponding tag records
        tags = [
            Tag(name="react", category=TagCategory.TECHNOLOGY),
            Tag(name="python", category=TagCategory.TECHNOLOGY),
            Tag(name="postgresql", category=TagCategory.TECHNOLOGY),
            Tag(name="frontend", category=TagCategory.SKILL),
            Tag(name="backend", category=TagCategory.SKILL),
            Tag(name="database", category=TagCategory.SKILL),
            Tag(name="agile", category=TagCategory.METHODOLOGY),
            Tag(name="tdd", category=TagCategory.METHODOLOGY),
        ]

        db_session.add(job)
        db_session.add_all(tags)
        db_session.commit()

        # Create relationships
        job_tags = [JobTag(job_id=job.id, tag_id=tag.id) for tag in tags]
        db_session.add_all(job_tags)
        db_session.commit()

        # Verify
        assert len(job.tag_relations) == 8

        # Test filtering by category
        tech_tags = [
            rel.tag
            for rel in job.tag_relations
            if rel.tag.category == TagCategory.TECHNOLOGY
        ]
        assert len(tech_tags) == 3
        assert {tag.name for tag in tech_tags} == {"react", "python", "postgresql"}

    def test_orphaned_tags_cleanup(self, db_session):
        """Test that tags can exist without jobs (for reference data)"""
        # Create tags without jobs
        tags = [
            Tag(name="kubernetes", category=TagCategory.TECHNOLOGY),
            Tag(name="devops", category=TagCategory.SKILL),
            Tag(name="ci-cd", category=TagCategory.METHODOLOGY),
        ]

        db_session.add_all(tags)
        db_session.commit()

        all_tags = db_session.query(Tag).all()
        assert len(all_tags) == 3

        # These tags should have no job relationships
        for tag in all_tags:
            assert len(tag.job_relations) == 0
