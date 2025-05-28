import os
import sys

import pytest
from app.core.db import Base, get_db
from app.main import app
from app.models.job_tag import JobTag
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def create_test_engine(db_name="test.db"):
    """Create a test database engine"""
    database_url = f"sqlite:///./test_{db_name}"
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    return engine


def create_test_session(engine):
    """Create a test session maker"""
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_override_get_db(testing_session_local):
    """Create database dependency override function"""

    def override_get_db():
        try:
            db = testing_session_local()
            yield db
        finally:
            db.close()

    return override_get_db


@pytest.fixture(autouse=True)
def setup_and_cleanup_app():
    """Setup and cleanup FastAPI app state for each test"""
    # Store original dependency overrides
    original_overrides = app.dependency_overrides.copy()

    yield

    # Cleanup: restore original dependency overrides
    app.dependency_overrides.clear()
    app.dependency_overrides.update(original_overrides)


def create_test_client_with_db(db_name="test.db"):
    """Create a test client with database override"""
    engine = create_test_engine(db_name)
    Base.metadata.create_all(bind=engine)  # Create tables
    testing_session_local = create_test_session(engine)
    override_get_db = create_override_get_db(testing_session_local)

    # Override the dependency
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    return client, engine, testing_session_local


def create_test_db_session(engine):
    """Create a test database session fixture"""
    Base.metadata.create_all(bind=engine)
    testing_session_local = create_test_session(engine)
    db = testing_session_local()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def create_job_tag_relations_from_mappings(jobs, tags, job_tag_mapping):
    """
    Create JobTag relationships using actual primary keys

    Args:
        jobs: List of Job objects
        tags: List of Tag objects
        job_tag_mapping: Dict mapping job_id to list of tag names
                        e.g., {"JOB001": ["python", "django"], "JOB002": ["react"]}

    Returns:
        List of JobTag objects
    """
    # Create mappings for easier reference
    tag_name_to_id = {tag.name: tag.id for tag in tags}
    job_id_to_pk = {job.job_id: job.id for job in jobs}

    job_tag_relations = []
    for job_id, tag_names in job_tag_mapping.items():
        for tag_name in tag_names:
            if tag_name in tag_name_to_id and job_id in job_id_to_pk:
                job_tag_relations.append(
                    JobTag(job_id=job_id_to_pk[job_id], tag_id=tag_name_to_id[tag_name])
                )

    return job_tag_relations


def refresh_objects(db_session, objects):
    """Refresh database objects to get their IDs"""
    for obj in objects:
        db_session.refresh(obj)
