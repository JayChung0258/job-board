from datetime import date, timedelta

import pytest
from app.managers.job_manager import JobManager
from app.managers.job_tag_manager import JobTagManager
from app.managers.tag_manager import TagManager
from app.models import Job, Tag
from app.models.tag import TagCategory
from app.schemas.job_filter import JobSearchFilter
from app.services.search import SearchService
from tests.conftest import (
    create_job_tag_relations_from_mappings,
    create_test_db_session,
    create_test_engine,
    refresh_objects,
)

# Create test engine for services
engine = create_test_engine("services.db")


@pytest.fixture
def db_session():
    """Create a test database session"""
    engine = create_test_engine("test_services.db")
    yield from create_test_db_session(engine)


@pytest.fixture
def job_manager(db_session):
    """Fixture that provides a JobManager instance"""
    return JobManager(db_session)


@pytest.fixture
def tag_manager(db_session):
    """Fixture that provides a TagManager instance"""
    return TagManager(db_session)


@pytest.fixture
def job_tag_manager(db_session):
    """Fixture that provides a JobTagManager instance"""
    return JobTagManager(db_session)


@pytest.fixture
def search_service(job_manager, tag_manager, job_tag_manager):
    """Fixture that provides a SearchService instance with managers"""
    return SearchService(job_manager, tag_manager, job_tag_manager)


@pytest.fixture
def sample_jobs(db_session):
    """Create sample jobs for testing"""
    today = date.today()
    yesterday = today - timedelta(days=1)
    week_ago = today - timedelta(days=7)

    jobs = [
        Job(
            job_id="JOB001",
            job_position="Senior Python Developer",
            job_link="https://example.com/job001",
            company_name="TechCorp",
            job_location="San Francisco, CA",
            job_posting_date=today,
            tags={"technology": ["python", "django"], "skill": ["backend"]},
        ),
        Job(
            job_id="JOB002",
            job_position="React Frontend Developer",
            job_link="https://example.com/job002",
            company_name="WebDev Inc",
            job_location="New York, NY",
            job_posting_date=yesterday,
            tags={"technology": ["react", "javascript"], "skill": ["frontend"]},
        ),
        Job(
            job_id="JOB003",
            job_position="Full Stack Engineer",
            job_link="https://example.com/job003",
            company_name="StartupXYZ",
            job_location="Remote",
            job_posting_date=week_ago,
            tags={"technology": ["python", "react"], "skill": ["fullstack"]},
        ),
        Job(
            job_id="JOB004",
            job_position="DevOps Engineer",
            job_link="https://example.com/job004",
            company_name="CloudSoft",
            job_location="Seattle, WA",
            job_posting_date=today,
            tags={"technology": ["docker", "kubernetes"], "skill": ["devops"]},
        ),
        Job(
            job_id="JOB005",
            job_position="Data Scientist",
            job_link="https://example.com/job005",
            company_name="DataTech",
            job_location="Austin, TX",
            job_posting_date=yesterday,
            tags={
                "technology": ["python", "tensorflow"],
                "skill": ["machine-learning"],
            },
        ),
    ]

    # Create corresponding tags
    tags = [
        Tag(name="python", category=TagCategory.TECHNOLOGY),
        Tag(name="django", category=TagCategory.TECHNOLOGY),
        Tag(name="react", category=TagCategory.TECHNOLOGY),
        Tag(name="javascript", category=TagCategory.TECHNOLOGY),
        Tag(name="docker", category=TagCategory.TECHNOLOGY),
        Tag(name="kubernetes", category=TagCategory.TECHNOLOGY),
        Tag(name="tensorflow", category=TagCategory.TECHNOLOGY),
        Tag(name="backend", category=TagCategory.SKILL),
        Tag(name="frontend", category=TagCategory.SKILL),
        Tag(name="fullstack", category=TagCategory.SKILL),
        Tag(name="devops", category=TagCategory.SKILL),
        Tag(name="machine-learning", category=TagCategory.SKILL),
    ]

    db_session.add_all(jobs + tags)
    db_session.commit()

    # Refresh all objects to get their IDs
    refresh_objects(db_session, jobs + tags)

    # Define job-tag relationships mapping
    job_tag_mapping = {
        "JOB001": ["python", "django", "backend"],
        "JOB002": ["react", "javascript", "frontend"],
        "JOB003": ["python", "react", "fullstack"],
        "JOB004": ["docker", "kubernetes", "devops"],
        "JOB005": ["python", "tensorflow", "machine-learning"],
    }

    # Create job-tag relationships using shared utility
    job_tag_relations = create_job_tag_relations_from_mappings(
        jobs, tags, job_tag_mapping
    )

    db_session.add_all(job_tag_relations)
    db_session.commit()

    return jobs


