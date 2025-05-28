from datetime import date, timedelta

import pytest
from app.models import Job, Tag
from app.models.tag import TagCategory

from .conftest import (
    create_job_tag_relations_from_mappings,
    create_test_client_with_db,
    create_test_db_session,
    refresh_objects,
)

# Create test client and database components
client, engine, TestingSessionLocal = create_test_client_with_db("integration.db")


@pytest.fixture
def db_session():
    """Create a test database session"""
    yield from create_test_db_session(engine)


@pytest.fixture
def comprehensive_test_data(db_session):
    """Create comprehensive test data for integration tests"""
    today = date.today()
    yesterday = today - timedelta(days=1)
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    # Create jobs with various characteristics
    jobs = [
        Job(
            job_id="INT001",
            job_position="Senior Python Developer",
            job_link="https://example.com/int001",
            company_name="TechCorp",
            job_location="San Francisco, CA",
            job_posting_date=today,
            tags={
                "technology": ["python", "django", "postgresql"],
                "skill": ["backend", "api-development"],
            },
        ),
        Job(
            job_id="INT002",
            job_position="React Frontend Developer",
            job_link="https://example.com/int002",
            company_name="WebDev Inc",
            job_location="New York, NY",
            job_posting_date=yesterday,
            tags={
                "technology": ["react", "javascript", "typescript"],
                "skill": ["frontend", "ui-ux"],
            },
        ),
        Job(
            job_id="INT003",
            job_position="Full Stack Engineer",
            job_link="https://example.com/int003",
            company_name="StartupXYZ",
            job_location="Remote",
            job_posting_date=week_ago,
            tags={
                "technology": ["python", "react", "mongodb"],
                "skill": ["fullstack", "agile"],
            },
        ),
        Job(
            job_id="INT004",
            job_position="DevOps Engineer",
            job_link="https://example.com/int004",
            company_name="CloudSoft",
            job_location="Seattle, WA",
            job_posting_date=today,
            tags={
                "technology": ["docker", "kubernetes", "aws"],
                "skill": ["devops", "ci-cd"],
            },
        ),
        Job(
            job_id="INT005",
            job_position="Data Scientist",
            job_link="https://example.com/int005",
            company_name="DataTech",
            job_location="Austin, TX",
            job_posting_date=yesterday,
            tags={
                "technology": ["python", "tensorflow", "pandas"],
                "skill": ["machine-learning", "analytics"],
            },
        ),
        Job(
            job_id="INT006",
            job_position="Mobile Developer",
            job_link="https://example.com/int006",
            company_name="MobileCorp",
            job_location="Los Angeles, CA",
            job_posting_date=month_ago,
            tags={
                "technology": ["react-native", "swift", "kotlin"],
                "skill": ["mobile", "ios", "android"],
            },
        ),
        Job(
            job_id="INT007",
            job_position="Backend Engineer",
            job_link="https://example.com/int007",
            company_name="BackendSoft",
            job_location="Remote",
            job_posting_date=week_ago,
            tags={
                "technology": ["java", "spring", "mysql"],
                "skill": ["backend", "microservices"],
            },
        ),
        Job(
            job_id="INT008",
            job_position="QA Engineer",
            job_link="https://example.com/int008",
            company_name="QualityFirst",
            job_location="Chicago, IL",
            job_posting_date=today,
            tags={
                "technology": ["selenium", "cypress", "jest"],
                "skill": ["testing", "automation"],
            },
        ),
    ]

    # Create comprehensive tag set
    tags = [
        # Technology tags
        Tag(name="python", category=TagCategory.TECHNOLOGY),
        Tag(name="django", category=TagCategory.TECHNOLOGY),
        Tag(name="postgresql", category=TagCategory.TECHNOLOGY),
        Tag(name="react", category=TagCategory.TECHNOLOGY),
        Tag(name="javascript", category=TagCategory.TECHNOLOGY),
        Tag(name="typescript", category=TagCategory.TECHNOLOGY),
        Tag(name="mongodb", category=TagCategory.TECHNOLOGY),
        Tag(name="docker", category=TagCategory.TECHNOLOGY),
        Tag(name="kubernetes", category=TagCategory.TECHNOLOGY),
        Tag(name="aws", category=TagCategory.TECHNOLOGY),
        Tag(name="tensorflow", category=TagCategory.TECHNOLOGY),
        Tag(name="pandas", category=TagCategory.TECHNOLOGY),
        Tag(name="react-native", category=TagCategory.TECHNOLOGY),
        Tag(name="swift", category=TagCategory.TECHNOLOGY),
        Tag(name="kotlin", category=TagCategory.TECHNOLOGY),
        Tag(name="java", category=TagCategory.TECHNOLOGY),
        Tag(name="spring", category=TagCategory.TECHNOLOGY),
        Tag(name="mysql", category=TagCategory.TECHNOLOGY),
        Tag(name="selenium", category=TagCategory.TECHNOLOGY),
        Tag(name="cypress", category=TagCategory.TECHNOLOGY),
        Tag(name="jest", category=TagCategory.TECHNOLOGY),
        # Skill tags
        Tag(name="backend", category=TagCategory.SKILL),
        Tag(name="api-development", category=TagCategory.SKILL),
        Tag(name="frontend", category=TagCategory.SKILL),
        Tag(name="ui-ux", category=TagCategory.SKILL),
        Tag(name="fullstack", category=TagCategory.SKILL),
        Tag(name="agile", category=TagCategory.SKILL),
        Tag(name="devops", category=TagCategory.SKILL),
        Tag(name="ci-cd", category=TagCategory.SKILL),
        Tag(name="machine-learning", category=TagCategory.SKILL),
        Tag(name="analytics", category=TagCategory.SKILL),
        Tag(name="mobile", category=TagCategory.SKILL),
        Tag(name="ios", category=TagCategory.SKILL),
        Tag(name="android", category=TagCategory.SKILL),
        Tag(name="microservices", category=TagCategory.SKILL),
        Tag(name="testing", category=TagCategory.SKILL),
        Tag(name="automation", category=TagCategory.SKILL),
    ]

    db_session.add_all(jobs + tags)
    db_session.commit()

    # Refresh all objects to get their IDs
    refresh_objects(db_session, jobs + tags)

    # Define job-tag relationships mapping
    job_tag_mapping = {
        "INT001": ["python", "django", "postgresql", "backend", "api-development"],
        "INT002": ["react", "javascript", "typescript", "frontend", "ui-ux"],
        "INT003": ["python", "react", "mongodb", "fullstack", "agile"],
        "INT004": ["docker", "kubernetes", "aws", "devops", "ci-cd"],
        "INT005": ["python", "tensorflow", "pandas", "machine-learning", "analytics"],
        "INT006": ["react-native", "swift", "kotlin", "mobile", "ios", "android"],
        "INT007": ["java", "spring", "mysql", "backend", "microservices"],
        "INT008": ["selenium", "cypress", "jest", "testing", "automation"],
    }

    # Create job-tag relationships using shared utility
    job_tag_relations = create_job_tag_relations_from_mappings(
        jobs, tags, job_tag_mapping
    )

    db_session.add_all(job_tag_relations)
    db_session.commit()

    return jobs, tags


