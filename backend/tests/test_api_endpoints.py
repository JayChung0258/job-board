from datetime import date, timedelta

import pytest
from app.main import app
from app.models import Job, JobTag, Tag
from app.models.tag import TagCategory

from .conftest import (
    create_job_tag_relations_from_mappings,
    create_test_client_with_db,
    refresh_objects,
)

# Create test client and database components
client, engine, TestingSessionLocal = create_test_client_with_db("api.db")


@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    # Get the database session from the dependency override
    from app.core.db import get_db

    db = next(app.dependency_overrides[get_db]())

    try:
        today = date.today()
        yesterday = today - timedelta(days=1)

        # Create jobs
        jobs = [
            Job(
                job_id="API001",
                job_position="Senior Python Developer",
                job_link="https://example.com/api001",
                company_name="TechCorp",
                job_location="San Francisco, CA",
                job_posting_date=today,
                tags={"technology": ["python", "django"], "skill": ["backend"]},
            ),
            Job(
                job_id="API002",
                job_position="React Developer",
                job_link="https://example.com/api002",
                company_name="WebDev Inc",
                job_location="New York, NY",
                job_posting_date=yesterday,
                tags={"technology": ["react", "javascript"], "skill": ["frontend"]},
            ),
            Job(
                job_id="API003",
                job_position="DevOps Engineer",
                job_link="https://example.com/api003",
                company_name="CloudSoft",
                job_location="Remote",
                job_posting_date=today,
                tags={"technology": ["docker", "kubernetes"], "skill": ["devops"]},
            ),
        ]

        # Create tags
        tags = [
            Tag(name="python", category=TagCategory.TECHNOLOGY),
            Tag(name="django", category=TagCategory.TECHNOLOGY),
            Tag(name="react", category=TagCategory.TECHNOLOGY),
            Tag(name="javascript", category=TagCategory.TECHNOLOGY),
            Tag(name="docker", category=TagCategory.TECHNOLOGY),
            Tag(name="kubernetes", category=TagCategory.TECHNOLOGY),
            Tag(name="backend", category=TagCategory.SKILL),
            Tag(name="frontend", category=TagCategory.SKILL),
            Tag(name="devops", category=TagCategory.SKILL),
        ]

        db.add_all(jobs + tags)
        db.commit()

        # Refresh all objects to get their IDs
        refresh_objects(db, jobs + tags)

        # Define job-tag relationships mapping
        job_tag_mapping = {
            "API001": ["python", "django", "backend"],
            "API002": ["react", "javascript", "frontend"],
            "API003": ["docker", "kubernetes", "devops"],
        }

        # Create job-tag relationships using shared utility
        job_tag_relations = create_job_tag_relations_from_mappings(
            jobs, tags, job_tag_mapping
        )

        db.add_all(job_tag_relations)
        db.commit()

        yield jobs, tags

        # Cleanup: remove all data
        db.query(JobTag).delete()
        db.query(Job).delete()
        db.query(Tag).delete()
        db.commit()
    finally:
        # Don't close the session as it's managed by the dependency override
        pass


