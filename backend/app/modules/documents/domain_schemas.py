"""
MediCore Nexus - Document Vault & Imaging (documents) Pydantic v2 Domain Schemas
Defines request payloads, response serializations, validation models, and filter parameters.
"""

from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class DocumentArchiveBaseSchema(BaseModel):
    """Core attributes for DocumentArchive."""
    model_config = ConfigDict(extra="ignore", arbitrary_types_allowed=True)

    name: Optional[str] = Field(None, description="Primary title or descriptor")
    code: Optional[str] = Field(None, description="System code or reference identifier")
    description: Optional[str] = Field(None, description="Clinical or administrative notes")
    status: Optional[str] = Field("Active", description="Current operational status")
    hospital_id: Optional[str] = Field("hosp-001", description="Associated hospital facility ID")
    department_id: Optional[str] = Field(None, description="Department identifier")
    metadata_payload: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Flexible domain attributes")


class DocumentArchiveCreateSchema(DocumentArchiveBaseSchema):
    """Payload required to create a new DocumentArchive record."""
    is_urgent: Optional[bool] = False
    priority_level: Optional[str] = "Normal"


class DocumentArchiveUpdateSchema(BaseModel):
    """Payload permitted for partial update of DocumentArchive."""
    model_config = ConfigDict(extra="ignore")

    name: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    metadata_payload: Optional[Dict[str, Any]] = None


class DocumentArchiveFilterSchema(BaseModel):
    """Query parameters for filtering DocumentArchive collections."""
    status: Optional[str] = None
    hospital_id: Optional[str] = None
    department_id: Optional[str] = None
    search_query: Optional[str] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    skip: int = Field(0, ge=0)
    limit: int = Field(50, ge=1, le=500)
    sort_by: str = "created_at"
    descending: bool = True


class DocumentArchiveDetailResponseSchema(DocumentArchiveBaseSchema):
    """Detailed response schema for DocumentArchive with audit timestamps."""
    id: str
    created_at: str
    updated_at: str
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    version: int = 1
    is_deleted: bool = False


class DocumentArchiveListResponseSchema(BaseModel):
    """Paginated collection response for DocumentArchive."""
    items: List[DocumentArchiveDetailResponseSchema]
    total: int
    skip: int
    limit: int
    has_more: bool


class DocumentArchiveBulkActionRequest(BaseModel):
    """Batch operation request for DocumentArchive entities."""
    action: str = Field(..., description="Action to perform: ACTIVATE, ARCHIVE, DELETE, EXPORT")
    entity_ids: List[str] = Field(..., min_length=1)
    reason: Optional[str] = None


class DocumentArchiveBulkActionResponse(BaseModel):
    """Summary of completed bulk operation."""
    action: str
    total_processed: int
    successful_count: int
    failed_count: int
    errors: List[Dict[str, str]] = []
