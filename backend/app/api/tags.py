from typing import List

from app.core.db import get_db
from app.models.tag import Tag, TagCategory
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/categories", response_model=List[str])
def get_tag_categories():
    """
    Get all available tag categories
    """
    # Convert enum values to list of strings
    return [category.value for category in TagCategory]


@router.get("/by-category/{category}", response_model=List[str])
def get_tags_by_category(category: str, db: Session = Depends(get_db)):
    """
    Get all tags for a specific category
    """
    # Validate the category exists
    try:
        tag_category = TagCategory(category)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid category: {category}")

    # Query tags by category
    tags = db.query(Tag.name).filter(Tag.category == tag_category).all()

    # Extract tag names from the result
    return [tag[0] for tag in tags]
