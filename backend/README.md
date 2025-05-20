# Job Board API Documentation

## Overview

This is the backend API for the Job Board application, providing endpoints for job listings, tags, and search functionality. The API is versioned (v1) and organized into modular routers for better maintainability.

## API Structure

The API is organized into the following routers:

- `/api/v1/jobs/*` - Job-related endpoints
- `/api/v1/tags/*` - Tag-related endpoints

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
