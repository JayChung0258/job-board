import json
import pytest
import os
from datetime import date, datetime
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a mock Base for testing
Base = declarative_base()

from app.models.job import Job
from app.models.tag import Tag, TagCategory
from app.models.job_tag import JobTag
from app.schemas.job_filter import JobSearchFilter
from app.services.search import SearchService


class TestSearchService:
    @pytest.fixture
    def mock_db(self):
        # Create mock session with mock query results
        mock_session = MagicMock(spec=Session)
        return mock_session
    
    @pytest.fixture
    def mock_jobs_data(self):
        # Load mock jobs from the json file
        mock_jobs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app/data/mock_jobs.json")
        with open(mock_jobs_path, "r") as f:
            return json.load(f)["jobs"]
    
    @pytest.fixture
    def search_service(self, mock_db):
        return SearchService(mock_db)
    
    def test_search_by_query(self, search_service, mock_db, mock_jobs_data):
        # Setup mock query with Python developer job
        query_mock = MagicMock()
        mock_db.query.return_value = query_mock
        
        # Mock filtered job
        python_job = [job for job in mock_jobs_data if "Python" in job["job_position"]][0]
        mock_job = MagicMock(spec=Job)
        mock_job.job_position = python_job["job_position"]
        mock_job.company_name = python_job["company_name"]
        
        # Chain mock returns for query builder methods
        query_mock.filter.return_value = query_mock
        query_mock.offset.return_value = query_mock
        query_mock.limit.return_value = query_mock
        query_mock.all.return_value = [mock_job]
        query_mock.count.return_value = 1
        
        # Create search parameters for Python developer
        search_params = JobSearchFilter(query="Python")
        
        # Execute search
        result = search_service.search_jobs(search_params)
        
        # Verify mocks were called correctly
        mock_db.query.assert_called_once_with(Job)
        
        # Verify results
        assert len(result["items"]) == 1
        assert result["total"] == 1
        assert result["page"] == 1
        assert result["limit"] == 10
        assert result["pages"] == 1
    
    def test_search_by_location(self, search_service, mock_db, mock_jobs_data):
        # Setup mock query with San Francisco job
        query_mock = MagicMock()
        mock_db.query.return_value = query_mock
        
        # Mock filtered job
        sf_job = [job for job in mock_jobs_data if "San Francisco" in job["job_location"]][0]
        mock_job = MagicMock(spec=Job)
        mock_job.job_position = sf_job["job_position"]
        mock_job.job_location = sf_job["job_location"]
        
        # Chain mock returns for query builder methods
        query_mock.filter.return_value = query_mock
        query_mock.offset.return_value = query_mock
        query_mock.limit.return_value = query_mock
        query_mock.all.return_value = [mock_job]
        query_mock.count.return_value = 1
        
        # Create search parameters for San Francisco location
        search_params = JobSearchFilter(location="San Francisco")
        
        # Execute search
        result = search_service.search_jobs(search_params)
        
        # Verify results
        assert len(result["items"]) == 1
        assert result["total"] == 1
        assert mock_job.job_location == sf_job["job_location"]
    
    def test_search_by_tags(self, search_service, mock_db, mock_jobs_data):
        # Setup mock query with Python tag
        query_mock = MagicMock()
        mock_db.query.return_value = query_mock
        
        # Mock jobs with Python tag
        python_jobs = [job for job in mock_jobs_data 
                      if any(tech == "Python" for tech in job["tags"].get("technology", []))]
        
        mock_jobs = []
        for job in python_jobs:
            mock_job = MagicMock(spec=Job)
            mock_job.job_position = job["job_position"]
            mock_jobs.append(mock_job)
        
        # Chain mock returns for query builder methods
        query_mock.join.return_value = query_mock
        query_mock.filter.return_value = query_mock
        query_mock.offset.return_value = query_mock
        query_mock.limit.return_value = query_mock
        query_mock.all.return_value = mock_jobs
        query_mock.count.return_value = len(mock_jobs)
        
        # Create search parameters for Python tag
        search_params = JobSearchFilter(tags=["Python"])
        
        # Execute search
        result = search_service.search_jobs(search_params)
        
        # Verify joins were called for tag filtering
        query_mock.join.assert_called()
        
        # Verify results
        assert len(result["items"]) == len(mock_jobs)
        assert result["total"] == len(mock_jobs)
    
    def test_search_with_pagination(self, search_service, mock_db, mock_jobs_data):
        # Setup mock query 
        query_mock = MagicMock()
        mock_db.query.return_value = query_mock
        
        # Mock all jobs
        mock_jobs = []
        for job in mock_jobs_data[:3]:  # Just use first 3 jobs
            mock_job = MagicMock(spec=Job)
            mock_job.job_position = job["job_position"]
            mock_jobs.append(mock_job)
        
        # Chain mock returns for query builder methods
        query_mock.offset.return_value = query_mock
        query_mock.limit.return_value = query_mock
        query_mock.all.return_value = mock_jobs[:2]  # Return only first 2 jobs
        query_mock.count.return_value = len(mock_jobs_data)  # Total count is all jobs
        
        # Create search parameters with pagination
        search_params = JobSearchFilter(page=1, limit=2)
        
        # Execute search
        result = search_service.search_jobs(search_params)
        
        # Verify pagination was applied correctly
        query_mock.offset.assert_called_once_with(0)  # (page-1) * limit = (1-1) * 2 = 0
        query_mock.limit.assert_called_once_with(2)
        
        # Verify results
        assert len(result["items"]) == 2
        assert result["total"] == len(mock_jobs_data)
        assert result["page"] == 1
        assert result["limit"] == 2
        assert result["pages"] == (len(mock_jobs_data) + 1) // 2  # Calculate expected pages 