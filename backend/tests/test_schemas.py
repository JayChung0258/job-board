from datetime import date, timedelta

import pytest
from app.schemas.job_filter import JobSearchFilter
from pydantic import ValidationError


class TestJobSearchFilterSchema:
    """Test cases for JobSearchFilter Pydantic schema"""

    def test_job_search_filter_default_values(self):
        """Test JobSearchFilter with default values"""
        filter_obj = JobSearchFilter()

        assert filter_obj.query is None
        assert filter_obj.location is None
        assert filter_obj.tags is None
        assert filter_obj.tag_categories is None
        assert filter_obj.date_from is None
        assert filter_obj.date_to is None
        assert filter_obj.page == 1
        assert filter_obj.limit == 10
        assert filter_obj.match_all_tags is False

    def test_job_search_filter_with_all_fields(self):
        """Test JobSearchFilter with all fields populated"""
        today = date.today()
        yesterday = today - timedelta(days=1)

        filter_obj = JobSearchFilter(
            query="Python Developer",
            location="San Francisco",
            tags=["python", "django", "fastapi"],
            tag_categories=["technology", "skill"],
            date_from=yesterday,
            date_to=today,
            page=2,
            limit=20,
            match_all_tags=True,
        )

        assert filter_obj.query == "Python Developer"
        assert filter_obj.location == "San Francisco"
        assert filter_obj.tags == ["python", "django", "fastapi"]
        assert filter_obj.tag_categories == ["technology", "skill"]
        assert filter_obj.date_from == yesterday
        assert filter_obj.date_to == today
        assert filter_obj.page == 2
        assert filter_obj.limit == 20
        assert filter_obj.match_all_tags is True

    def test_job_search_filter_with_partial_fields(self):
        """Test JobSearchFilter with only some fields populated"""
        filter_obj = JobSearchFilter(query="React", page=3, limit=5)

        assert filter_obj.query == "React"
        assert filter_obj.location is None
        assert filter_obj.tags is None
        assert filter_obj.tag_categories is None
        assert filter_obj.date_from is None
        assert filter_obj.date_to is None
        assert filter_obj.page == 3
        assert filter_obj.limit == 5
        assert filter_obj.match_all_tags is False

    def test_job_search_filter_empty_lists(self):
        """Test JobSearchFilter with empty lists"""
        filter_obj = JobSearchFilter(tags=[], tag_categories=[])

        assert filter_obj.tags == []
        assert filter_obj.tag_categories == []

    def test_job_search_filter_single_item_lists(self):
        """Test JobSearchFilter with single-item lists"""
        filter_obj = JobSearchFilter(tags=["python"], tag_categories=["technology"])

        assert filter_obj.tags == ["python"]
        assert filter_obj.tag_categories == ["technology"]

    def test_job_search_filter_page_validation(self):
        """Test page number validation"""
        # Valid page numbers
        filter_obj = JobSearchFilter(page=1)
        assert filter_obj.page == 1

        filter_obj = JobSearchFilter(page=100)
        assert filter_obj.page == 100

        # Test with zero (should be handled by application logic, not schema)
        filter_obj = JobSearchFilter(page=0)
        assert filter_obj.page == 0

        # Test with negative (should be handled by application logic, not schema)
        filter_obj = JobSearchFilter(page=-1)
        assert filter_obj.page == -1

    def test_job_search_filter_limit_validation(self):
        """Test limit validation"""
        # Valid limits
        filter_obj = JobSearchFilter(limit=1)
        assert filter_obj.limit == 1

        filter_obj = JobSearchFilter(limit=100)
        assert filter_obj.limit == 100

        filter_obj = JobSearchFilter(limit=1000)
        assert filter_obj.limit == 1000

        # Test with zero and negative (should be handled by application logic)
        filter_obj = JobSearchFilter(limit=0)
        assert filter_obj.limit == 0

        filter_obj = JobSearchFilter(limit=-1)
        assert filter_obj.limit == -1

    def test_job_search_filter_date_validation(self):
        """Test date field validation"""
        today = date.today()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)

        # Valid date range
        filter_obj = JobSearchFilter(date_from=yesterday, date_to=today)
        assert filter_obj.date_from == yesterday
        assert filter_obj.date_to == today

        # Same date for from and to
        filter_obj = JobSearchFilter(date_from=today, date_to=today)
        assert filter_obj.date_from == today
        assert filter_obj.date_to == today

        # Future dates
        filter_obj = JobSearchFilter(date_from=today, date_to=tomorrow)
        assert filter_obj.date_from == today
        assert filter_obj.date_to == tomorrow

        # Reverse date range (from > to) - should be handled by application logic
        filter_obj = JobSearchFilter(date_from=today, date_to=yesterday)
        assert filter_obj.date_from == today
        assert filter_obj.date_to == yesterday

    def test_job_search_filter_string_fields_validation(self):
        """Test string field validation and edge cases"""
        # Empty strings
        filter_obj = JobSearchFilter(query="", location="")
        assert filter_obj.query == ""
        assert filter_obj.location == ""

        # Whitespace strings
        filter_obj = JobSearchFilter(query="   ", location="   ")
        assert filter_obj.query == "   "
        assert filter_obj.location == "   "

        # Very long strings
        long_string = "x" * 1000
        filter_obj = JobSearchFilter(query=long_string, location=long_string)
        assert filter_obj.query == long_string
        assert filter_obj.location == long_string

        # Special characters
        special_string = "Python & Django @ San Francisco (Remote) 100%"
        filter_obj = JobSearchFilter(query=special_string, location=special_string)
        assert filter_obj.query == special_string
        assert filter_obj.location == special_string

        # Unicode characters
        unicode_string = "Python Développeur à Paris 🐍"
        filter_obj = JobSearchFilter(query=unicode_string, location=unicode_string)
        assert filter_obj.query == unicode_string
        assert filter_obj.location == unicode_string

    def test_job_search_filter_list_fields_validation(self):
        """Test list field validation and edge cases"""
        # Lists with various string types
        filter_obj = JobSearchFilter(
            tags=["python", "django", "fastapi", ""],
            tag_categories=["technology", "skill", ""],
        )
        assert filter_obj.tags == ["python", "django", "fastapi", ""]
        assert filter_obj.tag_categories == ["technology", "skill", ""]

        # Lists with whitespace
        filter_obj = JobSearchFilter(
            tags=["  python  ", "django", "  "],
            tag_categories=["  technology  ", "skill"],
        )
        assert filter_obj.tags == ["  python  ", "django", "  "]
        assert filter_obj.tag_categories == ["  technology  ", "skill"]

        # Lists with duplicates
        filter_obj = JobSearchFilter(
            tags=["python", "python", "django"],
            tag_categories=["technology", "technology", "skill"],
        )
        assert filter_obj.tags == ["python", "python", "django"]
        assert filter_obj.tag_categories == ["technology", "technology", "skill"]

        # Large lists
        large_list = [f"tag{i}" for i in range(100)]
        filter_obj = JobSearchFilter(tags=large_list)
        assert filter_obj.tags == large_list

    def test_job_search_filter_boolean_validation(self):
        """Test boolean field validation"""
        # Explicit True/False
        filter_obj = JobSearchFilter(match_all_tags=True)
        assert filter_obj.match_all_tags is True

        filter_obj = JobSearchFilter(match_all_tags=False)
        assert filter_obj.match_all_tags is False

        # Truthy/Falsy values (Pydantic should convert)
        filter_obj = JobSearchFilter(match_all_tags=1)
        assert filter_obj.match_all_tags is True

        filter_obj = JobSearchFilter(match_all_tags=0)
        assert filter_obj.match_all_tags is False

        filter_obj = JobSearchFilter(match_all_tags="true")
        assert filter_obj.match_all_tags is True

        filter_obj = JobSearchFilter(match_all_tags="false")
        assert filter_obj.match_all_tags is False

    def test_job_search_filter_type_coercion(self):
        """Test Pydantic type coercion"""
        # String to int coercion for page and limit
        filter_obj = JobSearchFilter(page="5", limit="20")
        assert filter_obj.page == 5
        assert filter_obj.limit == 20

        # String to date coercion
        filter_obj = JobSearchFilter(date_from="2024-01-01", date_to="2024-12-31")
        assert filter_obj.date_from == date(2024, 1, 1)
        assert filter_obj.date_to == date(2024, 12, 31)

    def test_job_search_filter_invalid_types(self):
        """Test validation errors with invalid types"""
        # Invalid date format
        with pytest.raises(ValidationError) as exc_info:
            JobSearchFilter(date_from="invalid-date")
        assert "date_from" in str(exc_info.value)

        # Invalid date format for date_to
        with pytest.raises(ValidationError) as exc_info:
            JobSearchFilter(date_to="not-a-date")
        assert "date_to" in str(exc_info.value)

        # Invalid page type (non-numeric string)
        with pytest.raises(ValidationError) as exc_info:
            JobSearchFilter(page="not-a-number")
        assert "page" in str(exc_info.value)

        # Invalid limit type
        with pytest.raises(ValidationError) as exc_info:
            JobSearchFilter(limit="not-a-number")
        assert "limit" in str(exc_info.value)

    def test_job_search_filter_json_serialization(self):
        """Test JSON serialization and deserialization"""
        today = date.today()

        # Create filter object
        original_filter = JobSearchFilter(
            query="Python Developer",
            location="San Francisco",
            tags=["python", "django"],
            tag_categories=["technology"],
            date_from=today,
            page=2,
            limit=15,
            match_all_tags=True,
        )

        # Serialize to dict
        filter_dict = original_filter.model_dump()

        # Verify dict structure
        assert filter_dict["query"] == "Python Developer"
        assert filter_dict["location"] == "San Francisco"
        assert filter_dict["tags"] == ["python", "django"]
        assert filter_dict["tag_categories"] == ["technology"]
        assert filter_dict["date_from"] == today
        assert filter_dict["page"] == 2
        assert filter_dict["limit"] == 15
        assert filter_dict["match_all_tags"] is True

        # Deserialize back to object
        recreated_filter = JobSearchFilter(**filter_dict)

        # Verify objects are equivalent
        assert recreated_filter.query == original_filter.query
        assert recreated_filter.location == original_filter.location
        assert recreated_filter.tags == original_filter.tags
        assert recreated_filter.tag_categories == original_filter.tag_categories
        assert recreated_filter.date_from == original_filter.date_from
        assert recreated_filter.page == original_filter.page
        assert recreated_filter.limit == original_filter.limit
        assert recreated_filter.match_all_tags == original_filter.match_all_tags

    def test_job_search_filter_model_validation(self):
        """Test model-level validation"""
        # Test that the model accepts valid combinations
        valid_combinations = [
            {},  # All defaults
            {"query": "Python"},
            {"location": "Remote"},
            {"tags": ["python"]},
            {"tag_categories": ["technology"]},
            {"page": 1, "limit": 10},
            {"date_from": date.today()},
            {"date_to": date.today()},
            {"match_all_tags": True},
            {  # All fields
                "query": "Full Stack",
                "location": "New York",
                "tags": ["python", "react"],
                "tag_categories": ["technology", "skill"],
                "date_from": date.today() - timedelta(days=30),
                "date_to": date.today(),
                "page": 1,
                "limit": 20,
                "match_all_tags": False,
            },
        ]

        for combination in valid_combinations:
            filter_obj = JobSearchFilter(**combination)
            assert isinstance(filter_obj, JobSearchFilter)

    def test_job_search_filter_edge_cases(self):
        """Test edge cases and boundary conditions"""
        # Very large page and limit
        filter_obj = JobSearchFilter(page=999999, limit=999999)
        assert filter_obj.page == 999999
        assert filter_obj.limit == 999999

        # Very old and future dates
        old_date = date(1900, 1, 1)
        future_date = date(2100, 12, 31)
        filter_obj = JobSearchFilter(date_from=old_date, date_to=future_date)
        assert filter_obj.date_from == old_date
        assert filter_obj.date_to == future_date

        # Empty and None combinations
        filter_obj = JobSearchFilter(
            query=None, location=None, tags=None, tag_categories=None
        )
        assert filter_obj.query is None
        assert filter_obj.location is None
        assert filter_obj.tags is None
        assert filter_obj.tag_categories is None
