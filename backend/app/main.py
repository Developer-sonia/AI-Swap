from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import json
from pathlib import Path

# Import services
from app.services.face_service import FaceService
from app.services.template_service import TemplateService
from app.models.schemas import UploadResponse, SwapRequest, SwapResponse

app = FastAPI(
    title="AI-Swap API",
    description="Professional face swapping application API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Initialize services
face_service = FaceService()
template_service = TemplateService()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI-Swap API",
        "version": "1.0.0",
        "status": "running",
        "note": "Professional face swapping application",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "professions": "/professions",
            "upload": "/upload",
            "swap": "/swap-face"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "ai-swap-api",
        "version": "1.0.0"
    }

@app.get("/test")
async def test():
    """Simple test endpoint"""
    return {"message": "API is working!", "test": "success"}

@app.get("/professions")
async def get_professions():
    """Get available professions"""
    try:
        professions = template_service.get_available_professions()
        return {"professions": professions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/templates/{profession}")
async def get_templates(profession: str):
    """Get templates for a specific profession"""
    try:
        templates = template_service.get_templates_for_profession(profession)
        return {"profession": profession, "templates": templates}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Profession {profession} not found")

@app.post("/upload", response_model=UploadResponse)
async def upload_image(file: UploadFile = File(...)):
    """Upload user image for face swapping"""
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Validate file size (10MB max)
        if file.size > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size must be less than 10MB")
        
        # Save uploaded file
        upload_path = face_service.save_uploaded_image(file)
        
        return UploadResponse(
            message="Image uploaded successfully",
            file_path=upload_path,
            file_name=file.filename
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/swap-face", response_model=SwapResponse)
async def swap_face(request: SwapRequest):
    """Perform face swapping with uploaded image and template"""
    try:
        # Validate input
        if not request.image_path or not request.profession:
            raise HTTPException(status_code=400, detail="Image path and profession are required")
        
        # Perform face swapping
        result_path = face_service.perform_face_swap(
            request.image_path,
            request.profession,
            request.angle or "front"
        )
        
        return SwapResponse(
            message="Face swap completed successfully",
            result_path=result_path,
            profession=request.profession,
            angle=request.angle or "front"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results/{filename}")
async def get_result(filename: str):
    """Get a specific result image"""
    try:
        result_path = f"results/{filename}"
        if not os.path.exists(result_path):
            raise HTTPException(status_code=404, detail="Result not found")
        
        return {"result_path": result_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 