class TestSearchService:
    """Test cases for SearchService"""

    def test_search_service_initialization(self, search_service):
        """Test SearchService initialization"""
        assert search_service is not None
        assert hasattr(search_service, "job_manager")
        assert hasattr(search_service, "tag_manager")
        assert hasattr(search_service, "job_tag_manager")

    def test_search_all_jobs_no_filters(self, search_service, sample_jobs):
        """Test searching without any filters returns all jobs"""
        params = JobSearchFilter()

        result = search_service.search_jobs(params)

        assert result["total"] == 5
        assert len(result["items"]) == 5
        assert result["page"] == 1
        assert result["limit"] == 10
        assert result["pages"] == 1

    def test_search_by_query_position(self, search_service, sample_jobs):
        """Test searching by job position"""
        params = JobSearchFilter(query="Python Developer")

        result = search_service.search_jobs(params)

        assert result["total"] == 1
        assert len(result["items"]) == 1
        assert result["items"][0]["job_position"] == "Senior Python Developer"

    def test_search_by_query_company(self, search_service, sample_jobs):
        """Test searching by company name"""
        params = JobSearchFilter(query="TechCorp")

        result = search_service.search_jobs(params)

        assert result["total"] == 1
        assert len(result["items"]) == 1
        assert result["items"][0]["company_name"] == "TechCorp"

    def test_search_by_query_location(self, search_service, sample_jobs):
        """Test searching by location"""
        params = JobSearchFilter(query="San Francisco")

        result = search_service.search_jobs(params)

        assert result["total"] == 1
        assert len(result["items"]) == 1
        assert "San Francisco" in result["items"][0]["job_location"]

    def test_search_by_location_filter(self, search_service, sample_jobs):
        """Test searching by location filter"""
        params = JobSearchFilter(location="Seattle")

        result = search_service.search_jobs(params)

        assert result["total"] == 1
        assert len(result["items"]) == 1
        assert result["items"][0]["job_location"] == "Seattle, WA"

    def test_search_by_single_tag(self, search_service, sample_jobs):
        """Test searching by a single tag"""
        params = JobSearchFilter(tags=["python"])

        result = search_service.search_jobs(params)

        assert result["total"] == 3  # JOB001, JOB003, JOB005
        job_ids = [job["job_id"] for job in result["items"]]
        assert "JOB001" in job_ids
        assert "JOB003" in job_ids
        assert "JOB005" in job_ids

    def test_search_by_multiple_tags(self, search_service, sample_jobs):
        """Test searching by multiple tags (OR logic)"""
        params = JobSearchFilter(tags=["python", "react"])

        result = search_service.search_jobs(params)

        assert result["total"] == 4  # All jobs except JOB004 (DevOps)
        job_ids = [job["job_id"] for job in result["items"]]
        expected_job_ids = ["JOB001", "JOB002", "JOB003", "JOB005"]
        for job_id in expected_job_ids:
            assert job_id in job_ids

    def test_search_by_tag_category(self, search_service, sample_jobs):
        """Test searching by tag category"""
        params = JobSearchFilter(tag_categories=["technology"])

        result = search_service.search_jobs(params)

        assert result["total"] == 5  # All jobs have technology tags

    def test_search_by_date_range(self, search_service, sample_jobs):
        """Test searching by date range"""
        today = date.today()
        params = JobSearchFilter(date_from=today)

        result = search_service.search_jobs(params)

        assert result["total"] == 2  # Only jobs posted today
        for job in result["items"]:
            assert job["job_posting_date"] >= today

    def test_search_pagination_first_page(self, search_service, sample_jobs):
        """Test pagination - first page"""
        params = JobSearchFilter(page=1, limit=2)

        result = search_service.search_jobs(params)

        assert result["total"] == 5
        assert len(result["items"]) == 2
        assert result["page"] == 1
        assert result["limit"] == 2
        assert result["pages"] == 3  # ceil(5/2) = 3

    def test_search_pagination_last_page(self, search_service, sample_jobs):
        """Test pagination - last page"""
        params = JobSearchFilter(page=3, limit=2)

        result = search_service.search_jobs(params)

        assert result["total"] == 5
        assert len(result["items"]) == 1  # Last item
        assert result["page"] == 3
        assert result["limit"] == 2
        assert result["pages"] == 3

    def test_search_pagination_beyond_range(self, search_service, sample_jobs):
        """Test pagination beyond available pages"""
        params = JobSearchFilter(page=10, limit=2)

        result = search_service.search_jobs(params)

        assert result["total"] == 5
        assert len(result["items"]) == 0  # No items on page 10
        assert result["page"] == 10
        assert result["pages"] == 3

    def test_search_combined_filters(self, search_service, sample_jobs):
        """Test searching with multiple filters combined"""
        params = JobSearchFilter(
            query="Developer", location="San Francisco", tags=["python"]
        )

        result = search_service.search_jobs(params)

        assert result["total"] == 1
        assert result["items"][0]["job_id"] == "JOB001"

    def test_search_no_results(self, search_service, sample_jobs):
        """Test searching with filters that return no results"""
        params = JobSearchFilter(query="Nonexistent Job")

        result = search_service.search_jobs(params)

        assert result["total"] == 0
        assert len(result["items"]) == 0
        assert result["pages"] == 0

    def test_search_case_insensitive(self, search_service, sample_jobs):
        """Test that search is case insensitive"""
        params = JobSearchFilter(query="PYTHON")

        result = search_service.search_jobs(params)

        assert result["total"] == 1  # Should find "Senior Python Developer"
        assert result["items"][0]["job_position"] == "Senior Python Developer"

    def test_search_partial_match(self, search_service, sample_jobs):
        """Test partial string matching"""
        params = JobSearchFilter(query="Dev")  # Should match "Developer", "DevOps"

        result = search_service.search_jobs(params)

        assert result["total"] >= 2  # At least Developer positions and DevOps

    def test_search_empty_database(self, search_service):
        """Test searching in empty database"""
        params = JobSearchFilter()

        result = search_service.search_jobs(params)

        assert result["total"] == 0
        assert len(result["items"]) == 0

    def test_search_with_date_range_no_results(self, search_service, sample_jobs):
        """Test date range that excludes all jobs"""
        # Use a future date range that won't match any jobs
        future_date = date.today() + timedelta(days=30)
        params = JobSearchFilter(date_from=future_date)

        result = search_service.search_jobs(params)

        assert result["total"] == 0
        assert len(result["items"]) == 0

    def test_search_with_nonexistent_tag(self, search_service, sample_jobs):
        """Test searching with non-existent tag"""
        params = JobSearchFilter(tags=["nonexistent_tag"])

        result = search_service.search_jobs(params)

        assert result["total"] == 0
        assert len(result["items"]) == 0


