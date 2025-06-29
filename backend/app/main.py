from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List
import os
import uuid
import time

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

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI-Swap API",
        "version": "1.0.0",
        "status": "running",
        "note": "Deployment test version - basic functionality only"
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

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """Upload and validate user image (simplified version)"""
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Validate file size (10MB limit)
        if file.size > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size must be less than 10MB")
        
        # Generate unique image ID
        image_id = str(uuid.uuid4())
        
        return {
            "success": True,
            "message": "Image uploaded successfully (test mode)",
            "image_id": image_id,
            "face_detected": True,
            "landmarks": []
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/swap-face")
async def swap_face(request: dict):
    """Perform face swapping with selected profession template (simplified version)"""
    try:
        # Validate request
        if not request.get("image_id") or not request.get("profession"):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        result_id = str(uuid.uuid4())
        
        return {
            "success": True,
            "message": "Face swap completed successfully (test mode)",
            "result_url": f"/results/{result_id}.jpg",
            "profession": request.get("profession"),
            "angle": request.get("angle", "front")
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/templates/{profession}")
async def get_templates(profession: str):
    """Get available templates for a specific profession"""
    templates = [
        {"id": "front", "name": "Front View", "angle": "front"},
        {"id": "side", "name": "Side View", "angle": "side"},
        {"id": "three-quarter", "name": "Three Quarter", "angle": "three-quarter"}
    ]
    return {"profession": profession, "templates": templates}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 