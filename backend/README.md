# Job Board Backend API

## Overview

This is the backend API for the Job Board application, built with **FastAPI and clean architecture principles**. The backend provides endpoints for job listings, tags, and advanced search functionality with a **layered architecture** that emphasizes maintainability, testability, and scalability.

## Architecture & Design

### **Clean Architecture Pattern**

The backend follows a **clean architecture pattern** with clear separation of concerns across four distinct layers:

```
┌─────────────────────────────────────────────────────────────┐
│                      API Layer                             │
│  ┌─────────────────┐  ┌─────────────────┐                 │
│  │   jobs.py       │  │   tags.py       │                 │
│  │ (HTTP Endpoints)│  │ (HTTP Endpoints)│                 │
│  └─────────────────┘  └─────────────────┘                 │
├─────────────────────────────────────────────────────────────┤
│                    Service Layer                           │
│  ┌─────────────────┐  ┌─────────────────┐                 │
│  │   search.py     │  │ tag_service.py  │                 │
│  │ (Business Logic)│  │ (Business Logic)│                 │
│  └─────────────────┘  └─────────────────┘                 │
├─────────────────────────────────────────────────────────────┤
│                    Manager Layer                           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │
│  │job_manager.py│ │tag_manager.py│ │job_tag_manager.py│    │
│  │(Data Access) │ │(Data Access) │ │(Relationships)   │    │
│  └──────────────┘ └──────────────┘ └──────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│                     Model Layer                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   job.py    │  │   tag.py    │  │ job_tag.py  │        │
│  │(SQLAlchemy) │  │(SQLAlchemy) │  │(SQLAlchemy) │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘

         ┌─────────────────────────────────────┐
         │        Core Components              │
         │ ┌─────────────┐ ┌─────────────────┐ │
         │ │dependencies │ │   config.py     │ │
         │ │    .py      │ │   db.py         │ │
         │ │(DI Container│ │(Configuration)  │ │
         │ └─────────────┘ └─────────────────┘ │
         └─────────────────────────────────────┘
```

### **Design Principles**

#### **1. Separation of Concerns**

Each layer has a single, well-defined responsibility:

- **API Layer**: HTTP request/response handling, routing, validation
- **Service Layer**: Business logic, coordination, data transformation
- **Manager Layer**: Database operations, queries, data persistence
- **Model Layer**: Data entities, relationships, schema definitions

#### **2. Dependency Injection**

- Centralized dependency container in `core/dependencies.py`
- Loose coupling between layers for better testability
- Easy to mock dependencies for unit testing

#### **3. Single Responsibility Principle**

Each component has a focused purpose:

- `JobManager`: Job database operations and queries
- `TagManager`: Tag CRUD operations and categorization
- `JobTagManager`: Job-Tag relationship management
- `SearchService`: Search coordination and filtering logic
- `TagService`: Tag business logic and validation

### **Component Details**

#### **API Layer** (`app/api/`)

**File: `jobs.py` (55 lines)**

- `GET /api/v1/jobs/search` - Advanced job search with filters
- `GET /api/v1/jobs/{job_id}` - Get job by ID
- Input validation using Pydantic schemas
- HTTP status code management

**File: `tags.py` (33 lines)**

- `GET /api/v1/tags/categories` - Get all tag categories
- `GET /api/v1/tags/by-category/{category}` - Get tags by category
- RESTful endpoint design

#### **Service Layer** (`app/services/`)

**File: `search.py` (113 lines)**

- Job search business logic and orchestration
- Filter coordination across multiple criteria
- Result formatting and pagination logic
- Performance optimization for complex queries

**File: `tag_service.py` (75 lines)**

- Tag management business logic
- Category validation and organization
- Tag relationship management

#### **Manager Layer** (`app/managers/`)

**File: `job_manager.py` (150 lines)**

- Job CRUD operations with SQLAlchemy
- Complex filtering and search queries
- Optimized database queries with `distinct(Job.id)`
- Join operations with tag relationships