class TestSearchServiceEdgeCases:
    """Test edge cases and error scenarios"""

    def test_search_with_none_parameters(self, search_service, sample_jobs):
        """Test search with None values in parameters"""
        params = JobSearchFilter(
            query=None, location=None, tags=None, tag_categories=None
        )

        result = search_service.search_jobs(params)

        assert result["total"] == 5  # Should return all jobs
        assert len(result["items"]) == 5

    def test_search_with_empty_lists(self, search_service, sample_jobs):
        """Test search with empty lists"""
        params = JobSearchFilter(tags=[], tag_categories=[])

        result = search_service.search_jobs(params)

        assert result["total"] == 5  # Should return all jobs
        assert len(result["items"]) == 5

    def test_search_with_zero_page(self, search_service, sample_jobs):
        """Test search with page 0 (should handle gracefully)"""
        params = JobSearchFilter(page=0, limit=2)

        result = search_service.search_jobs(params)

        # Depending on implementation, might return empty or handle differently
        assert isinstance(result["total"], int)
        assert isinstance(result["items"], list)

    def test_search_with_negative_page(self, search_service, sample_jobs):
        """Test search with negative page number"""
        params = JobSearchFilter(page=-1, limit=2)

        result = search_service.search_jobs(params)

        # Should handle gracefully
        assert isinstance(result, dict)
        assert "items" in result

    def test_search_with_very_large_limit(self, search_service, sample_jobs):
        """Test search with very large limit"""
        params = JobSearchFilter(limit=1000)

        result = search_service.search_jobs(params)

        assert result["total"] == 5
        assert len(result["items"]) == 5  # Can't return more than exist
        assert result["limit"] == 1000

    def test_pages_calculation_edge_cases(self, search_service, db_session):
        """Test pages calculation with various totals and limits"""
        # Test with no jobs
        params = JobSearchFilter(limit=10)
        result = search_service.search_jobs(params)
        assert result["pages"] == 0

        # Add one job for further testing
        job = Job(
            job_id="SINGLE",
            job_position="Test Job",
            job_link="https://example.com/single",
            company_name="Test Company",
            job_posting_date=date.today(),
        )
        db_session.add(job)
        db_session.commit()

        # Test with 1 job, limit 1
        params = JobSearchFilter(limit=1)
        result = search_service.search_jobs(params)
        assert result["pages"] == 1

        # Test with 1 job, limit 10
        params = JobSearchFilter(limit=10)
        result = search_service.search_jobs(params)
        assert result["pages"] == 1