class TestRootEndpoints:
    """Test root and health endpoints"""

    def test_root_endpoint(self):
        """Test root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to Job Board API"}

    def test_health_check_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestJobSearchEndpoints:
    """Test job search API endpoints"""

    def test_search_jobs_no_filters(self, sample_data):
        """Test searching jobs without filters"""
        response = client.get("/api/v1/jobs/search")
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "limit" in data
        assert "pages" in data
        assert data["total"] == 3
        assert len(data["items"]) == 3

    def test_search_jobs_with_query(self, sample_data):
        """Test searching jobs with query parameter"""
        response = client.get("/api/v1/jobs/search?query=Python")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1
        assert "Python" in data["items"][0]["job_position"]

    def test_search_jobs_with_location(self, sample_data):
        """Test searching jobs with location parameter"""
        response = client.get("/api/v1/jobs/search?location=San Francisco")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1
        assert "San Francisco" in data["items"][0]["job_location"]

    def test_search_jobs_with_tags(self, sample_data):
        """Test searching jobs with tags parameter"""
        response = client.get("/api/v1/jobs/search?tags=python&tags=react")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 2  # Python and React jobs
        assert len(data["items"]) == 2

    def test_search_jobs_with_tag_categories(self, sample_data):
        """Test searching jobs with tag categories"""
        response = client.get("/api/v1/jobs/search?tag_categories=technology")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 3  # All jobs have technology tags
        assert len(data["items"]) == 3

    def test_search_jobs_with_pagination(self, sample_data):
        """Test searching jobs with pagination"""
        response = client.get("/api/v1/jobs/search?page=1&limit=2")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 3
        assert len(data["items"]) == 2
        assert data["page"] == 1
        assert data["limit"] == 2
        assert data["pages"] == 2  # ceil(3/2) = 2

    def test_search_jobs_with_date_range(self, sample_data):
        """Test searching jobs with date range"""
        today = date.today().isoformat()
        response = client.get(f"/api/v1/jobs/search?date_from={today}")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 2  # Jobs posted today
        assert len(data["items"]) == 2

    def test_search_jobs_combined_filters(self, sample_data):
        """Test searching jobs with multiple filters"""
        response = client.get(
            "/api/v1/jobs/search?query=Developer&location=San Francisco&tags=python"
        )
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1
        assert data["items"][0]["job_id"] == "API001"

    def test_search_jobs_no_results(self, sample_data):
        """Test searching jobs with no matching results"""
        response = client.get("/api/v1/jobs/search?query=Nonexistent")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 0
        assert len(data["items"]) == 0
        assert data["pages"] == 0

    def test_search_jobs_invalid_page(self, sample_data):
        """Test searching jobs with invalid page number"""
        response = client.get("/api/v1/jobs/search?page=0")
        assert response.status_code == 200  # Should handle gracefully

        data = response.json()
        assert isinstance(data, dict)
        assert "items" in data

    def test_search_jobs_invalid_limit(self, sample_data):
        """Test searching jobs with invalid limit"""
        response = client.get("/api/v1/jobs/search?limit=-1")
        assert response.status_code == 200  # Should handle gracefully

        data = response.json()
        assert isinstance(data, dict)
        assert "items" in data

    def test_search_jobs_large_page_number(self, sample_data):
        """Test searching jobs with page number beyond available pages"""
        response = client.get("/api/v1/jobs/search?page=100")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 3
        assert len(data["items"]) == 0  # No items on page 100
        assert data["page"] == 100


class TestJobDetailEndpoints:
    """Test individual job detail endpoints"""

    def test_get_job_by_id_success(self, sample_data):
        """Test getting a job by valid ID"""
        response = client.get("/api/v1/jobs/API001")
        assert response.status_code == 200

        data = response.json()
        assert data["job_id"] == "API001"
        assert data["job_position"] == "Senior Python Developer"
        assert data["company_name"] == "TechCorp"

    def test_get_job_by_id_not_found(self, sample_data):
        """Test getting a job by non-existent ID"""
        response = client.get("/api/v1/jobs/NONEXISTENT")
        assert response.status_code == 404

        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_get_job_by_id_empty_database(self):
        """Test getting a job when database is empty"""
        response = client.get("/api/v1/jobs/ANY_ID")
        assert response.status_code == 404


class TestTagEndpoints:
    """Test tag-related API endpoints"""

    def test_get_tag_categories(self, sample_data):
        """Test getting all tag categories"""
        response = client.get("/api/v1/tags/categories")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        expected_categories = ["role", "technology", "skill", "methodology", "tool"]
        assert set(data) == set(expected_categories)

    def test_get_tags_by_valid_category(self, sample_data):
        """Test getting tags by valid category"""
        response = client.get("/api/v1/tags/by-category/technology")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        # Should contain technology tags from sample data
        assert "python" in data
        assert "react" in data

    def test_get_tags_by_invalid_category(self, sample_data):
        """Test getting tags by invalid category"""
        response = client.get("/api/v1/tags/by-category/invalid-category")
        assert response.status_code == 400

        data = response.json()
        assert "detail" in data
        assert "Invalid category" in data["detail"]

    def test_get_tags_by_empty_category(self, sample_data):
        """Test getting tags by category with no tags"""
        response = client.get("/api/v1/tags/by-category/methodology")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0  # No methodology tags in sample data


class TestAPIValidation:
    """Test API request validation and error handling"""

    def test_search_jobs_with_invalid_date_format(self, sample_data):
        """Test search with invalid date format"""
        response = client.get("/api/v1/jobs/search?date_from=invalid-date")
        assert response.status_code == 422  # Validation error

        data = response.json()
        assert "detail" in data

    def test_search_jobs_with_invalid_query_params(self, sample_data):
        """Test search with invalid query parameters"""
        # Test with very long query string
        long_query = "x" * 1000
        response = client.get(f"/api/v1/jobs/search?query={long_query}")
        assert response.status_code in [200, 422]  # Either handled or validation error

    def test_search_jobs_with_special_characters(self, sample_data):
        """Test search with special characters"""
        special_query = "python%20&<>\"'"
        response = client.get(f"/api/v1/jobs/search?query={special_query}")
        assert response.status_code == 200  # Should handle gracefully

    def test_api_endpoints_return_json(self, sample_data):
        """Test that all endpoints return valid JSON"""
        endpoints = [
            "/",
            "/health",
            "/api/v1/jobs/search",
            "/api/v1/tags/categories",
            "/api/v1/tags/by-category/technology",
        ]

        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code in [200, 404]  # Valid responses
            assert response.headers["content-type"] == "application/json"
            # Should be valid JSON
            data = response.json()
            assert isinstance(data, (dict, list))


class TestAPIPerformance:
    """Test API performance and edge cases"""

    def test_search_jobs_with_many_tags(self, sample_data):
        """Test search with many tag parameters"""
        tags_param = "&".join([f"tags=tag{i}" for i in range(20)])
        response = client.get(f"/api/v1/jobs/search?{tags_param}")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, dict)
        assert "items" in data

    def test_search_jobs_with_large_limit(self, sample_data):
        """Test search with very large limit"""
        response = client.get("/api/v1/jobs/search?limit=10000")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 3
        assert len(data["items"]) == 3  # Can't return more than exist
        assert data["limit"] == 10000

    def test_concurrent_requests_simulation(self, sample_data):
        """Test multiple concurrent-like requests"""
        # Simulate multiple requests
        responses = []
        for i in range(10):
            response = client.get(f"/api/v1/jobs/search?page={i+1}")
            responses.append(response)

        # All should succeed
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, dict)
            assert "total" in data


class TestAPIDocumentation:
    """Test API documentation and OpenAPI schema"""

    def test_openapi_schema_available(self):
        """Test that OpenAPI schema is available"""
        response = client.get("/api/v1/openapi.json")
        assert response.status_code == 200

        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data

    def test_api_endpoints_documented(self):
        """Test that main endpoints are documented in OpenAPI schema"""
        response = client.get("/api/v1/openapi.json")
        assert response.status_code == 200

        data = response.json()
        paths = data["paths"]

        # Check that main endpoints are documented
        assert "/api/v1/jobs/search" in paths
        assert "/api/v1/jobs/{job_id}" in paths
        assert "/api/v1/tags/categories" in paths
        assert "/api/v1/tags/by-category/{category}" in paths