**File: `tag_manager.py` (74 lines)**

- Tag database operations
- Category-based tag retrieval
- Unique tag management

**File: `job_tag_manager.py` (85 lines)**

- Many-to-many relationship management
- Job-Tag association operations
- Relationship queries and filters

#### **Model Layer** (`app/models/`)

**File: `job.py`**

```python
class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    job_id = Column(String, unique=True, index=True)
    job_position = Column(String, index=True)
    company_name = Column(String, index=True)
    job_location = Column(String, index=True)
    job_posting_date = Column(Date, index=True)
    # ... other fields

    # Relationships
    job_tags = relationship("JobTag", back_populates="job")
```

**File: `tag.py`**

```python
class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    category = Column(String, index=True)

    # Relationships
    job_tags = relationship("JobTag", back_populates="tag")
```

**File: `job_tag.py`**

```python
class JobTag(Base):
    __tablename__ = "job_tags"

    job_id = Column(Integer, ForeignKey("jobs.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)

    # Relationships
    job = relationship("Job", back_populates="job_tags")
    tag = relationship("Tag", back_populates="job_tags")
```

#### **Core Infrastructure** (`app/core/`)

**File: `dependencies.py` (46 lines)**

```python
# Dependency injection container
def get_job_manager(db: Session = Depends(get_db)) -> JobManager:
    return JobManager(db)

def get_search_service(
    job_manager: JobManager = Depends(get_job_manager),
    tag_manager: TagManager = Depends(get_tag_manager),
    job_tag_manager: JobTagManager = Depends(get_job_tag_manager)
) -> SearchService:
    return SearchService(job_manager, tag_manager, job_tag_manager)
```

**File: `config.py` (33 lines)**

- Environment configuration management
- Database URL and connection settings
- Application settings

**File: `db.py` (23 lines)**

- Database connection setup
- Session management
- Engine configuration

### **Database Schema Design**

```sql
-- Optimized for search performance
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    job_id VARCHAR UNIQUE,
    job_position VARCHAR,
    company_name VARCHAR,
    job_location VARCHAR,
    job_posting_date DATE,
    -- Additional indexes for search optimization
    INDEX idx_job_position (job_position),
    INDEX idx_job_location (job_location),
    INDEX idx_company_name (company_name),
    INDEX idx_posting_date (job_posting_date)
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE,
    category VARCHAR,
    INDEX idx_tag_category (category),
    INDEX idx_tag_name (name)
);

CREATE TABLE job_tags (
    job_id INTEGER REFERENCES jobs(id),
    tag_id INTEGER REFERENCES tags(id),
    PRIMARY KEY (job_id, tag_id)
);
```

### **Testing Architecture**

**Comprehensive Test Suite** (`tests/` - 92 tests total)

- **`test_models.py` (310 lines)**: Model validation and relationships
- **`test_services.py` (441 lines)**: Service layer business logic
- **`test_api_endpoints.py` (431 lines)**: API endpoint testing
- **`test_integration.py` (492 lines)**: Full-stack integration tests
- **`test_schemas.py` (353 lines)**: Data validation testing
- **`conftest.py` (112 lines)**: Shared test utilities and fixtures

**Testing Strategy**:

- Unit tests for each layer independently
- Integration tests for cross-layer functionality
- API endpoint tests with real HTTP requests
- Database testing with SQLite for speed
- Dependency injection testing with mocks

### **Performance Optimizations**

1. **Database Query Optimization**

   - Use of `distinct(Job.id)` to avoid PostgreSQL JSON column issues
   - Strategic indexing on searchable fields
   - Efficient join operations in manager layer

2. **Architecture Benefits**

   - Caching can be easily added at service layer
   - Database operations isolated in manager layer
   - Business logic separated from data access

3. **Search Performance**
   - Multi-criteria filtering in single query
   - Pagination to limit result sets
   - Tag-based search using relationships instead of JSON