class TestFullStackIntegration:
    """Integration tests covering the full application stack"""

    def test_complete_job_search_workflow(self, comprehensive_test_data):
        """Test complete job search workflow from API to database"""
        # Test 1: Search all jobs
        response = client.get("/api/v1/jobs/search")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 8
        assert len(data["items"]) == 8

        # Test 2: Search by technology
        response = client.get("/api/v1/jobs/search?tags=python")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3  # INT001, INT003, INT005
        python_jobs = [job["job_id"] for job in data["items"]]
        assert "INT001" in python_jobs
        assert "INT003" in python_jobs
        assert "INT005" in python_jobs

        # Test 3: Search by skill category
        response = client.get("/api/v1/jobs/search?tag_categories=skill")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 8  # All jobs have skill tags

        # Test 4: Complex search with multiple filters
        response = client.get(
            "/api/v1/jobs/search?query=Developer&location=San Francisco&tags=python"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["job_id"] == "INT001"

        # Test 5: Date range search
        today = date.today().isoformat()
        response = client.get(f"/api/v1/jobs/search?date_from={today}")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3  # Jobs posted today

        # Test 6: Pagination
        response = client.get("/api/v1/jobs/search?page=1&limit=3")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 8
        assert len(data["items"]) == 3
        assert data["pages"] == 3  # ceil(8/3) = 3

        # Test 7: Second page
        response = client.get("/api/v1/jobs/search?page=2&limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert data["page"] == 2

    def test_job_detail_integration(self, comprehensive_test_data):
        """Test job detail retrieval integration"""
        # Test getting existing job
        response = client.get("/api/v1/jobs/INT001")
        assert response.status_code == 200
        data = response.json()
        assert data["job_id"] == "INT001"
        assert data["job_position"] == "Senior Python Developer"
        assert data["company_name"] == "TechCorp"
        assert data["job_location"] == "San Francisco, CA"

        # Test getting non-existent job
        response = client.get("/api/v1/jobs/NONEXISTENT")
        assert response.status_code == 404

        # Test all jobs can be retrieved individually
        job_ids = [
            "INT001",
            "INT002",
            "INT003",
            "INT004",
            "INT005",
            "INT006",
            "INT007",
            "INT008",
        ]
        for job_id in job_ids:
            response = client.get(f"/api/v1/jobs/{job_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["job_id"] == job_id

    def test_tag_system_integration(self, comprehensive_test_data):
        """Test tag system integration"""
        # Test getting all categories
        response = client.get("/api/v1/tags/categories")
        assert response.status_code == 200
        categories = response.json()
        assert "technology" in categories
        assert "skill" in categories

        # Test getting technology tags
        response = client.get("/api/v1/tags/by-category/technology")
        assert response.status_code == 200
        tech_tags = response.json()
        assert "python" in tech_tags
        assert "react" in tech_tags
        assert "docker" in tech_tags
        assert len(tech_tags) > 10  # Should have many technology tags

        # Test getting skill tags
        response = client.get("/api/v1/tags/by-category/skill")
        assert response.status_code == 200
        skill_tags = response.json()
        assert "backend" in skill_tags
        assert "frontend" in skill_tags
        assert "devops" in skill_tags
        assert len(skill_tags) > 10  # Should have many skill tags

        # Test invalid category
        response = client.get("/api/v1/tags/by-category/invalid")
        assert response.status_code == 400

    def test_search_performance_integration(self, comprehensive_test_data):
        """Test search performance with various query patterns"""
        # Test simple queries
        simple_queries = ["Python", "React", "Developer", "Engineer", "Remote"]
        for query in simple_queries:
            response = client.get(f"/api/v1/jobs/search?query={query}")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data["total"], int)
            assert isinstance(data["items"], list)

        # Test location searches
        locations = ["San Francisco", "New York", "Remote", "Seattle", "Austin"]
        for location in locations:
            response = client.get(f"/api/v1/jobs/search?location={location}")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data["total"], int)

        # Test tag combinations
        tag_combinations = [
            ["python"],
            ["python", "react"],
            ["backend", "api-development"],
            ["frontend", "ui-ux"],
            ["devops", "docker", "kubernetes"],
        ]
        for tags in tag_combinations:
            tags_param = "&".join([f"tags={tag}" for tag in tags])
            response = client.get(f"/api/v1/jobs/search?{tags_param}")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data["total"], int)

    def test_data_consistency_integration(self, comprehensive_test_data):
        """Test data consistency across different access patterns"""
        # Get total count via search
        response = client.get("/api/v1/jobs/search")
        assert response.status_code == 200
        total_via_search = response.json()["total"]

        # Get all jobs via pagination and count
        all_jobs = []
        page = 1
        while True:
            response = client.get(f"/api/v1/jobs/search?page={page}&limit=3")
            assert response.status_code == 200
            data = response.json()
            all_jobs.extend(data["items"])
            if len(data["items"]) < 3:  # Last page
                break
            page += 1

        # Verify counts match
        assert len(all_jobs) == total_via_search
        assert len(all_jobs) == 8

        # Verify all job IDs are unique
        job_ids = [job["job_id"] for job in all_jobs]
        assert len(job_ids) == len(set(job_ids))

        # Verify each job can be accessed individually
        for job in all_jobs:
            response = client.get(f"/api/v1/jobs/{job['job_id']}")
            assert response.status_code == 200
            individual_job = response.json()
            assert individual_job["job_id"] == job["job_id"]
            assert individual_job["job_position"] == job["job_position"]

    def test_edge_case_integration(self, comprehensive_test_data):
        """Test edge cases in integration scenarios"""
        # Test empty search results
        response = client.get("/api/v1/jobs/search?query=NonexistentTechnology")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert len(data["items"]) == 0
        assert data["pages"] == 0

        # Test very specific search that should return one result
        response = client.get("/api/v1/jobs/search?query=QA Engineer&location=Chicago")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["job_id"] == "INT008"

        # Test search with future date (should return no results)
        future_date = (date.today() + timedelta(days=30)).isoformat()
        response = client.get(f"/api/v1/jobs/search?date_from={future_date}")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0

        # Test search with very old date (should return all results)
        old_date = (date.today() - timedelta(days=365)).isoformat()
        response = client.get(f"/api/v1/jobs/search?date_from={old_date}")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 8

        # Test large page number
        response = client.get("/api/v1/jobs/search?page=100&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 8
        assert len(data["items"]) == 0  # No items on page 100
        assert data["page"] == 100

    def test_api_error_handling_integration(self, comprehensive_test_data):
        """Test API error handling in integration scenarios"""
        # Test invalid date format
        response = client.get("/api/v1/jobs/search?date_from=invalid-date")
        assert response.status_code == 422

        # Test invalid job ID format (should return 404, not error)
        response = client.get("/api/v1/jobs/invalid-id-format")
        assert response.status_code == 404

        # Test malformed query parameters (should handle gracefully)
        response = client.get("/api/v1/jobs/search?page=abc")
        assert response.status_code == 422

        # Test very long query string (should handle gracefully)
        long_query = "x" * 1000
        response = client.get(f"/api/v1/jobs/search?query={long_query}")
        assert response.status_code in [200, 422]  # Either handled or validation error

    def test_concurrent_access_simulation(self, comprehensive_test_data):
        """Simulate concurrent access patterns"""
        # Simulate multiple users searching simultaneously
        search_patterns = [
            "/api/v1/jobs/search?query=Python",
            "/api/v1/jobs/search?location=Remote",
            "/api/v1/jobs/search?tags=react",
            "/api/v1/jobs/search?tag_categories=technology",
            "/api/v1/jobs/search?page=1&limit=5",
            "/api/v1/jobs/search?page=2&limit=5",
        ]

        # Execute all patterns and verify they all succeed
        responses = []
        for pattern in search_patterns:
            response = client.get(pattern)
            responses.append(response)

        # All should succeed
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert "total" in data
            assert "items" in data
            assert isinstance(data["items"], list)

        # Simulate accessing individual jobs
        job_ids = ["INT001", "INT002", "INT003", "INT004", "INT005"]
        job_responses = []
        for job_id in job_ids:
            response = client.get(f"/api/v1/jobs/{job_id}")
            job_responses.append(response)

        # All should succeed
        for response in job_responses:
            assert response.status_code == 200
            data = response.json()
            assert "job_id" in data
            assert "job_position" in data
