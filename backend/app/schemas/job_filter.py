from typing import List, Optional
from pydantic import BaseModel
from datetime import date

class JobSearchFilter(BaseModel):
    query: Optional[str] = None
    location: Optional[str] = None
    tags: Optional[List[str]] = None
    tag_categories: Optional[List[str]] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    page: int = 1
    limit: int = 10 