from app.api import jobs, tags
from app.core.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(jobs.router, prefix=f"{settings.API_V1_STR}/jobs", tags=["jobs"])
app.include_router(tags.router, prefix=f"{settings.API_V1_STR}/tags", tags=["tags"])


@app.get("/")
def root():
    return {"message": "Welcome to Job Board API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
