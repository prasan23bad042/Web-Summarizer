from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any
from enum import Enum

class SummaryType(str, Enum):
    URL = "url"
    TEXT = "text"

class SummaryRequest(BaseModel):
    type: SummaryType
    content: str
    max_length: Optional[int] = 300

class SummaryResponse(BaseModel):
    summary: str
    metadata: Optional[Dict[str, Any]] = None

class HealthCheck(BaseModel):
    status: str
    version: str
