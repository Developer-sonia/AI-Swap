from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class UploadResponse(BaseModel):
    """Response model for image upload"""
    message: str
    file_path: str
    file_name: str
    uploaded_at: datetime = Field(default_factory=datetime.now)

class SwapRequest(BaseModel):
    """Request model for face swapping"""
    image_path: str = Field(..., description="Path to uploaded image")
    profession: str = Field(..., description="Target profession for face swap")
    angle: Optional[str] = Field(default="front", description="Target angle (front, side, three_quarter, back)")
    color: Optional[str] = Field(default=None, description="Target color scheme")
    accessories: Optional[List[str]] = Field(default=None, description="Target accessories")

class SwapResponse(BaseModel):
    """Response model for face swapping"""
    message: str
    result_path: str
    profession: str
    angle: str
    processed_at: datetime = Field(default_factory=datetime.now)

class ProfessionInfo(BaseModel):
    """Model for profession information"""
    name: str
    description: str
    angles: List[str]
    colors: List[str]
    accessories: List[str]

class TemplateInfo(BaseModel):
    """Model for template information"""
    profession: str
    angle: str
    color: Optional[str] = None
    accessories: Optional[List[str]] = None
    template_path: str

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.now)

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class APIInfo(BaseModel):
    """API information response"""
    message: str
    version: str
    status: str
    note: str
    endpoints: Dict[str, str]

class FileUploadResponse(BaseModel):
    """File upload response"""
    success: bool
    file_path: Optional[str] = None
    error: Optional[str] = None
    file_size: Optional[int] = None
    content_type: Optional[str] = None

class ProcessingStatus(BaseModel):
    """Processing status response"""
    status: str  # "pending", "processing", "completed", "failed"
    progress: Optional[int] = None  # 0-100
    message: Optional[str] = None
    result_path: Optional[str] = None
    error: Optional[str] = None

class UserSession(BaseModel):
    """User session model"""
    session_id: str
    user_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)
    uploads: List[str] = Field(default_factory=list)
    results: List[str] = Field(default_factory=list)

class AnalyticsData(BaseModel):
    """Analytics data model"""
    total_uploads: int
    total_swaps: int
    popular_professions: List[Dict[str, Any]]
    average_processing_time: float
    success_rate: float
    timestamp: datetime = Field(default_factory=datetime.now) 