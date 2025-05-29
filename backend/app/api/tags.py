"""
Tag API Endpoints - HTTP layer for tag-related operations
"""

from typing import List

from app.core.dependencies import get_tag_service
from app.services.tag_service import TagService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/categories", response_model=List[str])
def get_tag_categories(
    tag_service: TagService = Depends(get_tag_service),
):
    """
    Get all available tag categories
    """
    return tag_service.get_tag_categories()


@router.get("/by-category/{category}", response_model=List[str])
def get_tags_by_category(
    category: str,
    tag_service: TagService = Depends(get_tag_service),
):
    """
    Get all tags for a specific category
    """
    return tag_service.get_tags_by_category(category)