### **Key Features**

✅ **Advanced Job Search**: Multi-criteria filtering (position, location, tags, date range)
✅ **Tag Management**: Categorized tags with efficient retrieval
✅ **Pagination**: Efficient browsing of large datasets
✅ **Data Validation**: Pydantic schemas for request/response validation
✅ **Error Handling**: Comprehensive error responses with proper HTTP status codes
✅ **API Documentation**: Auto-generated OpenAPI/Swagger documentation
✅ **Database Migrations**: Alembic for schema management
✅ **Dependency Injection**: Clean, testable architecture
✅ **Comprehensive Testing**: 92 tests with 100% pass rate

## API Structure

The API is organized into versioned routers for better maintainability:

- **`/api/v1/jobs/*`** - Job-related endpoints
- **`/api/v1/tags/*`** - Tag-related endpoints

## API Endpoints

### Jobs Router (`/api/v1/jobs`)

#### Search Jobs

```http
GET /api/v1/jobs/search
```

Query Parameters:

- `query` (optional): Search query string
- `location` (optional): Location filter
- `tags` (optional): List of tag names to filter by
- `tag_categories` (optional): List of tag categories to filter by
- `date_from` (optional): Start date for posting date range
- `date_to` (optional): End date for posting date range
- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Number of items per page (default: 10)

Example Requests:

```bash
# Search for jobs containing "python" in name field
curl your_host/api/v1/jobs/search?query=python

# Search for jobs with specific tags (multiple tags as repeated parameters)
curl your_host/api/v1/jobs/search?tags=Backend-Development&tags=Database

# Search with multiple filters
curl your_host/api/v1/jobs/search?query=developer&location=New%20York&tags=Python&tags=AWS&page=1&limit=20
```

Response:

```json
{
  "items": [
    {
      "id": "string",
      "job_id": "string",
      "job_position": "string",
      "job_link": "string",
      "company_name": "string",
      "company_profile": "string",
      "job_location": "string",
      "job_posting_date": "string (ISO date)",
      "tags": {
        "role": ["string"],
        "technology": ["string"],
        "skill": ["string"],
        "methodology": ["string"],
        "tool": ["string"]
      }
    }
  ],
  "total": "integer",
  "page": "integer",
  "limit": "integer",
  "pages": "integer"
}
```

#### Get Job by ID

```http
GET /api/v1/jobs/{job_id}
```

Example Request:

```bash
# Get job with specific ID
curl your_host/api/v1/jobs/123e4567-e89b-12d3-a456-426614174000
```

Response:

```json
{
  "id": "string",
  "job_id": "string",
  "job_position": "string",
  "job_link": "string",
  "company_name": "string",
  "company_profile": "string",
  "job_location": "string",
  "job_posting_date": "string (ISO date)",
  "tags": {
    "role": ["string"],
    "technology": ["string"],
    "skill": ["string"],
    "methodology": ["string"],
    "tool": ["string"]
  }
}
```

### Tags Router (`/api/v1/tags`)

#### Get Tag Categories

```http
GET /api/v1/tags/categories
```

Response:

```json
["role", "technology", "skill", "methodology", "tool"]
```

#### Get Tags by Category

```http
GET /api/v1/tags/by-category/{category}
```

Example Request:

```bash
# Get all technology tags
curl your_host/api/v1/tags/by-category/technology
```

Response:

```json
[
  "Python",
  "JavaScript",
  "TypeScript",
  "React",
  "Node.js",
  "FastAPI",
  "SQLAlchemy",
  "AWS",
  "Kubernetes",
  "Docker"
]
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request

```json
{
  "detail": "string"
}
```

Common causes:

- Invalid query parameters
- Malformed request data
- Invalid UUID format
- Invalid tag category

### 404 Not Found

```json
{
  "detail": "string"
}
```

Common causes:

- Job or tag not found
- Invalid endpoint

### 500 Internal Server Error

```json
{
  "detail": "string"
}
```

Common causes:

- Database connection issues
- Server configuration problems

## Data Models

### Job

```json
{
  "id": "integer",
  "job_id": "string (UUID)",
  "job_position": "string",
  "job_link": "string",
  "company_name": "string",
  "company_profile": "string",
  "job_location": "string",
  "job_posting_date": "string (ISO date)",
  "tags": {
    "role": ["string"],
    "technology": ["string"],
    "skill": ["string"],
    "methodology": ["string"],
    "tool": ["string"]
  }
}
```

### Tag Categories

```json
{
  "role": [
    "Frontend-Development",
    "Backend-Development",
    "Full-Stack-Development",
    "DevOps",
    "Data-Science",
    "Product-Management",
    "UX-Design",
    "UI-Design",
    "Business-Analysis"
  ],
  "technology": [
    "Python",
    "JavaScript",
    "TypeScript",
    "React",
    "Node.js",
    "FastAPI",
    "SQLAlchemy",
    "AWS",
    "Kubernetes",
    "Docker"
  ],
  "skill": [
    "API-Development",
    "Database",
    "Microservices",
    "CI-CD",
    "Cloud-Computing",
    "Machine-Learning",
    "Big-Data",
    "Analytics",
    "AI",
    "Cybersecurity",
    "UI-Development",
    "Web-Development",
    "Infrastructure",
    "User-Experience"
  ],
  "methodology": [
    "Agile",
    "Scrum",
    "Requirements-Gathering",
    "Documentation",
    "Stakeholder-Management",
    "User-Research",
    "Design-Systems",
    "Product-Analytics",
    "Strategy",
    "Roadmapping"
  ],
  "tool": ["Figma", "Git", "Jira", "Confluence", "Azure", "GCP"]
}
```

## Setup and Installation

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/job_board"
export POSTGRES_USER="your_username"
export POSTGRES_PASSWORD="your_password"
```

4. Run database migrations:

```bash
alembic upgrade head
```

5. Start the server:

```bash
uvicorn app.main:app --reload
```

## Database Reset and Data Import

To reset the database and import mock data:

```bash
python app/data/db_reset_and_import.py
```

Options:

- `--num-jobs N`: Generate N mock jobs (default: 500)
- `--skip-generate`: Skip mock data generation and use existing data

Example Usage:

```bash
# Generate 1000 mock jobs
python app/data/db_reset_and_import.py --num-jobs 1000

# Reset database using existing mock data
python app/data/db_reset_and_import.py --skip-generate
```

## Development

### Running Tests

```bash
pytest
```

### Database Migrations

Create a new migration:

```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:

```bash
alembic upgrade head
```

### Code Style

The project follows PEP 8 style guidelines. Use `black` for code formatting:

```bash
black .
```

## Common Use Cases

### 1. Job Search with Multiple Criteria

```bash
# Search for Python developer jobs in New York
curl "your_host/api/v1/jobs/search?query=python&location=New%20York"

# Search for jobs requiring both Python and AWS skills
curl "your_host/api/v1/jobs/search?tags=Python&tags=AWS"
```

### 2. Tag Management

```bash
# Get all technology tags
curl "your_host/api/v1/tags/by-category/technology"

# Get all available tag categories
curl "your_host/api/v1/tags/categories"
```

### 3. Job Listing with Sorting

```bash
# Get latest jobs first
curl "your_host/api/v1/jobs/search?sort_by=posting_date&sort_order=desc"

# Get jobs sorted by company name
curl "your_host/api/v1/jobs/search?sort_by=company_name&sort_order=asc"
```

## Best Practices

1. **Pagination**: Always use pagination when fetching large datasets to improve performance.
2. **Error Handling**: Implement proper error handling for all API responses.
3. **Caching**: Consider implementing caching for frequently accessed data.
4. **Rate Limiting**: Be mindful of API rate limits in production environments.
5. **Security**: Always use HTTPS in production and validate all input data.
