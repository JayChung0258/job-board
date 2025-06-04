"""
Tag Service - Business logic for tag operations
"""

from typing import List

from app.managers.tag_manager import TagManager
from app.models.tag import TagCategory
from fastapi import HTTPException


class TagService:
    """
    Handles business logic for tag operations.
    Uses TagManager for all database interactions.
    """

    def __init__(self, tag_manager: TagManager):
        self.tag_manager = tag_manager

    def get_tag_categories(self) -> List[str]:
        """
        Get all available tag categories.
        Returns category values as strings.
        """
        categories = self.tag_manager.find_all_categories()
        return [category.value for category in categories]

    def get_tags_by_category(self, category: str) -> List[str]:
        """
        Get all tags for a specific category.
        Validates category exists before querying.
        """
        # Validate the category exists
        if not self._validate_category(category):
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")

        # Convert string to enum
        tag_category = TagCategory(category)

        # Get tags from manager
        tags = self.tag_manager.find_by_category(tag_category)

        # Return tag names
        return [tag.name for tag in tags]

    def create_tag(self, name: str, category: str) -> dict:
        """
        Create a new tag.
        Validates category and checks for duplicates.
        """
        # Validate category
        if not self._validate_category(category):
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")

        # Check if tag already exists
        if self.tag_manager.exists_by_name(name):
            raise HTTPException(status_code=400, detail=f"Tag '{name}' already exists")

        # Convert string to enum
        tag_category = TagCategory(category)

        # Create tag
        tag = self.tag_manager.create(name, tag_category)

        return {"name": tag.name, "category": tag.category.value}

    def _validate_category(self, category: str) -> bool:
        """Validate that the category string is a valid TagCategory."""
        try:
            TagCategory(category)
            return True
        except ValueError:
            return False
