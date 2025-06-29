from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class UploadResponse(BaseModel):
    """Response model for image upload"""
    success: bool
    message: str
    image_id: Optional[str] = None
    face_detected: Optional[bool] = None
    landmarks: Optional[List[Dict[str, Any]]] = None

class SwapRequest(BaseModel):
    """Request model for face swapping"""
    image_id: str = Field(..., description="ID of the uploaded image")
    profession: str = Field(..., description="Target profession for face swap")
    angle: str = Field(default="front", description="Target angle (front, side, three_quarter, back)")

class SwapResponse(BaseModel):
    """Response model for face swapping"""
    success: bool
    message: str
    result_url: Optional[str] = None
    profession: Optional[str] = None
    angle: Optional[str] = None

class Profession(BaseModel):
    """Model for profession data"""
    id: str
    name: str
    description: str

class Template(BaseModel):
    """Model for template data"""
    id: str
    profession: str
    angle: str
    image_url: str
    description: str

class FaceLandmarks(BaseModel):
    """Model for facial landmarks"""
    nose: Dict[str, float]
    left_eye: Dict[str, float]
    right_eye: Dict[str, float]
    left_ear: Dict[str, float]
    right_ear: Dict[str, float]
    mouth: Dict[str, float]
    chin: Dict[str, float]

class ProcessingResult(BaseModel):
    """Model for image processing results"""
    image_id: str
    face_detected: bool
    landmarks: Optional[FaceLandmarks] = None
    confidence: float
    processing_time: float 