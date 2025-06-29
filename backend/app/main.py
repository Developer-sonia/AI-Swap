from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List
import os
from .services.face_service import FaceService
from .services.template_service import TemplateService
from .models.schemas import UploadResponse, SwapRequest, SwapResponse

app = FastAPI(
    title="AI-Swap API",
    description="Professional face swapping application API",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
face_service = FaceService()
template_service = TemplateService()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI-Swap API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ai-swap-api"}

@app.get("/professions")
async def get_professions():
    """Get available professions for face swapping"""
    professions = [
        {"id": "doctor", "name": "Doctor", "description": "Medical professional"},
        {"id": "professor", "name": "Professor", "description": "Academic educator"},
        {"id": "engineer", "name": "Engineer", "description": "Technical professional"},
        {"id": "lawyer", "name": "Lawyer", "description": "Legal professional"},
        {"id": "business", "name": "Business Executive", "description": "Corporate professional"},
        {"id": "artist", "name": "Artist", "description": "Creative professional"}
    ]
    return {"professions": professions}

@app.post("/upload", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)):
    """Upload and validate user image"""
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Validate file size (10MB limit)
        if file.size > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size must be less than 10MB")
        
        # Process the uploaded image
        result = await face_service.process_upload(file)
        
        return UploadResponse(
            success=True,
            message="Image uploaded successfully",
            image_id=result["image_id"],
            face_detected=result["face_detected"],
            landmarks=result["landmarks"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/swap-face", response_model=SwapResponse)
async def swap_face(request: SwapRequest):
    """Perform face swapping with selected profession template"""
    try:
        # Validate request
        if not request.image_id or not request.profession:
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        # Perform face swapping
        result = await face_service.swap_face(
            image_id=request.image_id,
            profession=request.profession,
            angle=request.angle
        )
        
        return SwapResponse(
            success=True,
            message="Face swap completed successfully",
            result_url=result["result_url"],
            profession=request.profession,
            angle=request.angle
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/templates/{profession}")
async def get_templates(profession: str):
    """Get available templates for a specific profession"""
    try:
        templates = await template_service.get_templates(profession)
        return {"profession": profession, "templates": templates}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Templates not found for profession: {profession}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 